"""NFL matchup breakdown: the WHY behind a receiving / rushing line, line last.
    python engine/nfl/matchup.py DATE "Full Name" [...]            (opponent + lines from data/odds/nfl/DATE/)
    python engine/nfl/matchup.py DATE "Full Name@OPP"              (force opponent, e.g. "Ja'Marr Chase@PIT")
Data: engine/data/nfl/pbp_<season>_slim.csv.gz + engine/data/nfl/context/<season>/ (fetch_context.py).
Per player:
  1. Role: snap share (last 3 vs season), routes proxy, targets / target share, share of team air yards, aDOT (NGS),
     separation and cushion (NGS), YAC over expected; for runners carries share, rush yards over expected, % vs 8+ boxes.
  2. Opponent defense vs his position (WR / TE / RB): targets, yards and yards per target allowed per game vs league.
  3. Opponent pressure / blitz / box: pressure rate (PFR), blitz rate and stacked boxes (FTN charting), play-action seen.
  4. Script and pace: spread, total, both teams' plays per game and pass rate over expected (PROE).
  5. Context multipliers for receiving yards / receptions / rushing yards (shrunk: 2026 games vs 2025, k = 4 games;
     half of a defense's deviation counted as real).
Facts and multipliers only: the NFL engine (run_nfl.py) owns the full simulation."""
import sys, os, glob
import numpy as np, pandas as pd

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
CUR, PRI = 2026, 2025
K = 4.0
TEAMS = {"Arizona Cardinals": "ARI", "Atlanta Falcons": "ATL", "Baltimore Ravens": "BAL", "Buffalo Bills": "BUF", "Carolina Panthers": "CAR",
    "Chicago Bears": "CHI", "Cincinnati Bengals": "CIN", "Cleveland Browns": "CLE", "Dallas Cowboys": "DAL", "Denver Broncos": "DEN",
    "Detroit Lions": "DET", "Green Bay Packers": "GB", "Houston Texans": "HOU", "Indianapolis Colts": "IND", "Jacksonville Jaguars": "JAX",
    "Kansas City Chiefs": "KC", "Las Vegas Raiders": "LV", "Los Angeles Chargers": "LAC", "Los Angeles Rams": "LA", "Miami Dolphins": "MIA",
    "Minnesota Vikings": "MIN", "New England Patriots": "NE", "New Orleans Saints": "NO", "New York Giants": "NYG", "New York Jets": "NYJ",
    "Philadelphia Eagles": "PHI", "Pittsburgh Steelers": "PIT", "San Francisco 49ers": "SF", "Seattle Seahawks": "SEA",
    "Tampa Bay Buccaneers": "TB", "Tennessee Titans": "TEN", "Washington Commanders": "WAS"}
_c = {}

def pbp(season):
    if season not in _c:
        d = pd.read_csv(os.path.join(ROOT, f"engine/data/nfl/pbp_{season}_slim.csv.gz"), low_memory=False)
        d = d[(d.season_type == "REG") & d.play_type.isin(["pass", "run"]) & (d.two_point_attempt != 1)]
        _c[season] = d
    return _c[season]

def cx(name, season):
    k = (name, season)
    if k not in _c:
        p = os.path.join(ROOT, f"engine/data/nfl/context/{season}/{name}.csv")
        _c[k] = pd.read_csv(p, low_memory=False) if os.path.exists(p) else None
    return _c[k]

def norm(s): return str(s).lower().replace(".", "").replace("'", "").replace(" jr", "").replace(" sr", "").replace(" iii", "").replace(" ii", "").strip()

def positions():
    if "pos" not in _c:
        m = {}
        for s in (PRI, CUR):
            for f in ("ngs_rec", "ngs_rush"):
                d = cx(f, s)
                if d is not None: m.update(dict(zip(d.player_gsis_id, d.player_position)))
        _c["pos"] = m
    return _c["pos"]

def wgt(n): return n / (n + K)

def team_games(d, team): return d[d.posteam == team].game_id.nunique()

