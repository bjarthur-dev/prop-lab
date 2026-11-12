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
KEYS = list(dict.fromkeys(KEYS))   # dedupe (ODDS_API_KEY may equal key 1)
KEY = KEYS[0] if KEYS else ""   # key 1 first; switch to the next key only when one is out of credits (401/429)
BOOKS = "fanduel,draftkings,betmgm,williamhill_us,espnbet,fanatics,betrivers,pinnacle,betonlineag,pick6"   # pick6 = DraftKings Pick6 (us_dfs); 10 books = 1 region, so no extra credits
TIER = os.environ.get("ODDS_TIER", "free")   # free = 500 credits/month: NBA board (pts/reb/ast) + closes only for games with logged bets
SPORTS_FREE = {"nba": ("basketball_nba", "player_points,player_rebounds,player_assists,player_threes"),
               "nfl": ("americanfootball_nfl", "player_reception_yds,player_rush_yds"),
               "mlb": ("baseball_mlb", "pitcher_strikeouts,pitcher_outs")}   # 1 World Series game = 2 credits
SPORTS = {
    "nba": ("basketball_nba", "player_points,player_rebounds,player_assists,player_threes,player_points_rebounds_assists"),
    "nfl": ("americanfootball_nfl", "player_receptions,player_reception_yds,player_rush_yds,player_rush_attempts,player_anytime_td"),
    "mlb": ("baseball_mlb", "pitcher_strikeouts,pitcher_outs,batter_hits,batter_total_bases"),
}
left = {"remaining": None, "used": None}
EXTRAS_OK = [True]
LOW = [False]   # set False by the budget guard when credits are short; game-line extras are skipped then

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

GAME_SPORTS = {"ncaab": "basketball_ncaab", "nba": "basketball_nba", "nfl": "americanfootball_nfl", "ncaaf": "americanfootball_ncaaf",
               "nhl": "icehockey_nhl", "ucl": "soccer_uefa_champs_league"}

def bulk_lines(sp, now, today, tag):
    """one call = every game's spreads/totals/moneyline for a sport (3 credits); writes data/odds/<sp>/<date>/games_<tag>_HHMM.csv"""
    g = get(f"sports/{GAME_SPORTS[sp]}/odds", markets="spreads,totals,h2h", bookmakers=BOOKS.replace(",pick6", ""), oddsFormat="american") or []
    rows = [dict(snap_et=now.isoformat(timespec="seconds"), sport=sp.upper(), event_id=e["id"], home=e["home_team"], away=e["away_team"],
                 start=e["commence_time"], book=bk["key"], market=m["key"], name=oc["name"], point=oc.get("point"), price=oc.get("price"))
            for e in g for bk in e.get("bookmakers", []) for m in bk.get("markets", []) for oc in m.get("outcomes", [])]
    if rows:
        os.makedirs(f"data/odds/{sp}/{today}", exist_ok=True)
        pd.DataFrame(rows).to_csv(f"data/odds/{sp}/{today}/games_{tag}_{now:%H%M}.csv", index=False)
    print(f"::notice::{sp} game lines ({tag}): {len(g)} games, credits left {left['remaining']}")
    return len(g)

