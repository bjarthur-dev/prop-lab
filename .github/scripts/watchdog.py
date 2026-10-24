"""Prints ok=true|false and problems=... for GITHUB_OUTPUT."""
import json, os, datetime as dt
from zoneinfo import ZoneInfo
now = dt.datetime.now(ZoneInfo("America/New_York")); today = now.date().isoformat()
probs = []
try:
    s = json.load(open("status/actions.json"))["results"]
    age = (now - dt.datetime.fromisoformat(s["last_ok"])).total_seconds() / 3600
    if age > 26: probs.append(f"results.yml last succeeded {age:.0f} h ago")
    for k in ("mlb",):
        if str(s.get(k, "")).startswith("error"): probs.append(f"results {k}: {s[k]}")
except Exception as e:
    probs.append(f"no results heartbeat ({e})")
try:
    c = json.load(open("status/claude.json"))["morning_settlement"]
    age = (now - dt.datetime.fromisoformat(c["last_ok"])).total_seconds() / 3600
    if now.hour >= 10 and age > 26: probs.append(f"Claude morning settlement last ran {age:.0f} h ago")
except FileNotFoundError:
    if now.hour >= 10 and now.date() > dt.date(2026, 10, 24): probs.append("no Claude heartbeat (status/claude.json)")
except Exception as e:
    probs.append(f"bad Claude heartbeat ({e})")
slate = os.path.exists(f"Inbox/Requests/{today} requests.md") or any(f.startswith(today) for f in os.listdir("Slates"))
# Scout checks are OFF while Perplexity jobs are paused to save credits (until weekly usage resets Thu 2026-10-29).
# Turn back on by setting SCOUT_CHECKS = True.
SCOUT_CHECKS = False
for f, by in (((f"{today} C board.md", 15),) if SCOUT_CHECKS else ()):
    if slate and now.hour >= by and not os.path.exists(f"Inbox/Perplexity/{f}"):
        probs.append(f"Scout file missing: Inbox/Perplexity/{f} (due before {by}:00 ET)")
print("ok=" + ("true" if not probs else "false"))
print("problems=" + (" | ".join(probs) if probs else "none"))
