"""Grade the PRICE-EDGE method on every qualifying leg the scans found, not only the ones placed.
    python engine/edge_grade.py            (all dates)  -> Record/Shadow/Price Edge Report.md + data/shadow/edges_graded.csv
Qualifying = DraftKings price beats the sharp fair (EV vs Pinnacle/FanDuel >= 2%) and the all-book consensus (EV >= 0).
For each leg: result (NBA game logs), profit at the DK price for a 1-unit bet, and CLV = sharp fair at the last
pre-tip snapshot x DK decimal - 1 (did the market move toward us?). This is the evidence for how much to bet on it."""
import os, sys, glob
import numpy as np, pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "nba"))
from common import norm_name

COL = {"player_points": "PTS", "player_rebounds": "REB", "player_assists": "AST", "player_threes": "FG3M"}
def imp(a): a = float(a); return 100 / (a + 100) if a > 0 else -a / (-a + 100)
def dec(a): a = float(a); return 1 + a / 100 if a > 0 else 1 + 100 / -a

def actuals():
    d = pd.read_csv("engine/data/players_2026-27.csv"); d["key"] = d.PLAYER_NAME.map(norm_name)
    d["date"] = d.GAME_DATE.astype(str).str[:10]; return d

def close_fair(date, player, market, line, start):
    """sharp devigged P(over) at the latest snapshot taken before tip-off."""
    best = None
    for f in sorted(glob.glob(f"data/odds/nba/{date}/*.csv")):
        if os.path.basename(f).startswith("games_"): continue
        try: o = pd.read_csv(f)
        except Exception: continue
        if "snap_et" not in o or o.empty: continue
        snap = str(o.snap_et.iloc[0])[:16]
        if start and snap >= str(start)[:16]: continue
        x = o[(o.player == player) & (o.market == market) & (o.line == line) & o.book.isin(["pinnacle", "fanduel"]) & o.over.notna() & o.under.notna()]
        if len(x): best = (snap, float(np.mean([imp(a) / (imp(a) + imp(b)) for a, b in zip(x.over, x.under)])))
    return best

