"""Every betting idea, graded the same way against every NBA prop line we have, every morning.
    python engine/hypotheses.py        -> Record/Hypotheses.md
An idea is a rule that picks a side of a line. Each is graded on: hit rate vs the market's no-vig chance,
return at DraftKings' price, return at the best price on any book, and how many of the days it was ahead.
'Found' = dates up to FOUND_THROUGH (the data the idea was found on, so it flatters the idea).
'Forward' = dates after it: the only honest test. Trust an idea only when Forward has 150+ lines and still wins."""
import sys
import numpy as np, pandas as pd
sys.path.insert(0, "engine"); import market_backtest as mb
FOUND_THROUGH = "2026-11-08"

def build():
    m = mb.load(); m = m[m.book != "pick6"].copy()
    m["do"] = mb.dec(m.over); m["du"] = mb.dec(m.under); m["w"] = m.book.map({"pinnacle": 2.0, "fanduel": 1.5}).fillna(1.0)
    m["wf"] = m.w * m.fair_over
    key = ["date", "k", "market", "line"]
    c = m.groupby(key).agg(player=("player", "first"), nb=("book", "size"), sw=("w", "sum"), swf=("wf", "sum"), actual=("actual", "first"),
                           over_hit=("over_hit", "first"), best_o=("do", "max"), best_u=("du", "max"), fmin=("fair_over", "min"), fmax=("fair_over", "max")).reset_index()
    c["fair"] = c.swf / c.sw
    dk = m[m.book == "draftkings"][key + ["do", "du", "fair_over"]].rename(columns={"do": "dk_o", "du": "dk_u", "fair_over": "dk_fair"})
    c = c.merge(dk, on=key, how="left")
    # consensus of the non-DK books, for the off-market idea
    nd = m[m.book != "draftkings"].groupby(key).agg(osw=("w", "sum"), oswf=("wf", "sum"), onb=("book", "size")).reset_index()
    c = c.merge(nd, on=key, how="left"); c["others"] = c.oswf / c.osw
    c = c[c.nb >= 3].copy()
    # main line only (most books) so one player-market is one trial
    c = c.sort_values("nb").drop_duplicates(["date", "k", "market"], keep="last")
    return c

def ideas(c):
    T, P, R, A, PRA = (c.market == "player_threes"), (c.market == "player_points"), (c.market == "player_rebounds"), (c.market == "player_assists"), (c.market == "player_points_rebounds_assists")
    ev_o = (c.others - 0.015) * c.dk_o - 1; ev_u = (1 - c.others) * c.dk_u - 1
    return [
        ("Every over (baseline)", "over", c.fair > 0),
        ("Every under (baseline)", "under", c.fair > 0),
        ("Threes under, line 1.5 or less, under priced 55%+", "under", T & (c.line <= 1.5) & (c.fair <= .45)),
        ("Threes under, any line, under priced 55%+", "under", T & (c.fair <= .45)),
        ("Points under, line 10.5 or less", "under", P & (c.line <= 10.5)),
        ("Points+rebounds+assists under", "under", PRA),
        ("Rebounds over, over priced 55%+", "over", R & (c.fair >= .55)),
        ("Assists under, line 2.5-4.5", "under", A & (c.line >= 2.5) & (c.line <= 4.5)),
        ("Any under priced 58%+ (pick'em favourite)", "under", c.fair <= .42),
        ("Any over priced 58%+ (pick'em favourite)", "over", c.fair >= .58),
        ("DraftKings over 6%+ better than other books", "over", (ev_o >= .06) & (c.onb >= 3)),
        ("DraftKings under 6%+ better than other books", "under", (ev_u >= .06) & (c.onb >= 3)),
        ("DraftKings either side 3-6% better (expected to fail)", "best", (np.maximum(ev_o, ev_u) >= .03) & (np.maximum(ev_o, ev_u) < .06) & (c.onb >= 3)),
        ("Books disagree by 8+ points: take the under", "under", (c.fmax - c.fmin) >= .08),
    ], ev_o, ev_u

def grade(c, side, mask, ev_o, ev_u):
    d = c[mask].copy()
    if side == "best": s = np.where(ev_o[mask] >= ev_u[mask], "over", "under")
    else: s = np.full(len(d), side)
    over = s == "over"
    d["won"] = np.where(over, d.over_hit, 1 - d.over_hit); d["p"] = np.where(over, d.fair, 1 - d.fair)
    d["r_dk"] = d.won * np.where(over, d.dk_o, d.dk_u) - 1; d["r_best"] = d.won * np.where(over, d.best_o, d.best_u) - 1
    return d