# ------------------------------------------------------------- defense vs position (per game, vs league)
def def_vs_pos(season, opp, pos):
    d = pbp(season); P = positions()
    x = d[(d.play_type == "pass") & d.receiver_player_id.notna()].copy(); x["pos"] = x.receiver_player_id.map(P)
    x = x[x.pos == pos]
    g = x.groupby("defteam").agg(tg=("pass_attempt", "size"), yds=("receiving_yards", "sum"), games=("game_id", "nunique"))
    g["tg_pg"] = g.tg / g.games; g["yds_pg"] = g.yds / g.games; g["ypt"] = g.yds / g.tg
    if opp not in g.index: return None
    return g.loc[opp], g[["tg_pg", "yds_pg", "ypt"]].mean(), int(g.loc[opp, "games"])

def blend_def(opp, pos):
    c, p = def_vs_pos(CUR, opp, pos), def_vs_pos(PRI, opp, pos)
    if c is None: return None
    w = wgt(c[2]); out = {}
    for k in ("tg_pg", "yds_pg", "ypt"):
        rel_c = c[0][k] / c[1][k]; rel_p = (p[0][k] / p[1][k]) if p is not None else 1.0
        out[k] = (w * rel_c + (1 - w) * rel_p, c[0][k], c[1][k])
    out["games"] = c[2]; return out

def rush_def(opp):
    res = []
    for s in (CUR, PRI):
        d = pbp(s); r = d[(d.play_type == "run") & (d.qb_scramble != 1)]
        g = r.groupby("defteam").agg(ypc=("rushing_yards", "mean"), att=("rush_attempt", "size"), games=("game_id", "nunique"))
        g["att_pg"] = g.att / g.games
        res.append((g.loc[opp] if opp in g.index else None, g[["ypc", "att_pg"]].mean()))
    (c, lc), (p, lp) = res
    if c is None: return None
    w = wgt(c.games)
    return {k: (w * c[k] / lc[k] + (1 - w) * ((p[k] / lp[k]) if p is not None else 1.0), c[k], lc[k]) for k in ("ypc", "att_pg")} | {"games": int(c.games)}

def pressure(opp):
    d = pbp(CUR); db = d[(d.defteam == opp) & (d.qb_dropback == 1)]
    pf = cx("pfr_def", CUR); pr = pf[pf.team == opp].def_pressures.sum() if pf is not None else np.nan
    allp = d[d.qb_dropback == 1].groupby("defteam").size()
    lg = (pf.groupby("team").def_pressures.sum() / allp).mean() if pf is not None else np.nan
    ftn = cx("ftn", CUR); bl = box8 = lgbl = lgbox = np.nan
    if ftn is not None and "play_id" in d.columns:
        j = ftn.merge(d[["game_id", "play_id", "defteam", "qb_dropback", "play_type"]], left_on=["nflverse_game_id", "nflverse_play_id"],
                      right_on=["game_id", "play_id"])
        dbs = j[j.qb_dropback == 1]; runs = j[j.play_type == "run"]
        bt = dbs.groupby("defteam").n_blitzers.apply(lambda s: (s > 0).mean()); bx = runs.groupby("defteam").n_defense_box.apply(lambda s: (s >= 8).mean())
        bl, lgbl = bt.get(opp, np.nan), bt.mean(); box8, lgbox = bx.get(opp, np.nan), bx.mean()
    return dict(press=pr / len(db) if len(db) else np.nan, lg_press=lg, blitz=bl, lg_blitz=lgbl, box8=box8, lg_box8=lgbox)

def pace(team):
    d = pbp(CUR); t = d[d.posteam == team]; n = t.game_id.nunique()
    allp = d.groupby("posteam").size() / d.groupby("posteam").game_id.nunique()
    neutral = t[(t.wp.between(0.2, 0.8)) & (t.qtr <= 3)]
    return dict(plays=len(t) / n if n else np.nan, lg=allp.mean(), proe=float(neutral.pass_oe.mean()) if len(neutral) else np.nan)

