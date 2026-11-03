"""Game-line edge scan (spreads, totals, moneylines) for any sport with bulk games files.
    python engine/game_scan.py [YYYY-MM-DD] [ncaab|nba|nfl|ncaaf]   -> data/edges/<date>_games_<sport>.csv
For each DraftKings side: sharp fair = Pinnacle devig at the SAME number (FanDuel if Pinnacle missing), consensus = mean devig of
all other books at the same number. Qualifies when EV vs sharp >= 2% AND EV vs consensus >= 0 (same rule as props)."""
import sys, glob, os, datetime as dt
import numpy as np, pandas as pd
def imp(a): a = float(a); return 100 / (a + 100) if a > 0 else -a / (-a + 100)
def dec(a): a = float(a); return 1 + a / 100 if a > 0 else 1 + 100 / -a

def scan(date, sp):
    fs = sorted(glob.glob(f"data/odds/{sp}/{date}/games_*.csv"))
    if not fs: return pd.DataFrame()
    g = pd.read_csv(fs[-1]); g["point"] = g.point.fillna(0)
    rows = []
    for (eid, mk), x in g.groupby(["event_id", "market"]):
        def dev(b):
            y = x[x.book == b]
            if len(y) != 2: return {}
            p = [imp(v) for v in y.price]; s = sum(p)
            return {(n, pt): q / s for n, pt, q in zip(y.name, y.point, p)}
        dk = x[x.book == "draftkings"]
        if dk.empty: continue
        sh = dev("pinnacle"); src = "pinnacle"
        if not sh: sh = dev("fanduel"); src = "fanduel"
        others = [dev(b) for b in x.book.unique() if b != "draftkings"]
        for _, o in dk.iterrows():
            k = (o["name"], o.point)
            if k not in sh: continue
            cons = [d[k] for d in others if k in d]
            p = sh[k]; pc = float(np.mean(cons)) if cons else np.nan
            rows.append(dict(game=f"{o.away} @ {o.home}", start=pd.Timestamp(o.start).tz_convert("America/New_York").strftime("%H:%M"),
                             market=mk, side=o["name"], point=o.point, dk=o.price, sharp=src, fair=round(p, 3), fair_cons=round(pc, 3),
                             n_books=len(cons), ev_sharp=round(100 * (p * dec(o.price) - 1), 1), ev_cons=round(100 * (pc * dec(o.price) - 1), 1)))
    return pd.DataFrame(rows)

if __name__ == "__main__":
    a = sys.argv[1:]
    date = next((x for x in a if x[:2] == "20"), dt.date.today().isoformat()); sp = next((x for x in a if not x[:2] == "20"), "ncaab")
    d = scan(date, sp)
    if d.empty: print("no games file"); sys.exit()
    d.to_csv(f"data/edges/{date}_games_{sp}.csv", index=False)
    q = d[(d.ev_sharp >= 2) & (d.ev_cons >= 0)].sort_values("ev_sharp", ascending=False)
    print(f"{sp} {date}: {d.game.nunique()} games, {len(d)} DK sides with a sharp price at the same number; {len(q)} qualify")
    print(q.to_string(index=False))
