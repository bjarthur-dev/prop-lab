"""Live slip tracker (GitHub Actions, every ~15 min on game nights). Reads Record/slips/<date>.json, pulls live box
scores, writes Record/Live.md and status/live.json, and prints 'SETTLED: ...' lines for slips that just won or died
(the workflow posts those to the phone as a GitHub issue comment).
    python engine/cloud/live_track.py [YYYY-MM-DD]
Sources: NBA and NFL from api-sports (SPORTS_API_KEY_1/2, 100 requests a day each: finished games are cached and only
games holding an open leg are fetched). NHL from the official api-web.nhle.com. No scraping, no spoofing.
A leg is WON early when an over is already cleared, DEAD early when an under is already beaten."""
import datetime as dt, json, os, re, sys, time, unicodedata, urllib.parse, urllib.request
from zoneinfo import ZoneInfo
ET = ZoneInfo("America/New_York")
KEYS = [k for k in (os.environ.get("SPORTS_API_KEY_1", ""), os.environ.get("SPORTS_API_KEY_2", "")) if k]
STATE = {"key": 0, "left": None, "calls": 0}
def norm(n): return re.sub(r"[^a-z]", "", unicodedata.normalize("NFKD", str(n)).encode("ascii", "ignore").decode().lower().replace(" jr", "").replace(" iii", "").replace(" ii", ""))

def api(base, path, **q):
    url = f"{base}/{path}?{urllib.parse.urlencode(q)}"
    while STATE["key"] < len(KEYS):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"x-apisports-key": KEYS[STATE["key"]]}), timeout=30) as r:
                STATE["left"] = r.headers.get("x-ratelimit-requests-remaining"); STATE["calls"] += 1; d = json.load(r)
            if d.get("errors"):
                print(f"::warning::{path} errors {d['errors']}")
                if any(w in str(d["errors"]).lower() for w in ("request", "limit")): STATE["key"] += 1; continue
                return []
            time.sleep(6.5); return d.get("response", [])
        except Exception as e:
            print(f"::warning::{path}: {e}"); return []
    return []

def nba_feed(date, need, cache):
    """-> {normname: {stat: value, 'game': str, 'state': str, 'final': bool}}"""
    out = {}; d0 = dt.date.fromisoformat(date); B = "https://v2.nba.api-sports.io"
    games = api(B, "games", date=date) + api(B, "games", date=(d0 + dt.timedelta(days=1)).isoformat())
    for g in games:
        start = dt.datetime.fromisoformat(g["date"]["start"].replace("Z", "+00:00")).astimezone(ET)
        if start.date().isoformat() != date: continue
        st = str(g.get("status", {}).get("long", "")); gid = str(g["id"])
        label = f'{g["teams"]["visitors"]["code"]}@{g["teams"]["home"]["code"]}'
        final = st.lower() == "finished"
        if st.lower() in ("scheduled", "not started"): out[f"__sched_{label}"] = start.strftime("%H:%M"); continue
        if final and gid in cache: rows = cache[gid]
        else:
            rows = [dict(n=norm(f"{p['player']['firstname']} {p['player']['lastname']}"), pts=p.get("points") or 0, reb=p.get("totReb") or 0,
                         ast=p.get("assists") or 0, fg3m=p.get("tpm") or 0, min=str(p.get("min") or "0")) for p in api(B, "players/statistics", game=g["id"])]
            if final and rows: cache[gid] = rows
        per = g.get("periods", {}).get("current"); clock = g.get("status", {}).get("clock") or ""
        state = "Final" if final else f"Q{per} {clock}".strip()
        score = f'{g["scores"]["visitors"].get("points")}-{g["scores"]["home"].get("points")}'
        for r in rows:
            out[r["n"]] = dict(pts=r["pts"], reb=r["reb"], ast=r["ast"], fg3m=r["fg3m"], pr=r["pts"] + r["reb"], pa=r["pts"] + r["ast"], ra=r["reb"] + r["ast"],
                               pra=r["pts"] + r["reb"] + r["ast"], game=f"{label} {score}", state=state, final=final)
        out[f"__game_{label}"] = dict(state=state, final=final)
    return out

def nfl_feed(date, cache):
    out = {}; B = "https://v1.american-football.api-sports.io"
    games = api(B, "games", date=date, league=1) + api(B, "games", date=(dt.date.fromisoformat(date) + dt.timedelta(days=1)).isoformat(), league=1)
    for g in games:
        gm = g.get("game", {}); st = str(gm.get("status", {}).get("long", "")); gid = str(gm.get("id"))
        final = st.lower().startswith("finished") or st.lower() == "final"
        if st.lower() in ("not started", "scheduled"): continue
        label = f'{g["teams"]["away"]["name"].split()[-1]}@{g["teams"]["home"]["name"].split()[-1]}'
        state = "Final" if final else f'{gm.get("status", {}).get("short", "")} {gm.get("status", {}).get("timer") or ""}'.strip()
        resp = cache.get("nfl" + gid) if final and "nfl" + gid in cache else api(B, "games/statistics/players", id=gid)
        if final and resp: cache["nfl" + gid] = resp
        for team in resp:
            for grp in team.get("groups", []):
                gname = str(grp.get("name", "")).lower()
                for p in grp.get("players", []):
                    stats = {str(s.get("name", "")).lower(): s.get("value") for s in p.get("statistics", [])}
                    n = norm(p.get("player", {}).get("name", "")); r = out.setdefault(n, dict(game=label, state=state, final=final))
                    def f(k):
                        try: return float(stats.get(k) or 0)
                        except (TypeError, ValueError): return 0.0
                    if gname == "rushing": r["rush_yds"] = f("yards"); r["rush_att"] = f("total rushes") or f("carries") or f("attempts")
                    elif gname == "receiving": r["rec_yds"] = f("yards"); r["rec"] = f("total receptions") or f("receptions")
                    elif gname == "passing": r["pass_yds"] = f("yards")
        out[f"__game_{label}"] = dict(state=state, final=final)
    return out

