"""Grade GAME LINES (spreads, totals, moneylines) for college basketball, NFL and college football against final scores.
    python engine/game_grade.py   -> Record/Shadow/Game Lines Report.md + data/shadow/game_lines_graded.csv
Inputs: data/odds/<sport>/<date>/games_*.csv (bulk snapshots) and data/scores/<sport>/<date>.csv (Odds API scores).
Per game side: sharp fair (Pinnacle devig, else FanDuel) at the first and last snapshot, DraftKings price/point, result.
Tests the same ideas as props: are sharp prices calibrated, does DK-vs-sharp edge win, does the steam side win, unders vs overs,
favorites vs underdogs, and how a 30% profit boost would have done on each side."""
import os, glob
import numpy as np, pandas as pd

def imp(a): a = float(a); return 100 / (a + 100) if a > 0 else -a / (-a + 100)
def dec(a): a = float(a); return 1 + a / 100 if a > 0 else 1 + 100 / -a

def snaps(sp):
    out = []
    for f in sorted(glob.glob(f"data/odds/{sp}/*/games_*.csv")):
        try: g = pd.read_csv(f)
        except Exception: continue
        if g.empty or "event_id" not in g: continue
        out.append(g)
    return pd.concat(out) if out else pd.DataFrame()

def fair_side(g, book):
    """devigged prob per outcome for one book in one snapshot of one event/market"""
    b = g[g.book == book]
    if len(b) != 2: return {}
    p = [imp(x) for x in b.price]; s = sum(p)
    return {(n, pt): q / s for n, pt, q in zip(b.name, b.point.fillna(0), p)}

def grade(sp):
    s = snaps(sp)
    if s.empty: return pd.DataFrame()
    sc = pd.concat([pd.read_csv(f) for f in glob.glob(f"data/scores/{sp}/*.csv")]) if glob.glob(f"data/scores/{sp}/*.csv") else pd.DataFrame()
    if sc.empty: return pd.DataFrame()
    sc = sc.drop_duplicates("event_id").set_index("event_id")
    rows = []
    for (eid, mk), g in s.groupby(["event_id", "market"]):
        if eid not in sc.index: continue
        r = sc.loc[eid]; hs, as_ = float(r.home_score), float(r.away_score)
        g = g.sort_values("snap_et"); first, last = g.snap_et.min(), g.snap_et.max()
        def sharp(at):
            x = g[g.snap_et == at]
            return fair_side(x, "pinnacle") or fair_side(x, "fanduel")
        f0, f1 = sharp(first), sharp(last)
        dk = g[(g.book == "draftkings") & (g.snap_et == g[g.book == "draftkings"].snap_et.max())] if (g.book == "draftkings").any() else pd.DataFrame()
        for _, o in dk.iterrows():
            pt = 0 if pd.isna(o.point) else float(o.point)
            team = o["name"]
            if mk == "h2h":
                win = (hs > as_) if team == r.home else (as_ > hs)
            elif mk == "spreads":
                margin = (hs - as_) if team == r.home else (as_ - hs)
                if margin + pt == 0: continue   # push
                win = margin + pt > 0
            else:
                tot = hs + as_
                if tot == pt: continue
                win = tot > pt if team == "Over" else tot < pt
            # sharp prob for this side: same name; point may differ by a half point (noted)
            def pick(f):
                c = [(k, v) for k, v in f.items() if k[0] == team]
                return (c[0][1], c[0][0][1]) if c else (np.nan, np.nan)
            p0, _ = pick(f0); p1, spt = pick(f1)
            rows.append(dict(sport=sp, event_id=eid, game=f"{r.away}@{r.home}", date=r.date, market=mk, side=team, point=pt, sharp_point=spt,
                             dk=o.price, p_first=p0, p_last=p1, win=float(win), roi=dec(o.price) - 1 if win else -1.0,
                             roi_boost30=(dec(o.price) - 1) * 1.3 if win else -1.0))
    return pd.DataFrame(rows)

def section(x, name):
    if x.empty: return [f"## {name}", "No graded games yet.", ""]
    x = x.copy(); x["same_pt"] = (x.point == x.sharp_point) | (x.market == "h2h")
    y = x[x.same_pt & x.p_last.notna()]
    L = [f"## {name}", f"{x.event_id.nunique()} games, {len(x)} DK sides graded ({len(y)} with the sharp book at the same number).", "",
         "| slice | n | win | sharp fair | ROI flat | ROI with 30% boost |", "|---|---:|---:|---:|---:|---:|"]
    def row(lbl, z):
        if len(z): L.append(f"| {lbl} | {len(z)} | {100*z.win.mean():.1f}% | {100*z.p_last.mean():.1f}% | {100*z.roi.mean():+.1f}% | {100*z.roi_boost30.mean():+.1f}% |")
    for m in ["spreads", "totals", "h2h"]: row(m, y[y.market == m])
    row("unders", y[y.side == "Under"]); row("overs", y[y.side == "Over"])
    row("favorites (fair >= 55%)", y[y.p_last >= .55]); row("underdogs (fair < 45%)", y[y.p_last < .45])
    y = y.assign(ev=y.p_last * y.dk.map(dec) - 1, move=y.p_last - y.p_first)
    row("DK beats sharp (EV >= 2%)", y[y.ev >= .02]); row("steam side (sharp moved >= 2 pts toward)", y[y.move >= .02])
    row("steam + DK lagging", y[(y.move >= .02) & (y.ev >= 0)])
    return L + [""]

def main():
    parts, L = [], ["---", "tags: [record, shadow, game-lines]", "---", "", "# Game lines (college basketball, NFL, college football), graded", "",
                    "Written by `engine/game_grade.py`. Sharp fair = Pinnacle devig (FanDuel if missing) at the last snapshot. "
                    "ROI is per 1-unit DK bet; the boost column shows the same bets with a 30% profit boost.", ""]
    for sp, name in [("ncaab", "College basketball"), ("nfl", "NFL"), ("ncaaf", "College football")]:
        g = grade(sp); parts.append(g); L += section(g, name)
    allg = pd.concat([p for p in parts if len(p)]) if any(len(p) for p in parts) else pd.DataFrame()
    os.makedirs("data/shadow", exist_ok=True); os.makedirs("Record/Shadow", exist_ok=True)
    if len(allg): allg.to_csv("data/shadow/game_lines_graded.csv", index=False)
    open("Record/Shadow/Game Lines Report.md", "w").write("\n".join(L) + "\n"); print("\n".join(L[6:20]))

if __name__ == "__main__":
    main()
