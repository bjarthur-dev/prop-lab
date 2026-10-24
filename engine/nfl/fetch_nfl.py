"""Download nflverse play-by-play (2023-2026) and save slim copies the engine/backtest needs.
Run from the vault root:  python engine/nfl/fetch_nfl.py      (only needs pandas; no extra packages)
Writes engine/data/nfl/pbp_<season>_slim.csv.gz and prints a summary."""
import os, sys, time, urllib.request
import pandas as pd

OUT = "engine/data/nfl"
SEASONS = [2023, 2024, 2025, 2026]
URLS = ["https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_{y}.csv.gz"]
KEEP = ["game_id", "season", "week", "season_type", "game_date", "home_team", "away_team", "posteam", "defteam",
        "spread_line", "total_line", "home_score", "away_score", "roof", "wind", "temp", "weather",
        "play_type", "pass_attempt", "rush_attempt", "complete_pass", "sack", "qb_dropback", "qb_scramble",
        "yards_gained", "air_yards", "yards_after_catch", "receiving_yards", "rushing_yards", "yardline_100",
        "touchdown", "pass_touchdown", "rush_touchdown", "td_player_name", "td_player_id",
        "passer_player_name", "passer_player_id", "receiver_player_name", "receiver_player_id",
        "rusher_player_name", "rusher_player_id", "xpass", "pass_oe", "score_differential", "qtr",
        "game_seconds_remaining", "wp", "two_point_attempt", "qb_kneel", "qb_spike"]

def download(y):
    raw = f"{OUT}/play_by_play_{y}.csv.gz"
    for u in URLS:
        url = u.format(y=y)
        for attempt in range(3):
            try:
                print(f"downloading {y} ... ", end="", flush=True)
                urllib.request.urlretrieve(url, raw)
                print(f"{os.path.getsize(raw)/1e6:.1f} MB")
                return raw
            except Exception as e:
                print(f"failed ({e}); retrying"); time.sleep(3)
    return None

def main():
    os.makedirs(OUT, exist_ok=True)
    ok = []
    for y in SEASONS:
        slim = f"{OUT}/pbp_{y}_slim.csv.gz"
        if y < 2026 and os.path.exists(slim):
            print(f"{y}: already have it"); ok.append(y); continue
        raw = download(y)
        if not raw:
            print(f"{y}: NOT AVAILABLE"); continue
        df = pd.read_csv(raw, low_memory=False)
        cols = [c for c in KEEP if c in df.columns]
        df[cols].to_csv(slim, index=False, compression="gzip")
        os.remove(raw)
        g = df["game_id"].nunique(); wk = int(df["week"].max())
        print(f"{y}: {len(df):,} plays, {g} games, through week {wk} -> {slim} ({os.path.getsize(slim)/1e6:.1f} MB)")
        ok.append(y)
    print("\nDONE. Seasons saved:", ok)
    if not ok:
        print("Nothing downloaded - send Claude a screenshot of this window."); sys.exit(1)

if __name__ == "__main__":
    main()