# ------------------------------------------------------------- player role
def role(name):
    out = {}
    s = cx("snaps", CUR)
    if s is not None:
        x = s[s.player.map(norm) == norm(name)].sort_values("week")
        if len(x):
            out.update(team=x.team.iloc[-1], pos=x.position.iloc[-1], snap_season=x.offense_pct.mean(), snap_l3=x.tail(3).offense_pct.mean(),
                       snap_weeks=list(zip(x.tail(4).week, (100 * x.tail(4).offense_pct).round(0))))
    for f, cols in [("ngs_rec", ["targets", "receptions", "yards", "avg_separation", "avg_cushion", "avg_intended_air_yards",
                                 "percent_share_of_intended_air_yards", "avg_yac_above_expectation"]),
                    ("ngs_rush", ["rush_attempts", "rush_yards", "rush_yards_over_expected_per_att", "percent_attempts_gte_eight_defenders"])]:
        rows = []
        for se in (CUR, PRI):
            d = cx(f, se)
            if d is None: continue
            x = d[(d.player_display_name.map(norm) == norm(name)) & (d.season == se) & (d.week > 0) & (d.season_type == "REG")]
            rows.append((se, x))
        cur = rows[0][1] if rows else pd.DataFrame(); pri = rows[1][1] if len(rows) > 1 else pd.DataFrame()
        w = wgt(len(cur))
        for c in cols:
            vc = cur[c].mean() if len(cur) and c in cur else np.nan; vp = pri[c].mean() if len(pri) and c in pri else np.nan
            out[f"{f}_{c}"] = vc if np.isnan(vp) else (vp if np.isnan(vc) else w * vc + (1 - w) * vp)
        out[f"{f}_weeks"] = len(cur)
        if "team" not in out and len(cur): out["team"] = cur.team_abbr.iloc[-1]
        if "pos" not in out and len(cur): out["pos"] = cur.player_position.iloc[-1]
    # target share from pbp (team targets)
    d = pbp(CUR)
    if "team" in out:
        t = d[(d.posteam == out["team"]) & (d.play_type == "pass") & d.receiver_player_id.notna()]
        gid = None
        for f in ("ngs_rec", "ngs_rush"):
            for se in (CUR, PRI):
                g = cx(f, se)
                if gid is None and g is not None:
                    m = g[g.player_display_name.map(norm) == norm(name)]
                    gid = m.player_gsis_id.iloc[0] if len(m) else None
        if gid is not None and len(t):
            mine = t[t.receiver_player_id == gid]
            out["tgt_share"] = len(mine) / len(t); out["tgt_pg"] = len(mine) / max(1, t.game_id.nunique())
            out["air_share"] = mine.air_yards.sum() / t.air_yards.sum() if t.air_yards.sum() else np.nan
        r = d[(d.posteam == out["team"]) & (d.play_type == "run") & (d.qb_scramble != 1)]
        if gid is not None and len(r):
            mr = r[r.rusher_player_id == gid]; out["carry_share"] = len(mr) / len(r); out["carries_pg"] = len(mr) / max(1, r.game_id.nunique())
    return out

def odds_info(date, name):
    tm = TEAMS; lines = {}; opp = home = None
    for f in sorted(glob.glob(os.path.join(ROOT, f"data/odds/nfl/{date}/*.csv")), reverse=True):
        if os.path.basename(f).startswith("games_"): continue
        o = pd.read_csv(f); x = o[o.player.map(norm) == norm(name)]
        if x.empty: continue
        a, h = x.game.iloc[0].split("@"); game = (tm.get(a), tm.get(h))
        main = x[~x.market.str.endswith("_alternate") & x.over.notna() & x.under.notna() & (x.book != "pick6")]
        imp = lambda v: 100 / (v + 100) if v > 0 else -v / (-v + 100)
        for mk, g in main.groupby("market"):
            sh = g[g.book.isin(["pinnacle", "fanduel"])]; ref = sh if len(sh) else g
            L = ref.line.mode().iloc[0]; r = ref[ref.line == L]
            lines[mk] = (float(L), float(np.mean([imp(u_) / (imp(u_) + imp(v_)) for u_, v_ in zip(r.over, r.under)])))
        return game, lines
    return None, lines