def row(d):
    if d.empty: return ["0", "", "", "", "", "", ""]
    by = d.groupby("date").agg(e=("won", "mean"), p=("p", "mean")); diff = d.won.mean() - d.p.mean()
    days = by.e - by.p; se = days.std(ddof=1) / np.sqrt(len(days)) if len(days) > 2 else np.nan
    return [f"{len(d)}", f"{d.p.mean()*100:.1f}%", f"{d.won.mean()*100:.1f}%", f"{diff*100:+.1f}",
            f"{d.r_dk.mean()*100:+.1f}%" if d.r_dk.notna().any() else "", f"{d.r_best.mean()*100:+.1f}%", f"{(days>0).sum()}/{len(days)}" + (f" (±{se*100:.1f})" if se == se else "")]

def main():
    c = build(); L, ev_o, ev_u = ideas(c)
    hdr = "| Idea | Lines | Market chance | Hit | Gap (pts) | Return at DK | Return at best price | Days ahead (± daily error) |\n|---|---|---|---|---|---|---|---|\n"
    out = ["# Hypotheses: every idea, graded daily\n", f"Updated {pd.Timestamp.now(tz='America/New_York'):%Y-%m-%d %H:%M} ET by engine/hypotheses.py. {len(c):,} player-markets, {c.date.min()} to {c.date.max()}.\n",
           "How to read it: **Gap** is hit rate minus the market's chance. A gap smaller than about twice the daily error is noise. A straight bet needs a positive **Return**; a pick'em app at a flat payout needs the **Hit** column above its break-even (2-pick 3x: 57.7%, 3-pick 6x: 55%).\n"]
    for name, sel in (("Forward test (dates after %s): the honest one" % FOUND_THROUGH, c.date > FOUND_THROUGH), ("Found on (through %s): flatters the idea" % FOUND_THROUGH, c.date <= FOUND_THROUGH)):
        out.append(f"\n## {name}\n\n" + hdr + "\n".join("| " + " | ".join([n] + row(grade(c[sel], s, mk[sel], ev_o[sel], ev_u[sel]))) + " |" for n, s, mk in L) + "\n")
    txt = "\n".join(out); open("Record/Hypotheses.md", "w").write(txt); print(txt)

def today(date=None):
    """Lines on today's board that match the three lead ideas. Paper only until the forward test passes."""
    import datetime as dt; from zoneinfo import ZoneInfo; import fair
    date = date or dt.datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d")
    o = fair.load("nba", date); now = pd.Timestamp.now(tz="UTC")
    o = o[o.over.notna() & o.under.notna() & (o.book != "pick6") & (pd.to_datetime(o.start_et, utc=True) > now)].copy()
    if o.empty: print("no upcoming NBA lines"); return
    io, iu = o.over.map(fair.imp), o.under.map(fair.imp); o["f"] = io / (io + iu); o["w"] = o.book.map(fair.W).fillna(1.0)
    rows = []
    for (pl, mk, ln), g in o.groupby(["player", "market", "line"]):
        if len(g) < 3: continue
        f = float(np.average(g.f, weights=g.w)); dk = g[g.book == "draftkings"]
        idea = side = None
        if mk == "player_rebounds" and f >= .55: idea, side = "Rebounds over priced 55%+", "over"
        elif mk == "player_points" and ln <= 10.5: idea, side = "Points under, line 10.5 or less", "under"
        elif mk == "player_threes" and ln <= 1.5 and f <= .45: idea, side = "Threes under 1.5 or less priced 55%+", "under"
        if not idea: continue
        rows.append(dict(idea=idea, player=pl, side=side, line=ln, market_pct=round((f if side == "over" else 1 - f) * 100, 1), books=len(g),
                         dk_price=(int(dk.iloc[0][side]) if len(dk) else ""), game=g.game.iloc[0], start=g.start_et.iloc[0][11:16]))
    r = pd.DataFrame(rows)
    if r.empty: print("no matches"); return
    r = r.sort_values(["idea", "market_pct"], ascending=[True, False])
    open("Record/Ideas Today.md", "w").write(f"# Lines matching the lead ideas, {date}\n\nPaper only. These ideas were found in past data and are not proven; see [[Hypotheses]].\n\n" + r.to_markdown(index=False) + "\n")
    print(r.to_string(index=False))

if __name__ == "__main__":
    today(sys.argv[2] if len(sys.argv) > 2 else None) if len(sys.argv) > 1 and sys.argv[1] == "today" else main()
