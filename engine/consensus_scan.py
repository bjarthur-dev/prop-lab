"""The only pick-based edge the backtest supports: one book priced 6%+ away from every other book at the SAME line.
    python engine/consensus_scan.py [YYYY-MM-DD] [sport ...] [--book draftkings] [--min 0.06]
Backtest (Record/Market Backtest.md): claimed edges under 4% lost money; 6%+ hit 63% of 48. Rare: about 3 a day
across all books. Prints nothing when there is nothing, and that is the normal result."""
import sys, datetime as dt
from zoneinfo import ZoneInfo
import numpy as np, pandas as pd
sys.path.insert(0, "engine"); import fair

def scan(date, sport, book="draftkings", mn=0.06):
    try: o = fair.load(sport, date)
    except SystemExit: return pd.DataFrame()
    now = pd.Timestamp.now(tz="UTC")
    o = o[o.over.notna() & o.under.notna() & (o.book != "pick6") & (pd.to_datetime(o.start_et, utc=True) > now)].copy()
    if o.empty: return o
    io, iu = o.over.map(fair.imp), o.under.map(fair.imp); o["f"] = io / (io + iu); o["w"] = o.book.map(fair.W).fillna(1.0)
    rows = []
    for (pl, mk, ln), g in o.groupby(["player", "market", "line"]):
        me = g[g.book == book]; ot = g[g.book != book]
        if me.empty or len(ot) < 3: continue
        cons = float(np.average(ot.f, weights=ot.w)); r = me.iloc[0]
        for side, p, price in (("over", cons - fair.OVER_HAIRCUT, r.over), ("under", 1 - cons, r.under)):
            d = 1 + (price / 100 if price > 0 else 100 / -price); ev = p * d - 1
            if ev >= mn: rows.append(dict(sport=sport, game=r.game, start=r.start_et[11:16], player=pl, market=mk.replace("player_", ""), side=side, line=ln,
                                          price=int(price), fair_pct=round(p * 100, 1), ev_pct=round(ev * 100, 1), other_books=len(ot),
                                          spread_pct=round((ot.f.max() - ot.f.min()) * 100, 1), snap=r.snap_et[11:16]))
    return pd.DataFrame(rows)

if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    book = sys.argv[sys.argv.index("--book") + 1] if "--book" in sys.argv else "draftkings"
    mn = float(sys.argv[sys.argv.index("--min") + 1]) if "--min" in sys.argv else 0.06
    date = a[0] if a else dt.datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d")
    r = pd.concat([scan(date, s, book, mn) for s in (a[1:] or ["nba", "nfl", "nhl"])], ignore_index=True)
    if r.empty: print(f"{date}: no {book} line is {mn*100:.0f}%+ off the other books. Nothing to bet on price alone.")
    else: print(r.sort_values("ev_pct", ascending=False).to_string(index=False))
