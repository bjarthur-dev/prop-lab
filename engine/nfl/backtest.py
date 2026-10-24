"""Walk-forward NFL player-prop backtest (engine v1). Run from vault root: python engine/nfl/backtest.py [--sims 4000]
Each test week is projected from games BEFORE it only (current season, recency-weighted, + prior season at low weight).
No historical prop lines in pbp, so each player's 'line' = his own projected median rounded to .5 (where books set lines);
checks: mean error vs naive average, P(over) calibration, 10/90 band coverage, ATD calibration.
Writes engine/out/nfl_backtest_report.txt. Caveat: conditions on the player appearing (>=1 target/carry), which
slightly flatters volume vs a pregame view that must also price DNP/limited snaps."""
import os, sys, argparse
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config as C
ap = argparse.ArgumentParser(); ap.add_argument("--sims", type=int, default=4000); ap.add_argument("--hl", type=float, default=4.0)
ap.add_argument("--prior_w", type=float, default=0.3); ap.add_argument("--conc", type=float, default=None); ap.add_argument("--cconc", type=float, default=None)
ap.add_argument("--quiet", action="store_true")
A = ap.parse_args()
C.N_SIMS = A.sims
if A.conc: C.SHARE_CONC = A.conc
if A.cconc: C.CARRY_CONC = A.cconc
import model as M
from calibrate import load, team_games

d = load(); tg = team_games(d)
p = d[(d.two_point_attempt != 1) & (d.qb_kneel != 1) & (d.qb_spike != 1) & d.play_type.isin(["pass", "run"])].copy()
p["rz"] = p.yardline_100 <= 10
des_run = p[(p.play_type == "run") & (p.qb_scramble != 1) & p.rusher_player_id.notna()]
tgts = p[(p.play_type == "pass") & p.receiver_player_id.notna()]
team_rz_car = des_run[des_run.rz].groupby(["game_id", "posteam"]).size().rename("t_rz_car")
team_rz_tgt = tgts[tgts.rz].groupby(["game_id", "posteam"]).size().rename("t_rz_tgt")
rec = tgts.groupby(["game_id", "posteam", "receiver_player_id"]).agg(name=("receiver_player_name", "first"),
      targets=("pass_attempt", "size"), receptions=("complete_pass", "sum"), rec_yds=("receiving_yards", "sum"),
      rz_tgt=("rz", "sum")).reset_index().rename(columns={"receiver_player_id": "pid"})
ru = des_run.groupby(["game_id", "posteam", "rusher_player_id"]).agg(rname=("rusher_player_name", "first"),
      carries=("rush_attempt", "size"), rush_yds=("rushing_yards", "sum"), rz_car=("rz", "sum")).reset_index().rename(columns={"rusher_player_id": "pid"})
pg = rec.merge(ru, on=["game_id", "posteam", "pid"], how="outer")
pg["name"] = pg.name.fillna(pg.rname); pg = pg.drop(columns="rname").fillna({c: 0 for c in ["targets", "receptions", "rec_yds", "rz_tgt", "carries", "rush_yds", "rz_car"]})
td = d[d.td_player_id.notna() & (d.touchdown == 1) & ((d.rush_touchdown == 1) | (d.pass_touchdown == 1))]
tdc = td.groupby(["game_id", "td_player_id"]).size().rename("tds").reset_index().rename(columns={"td_player_id": "pid"})
pg = pg.merge(tdc, on=["game_id", "pid"], how="left").fillna({"tds": 0})
pg = pg.merge(tg[["game_id", "posteam", "season", "week", "att", "rushes", "team_spread", "total", "home", "away", "spread_line"]], on=["game_id", "posteam"])
pg = pg.merge(team_rz_car, on=["game_id", "posteam"], how="left").merge(team_rz_tgt, on=["game_id", "posteam"], how="left").fillna({"t_rz_car": 0, "t_rz_tgt": 0})
# a pass target counts against aimed attempts; use team targets as the share denominator (throwaways excluded)
team_tgt = tgts.groupby(["game_id", "posteam"]).size().rename("t_tgt")
pg = pg.merge(team_tgt, on=["game_id", "posteam"], how="left")
TGT_PER_ATT = (tgts.groupby(["game_id", "posteam"]).size().sum() / tg.att.sum())