def breakdown(date, name, opp=None):
    r = role(name)
    if "team" not in r: return f"### {name}\n- no 2026 snaps/NGS rows found (check the spelling)\n"
    team, pos = r["team"], r.get("pos", "?")
    game, lines = odds_info(date, name)
    if opp is None and game: opp = game[1] if game[0] == team else game[0]
    L = [f"### {name} ({team} {pos}) vs {opp or '?'}"]
    if "snap_season" in r:
        L.append(f"- **Snaps:** {100*r['snap_season']:.0f}% season, {100*r['snap_l3']:.0f}% last 3 (weeks: " +
                 ", ".join(f"wk{w} {p:.0f}%" for w, p in r["snap_weeks"]) + ")")
    if "tgt_share" in r:
        L.append(f"- **Targets:** {r['tgt_pg']:.1f}/g, {100*r['tgt_share']:.0f}% target share, {100*(r.get('air_share') or 0):.0f}% of team air yards · "
                 f"aDOT {r.get('ngs_rec_avg_intended_air_yards', np.nan):.1f} · separation {r.get('ngs_rec_avg_separation', np.nan):.1f} yd · "
                 f"cushion {r.get('ngs_rec_avg_cushion', np.nan):.1f} · YAC over exp {r.get('ngs_rec_avg_yac_above_expectation', np.nan):+.1f}")
    if r.get("carries_pg"):
        L.append(f"- **Carries:** {r['carries_pg']:.1f}/g ({100*r['carry_share']:.0f}% share) · rush yds over expected "
                 f"{r.get('ngs_rush_rush_yards_over_expected_per_att', np.nan):+.2f}/att · {r.get('ngs_rush_percent_attempts_gte_eight_defenders', np.nan):.0f}% of carries vs 8+ box")
    mult = {}
    if opp:
        pp = "WR" if pos in ("WR",) else ("TE" if pos == "TE" else ("RB" if pos in ("RB", "FB") else None))
        if pp:
            dv = blend_def(opp, pp)
            if dv:
                L.append(f"- **{opp} vs {pp}s:** {dv['tg_pg'][1]:.1f} targets/g (lg {dv['tg_pg'][2]:.1f}), {dv['yds_pg'][1]:.0f} yds/g (lg {dv['yds_pg'][2]:.0f}), "
                         f"{dv['ypt'][1]:.1f} yds/target (lg {dv['ypt'][2]:.1f}) over {dv['games']} g → shrunk factor yds x{dv['yds_pg'][0]:.2f}")
                mult["rec_yds"] = 1 + 0.5 * (dv["yds_pg"][0] - 1); mult["receptions"] = 1 + 0.5 * (dv["tg_pg"][0] - 1)
        if r.get("carries_pg"):
            rd = rush_def(opp)
            if rd:
                L.append(f"- **{opp} run defense:** {rd['ypc'][1]:.2f} yds/carry allowed (lg {rd['ypc'][2]:.2f}), {rd['att_pg'][1]:.1f} carries faced/g "
                         f"(lg {rd['att_pg'][2]:.1f}) → shrunk factor x{rd['ypc'][0]:.2f}")
                mult["rush_yds"] = 1 + 0.5 * (rd["ypc"][0] - 1)
        pr = pressure(opp)
        L.append(f"- **{opp} front:** pressure {100*pr['press']:.0f}% of dropbacks (lg {100*pr['lg_press']:.0f}%) · blitz {100*pr['blitz']:.0f}% "
                 f"(lg {100*pr['lg_blitz']:.0f}%) · 8+ man boxes on {100*pr['box8']:.0f}% of runs (lg {100*pr['lg_box8']:.0f}%)")
        pt, po = pace(team), pace(opp)
        L.append(f"- **Pace/script:** {team} {pt['plays']:.1f} plays/g (PROE {pt['proe']:+.1f}%), {opp} {po['plays']:.1f} (lg {pt['lg']:.1f})")
        pf = ((pt["plays"] + po["plays"]) / 2) / pt["lg"]
        for k in mult: mult[k] *= (1 + 0.5 * (pf - 1))
    if mult: L.append("- **Context multipliers (apply to the engine's mean):** " + ", ".join(f"{k} x{v:.2f}" for k, v in mult.items()))
    if lines: L.append("- **Market (line last):** " + ", ".join(f"{k.replace('player_', '')} {v[0]} ({100*v[1]:.0f}% over)" for k, v in lines.items()))
    return "\n".join(L) + "\n"

if __name__ == "__main__":
    D = sys.argv[1]
    for a in sys.argv[2:]:
        n, _, o = a.partition("@")
        print(breakdown(D, n.strip(), o.strip() or None))