def main():
    acts = actuals(); last = acts.date.max(); rows = []
    for f in sorted(glob.glob("data/edges/20??-??-??.csv")):
        date = os.path.basename(f)[:10]
        if date > last: continue
        e = pd.read_csv(f)
        e = e[(e.sport.str.upper() == "NBA") & (e.ev_sharp >= 2) & (e.ev_all >= 0) & e.market.isin(COL.keys())]
        a = acts[acts.date == date].set_index("key")
        for _, r in e.iterrows():
            k = norm_name(r.player); base = dict(date=date, player=r.player, market=r.market.replace("player_", ""), line=r.line, side=r.side,
                                                 dk_price=r.dk_price, fair_scan=r.fair_sharp if r.side == "over" else r.fair_sharp, ev_scan=r.ev_sharp)
            if k not in a.index: rows.append(dict(base, status="DNP/void")); continue
            v = a.loc[k, COL[r.market]]; v = float(v.iloc[0] if isinstance(v, pd.Series) else v)
            win = (v > r.line) if r.side == "over" else (v < r.line)
            cf = close_fair(date, r.player, r.market, r.line, r.start)
            clv = None
            if cf:
                p_side = cf[1] if r.side == "over" else 1 - cf[1]
                clv = round(100 * (p_side * dec(r.dk_price) - 1), 1)
            rows.append(dict(base, actual=v, win=float(win), profit=round(dec(r.dk_price) - 1 if win else -1.0, 3),
                             clv=clv, close_snap=cf[0] if cf else None, status="graded"))
    # alt-ladder rungs (over X+): DK pays >= 3 prob-pts more than the other books' median and fitted EV >= 3%
    AC = {"PTS": "PTS", "REB": "REB", "AST": "AST", "FG3M": "FG3M"}
    for f in sorted(glob.glob("data/edges/20??-??-??_alts.csv")):
        date = os.path.basename(f)[:10]
        if date > last: continue
        e = pd.read_csv(f)
        if not {"dk_imp", "others_imp", "ev"}.issubset(e.columns): continue
        e = e[(e.others_imp - e.dk_imp >= 0.03) & (e.ev >= 3) & (e.n_oth >= 3)]
        a = acts[acts.date == date].set_index("key")
        for _, r in e.iterrows():
            k = norm_name(r.player); base = dict(date=date, player=r.player, market="alt_" + str(r.market).lower(), line=r.line, side="over",
                                                 dk_price=r.dk, ev_scan=r.ev)
            if k not in a.index or r.market not in AC: rows.append(dict(base, status="DNP/void")); continue
            v = a.loc[k, AC[r.market]]; v = float(v.iloc[0] if isinstance(v, pd.Series) else v); win = v > r.line
            rows.append(dict(base, actual=v, win=float(win), profit=round(dec(r.dk) - 1 if win else -1.0, 3), clv=None, status="graded"))
    g = pd.DataFrame(rows)
    os.makedirs("data/shadow", exist_ok=True); g.to_csv("data/shadow/edges_graded.csv", index=False)
    gg = g[g.status == "graded"] if len(g) else g
    L = ["---", "tags: [record, shadow, price-edge]", "---", "", "# Price-edge method: every qualifying leg, graded", "",
         "Written by `engine/edge_grade.py` (morning settlement). Qualifying = DK beats the sharp fair by >= 2% EV and the all-book consensus. "
         "Profit is per 1-unit single at the DK price. CLV uses the last sharp snapshot before tip (a true close only when one was taken).", ""]
    if gg.empty:
        L.append("No graded legs yet.")
    else:
        c = gg[gg.clv.notna()]
        L += [f"**{len(gg)} legs over {gg.date.nunique()} days: {int(gg.win.sum())}-{int(len(gg)-gg.win.sum())}, "
              f"ROI {100*gg.profit.mean():+.1f}% per unit (expected at scan {gg.ev_scan.mean():+.1f}%).** "
              f"CLV: {len(c)} legs with a later snapshot, mean {c.clv.mean():+.1f}%, positive on {100*(c.clv > 0).mean():.0f}%." if len(c) else
              f"**{len(gg)} legs: {int(gg.win.sum())}-{int(len(gg)-gg.win.sum())}, ROI {100*gg.profit.mean():+.1f}%.** No later snapshots for CLV.",
              "", f"One standard error on ROI at this sample is about ±{100*gg.profit.std()/np.sqrt(len(gg)):.0f}%: CLV is the faster signal.", "",
              "| market | n | record | ROI | mean CLV |", "|---|---:|---:|---:|---:|"]
        for m, x in gg.groupby("market"):
            L.append(f"| {m} | {len(x)} | {int(x.win.sum())}-{int(len(x)-x.win.sum())} | {100*x.profit.mean():+.1f}% | "
                     f"{x.clv.mean():+.1f}% |" if x.clv.notna().any() else f"| {m} | {len(x)} | {int(x.win.sum())}-{int(len(x)-x.win.sum())} | {100*x.profit.mean():+.1f}% | n/a |")
        L += ["", "| date | n | record | ROI | mean CLV |", "|---|---:|---:|---:|---:|"]
        for d_, x in gg.groupby("date"):
            L.append(f"| {d_} | {len(x)} | {int(x.win.sum())}-{int(len(x)-x.win.sum())} | {100*x.profit.mean():+.1f}% | "
                     + (f"{x.clv.mean():+.1f}% |" if x.clv.notna().any() else "n/a |"))
    os.makedirs("Record/Shadow", exist_ok=True)
    open("Record/Shadow/Price Edge Report.md", "w").write("\n".join(L) + "\n")
    print("\n".join(L[8:]))

if __name__ == "__main__":
    main()
