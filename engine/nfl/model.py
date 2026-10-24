"""NFL engine v1: line -> plays -> script-aware pass rate -> dropbacks/rushes -> player shares -> simulated tails.
Inputs per game: home, away, spread_home, total, proe {team: (cur, prior)}, weather tag.
Inputs per player (shares.csv): player, team, pos, tgt_share (of pass attempts), catch_rate, ypc (catch yds mean, opt),
carry_share (of team rushes), ypc_rush (regressed), rz_carry_share (inside-10), ez_tgt_share (end-zone/RZ target share)."""
import numpy as np, pandas as pd
import config as C

def implied_points(spread_home, total):
    return (total - spread_home) / 2, (total + spread_home) / 2

def team_volume(rng, team_spread, total, proe_cur=0.0, proe_prior=0.0, sack=C.SACK_RATE, scramble=C.SCRAMBLE_RATE, n=C.N_SIMS):
    """team_spread: this team's spread (negative = favored). Returns per-sim plays, dropbacks, attempts, rushes, margin."""
    margin = rng.normal(-team_spread, C.MARGIN_SD, n)                    # positive = this team wins by
    plays = np.clip(rng.normal(C.PLAYS_BASE + C.PLAYS_PER_TOTAL_PT * (total - 44), C.PLAYS_SD, n), 45, 85)
    proe = C.PROE_WEIGHT_CUR * proe_cur + (1 - C.PROE_WEIGHT_CUR) * proe_prior
    pr = C.BASE_PASS_RATE + proe + C.SPREAD_PASS_SLOPE * team_spread - C.SCRIPT_K * ((margin + team_spread) / 14.0)
    pr = np.clip(pr, *C.PASS_RATE_CLIP)
    dropbacks = rng.binomial(plays.astype(int), pr)
    sacks = rng.binomial(dropbacks, sack); scr = rng.binomial(dropbacks - sacks, scramble)
    attempts = dropbacks - sacks - scr
    rushes = plays.astype(int) - dropbacks
    return dict(margin=margin, plays=plays, dropbacks=dropbacks, attempts=attempts, rushes=rushes, scrambles=scr)

def _beta_share(rng, share, n):
    share = float(np.clip(share, 1e-4, 0.95))
    return rng.beta(share * C.SHARE_CONC, (1 - share) * C.SHARE_CONC, n)

def _gamma_sum(rng, counts, mean, sd):
    k = (mean / sd) ** 2; theta = sd ** 2 / mean
    out = np.zeros(len(counts)); pos = counts > 0
    out[pos] = rng.gamma(k * counts[pos], theta)
    return out

def _longest(rng, counts, mean, sd, cap=15):
    k = (mean / sd) ** 2; theta = sd ** 2 / mean
    m = rng.gamma(k, theta, (len(counts), cap))
    mask = np.arange(cap)[None, :] < np.minimum(counts, cap)[:, None]
    return np.where(mask, m, 0).max(axis=1)

def simulate_player(rng, row, vol, team_pts, weather="calm"):
    row = {k: v for k, v in row.items() if not (isinstance(v, float) and np.isnan(v))}   # missing fields -> defaults
    n = len(vol["attempts"]); out = {}
    wx = C.WEATHER_PASS_YDS.get(weather, 1.0)
    if row.get("tgt_share", 0) > 0:
        tg = rng.binomial(vol["attempts"], _beta_share(rng, row["tgt_share"], n))
        rec = rng.binomial(tg, float(row.get("catch_rate", 0.65)))
        mean, sd = C.CATCH_YDS.get(row["pos"], C.CATCH_YDS["WR"])
        mean = float(row.get("ypc", mean) or mean) * wx
        out.update(targets=tg, receptions=rec, rec_yds=_gamma_sum(rng, rec, mean, sd * mean / C.CATCH_YDS.get(row["pos"], C.CATCH_YDS["WR"])[0]),
                   longest_rec=_longest(rng, rec, mean, sd))
    if row.get("carry_share", 0) > 0:
        car = rng.binomial(vol["rushes"], _beta_share(rng, row["carry_share"], n))
        ypc = float(row.get("ypc_rush", 4.2))
        pbig, mbig = C.CARRY_YDS_BIG
        core = ypc - pbig * mbig
        big = rng.binomial(car, pbig)
        yds = rng.normal(core * (car - big), 3.0 * np.sqrt(np.maximum(car - big, 1))) + _gamma_sum(rng, big, mbig, mbig)
        out.update(carries=car, rush_yds=yds)
    # anytime TD: lambda from team TD pool x role shares (Poisson per sim, scaled by realized volume)
    tds = team_pts * C.TD_PTS_SHARE / 7.0
    lam = tds * (C.RUSH_TD_SHARE * float(row.get("rz_carry_share", 0)) + (1 - C.RUSH_TD_SHARE) * float(row.get("ez_tgt_share", 0)))
    out["td"] = rng.poisson(lam, n); out["td_lambda"] = lam
    return out

def simulate_game(game, shares, seed=1):
    """game: dict(home, away, spread_home, total, proe={team:(cur,prior)}, weather). shares: DataFrame for both teams."""
    rng = np.random.default_rng(seed)
    pts = dict(zip((game["home"], game["away"]), implied_points(game["spread_home"], game["total"])))
    res = {}
    for team, sp in ((game["home"], game["spread_home"]), (game["away"], -game["spread_home"])):
        cur, prior = game.get("proe", {}).get(team, (0.0, 0.0))
        vol = team_volume(rng, sp, game["total"], cur, prior)
        for _, r in shares[shares["team"] == team].iterrows():
            res[r["player"]] = simulate_player(rng, r.to_dict(), vol, pts[team], game.get("weather", "calm"))
        res[f"_{team}_volume"] = vol
    return res
