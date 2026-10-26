"""Cloud NBA box scores from API-NBA (api-sports.io, free plan: 100 requests/day). Replaces the laptop nba_api refresh.
    python engine/cloud/nba_box.py [YYYY-MM-DD]     (default: yesterday ET)
Needs env NBA_API_KEY (GitHub secret). ~1 + (games) requests per day. Writes data/box/nba/DATE.csv and appends to
engine/data/players_2026-27.csv via engine/nba/append_box.py (which rejects any game whose player points != final score).
When the laptop runs fetch.py (official nba_api), that file replaces everything, so the two sources never double-count."""
import os, sys, json, time, datetime as dt, urllib.request, urllib.parse, subprocess
from zoneinfo import ZoneInfo
import pandas as pd
ET = ZoneInfo("America/New_York"); KEYS = [k for k in (os.environ.get("SPORTS_API_KEY_1", ""), os.environ.get("SPORTS_API_KEY_2", ""), os.environ.get("NBA_API_KEY", "")) if k]
KEY = KEYS[0] if KEYS else ""; BASE = "https://v2.nba.api-sports.io"

def get(path, **q):
    global KEY
    url = f"{BASE}/{path}?{urllib.parse.urlencode(q)}"
    for i in range(4):
        try:
            req = urllib.request.Request(url, headers={"x-apisports-key": KEY})
            with urllib.request.urlopen(req, timeout=30) as r:
                left = r.headers.get("x-ratelimit-requests-remaining")
                d = json.load(r)
                errs = d.get("errors")
                if errs:
                    print(f"::warning::api errors {errs} (requests left today: {left})")
                    if any(w in str(errs).lower() for w in ("requests", "limit", "suspend", "access", "token")) and KEY in KEYS and KEYS.index(KEY) + 1 < len(KEYS):
                        KEY = KEYS[KEYS.index(KEY) + 1]; print("::warning::switching to the next sports API key"); continue
                return d.get("response", [])
        except Exception as e:
            print(f"::warning::retry {path}: {e}"); time.sleep(4 * (i + 1))
    return []

def mins(v):
    if v in (None, "", "-"): return 0.0
    s = str(v)
    if ":" in s: m, sec = s.split(":")[:2]; return round(int(m) + int(sec) / 60, 2)
    try: return float(s)
    except ValueError: return 0.0

def main():
    if not KEY: print("::notice::SPORTS_API_KEY_1 not set; skipping cloud NBA box scores"); return
    args = [a for a in sys.argv[1:] if not a.startswith("--")]; check = "--check" in sys.argv
    date = args[0] if args else (dt.datetime.now(ET).date() - dt.timedelta(days=1)).isoformat()
    logs = pd.read_csv("engine/data/players_2026-27.csv")
    if not check and (logs["GAME_DATE"].astype(str).str[:10] == date).any():
        print(f"::notice::{date} already in NBA logs; nothing to do"); return
    d0 = dt.date.fromisoformat(date)
    games = get("games", date=date) + get("games", date=(d0 + dt.timedelta(days=1)).isoformat())   # API dates are UTC
    rows, seen = [], set()
    for g in games:
        if g["id"] in seen: continue
        seen.add(g["id"])
        start = dt.datetime.fromisoformat(g["date"]["start"].replace("Z", "+00:00")).astimezone(ET)
        if start.date().isoformat() != date or str(g.get("status", {}).get("long", "")).lower() != "finished": continue
        if g.get("league") not in (None, "standard"): continue
        home, away = g["teams"]["home"]["code"], g["teams"]["visitors"]["code"]
        final = {home: g["scores"]["home"]["points"], away: g["scores"]["visitors"]["points"]}
        for p in get("players/statistics", game=g["id"]):
            t = p["team"]["code"]
            rows.append(dict(date=date, game=f"{away}@{home}", team=t, player=f"{p['player']['firstname']} {p['player']['lastname']}".strip(),
                             min=mins(p.get("min")), pts=p.get("points") or 0, reb=p.get("totReb") or 0, ast=p.get("assists") or 0,
                             fg3m=p.get("tpm") or 0, fg3a=p.get("tpa") or 0, oreb=p.get("offReb") or 0, dreb=p.get("defReb") or 0,
                             stl=p.get("steals") or 0, blk=p.get("blocks") or 0, tov=p.get("turnovers") or 0,
                             team_final=final.get(t), source=f"api-sports game {g['id']}"))
        time.sleep(6.5)   # free plan: 10 requests/minute
    if not rows: print(f"::warning::no finished NBA games found for {date}"); return
    if check:   # compare against the official nba_api rows already in the logs; change nothing
        sys.path.insert(0, "engine/nba"); from common import norm_name
        b = pd.DataFrame(rows); b["key"] = b["player"].map(norm_name)
        o = logs[logs["GAME_DATE"].astype(str).str[:10] == date].copy(); o["key"] = o["PLAYER_NAME"].map(norm_name)
        m = b.merge(o, on="key", how="outer", indicator=True)
        both = m[m["_merge"] == "both"]
        diffs = sum(int((both[a] != both[b_]).sum()) for a, b_ in (("pts", "PTS"), ("reb", "REB"), ("ast", "AST"), ("fg3m", "FG3M")))
        teams_ok = sum(1 for _, g in b.groupby(["game", "team"]) if int(g["pts"].sum()) == int(g["team_final"].iloc[0]))
        print(f"::notice::CHECK {date}: api players {len(b)}, official {len(o)}, matched {len(both)}, unmatched api {int((m._merge=='left_only').sum())}, unmatched official {int((m._merge=='right_only').sum())}, stat mismatches (pts/reb/ast/3pm) {diffs}, team totals ok {teams_ok}/{b.groupby(['game','team']).ngroups}")
        for (gm, tm), g in b.groupby(["game", "team"]):
            s_, f_ = int(g["pts"].sum()), int(g["team_final"].iloc[0]); oo = o[o["TEAM_ABBREVIATION"] == tm]
            print(f"::notice::team {gm} {tm}: api players {len(g)} sum {s_} final {f_} | official players {len(oo)} sum {int(oo['PTS'].sum())}")
        bad = both[(both["pts"] != both["PTS"]) | (both["reb"] != both["REB"]) | (both["ast"] != both["AST"])]
        for _, r in bad.head(10).iterrows(): print(f"::warning::mismatch {r['player']}: api {r['pts']}/{r['reb']}/{r['ast']} vs official {r['PTS']}/{r['REB']}/{r['AST']}")
        for n in m[m._merge == "left_only"]["player"].head(8): print(f"::warning::api-only name: {n}")
        return
    os.makedirs("data/box/nba", exist_ok=True); path = f"data/box/nba/{date}.csv"
    pd.DataFrame(rows).to_csv(path, index=False)
    out = subprocess.run([sys.executable, "engine/nba/append_box.py", path], capture_output=True, text=True).stdout
    print("::notice::" + out.strip().replace("\n", " | "))

if __name__ == "__main__": main()
