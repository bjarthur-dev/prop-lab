"""Fill actual/hit in Record/mechanism_tracker.csv from data/results (official box scores pulled by results.py).
    python engine/cloud/autosettle.py [YYYY-MM-DD]
Only fills empty rows; never overwrites. Marks source in notes ('auto: ESPN box' / 'auto: MLB statsapi').
Claude's morning audit cross-checks these against the Scout's Job A (Rules: two sources). DNP -> hit left blank, notes 'DNP'."""
import os, sys, glob, re, unicodedata, datetime as dt
from zoneinfo import ZoneInfo
import pandas as pd
MK = {"pts": "pts", "reb": "reb", "ast": "ast", "fg3m": "fg3m", "3pm": "fg3m", "pra": "pra", "pr": "pr", "pa": "pa", "ra": "ra",
      "stl": "stl", "blk": "blk", "pitcher_strikeouts": "k", "k": "k", "outs": "outs", "hits": "hits", "tb": "tb", "hrr": "hrr"}
def norm(n): return re.sub(r"[^a-z]", "", unicodedata.normalize("NFKD", str(n)).encode("ascii", "ignore").decode().lower().replace(" jr", "").replace(" iii", "").replace(" ii", ""))

def main():
    date = sys.argv[1] if len(sys.argv) > 1 else (dt.datetime.now(ZoneInfo("America/New_York")).date() - dt.timedelta(days=1)).isoformat()
    p = "Record/mechanism_tracker.csv"; t = pd.read_csv(p, dtype=str)
    res = {s: pd.read_csv(f) for s in ("nba", "mlb") for f in glob.glob(f"data/results/{s}/{date}.csv")}
    if not res: print("no results files for", date); return
    filled = 0
    for i, r in t[(t.date == date) & (t.actual.isna() | (t.actual == ""))].iterrows():
        sp = r.sport.lower(); col = MK.get(str(r.market).lower())
        if sp not in res or not col: continue
        d = res[sp]; m = d[d.player.map(norm) == norm(r.player)]
        if m.empty: t.at[i, "notes"] = f"{r.notes if isinstance(r.notes, str) else ''} | auto: no box match".strip(" |"); continue
        m = m.iloc[0]
        if bool(m.get("dnp", False)) or pd.isna(m.get(col)):
            t.at[i, "notes"] = f"{r.notes if isinstance(r.notes, str) else ''} | auto: DNP".strip(" |"); continue
        a = float(m[col]); line = float(r.line)
        t.at[i, "actual"] = f"{a:g}"
        t.at[i, "hit"] = "" if a == line else str(int((a > line) == (str(r.side).lower() == "over")))
        src = "ESPN box" if sp == "nba" else "MLB statsapi"
        t.at[i, "notes"] = f"{r.notes if isinstance(r.notes, str) else ''} | auto: {src}".strip(" |"); filled += 1
    t.to_csv(p, index=False); print(f"::notice::autosettle {date}: filled {filled} tracker rows")

if __name__ == "__main__": main()