def features(s, w):
    h = pg[((pg.season == s) & (pg.week < w)) | (pg.season == s - 1)].copy()
    cur = h.season == s
    h["wt"] = np.where(cur, 0.5 ** ((w - h.week) / A.hl), A.prior_w)
    agg = lambda c: (h[c] * h.wt)
    h["w_tg"], h["w_ttg"], h["w_car"], h["w_tr"] = agg("targets"), agg("t_tgt"), agg("carries"), agg("rushes")
    h["w_rzc"], h["w_trzc"], h["w_rzt"], h["w_trzt"] = agg("rz_car"), agg("t_rz_car"), agg("rz_tgt"), agg("t_rz_tgt")
    f = h.groupby("pid").agg(name=("name", "last"), team=("posteam", "last"), n_cur=("season", lambda x: (x == s).sum()),
        w_tg=("w_tg", "sum"), w_ttg=("w_ttg", "sum"), w_car=("w_car", "sum"), w_tr=("w_tr", "sum"),
        w_rzc=("w_rzc", "sum"), w_trzc=("w_trzc", "sum"), w_rzt=("w_rzt", "sum"), w_trzt=("w_trzt", "sum"),
        tg=("targets", "sum"), rc=("receptions", "sum"), ry=("rec_yds", "sum"), car=("carries", "sum"), rsy=("rush_yds", "sum"),
        cur_rec_yds=("rec_yds", lambda x: x[h.loc[x.index, "season"] == s].mean()),
        cur_rush_yds=("rush_yds", lambda x: x[h.loc[x.index, "season"] == s].mean()),
        cur_rec=("receptions", lambda x: x[h.loc[x.index, "season"] == s].mean()),
        cur_car=("carries", lambda x: x[h.loc[x.index, "season"] == s].mean()))
    f["tgt_share"] = f.w_tg / f.w_ttg.clip(lower=1e-9) * TGT_PER_ATT       # targets per aimed attempt
    f["carry_share"] = f.w_car / f.w_tr.clip(lower=1e-9)
    f["catch_rate"] = (f.rc + 0.65 * 40) / (f.tg + 40)
    f["ypc"] = (f.ry + 10.9 * 30) / (f.rc + 30)
    f["ypc_rush"] = (f.rsy + 4.2 * 60) / (f.car + 60)
    f["rz_carry_share"] = (f.w_rzc + 0.5 * f.carry_share) / (f.w_trzc + 0.5)
    f["ez_tgt_share"] = (f.w_rzt + 0.5 * f.tgt_share) / (f.w_trzt + 0.5)
    f["pos"] = np.where(f.carry_share > 0.25, "RB", "WR")
    return f