def scores(now):
    """final scores for the last 3 days (2 credits per sport) -> data/scores/<sp>/<date>.csv; used to grade game lines"""
    n = {}
    for sp, key in GAME_SPORTS.items():
        if sp in ("nba", "nhl", "ucl"): continue   # NBA from API-NBA; NHL/UCL scores only when we start betting them
        g = get(f"sports/{key}/scores", daysFrom=3) or []
        rows = []
        for e in g:
            if not e.get("completed") or not e.get("scores"): continue
            sc = {x["name"]: x["score"] for x in e["scores"]}
            d = dt.datetime.fromisoformat(e["commence_time"].replace("Z", "+00:00")).astimezone(ET).date().isoformat()
            rows.append(dict(date=d, event_id=e["id"], home=e["home_team"], away=e["away_team"], home_score=sc.get(e["home_team"]), away_score=sc.get(e["away_team"])))
        for d, x in pd.DataFrame(rows).groupby("date") if rows else []:
            os.makedirs(f"data/scores/{sp}", exist_ok=True); x.to_csv(f"data/scores/{sp}/{d}.csv", index=False)
        n[sp] = len(rows)
    print(f"::notice::scores {n}, credits left {left['remaining']}"); return n

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
    global TIER
    if TIER != "paid":   # auto-detect the paid plan (2026-11-06): a key with >= 5,000 credits left means the 20K plan is active
        get("sports")
        if int(float(left["remaining"] or 0)) >= 5000:
            TIER = "paid"; print(f"::notice::paid plan detected ({left['remaining']} credits on key 1): full markets, no budget guard")
    now = dt.datetime.now(ET); today = now.date().isoformat(); info = {"tag": tag, "tier": TIER}
    if TIER != "paid" and os.environ.get("FORCE") != "1":   # credit budget (2026-11-01): keep the month's core feed alive until keys reset on the 1st
        total, k0 = 0, KEY
        for k in KEYS:   # 'sports' costs 0 credits and returns the key's remaining credits in the headers
            KEY = k; left["remaining"] = None; get("sports")
            total += int(left["remaining"] or 0)
        KEY = next((k for k in KEYS if k), k0)
        nxt = (now.replace(day=1) + dt.timedelta(days=32)).replace(day=1)
        days_left = max((nxt.date() - now.date()).days, 1)
        reserve = 25 * days_left   # board + close core floor (2-3 free keys = 1,000-1,500 a month)
        print(f"::notice::credits left across {len(KEYS)} keys: {total}; {days_left} days to reset; core reserve {reserve}")
        EXTRAS_OK[0] = total >= reserve + 150
        LOW[0] = total < 40 * days_left   # low-credit mode: board carries only the markets with proven under edges
        if tag not in ("board", "close", "pregame") and total < reserve + 60:
            print(f"::warning::budget: skipping optional tag '{tag}' to protect the core feed (FORCE=1 overrides)"); return
        if tag == "pregame" and total < reserve:
            print("::warning::budget: skipping pregame; only board + close until the reset (FORCE=1 overrides)"); return
    sports = SPORTS if TIER == "paid" else SPORTS_FREE
    if LOW[0] and tag == "board":
        sports = {**sports, "nba": ("basketball_nba", "player_rebounds,player_assists")}   # halves the board cost; points/threes skipped until the reset
        print("::notice::low-credit mode: NBA board = rebounds + assists only")
    if tag == "nbaq1":   # on-demand: NBA 1st-quarter player props (DK 1Q boosts)
        sports = {"nba": ("basketball_nba", "player_points_q1,player_rebounds_q1,player_assists_q1")}
    if tag in ("cbb", "lines", "nhl", "ucl"):   # on-demand game lines: cbb = college basketball; nhl; ucl = Champions League; lines = every sport we track
        info["games"] = {sp: bulk_lines(sp, now, today, tag) for sp in ({"cbb": ["ncaab"], "nhl": ["nhl"], "ucl": ["ucl"]}.get(tag) or ["ncaab", "nba", "nfl", "ncaaf"])}
        info["credits_remaining"] = left["remaining"]
        st = json.load(open("status/actions.json")) if os.path.exists("status/actions.json") else {}
        st[f"odds_{tag}"] = dict(last_ok=now.isoformat(timespec="seconds"), **info); json.dump(st, open("status/actions.json", "w"), indent=1)
        return
    if tag == "scores" or (tag == "open" and TIER != "paid"):   # the free tier skips the open prop snapshot; use the slot for final scores
        info["scores"] = scores(now); info["credits_remaining"] = left["remaining"]
        st = json.load(open("status/actions.json")) if os.path.exists("status/actions.json") else {}
        st["odds_scores"] = dict(last_ok=now.isoformat(timespec="seconds"), **info); json.dump(st, open("status/actions.json", "w"), indent=1)
        return
    if tag == "open" and TIER == "paid":   # paid: the open slot also pulls final scores (6 credits) before the open prop snapshot
        try: scores(now)
        except Exception as e: print(f"::warning::scores: {e}")
    if tag == "nbaalt":   # on-demand: NBA alternate ladders (one-sided X+ rungs) for parlay building
        sports = {"nba": ("basketball_nba", "player_points_alternate,player_rebounds_alternate,player_assists_alternate,player_threes_alternate")}
    if tag == "pregame":   # on-demand: main + alternate props for games starting in the next WINDOW_MIN minutes (all games, not just bet games)
        sports = {"nba": ("basketball_nba", "player_points,player_rebounds,player_assists,player_threes"),   # alt ladders dropped 2026-10-28 (alt rungs paper-only)
                  "mlb": ("baseball_mlb", "batter_hits_runs_rbis,batter_hits,batter_rbis,batter_runs_scored,batter_total_bases,pitcher_strikeouts"),
                  "nfl": ("americanfootball_nfl", "player_reception_yds,player_rush_yds,player_receptions,player_pass_yds,player_anytime_td")}
    if tag == "pick6":   # on-demand: Pick6 lines + the sportsbooks' main lines for every game in the next WINDOW_MIN minutes (default 12 h)
        sports = {"nba": ("basketball_nba", "player_points,player_rebounds,player_assists,player_threes"),
                  "mlb": ("baseball_mlb", "pitcher_strikeouts,batter_hits,batter_total_bases,batter_hits_runs_rbis"),
                  "nfl": ("americanfootball_nfl", "player_reception_yds,player_rush_yds,player_receptions,player_pass_yds")}
    if tag == "nfltmr":   # on-demand: tomorrow's NFL props (Thursday game, priced the night before); files go in tomorrow's folder
        today = (now + dt.timedelta(days=1)).date().isoformat()
        sports = {"nfl": ("americanfootball_nfl", "player_reception_yds,player_rush_yds,player_receptions,player_pass_yds,player_pass_tds,player_rush_attempts,player_anytime_td,player_reception_yds_alternate,player_pass_yds_alternate,player_rush_yds_alternate")}
    if tag.startswith("cbbprops"):   # on-demand: college basketball player props for games whose team name contains the text after ":" (e.g. cbbprops:Indiana)
        team = tag.split(":", 1)[1] if ":" in tag else ""; key = GAME_SPORTS["ncaab"]; rows = []
        for e in get(f"sports/{key}/events") or []:
            if team and team.lower() not in (e["home_team"] + e["away_team"]).lower(): continue
            t = dt.datetime.fromisoformat(e["commence_time"].replace("Z", "+00:00")).astimezone(ET)
            if t.date().isoformat() != today: continue
            o = get(f"sports/{key}/events/{e['id']}/odds", bookmakers=BOOKS, markets="player_points,player_rebounds,player_assists,player_threes,player_points_rebounds_assists", oddsFormat="american")
            for b in (o or {}).get("bookmakers", []):
                for m in b.get("markets", []):
                    for oc in m.get("outcomes", []):
                        rows.append(dict(snap_et=now.isoformat(timespec="seconds"), game=f"{e['away_team']}@{e['home_team']}", start_et=t.isoformat(timespec="minutes"), book=b["key"], market=m["key"], player=oc.get("description"), side=oc.get("name"), line=oc.get("point"), price=oc.get("price")))
        if rows:
            os.makedirs(f"data/odds/ncaab/{today}", exist_ok=True)
            pd.DataFrame(rows).to_csv(f"data/odds/ncaab/{today}/cbbprops_{now:%H%M}.csv", index=False)
        print(f"::notice::ncaab props: {len(rows)} rows"); info["ncaab"] = len(rows); sports = {}
    if tag == "cbbalt":   # on-demand: college basketball alternate spreads + totals for today's games (parlay/boost building); 2 credits per game
        key = GAME_SPORTS["ncaab"]; rows = []
        for e in get(f"sports/{key}/events") or []:
            t = dt.datetime.fromisoformat(e["commence_time"].replace("Z", "+00:00")).astimezone(ET)
            if t.date().isoformat() != today or t < now: continue
            o = get(f"sports/{key}/events/{e['id']}/odds", bookmakers=BOOKS.replace(",pick6", ""), markets="alternate_spreads,alternate_totals,spreads,totals,h2h", oddsFormat="american")
            for b in (o or {}).get("bookmakers", []):
                for m in b.get("markets", []):
                    for oc in m.get("outcomes", []):
                        rows.append(dict(snap_et=now.isoformat(timespec="seconds"), event_id=e["id"], away=e["away_team"], home=e["home_team"], start_et=t.isoformat(timespec="minutes"),
                                         book=b["key"], market=m["key"], name=oc.get("name"), point=oc.get("point"), price=oc.get("price")))
        if rows:
            os.makedirs(f"data/odds/ncaab/{today}", exist_ok=True)
            pd.DataFrame(rows).to_csv(f"data/odds/ncaab/{today}/cbbalt_{now:%H%M}.csv", index=False)
        print(f"::notice::ncaab cbbalt: {len(rows)} rows")
        info["ncaab"] = len(rows); sports = {}
    if tag == "nhlprops":   # on-demand: NHL player props (Pick6 promo hunting); ~6 credits per game
        sports = {"nhl": ("icehockey_nhl", "player_points,player_shots_on_goal,player_assists,player_goals,player_blocked_shots,player_total_saves,player_shots_on_goal_alternate,player_points_alternate,player_assists_alternate,player_total_saves_alternate")}
    if tag == "nflalt":   # on-demand: NFL alternate yardage/reception ladders (Sundays)
        sports = {"nfl": ("americanfootball_nfl", "player_reception_yds_alternate,player_rush_yds_alternate,player_receptions_alternate")}
    if tag == "mlbprops":   # on-demand: MLB batter/pitcher props for promo-token hunting (two-sided markets)
        sports = {"mlb": ("baseball_mlb", "batter_rbis,batter_runs_scored,batter_total_bases,batter_home_runs,batter_hits,batter_hits_runs_rbis,pitcher_strikeouts")}
    if tag == "mlbhrr":   # on-demand: MLB batter hits+runs+RBIs and hits (1 credit per market per game)
        sports = {"mlb": ("baseball_mlb", "batter_hits_runs_rbis,batter_hits")}
    if tag in ("mlbprops",): pass
    if tag == "board" and os.environ.get("FORCE") != "1":   # credit saver: one afternoon board per day is enough
        import glob as _g
        recent = [f for f in _g.glob(f"data/odds/nba/{today}/board_*.csv") if f[-8:-4] >= "1200"]
        if recent and now.hour >= 12:
            print(f"::notice::board already taken today ({recent[-1]}); skipping to save credits (set FORCE=1 to override)"); return
    if TIER != "paid" and tag == "board" and now.weekday() != 6: sports = {k: sports[k] for k in ("nba", "mlb")}   # NFL board only on Sundays
    bet_games = set()
    if TIER != "paid" and tag == "close":
        try:
            b = pd.read_csv("Record/bets.csv"); bet_games = set(b[b["date"] == today]["notes"].astype(str))
            if os.path.exists(f"data/edges/{today}.csv"):   # also every qualifying price-edge leg's game, so its CLV can be graded
                e = pd.read_csv(f"data/edges/{today}.csv")
                bet_games |= set(e[(e.ev_sharp.fillna(-99) >= 2) & (e.ev_all >= 0)]["game"].astype(str))
        except Exception: pass
        if not bet_games: return
    if tag in ("board", "pregame") and EXTRAS_OK[0]:
        for gsp in (("ncaab", "nfl", "ncaaf", "nba") if TIER == "paid" else ("ncaab", "nfl", "ncaaf") if tag == "board" else ("ncaab",)):
            try: bulk_lines(gsp, now, today, tag)
            except Exception as e: print(f"::warning::{gsp} lines: {e}")
    for sp, (key, markets) in sports.items():
        if tag in ("board", "open"):   # v1.2: game lines for the slate (spreads + totals, 3 books = 2 credits per sport)
            gl = get(f"sports/{key}/odds", markets="spreads,totals", bookmakers="draftkings,fanduel,pinnacle", oddsFormat="american") or []
            grows = []
            for e in gl:
                for bk in e.get("bookmakers", []):
                    for m in bk.get("markets", []):
                        for oc in m.get("outcomes", []):
                            grows.append(dict(snap_et=now.isoformat(timespec="seconds"), sport=sp.upper(), event_id=e["id"], home=e["home_team"],
                                              away=e["away_team"], start=e["commence_time"], book=bk["key"], market=m["key"], name=oc["name"],
                                              point=oc.get("point"), price=oc.get("price")))
            if grows:
                os.makedirs(f"data/odds/{sp}/{today}", exist_ok=True)
                pd.DataFrame(grows).to_csv(f"data/odds/{sp}/{today}/games_{now:%H%M}.csv", index=False)
        evs = get(f"sports/{key}/events") or []
        sel = []
        for e in evs:
            t = dt.datetime.fromisoformat(e["commence_time"].replace("Z", "+00:00")).astimezone(ET)
            if t.date().isoformat() != today: continue
            mins = (t - now).total_seconds() / 60
            if tag == "close" and not (0 < mins <= 75): continue
            if tag in ("pregame", "pick6") and not (0 < mins <= float(os.environ.get("WINDOW_MIN", "150" if tag == "pregame" else "720"))): continue
            if tag != "close" and mins < 0: continue
            sel.append((e, t))
        rows = []
        for e, t in sel:
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
    if left["remaining"] and int(float(left["remaining"])) < (1500 if TIER == "paid" else 60): print(f"::warning::Odds API credits low: {left['remaining']}")

if __name__ == "__main__": main()
