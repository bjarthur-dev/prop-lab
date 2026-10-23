"""End-to-end test on a synthetic league with known truth. Run: python engine/nba/tests/test_synthetic.py"""
import os, sys, tempfile
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import config as C
C.BLOWOUT_MIN_PER_PT = 0.0  # synthetic truth has no blowout minutes effect
from model import load_logs, player_baselines, project_game, fit_vmr, simulate
from price import price_board
from common import nb_draw

rng = np.random.default_rng(0)
TEAMS = [f"T{i:02d}" for i in range(30)]
VMR_TRUE = {"pts": 2.2, "reb": 1.3, "ast": 1.4, "fg3m": 1.2}

def make_league():
    players = []
    for t in TEAMS:
        mins = np.array([35, 33, 31, 29, 27, 22, 20, 17, 14, 12, 0, 0, 0], float)
        for j, m in enumerate(mins):
            players.append(dict(pid=len(players), name=f"P{len(players)}", team=t, min=m,
                                pts=rng.uniform(0.35, 0.9), reb=rng.uniform(0.1, 0.4), ast=rng.uniform(0.05, 0.3), fg3m=rng.uniform(0.02, 0.12),
                                p3=rng.uniform(0.30, 0.42)))
    return pd.DataFrame(players)

def play(P, season_id, start, n_days):
    rows = []
    for d in range(n_days):
        date = pd.Timestamp(start) + pd.Timedelta(days=2 * d)
        for t in TEAMS:
            team = P[(P.team == t) & (P["min"] > 0)]
            for r in team.itertuples():
                m = float(np.clip(rng.normal(r.min, 4), 0, 48))
                if m <= 0: continue
                rec = dict(SEASON_ID=season_id, PLAYER_ID=r.pid, PLAYER_NAME=r.name, TEAM_ABBREVIATION=t, GAME_ID=f"{t}{d}",
                           GAME_DATE=date.date(), MIN=round(m))
                for s in ("pts", "reb", "ast"):
                    rec[s.upper()] = int(nb_draw(rng, np.array([getattr(r, s) * m]), VMR_TRUE[s])[0])
                a3 = int(nb_draw(rng, np.array([r.fg3m / r.p3 * m]), 1.3)[0])
                rec["FG3A"], rec["FG3M"] = a3, int(rng.binomial(a3, r.p3))
                rows.append(rec)
    return pd.DataFrame(rows)