TESTS = [(2024, w) for w in range(3, 19)] + [(2025, w) for w in range(3, 19)] + [(2026, w) for w in range(3, 8)]
rows = []
for s, w in TESTS:
    wk = pg[(pg.season == s) & (pg.week == w)]
    if wk.empty: continue
    f = features(s, w)
    for gid, gg in wk.groupby("game_id"):
        g0 = gg.iloc[0]
        game = dict(home=g0.home, away=g0.away, spread_home=-g0.spread_line, total=g0.total)
        act = gg.set_index("pid")
        cand = f[f.index.isin(act.index) & (f.n_cur >= 2) & ((f.tgt_share >= 0.10) | (f.carry_share >= 0.30))].copy()
        cand["team"] = act.loc[cand.index, "posteam"].values          # current team (handles trades)
        if cand.empty: continue
        cand = cand.reset_index().rename(columns={"pid": "player"})
        cand.loc[cand.carry_share < 0.05, "carry_share"] = 0
        res = M.simulate_game(game, cand, seed=hash(gid) % 2**31)
        for _, r in cand.iterrows():
            o = res[r.player]; a = act.loc[r.player]
            base = dict(season=s, week=w, game_id=gid, pid=r.player, name=r["name"], pos=r.pos)
            for stat, naive in [("rec_yds", r.cur_rec_yds), ("receptions", r.cur_rec), ("rush_yds", r.cur_rush_yds), ("carries", r.cur_car)]:
                if stat not in o: continue
                if stat in ("rec_yds", "receptions") and r.tgt_share < 0.10: continue
                if stat in ("rush_yds", "carries") and r.carry_share < 0.30: continue
                sim = o[stat]; med = np.median(sim); line = np.floor(med) + 0.5
                rows.append(dict(base, stat=stat, mu=sim.mean(), med=med, naive=naive, actual=a[stat], line=line,
                                 p_over=(sim > line).mean(), q10=np.quantile(sim, .1), q90=np.quantile(sim, .9)))
            rows.append(dict(base, stat="atd", mu=o["td_lambda"], p_over=(o["td"] > 0).mean(), actual=float(a.tds > 0), line=0.5))
R = pd.DataFrame(rows); os.makedirs("engine/out", exist_ok=True); R.to_csv("engine/out/nfl_backtest_rows.csv", index=False)
out = []; P = lambda x: (out.append(x), None if A.quiet else print(x))
P(f"NFL engine v1 walk-forward backtest | {R[['season','week']].drop_duplicates().shape[0]} weeks | {R.game_id.nunique()} games | hl={A.hl} prior_w={A.prior_w} conc={C.SHARE_CONC} cconc={C.CARRY_CONC}")
for stat in ["rec_yds", "receptions", "rush_yds", "carries"]:
    x = R[R.stat == stat]
    mae_m, mae_n = (x.med - x.actual).abs().mean(), (x.naive - x.actual).abs().mean()
    over = (x.actual > x.line).mean(); pred = x.p_over.mean()
    cov_lo, cov_hi = (x.actual < x.q10).mean(), (x.actual > x.q90).mean()
    P(f"\n{stat}: n={len(x)}  MAE median {mae_m:.2f} vs naive season-avg {mae_n:.2f} ({(1-mae_m/mae_n)*100:+.1f}%)  bias(mean-actual) {(x.mu-x.actual).mean():+.2f}")
    P(f"  P(over own-median line): predicted {pred:.3f} actual {over:.3f} | below q10 {cov_lo:.3f} above q90 {cov_hi:.3f} (target .10/.10)")
    # discrimination: does the model's over-prob relative to 0.5 line up? use Brier vs 0.5 using a stricter line = naive-based
    xx = x.dropna(subset=["naive"]).copy()
    xx["nl"] = np.floor(xx.naive) + 0.5
    # p(over naive line) from normal approx of sim quantiles not stored; skip
    for lo, hi in [(0, .45), (.45, .55), (.55, 1)]:
        b = x[(x.p_over >= lo) & (x.p_over < hi)]
        if len(b) > 30: P(f"  bin {lo:.2f}-{hi:.2f}: n={len(b)} pred {b.p_over.mean():.3f} actual {(b.actual > b.line).mean():.3f}")
x = R[R.stat == "atd"]
P(f"\nanytime TD: n={len(x)} predicted {x.p_over.mean():.3f} actual {x.actual.mean():.3f}  Brier {((x.p_over-x.actual)**2).mean():.4f} vs base-rate {((x.actual.mean()-x.actual)**2).mean():.4f}")
for lo, hi in [(0, .15), (.15, .25), (.25, .35), (.35, .45), (.45, 1)]:
    b = x[(x.p_over >= lo) & (x.p_over < hi)]
    if len(b) > 30: P(f"  bin {lo:.2f}-{hi:.2f}: n={len(b)} pred {b.p_over.mean():.3f} actual {b.actual.mean():.3f}")
open("engine/out/nfl_backtest_report.txt", "w").write("\n".join(out))
