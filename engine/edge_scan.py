"""Price-edge scan: DraftKings prices that beat the sharp books' fair odds (no model needed).
    python engine/edge_scan.py YYYY-MM-DD [--min-ev 2.0]
Reads the newest data/odds/<sport>/DATE/board_*.csv (or close_*.csv). For each DK side with >= 2 other books at the same line:
fair = mean multiplicative devig of Pinnacle/FanDuel (sharp) and of all other books (consensus); EV = fair x DK decimal - 1.
A leg qualifies when EV vs sharp >= min_ev AND EV vs all-book consensus >= 0 (both views agree). Writes data/edges/DATE.csv
and prints the qualifying legs plus the best 2-leg slip from different games. Rules §3.8 (stale-price path) governs staking."""
import sys, glob, os, itertools
import numpy as np, pandas as pd

def imp(a): a = float(a); return 100 / (a + 100) if a > 0 else -a / (-a + 100)
def dec(a): a = float(a); return 1 + a / 100 if a > 0 else 1 + 100 / -a

def scan(date, min_ev=2.0):
    rows = []
    for sport_dir in glob.glob(f"data/odds/*/{date}"):
        files = sorted(glob.glob(f"{sport_dir}/board_*.csv"))
        if not files: continue
        b = pd.read_csv(files[-1]).dropna(subset=["over", "under"])
        for (pl, mk, ln), g in b.groupby(["player", "market", "line"]):
            dk = g[g.book == "draftkings"]; oth = g[g.book != "draftkings"]; sh = oth[oth.book.isin(["pinnacle", "fanduel"])]
            if dk.empty or len(oth) < 2 or sh.empty: continue
            f_sh = np.mean([imp(o) / (imp(o) + imp(u)) for o, u in zip(sh.over, sh.under)])
            f_all = np.mean([imp(o) / (imp(o) + imp(u)) for o, u in zip(oth.over, oth.under)])
            d = dk.iloc[0]
            for side, ps, pa, price in (("over", f_sh, f_all, d.over), ("under", 1 - f_sh, 1 - f_all, d.under)):
                rows.append(dict(sport=d.sport, game=d.game, start=d.start_et, player=pl, market=mk, line=ln, side=side, dk_price=int(price),
                                 fair_sharp=round(ps, 3), fair_all=round(pa, 3), ev_sharp=round(100 * (ps * dec(price) - 1), 1),
                                 ev_all=round(100 * (pa * dec(price) - 1), 1), n_books=len(oth), snap=d.snap_et))
    r = pd.DataFrame(rows)
    if r.empty: print("no boards for", date); return r
    q = r[(r.ev_sharp >= min_ev) & (r.ev_all >= 0)].sort_values("ev_sharp", ascending=False)
    os.makedirs("data/edges", exist_ok=True); r.to_csv(f"data/edges/{date}.csv", index=False)
    print(f"{len(r)} DK sides scanned; {len(q)} qualify (EV vs sharp >= {min_ev}% and vs all books >= 0)")
    print(q.head(15).to_string(index=False))
    best = None
    for a, b_ in itertools.combinations(q.to_dict("records"), 2):
        if a["game"] == b_["game"]: continue
        ev = 100 * (a["fair_sharp"] * b_["fair_sharp"] * dec(a["dk_price"]) * dec(b_["dk_price"]) - 1)
        if best is None or ev > best[0]: best = (ev, a, b_)
    if best: print(f"\nBest 2-leg slip (different games): {best[1]['player']} {best[1]['market']} {best[1]['side']} {best[1]['line']} ({best[1]['dk_price']}) + {best[2]['player']} {best[2]['market']} {best[2]['side']} {best[2]['line']} ({best[2]['dk_price']}) -> EV vs sharp {best[0]:+.1f}%")
    return q

if __name__ == "__main__":
    m = float(sys.argv[sys.argv.index("--min-ev") + 1]) if "--min-ev" in sys.argv else 2.0
    scan(sys.argv[1], m)
