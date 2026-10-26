"""Fill gaps in the NBA game logs from box scores Claude reads on the web (cloud, laptop off).
    python engine/nba/append_box.py data/box/nba/2026-10-25.csv
Input CSV columns: date, game (AWAY@HOME), team (3-letter), player, min, pts, reb, ast, fg3m, fg3a, oreb, dreb, stl, blk, tov,
team_final (that team's final score), source (url).
Checks before writing: every team's player points must sum to team_final (else the whole game is rejected), no duplicate dates.
Appends to engine/data/players_2026-27.csv with SEASON_ID 22026; PLAYER_ID from existing logs by name (else a negative
placeholder id). VIDEO_AVAILABLE = -1 marks cloud rows. When the laptop runs fetch.py (nba_api), the official file replaces it all."""
import sys, os
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from common import norm_name

LOG = "engine/data/players_2026-27.csv"

def main(path):
    box = pd.read_csv(path); logs = pd.read_csv(LOG)
    date = str(box["date"].iloc[0])
    if (logs["GAME_DATE"].astype(str).str[:10] == date).any():
        print(f"{date} already in logs; nothing appended"); return
    ids = dict(zip(logs["PLAYER_NAME"].map(norm_name), logs["PLAYER_ID"]))
    teams = logs.drop_duplicates("TEAM_ABBREVIATION").set_index("TEAM_ABBREVIATION")[["TEAM_ID", "TEAM_NAME"]]
    good, bad = [], []
    for (game, team), g in box.groupby(["game", "team"]):
        s, fin = int(g["pts"].sum()), int(g["team_final"].iloc[0])
        (good if s == fin else bad).append((game, team, s, fin))
    ok_games = {g for g, *_ in good} - {g for g, *_ in bad}
    for g, t, s, f in bad: print(f"REJECT {g} {t}: player points {s} != final {f}")
    rows = []
    for _, r in box[box["game"].isin(ok_games) & (box["min"] > 0)].iterrows():
        away, home = r["game"].split("@"); opp = home if r["team"] == away else away
        k = norm_name(r["player"]); pid = ids.get(k, -abs(hash(k)) % 10**7)
        rows.append({"SEASON_ID": 22026, "PLAYER_ID": pid, "PLAYER_NAME": r["player"],
                     "TEAM_ID": teams["TEAM_ID"].get(r["team"], -1), "TEAM_ABBREVIATION": r["team"], "TEAM_NAME": teams["TEAM_NAME"].get(r["team"], r["team"]),
                     "GAME_ID": f"cloud-{date}-{r['game']}", "GAME_DATE": date,
                     "MATCHUP": f"{r['team']} {'@' if r['team'] == away else 'vs.'} {opp}", "WL": None, "MIN": r["min"],
                     "FG3M": r["fg3m"], "FG3A": r["fg3a"], "OREB": r["oreb"], "DREB": r["dreb"], "REB": r["reb"], "AST": r["ast"],
                     "STL": r["stl"], "BLK": r["blk"], "TOV": r["tov"], "PTS": r["pts"], "VIDEO_AVAILABLE": -1})
    if rows:
        pd.concat([logs, pd.DataFrame(rows)], ignore_index=True).to_csv(LOG, index=False)
    print(f"{date}: appended {len(rows)} player rows from {len(ok_games)} games; rejected {len({g for g, *_ in bad})} games")

if __name__ == "__main__":
    main(sys.argv[1])
