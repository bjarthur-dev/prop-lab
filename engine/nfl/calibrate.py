"""Fit NFL engine v1 team-level constants from nflverse pbp (regular season). Run from vault root:
python engine/nfl/calibrate.py  -> prints fitted values + writes engine/out/nfl_calibration.txt"""
import glob, numpy as np, pandas as pd
def load(years=(2023, 2024, 2025, 2026)):
    fs = [f"engine/data/nfl/pbp_{y}_slim.csv.gz" for y in years]
    d = pd.concat([pd.read_csv(f, low_memory=False) for f in fs if glob.glob(f)], ignore_index=True)
    return d[d.season_type == "REG"]
def team_games(d):
    p = d[(d.two_point_attempt != 1) & (d.qb_kneel != 1) & (d.qb_spike != 1) & d.posteam.notna()]
    p = p[p.play_type.isin(["pass", "run"])]
    g = p.groupby(["game_id", "posteam"]).agg(season=("season", "first"), week=("week", "first"),
        home=("home_team", "first"), away=("away_team", "first"), spread_line=("spread_line", "first"),
        total=("total_line", "first"), hs=("home_score", "first"), as_=("away_score", "first"),
        plays=("play_type", "size"), dropbacks=("qb_dropback", "sum"), sacks=("sack", "sum"),
        scr=("qb_scramble", "sum"), att=("pass_attempt", "sum"), rush_td=("rush_touchdown", "sum"),
        pass_td=("pass_touchdown", "sum"), roof=("roof", "first"), wind=("wind", "first")).reset_index()
    g["att"] = g.dropbacks - g.sacks - g.scr                 # aimed throws (incl. throwaways)
    g["rushes"] = g.plays - g.dropbacks
    ish = g.posteam == g.home
    g["team_spread"] = np.where(ish, -g.spread_line, g.spread_line)   # nflverse spread_line>0 = home favored
    g["pts"] = np.where(ish, g.hs, g.as_); g["opp_pts"] = np.where(ish, g.as_, g.hs)
    g["margin"] = g.pts - g.opp_pts
    g["imp_pts"] = (g.total - g.team_spread) / 2
    g["pass_rate"] = g.dropbacks / g.plays
    return g
def main():
    d = load(); g = team_games(d)
    out = []
    P = lambda s: (print(s), out.append(s))
    P(f"team-games: {len(g)} (seasons {sorted(g.season.unique())})")
    b = np.polyfit(g.total - 44, g.plays, 1); P(f"PLAYS: base {b[1]:.1f} at 44 total, slope {b[0]:.3f}/pt, resid sd {np.std(g.plays - np.polyval(b, g.total - 44)):.1f}")
    P(f"MARGIN_SD: {np.std(g.margin + g.team_spread):.2f}  (bias {np.mean(g.margin + g.team_spread):+.2f})")
    X = np.column_stack([np.ones(len(g)), g.team_spread, (g.margin + g.team_spread) / 14.0])
    c, *_ = np.linalg.lstsq(X, g.pass_rate, rcond=None)
    P(f"PASS RATE: base {c[0]:.3f}, spread slope {c[1]:+.4f}/pt, script term {c[2]:+.4f} per 14 pts surprise (engine sign: -SCRIPT_K)")
    P(f"SACK_RATE {g.sacks.sum()/g.dropbacks.sum():.4f}  SCRAMBLE_RATE {g.scr.sum()/(g.dropbacks-g.sacks).sum():.4f}")
    tds = g.rush_td + g.pass_td
    P(f"TD_PTS_SHARE (7*off TDs / pts): {7*tds.sum()/g.pts.sum():.3f}   RUSH_TD_SHARE {g.rush_td.sum()/tds.sum():.3f}")
    P(f"implied-points check: mean pts {g.pts.mean():.2f} vs implied {g.imp_pts.mean():.2f}; corr {np.corrcoef(g.pts, g.imp_pts)[0,1]:.3f}")
    # per-play TD rate vs implied pts (for TD lambda)
    P(f"off TDs per team-game: {tds.mean():.2f}; slope vs implied pts {np.polyfit(g.imp_pts, tds, 1)[0]:.3f}/pt")
    # weather: pass yards per attempt by wind
    pp = d[(d.play_type == "pass") & (d.qb_spike != 1)].copy()
    pp["wind"] = pd.to_numeric(pp.wind, errors="coerce")
    outdoor = pp[pp.roof.isin(["outdoors", "open"])]
    base = outdoor[outdoor.wind < 10].yards_gained.mean()
    for lo, hi in [(10, 15), (15, 20), (20, 60)]:
        s = outdoor[(outdoor.wind >= lo) & (outdoor.wind < hi)]
        P(f"wind {lo}-{hi}: yds/dropback ratio {s.yards_gained.mean()/base:.3f} (n={len(s)})")
    rec = d[(d.complete_pass == 1) & d.receiving_yards.notna()]
    P(f"per-catch yds overall: mean {rec.receiving_yards.mean():.2f} sd {rec.receiving_yards.std():.2f}")
    ru = d[(d.play_type == "run") & (d.qb_scramble != 1) & d.rushing_yards.notna()]
    P(f"carries: ypc {ru.rushing_yards.mean():.2f}, share >=15 yds {(ru.rushing_yards>=15).mean():.3f}, mean yds of those {ru[ru.rushing_yards>=15].rushing_yards.mean():.1f}, sd of rest {ru[ru.rushing_yards<15].rushing_yards.std():.2f}")
    import os; os.makedirs("engine/out", exist_ok=True)
    open("engine/out/nfl_calibration.txt", "w").write("\n".join(out))
if __name__ == "__main__": main()
