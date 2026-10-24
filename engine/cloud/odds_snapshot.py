"""Prop-odds snapshots from The Odds API (the-odds-api.com; NOT theoddsapi.com). Runs in GitHub Actions.
    python engine/cloud/odds_snapshot.py open|board        -> all of today's events per sport
    python engine/cloud/odds_snapshot.py close             -> only events starting in the next 5-20 min (T-10 close)
Needs env ODDS_API_KEY (GitHub secret). Writes data/odds/<sport>/<date>/<tag>_<HHMM>.csv with one row per
book x player x market x line: over and under American prices + the API's last_update. Logs credits left to status/actions.json.
Cost: 1 credit per market per event per call (10 bookmakers = 1 region). NBA 8 games x 4 markets = 32 credits a snapshot."""
import os, sys, json, time, datetime as dt, urllib.request, urllib.parse
from zoneinfo import ZoneInfo
import pandas as pd
ET = ZoneInfo("America/New_York")
KEYS = [k for k in (os.environ.get("ODDS_API_KEY_1", ""), os.environ.get("ODDS_API_KEY_2", ""), os.environ.get("ODDS_API_KEY", "")) if k]
KEY = KEYS[0] if KEYS else ""   # key 1 first; switch to the next key only when one is out of credits (401/429)
BOOKS = "fanduel,draftkings,betmgm,williamhill_us,espnbet,fanatics,betrivers,pinnacle,betonlineag,bovada"
TIER = os.environ.get("ODDS_TIER", "free")   # free = 500 credits/month: NBA board (pts/reb/ast) + closes only for games with logged bets
SPORTS_FREE = {"nba": ("basketball_nba", "player_points,player_rebounds,player_assists"),
               "nfl": ("americanfootball_nfl", "player_reception_yds,player_rush_yds")}
SPORTS = {
    "nba": ("basketball_nba", "player_points,player_rebounds,player_assists,player_threes"),
    "nfl": ("americanfootball_nfl", "player_receptions,player_reception_yds,player_rush_yds,player_rush_attempts,player_anytime_td"),
    "mlb": ("baseball_mlb", "pitcher_strikeouts,pitcher_outs,batter_hits,batter_total_bases"),
}
left = {"remaining": None, "used": None}

def get(path, **q):
    global KEY
    q["apiKey"] = KEY
    url = f"https://api.the-odds-api.com/v4/{path}?{urllib.parse.urlencode(q)}"
    for i in range(3):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                left["remaining"] = r.headers.get("x-requests-remaining"); left["used"] = r.headers.get("x-requests-used")
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (401, 429) and KEY in KEYS and KEYS.index(KEY) + 1 < len(KEYS):
                KEY = KEYS[KEYS.index(KEY) + 1]; q["apiKey"] = KEY
                url = f"https://api.the-odds-api.com/v4/{path}?{urllib.parse.urlencode(q)}"
                print(f"::warning::key out of credits ({e.code}); switching to next key"); continue
            if e.code in (401, 422, 429): print(f"::error::odds api {e.code} on {path}"); return None
            time.sleep(3 * (i + 1))
        except Exception as e:
            print(f"::warning::retry {path}: {e}"); time.sleep(3 * (i + 1))
    return None

def main():
    global KEY
    tag = sys.argv[1] if len(sys.argv) > 1 else "board"
    if not KEY: print("::notice::ODDS_API_KEY not set; skipping odds snapshot"); return
    if tag == "check":   # 0-credit health check: sports + events lists only
        for i, k in enumerate(KEYS, 1):
            KEY = k
            sp = get("sports"); ev = get("sports/basketball_nba/events") or []
            print(f"::notice::key {i}: ok={sp is not None}, NBA events listed={len(ev)}, credits remaining={left['remaining']}, used={left['used']}")
        return
    now = dt.datetime.now(ET); today = now.date().isoformat(); info = {"tag": tag, "tier": TIER}
    sports = SPORTS if TIER == "paid" else SPORTS_FREE
    if TIER != "paid" and tag == "open": print("::notice::free tier: no open snapshot"); return
    if TIER != "paid" and tag == "board" and now.weekday() != 6: sports = {"nba": sports["nba"]}   # NFL board only on Sundays
    bet_games = set()
    if TIER != "paid" and tag == "close":
        try:
            b = pd.read_csv("Record/bets.csv"); bet_games = set(b[b["date"] == today]["notes"].astype(str))
        except Exception: pass
        if not bet_games: return
    for sp, (key, markets) in sports.items():
        evs = get(f"sports/{key}/events") or []
        sel = []
        for e in evs:
            t = dt.datetime.fromisoformat(e["commence_time"].replace("Z", "+00:00")).astimezone(ET)
            if t.date().isoformat() != today: continue
            mins = (t - now).total_seconds() / 60
            if tag == "close" and not (5 <= mins <= 20): continue
            if tag != "close" and mins < 0: continue
            sel.append((e, t))
        rows = []
        for e, t in sel:
            if tag == "close" and os.path.exists(f"data/odds/{sp}/{today}/close_{e['id']}.done"): continue
            if tag == "close" and TIER != "paid" and not any(e["home_team"].split()[-1] in g or e["away_team"].split()[-1] in g for g in bet_games): continue
            o = get(f"sports/{key}/events/{e['id']}/odds", bookmakers=BOOKS, markets=markets, oddsFormat="american")
            if not o: continue
            game = f"{e['away_team']}@{e['home_team']}"
            for b in o.get("bookmakers", []):
                for m in b.get("markets", []):
                    side = {}
                    for oc in m.get("outcomes", []):
                        k = (oc.get("description"), oc.get("point"))
                        side.setdefault(k, {})[oc["name"].lower()] = oc.get("price")
                    for (player, line), pr in side.items():
                        rows.append(dict(snap_et=now.isoformat(timespec="seconds"), tag=tag, sport=sp.upper(), event_id=e["id"], game=game,
                                         start_et=t.isoformat(timespec="minutes"), book=b["key"], market=m["key"], player=player, line=line,
                                         over=pr.get("over", pr.get("yes")), under=pr.get("under", pr.get("no")), last_update=m.get("last_update")))
            if tag == "close":
                os.makedirs(f"data/odds/{sp}/{today}", exist_ok=True); open(f"data/odds/{sp}/{today}/close_{e['id']}.done", "w").write(now.isoformat())
        info[sp] = len(rows)
        if rows:
            os.makedirs(f"data/odds/{sp}/{today}", exist_ok=True)
            pd.DataFrame(rows).to_csv(f"data/odds/{sp}/{today}/{tag}_{now:%H%M}.csv", index=False)
            print(f"::notice::{sp} {tag}: {len(sel)} events, {len(rows)} rows")
    if tag == "close" and not any(isinstance(v, int) and v > 0 for v in info.values()): return   # nothing starting: no commit
    info["credits_remaining"] = left["remaining"]
    os.makedirs("status", exist_ok=True); p = "status/actions.json"
    s = json.load(open(p)) if os.path.exists(p) else {}
    s[f"odds_{tag}"] = dict(last_ok=now.isoformat(timespec="seconds"), **info); json.dump(s, open(p, "w"), indent=1)
    if left["remaining"] and int(float(left["remaining"])) < 1500: print(f"::warning::Odds API credits low: {left['remaining']}")

if __name__ == "__main__": main()
