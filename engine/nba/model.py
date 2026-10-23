"""NBA projection engine v1: minutes -> shrunk per-minute rates -> market-anchored team scaling -> joint simulation.

Input: player game logs (nba_api LeagueGameLog columns) for last + current season.
Output: per-player projected minutes and stat means, plus a simulator for P(over line).
"""
import numpy as np
import pandas as pd
import config as C
from common import nb_draw, norm_name

STATS = ["pts", "reb", "ast", "fg3m"]


def load_logs(paths):
    df = pd.concat([pd.read_csv(p) for p in paths], ignore_index=True)
    df.columns = [c.lower() for c in df.columns]
    df["game_date"] = pd.to_datetime(df["game_date"])
    df = df[df["min"] > 0].copy()
    df["key"] = df["player_name"].map(norm_name)
    return df.sort_values("game_date")


def league_rates(df):
    rot = df[df["min"] >= 15]
    return {s: rot[s].sum() / rot["min"].sum() for s in STATS}


def fit_vmr(df, rates_by_player=None):
    """Variance/mean of each stat around player-season rate x minutes (rotation games)."""
    d = df[df["min"] >= 15].copy()
    out = {}
    for s in STATS:
        r = d.groupby(["player_id", "season_id"])[[s, "min"]].transform("sum")
        exp = r[s] / r["min"] * d["min"]
        m = exp.mean()
        out[s] = float(np.clip(((d[s] - exp) ** 2).mean() / m, 1.0, 4.0)) if m > 0 else C.VMR_DEFAULT[s]
    return out


def _weights(n, hl):
    ago = np.arange(n)[::-1]          # last row = most recent = 0 games ago
    return 0.5 ** (ago / hl)


def player_baselines(df, asof, cur_season_id):
    """One row per player: team, minutes projection/SD, shrunk per-minute rates. Uses games before `asof` only."""
    df = df[df["game_date"] < pd.Timestamp(asof)]
    lg = league_rates(df)
    rows = []
    for pid, g in df.groupby("player_id"):
        g = g.sort_values("game_date")
        cur = g[g["season_id"].astype(str) == str(cur_season_id)]
        prior = g[g["season_id"].astype(str) != str(cur_season_id)]
        team = (cur if len(cur) else g)["team_abbreviation"].iloc[-1]
        # minutes
        m_prior = prior["min"].mean() if len(prior) else np.nan
        if len(cur):
            w = _weights(len(cur), C.HL_MINUTES)
            num, den = (w * cur["min"].values).sum(), w.sum()
            if not np.isnan(m_prior):
                num += C.MIN_PRIOR_GAMES * m_prior; den += C.MIN_PRIOR_GAMES
            min_proj = num / den
            recent = cur["min"].values[-10:]
        else:
            min_proj = m_prior * C.NO_CUR_GAMES_MIN_FACTOR
            recent = prior["min"].values[-10:]
        sd_min = max(C.SD_MIN_DEFAULT, float(np.std(recent)) if len(recent) > 2 else C.SD_MIN_DEFAULT)
        # rates: decayed over both seasons, prior season discounted, shrunk to league
        w = _weights(len(g), C.HL_RATES) * np.where(g["season_id"].astype(str) == str(cur_season_id), 1.0, C.PRIOR_SEASON_DISCOUNT)
        mins = (w * g["min"].values).sum()
        rec = {"player_id": pid, "player": g["player_name"].iloc[-1], "key": g["key"].iloc[-1], "team": team,
               "min_base": float(min_proj), "sd_min": sd_min, "n_cur": len(cur), "n_prior": len(prior)}
        for s in STATS:
            k = C.SHRINK_MIN[s]
            rec[f"{s}_pm"] = float(((w * g[s].values).sum() + k * lg[s]) / (mins + k))
        rows.append(rec)
    return pd.DataFrame(rows), lg


def project_game(base, home, away, spread_home, total, out_keys=(), min_overrides=None, league_total=None, lg_team_pts=None):
    """Project both teams. spread_home < 0 means home favored. out_keys: normalized names ruled OUT.
    min_overrides: {key: minutes cap}. Returns per-player frame with stat means and sim params."""
    min_overrides = min_overrides or {}
    implied = {home: (total - spread_home) / 2, away: (total + spread_home) / 2}
    res = []
    for team in (home, away):
        t = base[(base["team"] == team) & (~base["key"].isin(out_keys))].copy()
        t["min_proj"] = t["min_base"]
        for k, cap in min_overrides.items():
            t.loc[t["key"] == k, "min_proj"] = np.minimum(t.loc[t["key"] == k, "min_proj"], cap)
        t = t.sort_values("min_proj", ascending=False)
        rot = t.head(C.ROTATION_SIZE)
        rot = rot[rot["min_proj"] >= C.ROTATION_MIN].copy()
        # blowout: starters lose minutes, bench absorbs
        excess = max(0.0, abs(spread_home) - C.BLOWOUT_START) * C.BLOWOUT_MIN_PER_PT
        starters = rot["min_proj"] >= C.STARTER_MIN
        rot.loc[starters, "min_proj"] -= excess
        # normalize to team minutes, respecting caps
        capped = rot["key"].isin(min_overrides.keys())
        for _ in range(5):
            free = ~capped & (rot["min_proj"] < C.MAX_MIN)
            gap = C.TEAM_MINUTES - rot["min_proj"].sum()
            if abs(gap) < 0.1 or free.sum() == 0:
                break
            share = rot.loc[free, "min_proj"] / rot.loc[free, "min_proj"].sum()
            rot.loc[free, "min_proj"] = np.minimum(rot.loc[free, "min_proj"] + gap * share, C.MAX_MIN)
        # means before team scaling
        for s in STATS:
            rot[f"{s}_mu"] = rot[f"{s}_pm"] * rot["min_proj"]
        f_pts = np.clip(implied[team] / rot["pts_mu"].sum(), *C.TEAM_PTS_CLIP)
        f_reb = (total / league_total) ** C.REB_EXP if league_total else 1.0
        rot["pts_mu"] *= f_pts
        rot["fg3m_mu"] *= f_pts
        rot["ast_mu"] *= f_pts ** C.AST_EXP
        rot["reb_mu"] *= f_reb
        rot["f_pts"], rot["implied_team_pts"] = f_pts, implied[team]
        rot["opp"] = away if team == home else home
        res.append(rot)
    return pd.concat(res, ignore_index=True)


def simulate(row, vmr, n=C.N_SIMS, seed=11, mult=1.0):
    """Joint sim for one player: shared minutes draw -> correlated stats. Returns dict of arrays."""
    rng = np.random.default_rng(seed)
    mins = np.clip(rng.normal(row["min_proj"], row["sd_min"], n), 0, 48)
    scale = mins / max(row["min_proj"], 1e-6)
    out = {}
    for s in STATS:
        out[s] = nb_draw(rng, row[f"{s}_mu"] * mult * scale, vmr[s])
    out["pra"] = out["pts"] + out["reb"] + out["ast"]
    out["pr"] = out["pts"] + out["reb"]
    out["pa"] = out["pts"] + out["ast"]
    out["ra"] = out["reb"] + out["ast"]
    out["min"] = mins
    return out
