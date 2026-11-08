"""NHL box scores from the official NHL web API (api-web.nhle.com). Prints skater/goalie lines; changes nothing.
    python engine/cloud/nhl_box.py YYYY-MM-DD"""
import sys, json, urllib.request
def get(u):
    with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "prop-lab results bot"}), timeout=30) as r: return json.load(r)
date = sys.argv[1]
for g in get(f"https://api-web.nhle.com/v1/score/{date}").get("games", []):
    a, h = g["awayTeam"], g["homeTeam"]
    print(f"GAME {a['abbrev']} {a.get('score')} @ {h['abbrev']} {h.get('score')} state {g.get('gameState')}")
    try: b = get(f"https://api-web.nhle.com/v1/gamecenter/{g['id']}/boxscore")
    except Exception as e: print("  box failed", e); continue
    for side in ("awayTeam", "homeTeam"):
        t = b.get("playerByGameStats", {}).get(side, {})
        for grp in ("forwards", "defense"):
            for p in t.get(grp, []):
                print(f"  SK {b[side]['abbrev']} {p['name']['default']}: g {p.get('goals')} a {p.get('assists')} sog {p.get('sog')} toi {p.get('toi')}")
        for p in t.get("goalies", []):
            print(f"  GK {b[side]['abbrev']} {p['name']['default']}: saves {p.get('saves')} sa {p.get('shotsAgainst')} toi {p.get('toi')}")
