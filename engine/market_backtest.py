"""Backtest the price-based strategy on every NBA prop we have snapshotted (not only the ones we bet).
    python engine/market_backtest.py            -> prints tables, writes Record/Market Backtest.md + data/market_bt.csv
Joins the last pre-game snapshot of each (date, player, market, book, line) to the official box score.
Answers: is each book's no-vig price calibrated, do overs or unders win, and does "book X is off the sharp
consensus by N%" actually pay."""
import glob, os, re, sys, unicodedata
import numpy as np, pandas as pd
STAT = {"player_points": "PTS", "player_rebounds": "REB", "player_assists": "AST", "player_threes": "FG3M",
        "player_points_rebounds_assists": "PRA", "player_points_rebounds": "PR", "player_points_assists": "PA",
        "player_rebounds_assists": "RA"}
def norm(n): return re.sub(r"[^a-z]", "", unicodedata.normalize("NFKD", str(n)).encode("ascii", "ignore").decode().lower().replace(" jr", "").replace(" iii", "").replace(" ii", "").replace(" sr", ""))
def imp(o): o = np.asarray(o, float); return np.where(o < 0, -o / (-o + 100), 100 / (o + 100))
def dec(o): o = np.asarray(o, float); return np.where(o < 0, 1 + 100 / -o, 1 + o / 100)

def load():
    fr = []
    for f in glob.glob("data/odds/nba/*/*.csv"):
        b = os.path.basename(f)
        if b.startswith("games") or "alt" in b or " " in b: continue
        try: d = pd.read_csv(f, low_memory=False)
        except Exception: continue
        if "player" not in d.columns: continue
        d["date"] = f.split("/")[-2]; fr.append(d)
    o = pd.concat(fr, ignore_index=True)
    o = o[o.market.isin(STAT) & o.over.notna() & o.under.notna()]
    o = o[pd.to_datetime(o.snap_et, utc=True) < pd.to_datetime(o.start_et, utc=True)]      # pre-game only
    o = o[pd.to_datetime(o.start_et, utc=True).dt.tz_convert("America/New_York").dt.strftime("%Y-%m-%d") == o.date]
    o = o.sort_values("snap_et").drop_duplicates(["date", "player", "market", "book", "line"], keep="last")
    # keep each book's latest line only
    last = o.groupby(["date", "player", "market", "book"]).snap_et.transform("max")
    o = o[o.snap_et == last].copy()
    box = pd.read_csv("engine/data/players_2026-27.csv", low_memory=False)
    box = box[pd.to_numeric(box.MIN, errors="coerce").fillna(0) > 0].copy()
    box["PRA"] = box.PTS + box.REB + box.AST; box["PR"] = box.PTS + box.REB; box["PA"] = box.PTS + box.AST; box["RA"] = box.REB + box.AST
    box["k"] = box.PLAYER_NAME.map(norm); o["k"] = o.player.map(norm)
    m = o.merge(box[["k", "GAME_DATE", "PTS", "REB", "AST", "FG3M", "PRA", "PR", "PA", "RA"]], left_on=["k", "date"], right_on=["k", "GAME_DATE"])
    m["actual"] = [r[STAT[mk]] for r, mk in zip(m.to_dict("records"), m.market)]
    m = m[m.actual != m.line].copy()
    m["over_hit"] = (m.actual > m.line).astype(int)
    io, iu = imp(m.over), imp(m.under); m["fair_over"] = io / (io + iu); m["hold"] = io + iu - 1
    return m

def table(df, by, name):
    g = df.groupby(by, observed=True).agg(n=("over_hit", "size"), fair_over=("fair_over", "mean"), over_hit=("over_hit", "mean"),
                                          roi_over=("ro", "mean"), roi_under=("ru", "mean")).round(3)
    return f"\n### {name}\n\n" + g.to_markdown() + "\n"

def main():
    m = load()
    m["ro"] = m.over_hit * dec(m.over) - 1; m["ru"] = (1 - m.over_hit) * dec(m.under) - 1
    out = [f"# Market backtest (NBA props)\n\n{len(m):,} book-lines, {m.date.nunique()} dates ({m.date.min()} to {m.date.max()}), {m.groupby(['date','k','market']).ngroups:,} player-markets.\n",
           "fair_over = the book's own no-vig over chance. roi = average return per $1 at that book's price.\n"]
    out.append(table(m, "book", "By book: is the no-vig price right, and which side pays"))
    out.append(table(m, "market", "By market"))
    m["fb"] = pd.cut(m.fair_over, [0, .35, .45, .5, .55, .65, 1])
    out.append(table(m, "fb", "By price bucket (calibration)"))
    # consensus of the OTHER books at the same line, then the edge of each book's price vs it
    sharp_w = {"pinnacle": 2.0, "fanduel": 1.5}
    m["w"] = m.book.map(sharp_w).fillna(1.0)
    m = m[m.book != "pick6"].copy() if False else m
    key = ["date", "k", "market", "line"]
    real = m[m.book != "pick6"]
    s = real.assign(wf=real.w * real.fair_over).groupby(key).agg(sw=("w", "sum"), swf=("wf", "sum"), nb=("book", "size")).reset_index()
    m = m.merge(s, on=key, how="left")
    own = np.where(m.book != "pick6", m.w, 0.0)
    m["cons"] = (m.swf - own * m.fair_over) / (m.sw - own).replace(0, np.nan)
    m["others"] = m.nb - (m.book != "pick6")
    e = m[(m.others >= 2) & m.cons.notna()].copy()
    e["ev_over"] = e.cons * dec(e.over) - 1; e["ev_under"] = (1 - e.cons) * dec(e.under) - 1
    e["side"] = np.where(e.ev_over >= e.ev_under, "over", "under")
    e["ev"] = np.maximum(e.ev_over, e.ev_under)
    e["ret"] = np.where(e.side == "over", e.ro, e.ru); e["won"] = np.where(e.side == "over", e.over_hit, 1 - e.over_hit)
    e["p"] = np.where(e.side == "over", e.cons, 1 - e.cons)
    e["evb"] = pd.cut(e.ev, [-1, 0, .02, .04, .06, .10, 5])
    def evt(d, by):
        return d.groupby(by, observed=True).agg(n=("ret", "size"), pred_p=("p", "mean"), hit=("won", "mean"), claimed_ev=("ev", "mean"), real_roi=("ret", "mean")).round(3).to_markdown()
    out.append("\n### Does 'this book is off the consensus' pay? (best side of every line, all books)\n\n" + evt(e, "evb") + "\n")
    for bk in ("draftkings", "fanduel", "betmgm", "espnbet"):
        d = e[e.book == bk]
        if len(d): out.append(f"\n### Same, {bk} only\n\n" + evt(d, "evb") + "\n")
    d = e[(e.book == "draftkings") & (e.ev >= .04)]
    if len(d):
        out.append("\n### DraftKings, claimed EV 4%+: by side and by market\n\n" + evt(d, "side") + "\n\n" + evt(d, "market") + "\n")
        d2 = d.assign(pb=pd.cut(d.p, [0, .4, .5, .6, 1]))
        out.append("\n" + evt(d2, "pb") + "\n")
    os.makedirs("data", exist_ok=True); e.to_csv("data/market_bt.csv", index=False)
    txt = "\n".join(out); open("Record/Market Backtest.md", "w").write(txt); print(txt)

if __name__ == "__main__": main()
