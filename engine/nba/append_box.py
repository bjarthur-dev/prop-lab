"""Fill gaps in the NBA game logs from box scores Claude reads on the web (cloud, laptop off).
    python engine/nba/append_box.py data/box/nba/2026-10-25.csv
Input CSV columns: date, game (AWAY@HOME), team (3-letter), player, min, pts, reb, ast, fg3m, fg3a, oreb, dreb, stl, blk, tov,
team_final (that team's final score), source (url).
Checks before writing: each team is written only if its player points sum exactly to team_final; failing teams go to DATE_gaps.csv
(the morning task looks up the missing players and re-runs with a completed file). A team already in the logs for that date is never duplicated.
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
    have = logs[logs["GAME_DATE"].astype(str).str[:10] == date]["TEAM_ABBREVIATION"].unique()
    box = box[~box["team"].isin(have)]          # allow filling gap teams later; never duplicate a team's game
    if box.empty: print(f"{date}: all teams already in logs; nothing appended"); return
    ids = dict(zip(logs["PLAYER_NAME"].map(norm_name), logs["PLAYER_ID"]))
    def ik(n, t):   # initial + last name + team: matches "D. Acuff Jr." to "Darius Acuff Jr."
        w = norm_name(n).replace(".", "").split(); return (w[0][:1] + " " + " ".join(w[1:]), t) if len(w) > 1 else (n, t)
    ids_it = {ik(n, t): i for n, t, i in zip(logs["PLAYER_NAME"], logs["TEAM_ABBREVIATION"], logs["PLAYER_ID"])}
    names_it = {ik(n, t): n for n, t in zip(logs["PLAYER_NAME"], logs["TEAM_ABBREVIATION"])}
    teams = logs.drop_duplicates("TEAM_ABBREVIATION").set_index("TEAM_ABBREVIATION")[["TEAM_ID", "TEAM_NAME"]]
    # v1.1: accept each TEAM separately when its player points equal its final score exactly; list the rest as gaps
    ok, gaps = set(), []
    for (game, team), g in box.groupby(["game", "team"]):
        s, fin = int(g["pts"].sum()), int(g["team_final"].iloc[0])
        if s == fin: ok.add((game, team))
        else: gaps.append(dict(date=date, game=game, team=team, players_found=len(g), pts_found=s, team_final=fin, missing_pts=fin - s)); print(f"GAP {game} {team}: player points {s} != final {fin} (missing {fin - s})")
    if gaps:
        os.makedirs("data/box/nba", exist_ok=True); pd.DataFrame(gaps).to_csv(f"data/box/nba/{date}_gaps.csv", index=False)
    rows = []
    keep = pd.Series([(g, t) in ok for g, t in zip(box["game"], box["team"])], index=box.index) & (box["min"] > 0)
    for _, r in box[keep].iterrows():
        away, home = r["game"].split("@"); opp = home if r["team"] == away else away
        k = norm_name(r["player"]); key2 = ik(r["player"], r["team"])
        pid = ids.get(k) or ids_it.get(key2) or -(int.from_bytes(k.encode(), "little") % 10**7)
        name = names_it.get(key2, r["player"])
        rows.append({"SEASON_ID": 22026, "PLAYER_ID": pid, "PLAYER_NAME": name,
                     "TEAM_ID": teams["TEAM_ID"].get(r["team"], -1), "TEAM_ABBREVIATION": r["team"], "TEAM_NAME": teams["TEAM_NAME"].get(r["team"], r["team"]),
                     "GAME_ID": f"cloud-{date}-{r['game']}", "GAME_DATE": date,
                     "MATCHUP": f"{r['team']} {'@' if r['team'] == away else 'vs.'} {opp}", "WL": None, "MIN": r["min"],
                     "FG3M": r["fg3m"], "FG3A": r["fg3a"], "OREB": r["oreb"], "DREB": r["dreb"], "REB": r["reb"], "AST": r["ast"],
                     "STL": r["stl"], "BLK": r["blk"], "TOV": r["tov"], "PTS": r["pts"], "VIDEO_AVAILABLE": -1})
    if rows:
        pd.concat([logs, pd.DataFrame(rows)], ignore_index=True).to_csv(LOG, index=False)
    print(f"{date}: appended {len(rows)} player rows for {len(ok)} teams; {len(gaps)} team gaps -> data/box/nba/{date}_gaps.csv")

if __name__ == "__main__":
    main(sys.argv[1])
