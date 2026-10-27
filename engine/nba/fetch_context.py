"""Matchup-context data from stats.nba.com (runs on the LAPTOP: stats.nba.com blocks cloud runners).
Pulls the "why" data the cards need: shot zones (player offense, team defense allowed), play types (Synergy: P&R,
iso, spot-up, post... offense and defense), tracking (drives, catch-and-shoot, pull-ups, passing, rebounding chances,
touches), defense (overall + rim + 3PT defended FG%), advanced/usage/four-factors/opponent team stats, hustle,
player-vs-defender matchups, and on/off splits for every team.

    python engine/nba/fetch_context.py              -> current season (refresh daily)
    python engine/nba/fetch_context.py 2025-26      -> any season (prior season once, for baselines)

Writes engine/data/context/<season>/<name>.csv. Every call is independent: a failure is logged and skipped."""
import os, sys, time, traceback
import pandas as pd

SEASON = sys.argv[1] if len(sys.argv) > 1 else "2026-27"
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "context", SEASON)
os.makedirs(OUT, exist_ok=True)
log = []

def flat(df):
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ["_".join(str(x) for x in c if str(x) and not str(x).startswith("Unnamed")).strip("_") for c in df.columns]
    return df

def get(name, fn, idx=0, **kw):
    path = os.path.join(OUT, f"{name}.csv")
    for attempt in range(3):
        try:
            obj = fn(timeout=60, **kw)
            frames = obj.get_data_frames()
            df = flat(frames[idx]) if frames else pd.DataFrame()
            df.to_csv(path, index=False)
            log.append(f"ok   {name}: {len(df)} rows"); print(log[-1])
            time.sleep(1.2); return df
        except Exception as e:
            msg = str(e).splitlines()[0][:160]
            print(f"retry {attempt+1} {name}: {msg}"); time.sleep(4 * (attempt + 1))
    log.append(f"FAIL {name}"); print(log[-1]); return None

def main():
    from nba_api.stats import endpoints as E
    S = dict(season=SEASON)
    # 1. shot zones: where each player shoots / what each defense allows, by zone
    get("player_shot_zones", E.leaguedashplayershotlocations.LeagueDashPlayerShotLocations, distance_range="By Zone", **S)
    get("team_shot_zones_allowed", E.leaguedashteamshotlocations.LeagueDashTeamShotLocations, distance_range="By Zone",
        measure_type_simple="Opponent", **S)
    # 2. team context: pace/ratings, opponent stats, four factors, defense
    for m in ["Advanced", "Opponent", "Four Factors", "Defense", "Misc"]:
        get(f"team_{m.lower().replace(' ', '_')}", E.leaguedashteamstats.LeagueDashTeamStats,
            measure_type_detailed_defense=m, per_mode_detailed="PerGame", **S)
    # 3. player context: usage / advanced / scoring breakdown
    for m in ["Usage", "Advanced", "Scoring", "Misc"]:
        get(f"player_{m.lower()}", E.leaguedashplayerstats.LeagueDashPlayerStats,
            measure_type_detailed_defense=m, per_mode_detailed="PerGame", **S)
    # 4. tracking: how each player gets his stats (and what teams allow via team tracking)
    for pt in ["Drives", "CatchShoot", "PullUpShot", "Passing", "Rebounding", "Possessions", "PaintTouch", "PostTouch",
               "ElbowTouch", "SpeedDistance", "Efficiency", "Defense"]:
        get(f"player_track_{pt.lower()}", E.leaguedashptstats.LeagueDashPtStats, pt_measure_type=pt,
            player_or_team="Player", per_mode_simple="PerGame", **S)
    for pt in ["Rebounding", "Drives", "CatchShoot", "Passing"]:
        get(f"team_track_{pt.lower()}", E.leaguedashptstats.LeagueDashPtStats, pt_measure_type=pt,
            player_or_team="Team", per_mode_simple="PerGame", **S)
    # 5. defense: defended FG% overall / at the rim / on threes (player and team)
    for cat in ["Overall", "3 Pointers", "Less Than 6Ft", "Greater Than 15Ft"]:
        k = cat.lower().replace(" ", "_")
        get(f"player_defend_{k}", E.leaguedashptdefend.LeagueDashPtDefend, defense_category=cat, per_mode_simple="PerGame", **S)
        get(f"team_defend_{k}", E.leaguedashptteamdefend.LeagueDashPtTeamDefend, defense_category=cat, per_mode_simple="PerGame", **S)
    # 6. play types (Synergy): offense for players/teams, defense allowed by teams
    for pt in ["PRBallHandler", "PRRollman", "Isolation", "Spotup", "Transition", "Postup", "Handoff", "Cut",
               "OffScreen", "OffRebound", "Misc"]:
        get(f"player_playtype_{pt.lower()}", E.synergyplaytypes.SynergyPlayTypes, play_type_nullable=pt,
            player_or_team_abbreviation="P", type_grouping_nullable="offensive", per_mode_simple="PerGame",
            season_type_all_star="Regular Season", **S)
        get(f"team_playtype_def_{pt.lower()}", E.synergyplaytypes.SynergyPlayTypes, play_type_nullable=pt,
            player_or_team_abbreviation="T", type_grouping_nullable="defensive", per_mode_simple="PerGame",
            season_type_all_star="Regular Season", **S)
    # 7. hustle (contests, deflections, box-outs)
    get("player_hustle", E.leaguehustlestatsplayer.LeagueHustleStatsPlayer, per_mode_time="PerGame", **S)
    get("team_hustle", E.leaguehustlestatsteam.LeagueHustleStatsTeam, per_mode_time="PerGame", **S)
    # 8. who guards whom: offensive player vs defender, partial possessions (season to date)
    get("matchups", E.leagueseasonmatchups.LeagueSeasonMatchups, per_mode_simple="Totals", **S)
    # 9. on/off: how each team (and each player's teammates) changes with a player on vs off the floor
    from nba_api.stats.static import teams
    frames_on, frames_off = [], []
    for t in teams.get_teams():
        for attempt in range(3):
            try:
                o = E.teamplayeronoffsummary.TeamPlayerOnOffSummary(team_id=t["id"], measure_type_detailed_defense="Advanced",
                                                                    timeout=60, **S).get_data_frames()
                on, off = o[1].assign(TEAM=t["abbreviation"]), o[2].assign(TEAM=t["abbreviation"])
                frames_on.append(on); frames_off.append(off); break
            except Exception as e:
                print(f"retry onoff {t['abbreviation']}: {str(e)[:120]}"); time.sleep(4 * (attempt + 1))
        time.sleep(1.2)
    if frames_on:
        pd.concat(frames_on).to_csv(os.path.join(OUT, "onoff_on.csv"), index=False)
        pd.concat(frames_off).to_csv(os.path.join(OUT, "onoff_off.csv"), index=False)
        log.append(f"ok   onoff: {len(frames_on)} teams")
    with open(os.path.join(OUT, "_log.txt"), "w") as f:
        f.write(time.strftime("%Y-%m-%d %H:%M") + "\n" + "\n".join(log) + "\n")
    fails = [l for l in log if l.startswith("FAIL")]
    print(f"\n{len(log) - len(fails)} ok, {len(fails)} failed -> {OUT}")

if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc(); sys.exit(1)
