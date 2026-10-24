"""Cloud results puller (runs in GitHub Actions; laptop not needed).
    python engine/cloud/results.py [YYYY-MM-DD]      (default: yesterday, US/Eastern)
NBA: ESPN public JSON (stats.nba.com / cdn.nba.com block cloud IPs). MLB: statsapi.mlb.com (official).
Writes data/results/<sport>/<date>.csv (one row per player-game) and appends status/actions.json."""
import os, sys, json, time, datetime as dt, urllib.request
from zoneinfo import ZoneInfo
import pandas as pd

UA = {"User-Agent": "Mozilla/5.0 (prop-lab results bot)"}
def get(url, tries=4):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                return json.load(r)
        except Exception as e:
            print(f"  retry {i+1} {url}: {e}"); time.sleep(3 * (i + 1))
    raise RuntimeError(f"failed: {url}")

def num(x):
    try: return float(str(x).split("-")[0]) if x not in ("", "--", None) else None
    except ValueError: return None

def nba(date):
    ymd = date.replace("-", "")
    sb = get(f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?dates={ymd}")
    rows = []
    for ev in sb.get("events", []):
        comp = ev["competitions"][0]
        if not comp["status"]["type"].get("completed"): print("  not final:", ev["shortName"]); continue
        teams = {c["homeAway"]: c["team"]["abbreviation"] for c in comp["competitors"]}
        game = f'{teams["away"]}@{teams["home"]}'
        s = get(f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/summary?event={ev['id']}")
        for tb in s["boxscore"].get("players", []):
            team = tb["team"]["abbreviation"]
            for st in tb["statistics"]:
                lab = [l.upper() for l in st.get("labels", [])]
                for a in st.get("athletes", []):
                    v = dict(zip(lab, a.get("stats", [])))
                    dnp = a.get("didNotPlay") or not a.get("stats")
                    fg3 = str(v.get("3PT", "0-0")).split("-")
                    r = dict(date=date, sport="NBA", game=game, espn_event=ev["id"], team=team, player=a["athlete"]["displayName"],
                             dnp=bool(dnp), starter=bool(a.get("starter")), min=num(v.get("MIN")), pts=num(v.get("PTS")),
                             reb=num(v.get("REB")), ast=num(v.get("AST")), stl=num(v.get("STL")), blk=num(v.get("BLK")),
                             tov=num(v.get("TO")), fg3m=num(fg3[0]) if len(fg3) == 2 else None, fg3a=num(fg3[1]) if len(fg3) == 2 else None,
                             oreb=num(v.get("OREB")), dreb=num(v.get("DREB")))
                    if not dnp:
                        r["pra"] = sum(r[k] or 0 for k in ("pts", "reb", "ast")); r["pr"] = (r["pts"] or 0) + (r["reb"] or 0)
                        r["pa"] = (r["pts"] or 0) + (r["ast"] or 0); r["ra"] = (r["reb"] or 0) + (r["ast"] or 0)
                    rows.append(r)
        time.sleep(0.5)
    return pd.DataFrame(rows)

def mlb(date):
    sch = get(f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={date}")
    rows = []
    for d in sch.get("dates", []):
        for g in d["games"]:
            if g["status"]["abstractGameState"] != "Final": print("  not final:", g["gamePk"]); continue
            box = get(f"https://statsapi.mlb.com/api/v1/game/{g['gamePk']}/boxscore")
            away, home = box["teams"]["away"]["team"]["abbreviation"], box["teams"]["home"]["team"]["abbreviation"]
            for side in ("away", "home"):
                t = box["teams"][side]
                for p in t["players"].values():
                    b, pi = p.get("stats", {}).get("batting", {}), p.get("stats", {}).get("pitching", {})
                    if not b and not pi: continue
                    r = dict(date=date, sport="MLB", game=f"{away}@{home}", game_pk=g["gamePk"], team=t["team"]["abbreviation"],
                             player=p["person"]["fullName"])
                    if b:
                        h, d2, t3, hr = b.get("hits", 0), b.get("doubles", 0), b.get("triples", 0), b.get("homeRuns", 0)
                        r.update(pa=b.get("plateAppearances"), ab=b.get("atBats"), hits=h, runs=b.get("runs"), rbi=b.get("rbi"),
                                 hr=hr, tb=h + d2 + 2 * t3 + 3 * hr, bb=b.get("baseOnBalls"), so_bat=b.get("strikeOuts"),
                                 hrr=h + (b.get("runs") or 0) + (b.get("rbi") or 0))
                    if pi:
                        r.update(k=pi.get("strikeOuts"), outs=pi.get("outs"), bf=pi.get("battersFaced"), pitches=pi.get("numberOfPitches"),
                                 er=pi.get("earnedRuns"), hits_allowed=pi.get("hits"), bb_allowed=pi.get("baseOnBalls"))
                    rows.append(r)
    return pd.DataFrame(rows)

def heartbeat(job, info):
    os.makedirs("status", exist_ok=True); p = "status/actions.json"
    s = json.load(open(p)) if os.path.exists(p) else {}
    s[job] = dict(last_ok=dt.datetime.now(ZoneInfo("America/New_York")).isoformat(timespec="seconds"), **info)
    json.dump(s, open(p, "w"), indent=1)

def main():
    date = sys.argv[1] if len(sys.argv) > 1 else (dt.datetime.now(ZoneInfo("America/New_York")).date() - dt.timedelta(days=1)).isoformat()
    info = {"date": date}
    for sport, fn in (("nba", nba), ("mlb", mlb)):
        try:
            df = fn(date)
        except Exception as e:
            print(f"{sport}: ERROR {e}"); info[sport] = f"error: {e}"[:200]; continue
        info[sport] = len(df)
        if df.empty: print(f"{sport}: no final games"); continue
        os.makedirs(f"data/results/{sport}", exist_ok=True)
        df.to_csv(f"data/results/{sport}/{date}.csv", index=False)
        print(f"{sport}: {df.game.nunique()} games, {len(df)} player rows -> data/results/{sport}/{date}.csv")
    heartbeat("results", info)
    if any(str(v).startswith("error") for v in info.values()): sys.exit(1)

if __name__ == "__main__": main()