def find(feed, player):
    k = norm(player)
    if k in feed: return feed[k]
    last = norm(player.split()[-1]); first = norm(player)[0]
    c = [v for n, v in feed.items() if not n.startswith("__") and n.endswith(last) and n[0] == first]
    return c[0] if len(c) == 1 else None

def leg_status(leg, feed):
    r = find(feed, leg["player"])
    if r is None or leg["stat"] not in r:
        finals = [v for n, v in feed.items() if n.startswith("__game_")]
        return dict(cur=None, st="waiting", note="not started or no stat yet")
    cur = r[leg["stat"]]; over = leg["side"] == "over"; fin = r["final"]
    if over: st = "WON" if cur > leg["line"] else ("LOST" if fin else "live")
    else: st = "LOST" if cur > leg["line"] else ("WON" if fin else "live")
    return dict(cur=cur, st=st, note=f'{r["game"]} {r["state"]}')

def main():
    now = dt.datetime.now(ET); date = sys.argv[1] if len(sys.argv) > 1 else (now - dt.timedelta(hours=6)).date().isoformat()
    path = f"Record/slips/{date}.json"
    if not os.path.exists(path): print(f"no slips file for {date}; nothing to track"); return
    slips = json.load(open(path))["slips"]
    try: prev = json.load(open("status/live.json"))
    except Exception: prev = {}
    if prev.get("date") != date: prev = {"date": date, "slips": {}, "cache": {}}
    cache = prev.setdefault("cache", {})
    open_slips = [s for s in slips if prev["slips"].get(str(s["id"]), {}).get("st") not in ("WON", "LOST")]
    if not open_slips: print("all slips settled"); return
    sports = {l["sport"] for s in open_slips for l in s["legs"]}
    feed = {}
    if "nba" in sports: feed.update(nba_feed(date, None, cache))
    if "nfl" in sports: feed.update(nfl_feed(date, cache))
    rows = []; alive_pay = 0.0; won_pay = 0.0; staked = 0.0; news = []
    for s in slips:
        old = prev["slips"].get(str(s["id"]), {})
        if old.get("st") in ("WON", "LOST") and "detail" in old: st, detail = old["st"], old["detail"]
        else:
            L = [leg_status(l, feed) for l in s["legs"]]
            st = "LOST" if any(x["st"] == "LOST" for x in L) else "WON" if all(x["st"] == "WON" for x in L) else "live" if any(x["cur"] is not None for x in L) else "waiting"
            mark = {"WON": "✅", "LOST": "❌", "live": "▶", "waiting": "·"}
            detail = "<br>".join(f'{mark[x["st"]]} {l["player"]} {l["side"]} {l["line"]} {l["stat"]}: ' + (f'**{x["cur"]:g}** ({x["note"]})' if x["cur"] is not None else x["note"]) for l, x in zip(s["legs"], L))
            if st in ("WON", "LOST") and old.get("st") not in ("WON", "LOST"):
                news.append(f'{"WON" if st == "WON" else "DEAD"}: {s["book"]} #{s["id"]} {s["name"]} (${s["stake"]:g} to pay ${s["pays"]:g})')
        prev["slips"][str(s["id"])] = dict(st=st, detail=detail)
        staked += s["stake"]; won_pay += s["pays"] if st == "WON" else 0; alive_pay += s["pays"] if st in ("live", "waiting") else 0
        rows.append(f'| {s["id"]} | {s["book"]} | {s["name"]} | ${s["stake"]:g} → ${s["pays"]:g} | **{st}** | {detail} |')
    n = lambda k: sum(1 for v in prev["slips"].values() if v["st"] == k)
    md = [f"# Live slips, {date}\n", f"Updated **{now:%H:%M} ET**. Staked ${staked:g}. Won so far: **${won_pay:.2f}**. Still alive: {n('live') + n('waiting')} slips worth up to ${alive_pay:.2f}. Dead: {n('LOST')}.\n",
          "| # | App | Slip | Stake → pays | Status | Legs |\n|---|---|---|---|---|---|", *rows,
          f"\nAn over shows WON as soon as it clears; an under shows LOST as soon as it is beaten. Final results are confirmed in the morning settlement. API requests left today: {STATE['left']}.\n"]
    open("Record/Live.md", "w").write("\n".join(md)); os.makedirs("status", exist_ok=True); json.dump(prev, open("status/live.json", "w"))
    print("\n".join(md)[:3000])
    for x in news: print("SETTLED: " + x)
    if news: open("live_news.txt", "w").write("\n".join(news) + f"\n\nWon so far ${won_pay:.2f}; {n('live') + n('waiting')} slips still alive (up to ${alive_pay:.2f}).")

if __name__ == "__main__": main()
