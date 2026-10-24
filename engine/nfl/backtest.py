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
ap = argparse.ArgumentParser(); ap.add_argument("--sims", type=int, default=4000); ap.add_argument("--hl", type=float, default=3.0)
ap.add_argument("--prior_w", type=float, default=0.1); ap.add_argument("--conc", type=float, default=None); ap.add_argument("--cconc", type=float, default=None)
ap.add_argument("--quiet", action="store_true")
A = ap.parse_args()
C.N_SIMS = A.sims
if A.conc: C.SHARE_CONC = A.conc
if A.cconc: C.CARRY_CONC = A.cconc
import model as M

import shares as S
pg = S.build(); TGT_PER_ATT = S.TGT_PER_ATT
features = lambda s, w: S.features(s, w, A.hl, A.prior_w)

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
