"""Run the NBA engine for one date. From the vault root:
    python engine/nba/run_slate.py 2026-10-24 [--class large] [--caps engine/out/DATE/min_caps.csv]
Reads engine/data/players_*.csv (fetch.py) and engine/out/DATE/{slate,outs,board}.csv (scout_to_csv.py).
Writes engine/out/DATE/projections.csv, candidates.csv and a markdown summary for the slate note."""
import os, sys, argparse, glob
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
import config as C
from common import norm_name
from model import load_logs, player_baselines, project_game, fit_vmr
from price import price_board

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("date"); ap.add_argument("--class", dest="cls", default="large")
    ap.add_argument("--caps", default=None); a = ap.parse_args()
    out = f"{C.OUT_DIR}/{a.date}"
    logs = load_logs(sorted(glob.glob(f"{C.DATA_DIR}/players_*.csv")))
    base, lg = player_baselines(logs, a.date, C.SEASON_ID_CUR)
    vmr = fit_vmr(logs)
    teams = glob.glob(f"{C.DATA_DIR}/teams_*.csv")
    lg_total = C.LEAGUE_AVG_TOTAL
    if teams:
        t = pd.concat(pd.read_csv(p) for p in teams); lg_total = 2 * t["PTS"].mean()
    slate = pd.read_csv(f"{out}/slate.csv")
    outs = set(pd.read_csv(f"{out}/outs.csv")["player"].map(norm_name)) if os.path.exists(f"{out}/outs.csv") else set()
    caps = {}
    if a.caps and os.path.exists(a.caps):
        caps = {norm_name(r.player): float(r.minutes) for r in pd.read_csv(a.caps).itertuples()}
    mset = {}
    if os.path.exists(f"{out}/min_set.csv"):   # confirmed starters / replacement roles: player,minutes
        mset = {norm_name(r.player): float(r.minutes) for r in pd.read_csv(f"{out}/min_set.csv").itertuples()}
    proj = pd.concat([project_game(base, g.home, g.away, g.spread_home, g.total, out_keys=outs, min_overrides=caps, min_set=mset,
                                   league_total=lg_total) for g in slate.dropna(subset=["spread_home", "total"]).itertuples()],
                     ignore_index=True)
    proj.to_csv(f"{out}/projections.csv", index=False)
    print(f"projected {len(proj)} players | VMR {dict((k, round(v, 2)) for k, v in vmr.items())} | league total {lg_total:.1f}")
    if os.path.exists(f"{out}/board.csv"):
        cand = price_board(proj, pd.read_csv(f"{out}/board.csv"), vmr, a.cls)
        # v1.4 model-health gate: if the model disagrees with the market in the SAME direction across the whole board,
        # that's a model problem, not dozens of edges. Downgrade every BET/PAPER to WATCH.
        gp = cand.dropna(subset=["p_model", "p_market"])
        over = gp[gp["side"] == "over"]
        lean = float(100 * (over["p_model"] - over["p_market"]).mean()) if len(over) >= 20 else 0.0
        print(f"board lean (model - market on overs): {lean:+.1f} pts over {len(over)} sides")
        if abs(lean) > C.MAX_BOARD_LEAN_PTS:
            hit = cand["decision"].isin(["BET", "PAPER"])
            cand.loc[hit, "why"] = f"board-wide lean {lean:+.1f} pts > {C.MAX_BOARD_LEAN_PTS} (model health gate)"
            cand.loc[hit, ["decision", "stake_pct"]] = ["WATCH", 0.0]
        cand.to_csv(f"{out}/candidates.csv", index=False)
        keep = cand[cand["decision"].isin(["BET", "PAPER", "WATCH"])].sort_values(["decision", "blend_edge_pts"], ascending=[True, False])
        cols = ["player", "market", "line", "side", "book", "price", "mu", "p_model", "p_market", "p_blend", "break_even", "shrunk_edge_pts", "market_edge_pts", "blend_edge_pts", "path", "decision", "stake_pct", "why"]
        with open(f"{out}/summary.md", "w", encoding="utf-8") as f:
            f.write(f"# NBA engine v1 — {a.date}\n\nPriced {len(cand)} sides; {(cand.decision.isin(["BET","PAPER"])).sum()} BET/PAPER (staked), {(cand.decision=="WATCH").sum()} WATCH (tracked, no stake), rest PASS. VMR fitted: {vmr}.\n\n")
            f.write(keep.reindex(columns=cols).to_markdown(index=False) if len(keep) else "_No candidates cleared the bar._")
            f.write("\n\nNo-projection rows (name mismatch / not in rotation): " + ", ".join(sorted(set(cand.loc[cand.get('why','').astype(str).str.startswith('no projection'), 'player']))) + "\n")
        print(open(f"{out}/summary.md", encoding="utf-8").read())

if __name__ == "__main__":
    main()
