"""System health check: is every data feed fresh, and will the free odds credits last the month?
    python engine/health.py  -> Record/System Health.md (and exit 0; problems are listed, never fatal)"""
import os, glob, json, datetime as dt
import pandas as pd

NOW = dt.datetime.now(dt.timezone(dt.timedelta(hours=-5)))
def age_days(ts):
    try: return (NOW - pd.Timestamp(ts).tz_convert(NOW.tzinfo).to_pydatetime()).total_seconds() / 86400
    except Exception: return None

def main():
    rows, warn = [], []
    def check(name, days, limit, fix):
        s = "n/a" if days is None else f"{days:.1f} d"
        bad = days is None or days > limit
        rows.append(f"| {name} | {s} | {limit} d | {'**STALE**' if bad else 'ok'} |")
        if bad: warn.append(f"- {name}: {fix}")
    st = json.load(open("status/actions.json")) if os.path.exists("status/actions.json") else {}
    check("results (box scores)", age_days(st.get("results", {}).get("last_ok")), 1.5, "re-run results.yml (Actions tab)")
    check("odds board", age_days(st.get("odds_board", {}).get("last_ok")), 1.5, "check odds.yml runs / API keys")
    check("odds pregame", age_days(st.get("odds_pregame", {}).get("last_ok")), 1.5, "check odds.yml pregame tag")
    p = pd.read_csv("engine/data/players_2026-27.csv", usecols=["GAME_DATE"])
    last = pd.to_datetime(p.GAME_DATE.astype(str).str[:10]).max()
    check("NBA game logs", (NOW.replace(tzinfo=None) - last).days + 0.0, 2.5, "run update_nba_data_auto.bat on the laptop or check nba_box.py")
    ctx = sorted(glob.glob("engine/data/context/2026-27/*.csv"), key=os.path.getmtime)
    if ctx:
        # git checkout resets mtimes, so use the newest commit time for the folder
        t = os.popen("git log -1 --format=%cI -- engine/data/context/2026-27").read().strip()
        check("NBA matchup context (laptop)", age_days(t) if t else None, 4, "run update_nba_context.bat on the laptop")
    t = os.popen("git log -1 --format=%cI -- engine/data/nfl").read().strip()
    check("NFL data (nflverse)", age_days(t) if t else None, 8, "results.yml refreshes Mon/Tue/Fri; dispatch it")
    # free credit runway: keys reset on the 1st; 3 keys x 500
    rem = [int(v["credits_remaining"]) for v in st.values() if isinstance(v, dict) and str(v.get("credits_remaining", "")).isdigit()
           and age_days(v.get("last_ok")) is not None and age_days(v.get("last_ok")) < 2]
    days_left = (pd.Timestamp(NOW.year + (NOW.month == 12), NOW.month % 12 + 1, 1) - pd.Timestamp(NOW.date())).days
    credit = ["", "## Odds API credits", ""]
    if rem:
        used = 500 - min(rem); day = max(NOW.day, 1)
        credit.append(f"Lowest key seen today: {min(rem)} left of 500 (about {used/day:.0f}/day on that key). "
                      f"{days_left} days until the 1st reset. Three keys x 500 = 1,500 a month, about {1500/30:.0f}/day sustainable.")
        if used / day * 30 > 1500: warn.append("- Odds credits: current pace runs out before the 1st. Cut extra tags (nbaalt, mlb) before the board/pregame/close core.")
    rows_txt = ["| feed | age | limit | status |", "|---|---:|---:|---|"] + rows
    L = ["---", "tags: [system, health]", "---", "", f"# System health ({NOW:%Y-%m-%d %H:%M} ET)", "",
         "Written by `engine/health.py` each morning. Fix STALE rows before trusting a card.", ""] + rows_txt + credit + \
        ["", "## Problems", ""] + (warn or ["None."])
    open("Record/System Health.md", "w").write("\n".join(L) + "\n"); print("\n".join(L[6:]))

if __name__ == "__main__":
    main()
