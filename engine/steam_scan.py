"""Steam scan: which side did the sharp books (Pinnacle/FanDuel devig) move toward between the day's first and latest snapshot,
and is DraftKings still pricing the old number?
    python engine/steam_scan.py [YYYY-MM-DD] [sport]   -> data/edges/<date>_steam.csv + printed list
Evidence (2026-10-24..11-01, 743 NBA props with a >= 1-pt move, Lessons.md): the side the sharp line moved toward won 55.6%,
above even its latest fair (~51.5%). Moves >= 6 pts: 61.5% (n=39). Pre-tip moves are information (injuries, minutes, lineup news)."""
import sys, os, glob, datetime as dt
import numpy as np, pandas as pd
def imp(a): a = float(a); return 100 / (a + 100) if a > 0 else -a / (-a + 100)
def dec(a): a = float(a); return 1 + a / 100 if a > 0 else 1 + 100 / -a
MK = {"nba": ["player_points", "player_rebounds", "player_assists", "player_threes"],
      "nfl": ["player_receptions", "player_reception_yds", "player_rush_yds", "player_pass_yds"]}

def scan(date, sport):
    rows = []
    for f in sorted(glob.glob(f"data/odds/{sport}/{date}/*.csv")):
        b = os.path.basename(f)
        if b.startswith("games") or "alt" in b: continue
        o = pd.read_csv(f)
        if o.empty or "snap_et" not in o: continue
        o = o[o.market.isin(MK[sport]) & o.over.notna() & o.under.notna()].copy()
        o["t"] = o.snap_et.astype(str).str[11:16]; rows.append(o)
    if not rows: return pd.DataFrame()
    o = pd.concat(rows); o["pov"] = [imp(a) / (imp(a) + imp(b)) for a, b in zip(o.over, o.under)]
    sh = o[o.book.isin(["pinnacle", "fanduel"])].groupby(["player", "market", "line", "t"]).pov.mean().reset_index().sort_values("t")
    m = sh.groupby(["player", "market", "line"]).agg(first=("pov", "first"), last=("pov", "last"), t0=("t", "first"), t1=("t", "last")).reset_index()
    m = m[m.t0 != m.t1]; m["move"] = m["last"] - m["first"]
    dk = o[o.book == "draftkings"].sort_values("t").drop_duplicates(["player", "market", "line"], keep="last").set_index(["player", "market", "line"])
    out = []
    for _, r in m[m.move.abs() >= 0.02].iterrows():
        k = (r.player, r.market, r.line)
        if k not in dk.index: continue
        side = "over" if r.move > 0 else "under"; price = dk.loc[k, side]
        p = r["last"] if side == "over" else 1 - r["last"]
        out.append(dict(player=r.player, market=r.market.replace("player_", ""), line=r.line, side=side, move_pts=round(100 * abs(r.move), 1),
                        fair_last=round(p, 3), dk=price, ev_last=round(100 * (p * dec(price) - 1), 1),
                        ev_steam=round(100 * ((p + 0.03) * dec(price) - 1), 1), window=f"{r.t0}->{r.t1}"))
    return pd.DataFrame(out).sort_values(["ev_steam"], ascending=False) if out else pd.DataFrame()

def grade_all():
    """Grade every day's steam list (moves >= 2 pts) vs NBA box scores -> Record/Shadow/Steam Report.md"""
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "nba"))
    from common import norm_name
    a = pd.read_csv("engine/data/players_2026-27.csv"); a["key"] = a.PLAYER_NAME.map(norm_name); a["d"] = a.GAME_DATE.astype(str).str[:10]
    a = a.drop_duplicates(["key", "d"]).set_index(["key", "d"]); C = {"points": "PTS", "rebounds": "REB", "assists": "AST", "threes": "FG3M"}
    rows = []
    for d in sorted(os.listdir("data/odds/nba")):
        x = scan(d, "nba")
        if x.empty: continue
        x["date"] = d; x["act"] = [a.loc[(norm_name(p), d), C[m]] if (norm_name(p), d) in a.index else np.nan for p, m in zip(x.player, x.market)]
        rows.append(x.dropna(subset=["act"]))
    if not rows: return
    x = pd.concat(rows); x["win"] = np.where(x.side == "over", x.act > x.line, x.act < x.line).astype(float)
    x["roi"] = np.where(x.win == 1, x.dk.map(dec) - 1, -1.0); q = x[x.ev_last >= 0]
    L = ["---", "tags: [record, shadow, steam]", "---", "", "# Steam method (sharp move >= 2 pts), graded", "",
         f"**All steam legs: {len(x)}, win {100*x.win.mean():.1f}% vs last fair {100*x.fair_last.mean():.1f}%, ROI {100*x.roi.mean():+.1f}% as DK singles.**",
         f"**DK lagging (price >= new fair): {len(q)}, win {100*q.win.mean():.1f}%, ROI {100*q.roi.mean():+.1f}%.**", "",
         "| date | n | win | ROI | lagging n | lagging win |", "|---|---:|---:|---:|---:|---:|"]
    for d, g in x.groupby("date"):
        gq = g[g.ev_last >= 0]
        L.append(f"| {d} | {len(g)} | {100*g.win.mean():.0f}% | {100*g.roi.mean():+.0f}% | {len(gq)} | {100*gq.win.mean() if len(gq) else 0:.0f}% |")
    os.makedirs("Record/Shadow", exist_ok=True); open("Record/Shadow/Steam Report.md", "w").write("\n".join(L) + "\n"); print("\n".join(L[6:8]))

if __name__ == "__main__" and "grade" in sys.argv:
    grade_all(); sys.exit()
if __name__ == "__main__":
    date = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1][:2] == "20" else dt.date.today().isoformat()
    sports = [a for a in sys.argv[1:] if a in MK] or ["nba", "nfl"]
    for sp in sports:
        d = scan(date, sp)
        if d.empty: print(f"{sp}: no 2-snapshot moves yet"); continue
        os.makedirs("data/edges", exist_ok=True); d.to_csv(f"data/edges/{date}_steam_{sp}.csv", index=False)
        print(f"== {sp.upper()} {date}: sharp moves >= 2 pts (ev_steam adds the +3 pt steam premium seen in the data)")
        print(d.head(25).to_string(index=False))
