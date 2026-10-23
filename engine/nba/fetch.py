"""Pull NBA player + team game logs for last and current season (run on your PC; needs: pip install nba_api pandas).
Usage (from the vault root):  python engine/nba/fetch.py"""
import os, sys, time
sys.path.insert(0, os.path.dirname(__file__))
import config as C

def main():
    from nba_api.stats.endpoints import leaguegamelog
    os.makedirs(C.DATA_DIR, exist_ok=True)
    for season in (C.SEASON_PRIOR, C.SEASON_CUR):
        for kind, flag in (("players", "P"), ("teams", "T")):
            path = f"{C.DATA_DIR}/{kind}_{season}.csv"
            if season == C.SEASON_PRIOR and os.path.exists(path):
                print("cached", path); continue
            for attempt in range(4):
                try:
                    df = leaguegamelog.LeagueGameLog(season=season, season_type_all_star="Regular Season",
                                                     player_or_team_abbreviation=flag, timeout=60).get_data_frames()[0]
                    df.to_csv(path, index=False); print(f"saved {path}: {len(df)} rows"); break
                except Exception as e:
                    print(f"retry {attempt+1} {season} {kind}: {e}"); time.sleep(5 * (attempt + 1))
            time.sleep(1.5)

if __name__ == "__main__":
    main()