def main():
    P = make_league()
    prior = play(P, "22025", "2025-10-21", 70)
    cur = play(P, "22026", "2026-10-21", 6)
    tmp = tempfile.mkdtemp()
    prior.to_csv(f"{tmp}/p1.csv", index=False); cur.to_csv(f"{tmp}/p2.csv", index=False)
    logs = load_logs([f"{tmp}/p1.csv", f"{tmp}/p2.csv"])
    base, lg = player_baselines(logs, "2026-11-05", "22026")
    vmr = fit_vmr(logs)
    print("fitted VMR:", {k: round(v, 2) for k, v in vmr.items()}, " true:", VMR_TRUE)
    # 1) rate recovery
    m = base.merge(P, left_on="player_id", right_on="pid")
    for s in ("pts", "reb", "ast"):
        err = (m[f"{s}_pm"] - m[s]).abs().mean() / m[s].mean()
        print(f"rate recovery {s}: mean abs error {err*100:.1f}% of avg"); assert err < 0.12
    # 1b) threes: padded 3P% beats raw current-season 3P% (the H4 mechanism)
    mm = m[m["fg3a_cur"] >= 15]
    e_pad, e_raw = (mm["p3_x"] - mm["p3_y"]).abs().mean(), (mm["p3_raw_cur"] - mm["p3_y"]).abs().mean()
    print(f"3P% error: padded {e_pad*100:.1f} pts vs raw current {e_raw*100:.1f} pts (n={len(mm)})"); assert e_pad < e_raw
    # 2) project a neutral game, compare projected means to truth (no market scaling: implied = truth sum)
    home, away = "T00", "T01"
    truth_pts = {t: (P[P.team == t]["min"] * P[P.team == t]["pts"]).sum() for t in (home, away)}
    total = truth_pts[home] + truth_pts[away]; spread_home = truth_pts[away] - truth_pts[home]
    proj = project_game(base, home, away, spread_home, total, league_total=total)
    j = proj.merge(P, left_on="player_id", right_on="pid")
    e = ((j["pts_mu"] - j["pts"] * j["min"]).abs()).mean()
    print(f"projected points MAE vs truth: {e:.2f}"); assert e < 2.5
    # 3) calibration: P(over truth-median line) on fresh simulated games should match
    briers, hits, preds = [], [], []
    for r in j.itertuples():
        sim = simulate(proj.loc[proj.player_id == r.player_id].iloc[0], vmr, n=8000)
        line = np.floor(r.pts * r.min) + 0.5
        p = (sim["pts"] > line).mean()
        for _ in range(100):
            mm = float(np.clip(rng.normal(r.min, 4), 0, 48))
            y = nb_draw(rng, np.array([r.pts * mm]), 2.2)[0] > line
            preds.append(p); hits.append(y)
    preds, hits = np.array(preds), np.array(hits)
    for lo, hi in ((0, .4), (.4, .5), (.5, .6), (.6, 1)):
        k = (preds >= lo) & (preds < hi)
        if k.sum(): print(f"  calib {lo:.1f}-{hi:.1f}: predicted {preds[k].mean():.3f} actual {hits[k].mean():.3f} (n={k.sum()})")
    gap = abs(preds.mean() - hits.mean()); print(f"calibration-in-the-large gap: {gap*100:.1f} pts"); assert gap < 0.04
    # 4) fair board (true probabilities + 4.5% vig) must produce few false edges; a planted mispricing must be found
    rows = []
    for r in j.itertuples():
        mm = rng.normal(r.min, 4, 20000).clip(0, 48)
        ytrue = nb_draw(rng, r.pts * mm, 2.2)
        line = np.floor(r.pts * r.min) + 0.5
        pt = (ytrue > line).mean()
        def am(p): p = min(max(p, .03), .97); return -100 * p / (1 - p) if p >= .5 else 100 * (1 - p) / p
        po, pu = pt * 1.0225, (1 - pt) * 1.0225
        rows.append(dict(player=r.name, market="pts", line=line, book="FanDuel", over=am(po), under=am(pu), executable=True, ts="t"))
        for bk in ("Pinnacle", "Circa", "Caesars"):
            rows.append(dict(player=r.name, market="pts", line=line, book=bk, over=am(po), under=am(pu), executable=False, ts="t"))
    board = pd.DataFrame(rows)
    proj["key"] = proj["player"].str.lower()
    res = price_board(proj, board, vmr)
    flagged = res[res["decision"] != "PASS"]
    full = flagged[flagged["decision"].isin(["BET", "PAPER"])]
    print(f"fair board: {len(flagged)} of {len(res)} sides flagged (WATCH or above), {len(full)} at the full Rules §3 bar (want 0-1)")
    print(flagged[["player","side","p_model","p_market","shrunk_edge_pts","p_blend","why"]].to_string(index=False))
    assert len(full) <= 1
    bad = board.copy(); fd0 = bad.index[(bad.book == "FanDuel")][0]
    bad.loc[fd0, ["over", "under"]] = [+150, -185]   # planted: soft book hangs the over far too long vs 3 sharp books
    res2 = price_board(proj, bad, vmr)
    hit = res2[(res2.player == board.loc[0, "player"]) & (res2.side == "over")]["decision"].iloc[0]
    print(f"planted mispricing on {board.loc[0,'player']} over: {hit}"); assert hit in ("PAPER", "BET")
    print("ALL SYNTHETIC TESTS PASSED")

if __name__ == "__main__":
    main()
