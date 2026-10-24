"""Run NFL engine v1 for a date. From the vault root:
    python engine/nfl/run_nfl.py 2026-10-25
Reads engine/out/DATE/nfl_games.csv (home,away,spread_home,total,weather[,proe_home_cur,proe_home_prior,proe_away_cur,proe_away_prior])
      engine/out/DATE/nfl_shares.csv (player,team,pos,tgt_share,catch_rate,ypc,carry_share,ypc_rush,rz_carry_share,ez_tgt_share)
      engine/out/DATE/nfl_board.csv  (player,market,line,book,over,under,executable)  market in receptions|rec_yds|rush_yds|carries|longest_rec|td
Writes engine/out/DATE/nfl_candidates.csv + nfl_summary.md. v1 = PAPER/WATCH only (no backtest yet)."""
import os, sys
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from model import simulate_game

MW, MIN_SHRUNK, MIN_BLEND, MAX_GAP = 0.75, 3.0, 2.0, 10.0

def dec(a): a = float(a); return 1 + a / 100 if a > 0 else 1 + 100 / -a
def imp(a): return 1 / dec(a)
def devig(o, u): po, pu = imp(o), imp(u); return po / (po + pu)

def main(date):
    out = f"engine/out/{date}"
    games, shares = pd.read_csv(f"{out}/nfl_games.csv"), pd.read_csv(f"{out}/nfl_shares.csv")
    board = pd.read_csv(f"{out}/nfl_board.csv")
    sims = {}
    for i, g in games.iterrows():
        proe = {g.home: (g.get("proe_home_cur", 0) or 0, g.get("proe_home_prior", 0) or 0),
                g.away: (g.get("proe_away_cur", 0) or 0, g.get("proe_away_prior", 0) or 0)}
        sims.update(simulate_game(dict(home=g.home, away=g.away, spread_home=g.spread_home, total=g.total, proe=proe,
                                       weather=g.get("weather", "calm") if isinstance(g.get("weather"), str) else "calm"),
                                  shares, seed=100 + i))
    rows = []
    for (pl, mk, ln), grp in board.groupby(["player", "market", "line"]):
        if pl not in sims or mk not in sims[pl]:
            rows.append(dict(player=pl, market=mk, line=ln, decision="PASS", why="no projection")); continue
        x = sims[pl][mk]; po = float((x > ln).mean() if mk != "td" else (x > 0).mean())
        two = grp.dropna(subset=["over", "under"])
        ex = grp[grp["executable"].astype(str).str.lower().isin(["true", "1"])]
        for side in ("over", "under"):
            best = ex.dropna(subset=[side])
            if best.empty: continue
            b = best.loc[best[side].map(dec).idxmax()]
            refs = two[two["book"] != b["book"]]; refs = refs if len(refs) else two
            pm = po if side == "over" else 1 - po
            pk = (np.median([devig(o, u) for o, u in zip(refs["over"], refs["under"])]) if len(refs) else np.nan)
            pk = pk if side == "over" else 1 - pk
            be = imp(b[side]); shrunk = 40 * (pm - be); gap = 100 * (pm - pk) if pk == pk else np.nan
            pb = MW * pk + (1 - MW) * pm if pk == pk else np.nan     # v1: probability blend (NBA uses mean blend)
            ok = pk == pk and shrunk >= MIN_SHRUNK and 3 <= gap <= MAX_GAP and 100 * (pb - be) >= MIN_BLEND
            dec_ = "PAPER" if ok else ("WATCH" if shrunk >= 1.5 else "PASS")
            rows.append(dict(player=pl, market=mk, line=ln, side=side, book=b["book"], price=b[side], mean=round(float(np.mean(x)), 1),
                             median=round(float(np.median(x)), 1), p_model=round(pm, 3), p_market=round(pk, 3) if pk == pk else None,
                             p_blend=round(pb, 3) if pb == pb else None, break_even=round(be, 3), shrunk_edge_pts=round(shrunk, 1),
                             model_vs_market_pts=round(gap, 1) if gap == gap else None, decision=dec_))
    res = pd.DataFrame(rows); res.to_csv(f"{out}/nfl_candidates.csv", index=False)
    # tracker trigger candidates (N1: RB/TE rec yds <= 24.5 under; N7: weather flag) — logged by Claude with controls
    pos = shares.set_index("player")["pos"].to_dict()
    n1 = board[(board.market == "rec_yds") & (board.line <= 24.5) & board.player.map(pos).isin(["RB", "TE"])]
    with open(f"{out}/nfl_summary.md", "w", encoding="utf-8") as f:
        keep = res[res.decision.isin(["PAPER", "WATCH"])] if "decision" in res else res
        f.write(f"# NFL engine v1 — {date}\n\nPriced {len(res)} sides; {(res.decision=='PAPER').sum()} PAPER, {(res.decision=='WATCH').sum()} WATCH.\n\n")
        f.write(keep.to_markdown(index=False) if len(keep) else "_Nothing cleared._")
        f.write(f"\n\n## N1 trigger candidates (RB/TE rec yds ≤ 24.5)\n" + (n1[["player", "line", "book", "over", "under"]].drop_duplicates().to_markdown(index=False) if len(n1) else "none") + "\n")
    print(open(f"{out}/nfl_summary.md", encoding="utf-8").read())

if __name__ == "__main__":
    main(sys.argv[1])
