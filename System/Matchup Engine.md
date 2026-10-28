---
tags: [system, engine, nba, matchup]
version: v1
updated: 2026-10-27
code: engine/nba/matchup.py, engine/nba/fetch_context.py
---

# Matchup Engine v1: the "why" layer

The user's standard: every stat has a reason. Find the reasons (role, shot diet, scheme, defenders, pace, who's out), project from them, and look at the line **last**.

## Data (laptop → GitHub)
`engine\update_nba_context.bat` runs `fetch_context.py`, which pulls 61 stats.nba.com tables per season into `engine/data/context/<season>/`:
- shot zones (player offense, team defense allowed)
- Synergy play types (offense and defense)
- tracking: drives, catch-and-shoot, pull-ups, passing / potential assists, rebound chances, touches, post / elbow / paint
- defended FG% (overall, rim, 3PT)
- hustle
- player-vs-defender matchups
- on/off for all 30 teams
- team advanced / opponent / four factors

**Run it daily** (about 5 min after the first run). stats.nba.com blocks the cloud, so only the laptop can run it.

## What `matchup.py DATE "Player"` prints
1. **Role:** minutes, usage, touches, time of possession, and how he creates (drives, pull-ups, catch-and-shoot, post).
2. **Shot diet vs this defense:** per-game FGA by zone × what the opponent allows in that zone vs league (½ of the deviation counted as real).
3. **Play types:** his top 3 Synergy play types × this defense's PPP allowed in them.
4. **Environment:** pace (both teams + market total), defensive rating, FTA allowed, rim / 3PT defended FG% vs expected.
5. **Boards / assists:** rebound pool (both teams' misses), opponent crash rate, potential assists × opponent FG% allowed (conversion).
6. **Defenders on this roster who have guarded him:** minutes, points, FG, and their defended FG% vs expected.
7. **Context projection** for PTS / REB / AST / 3PM, with P(over) at the sharp line next to the market's fair %. A gap of ≥ 8 pts is flagged **"explain it"**: either we know something (minutes change, scheme, absence) or the projection is missing it.

`--save` logs every projection to `data/shadow/matchup/DATE.csv` so the morning grading can test it. **It is not trusted until graded:** 200+ props where the context disagrees with the market by ≥ 8 pts must beat the market's Brier score.

## v1.1 (same night)
- **Who's out:** `--out "Name,Name"` (or engine/out/DATE/outs.csv). For each absent regular it compares the player's past games with vs without him: minutes shift shrunk n/(n+5), per-minute rates shrunk n/(n+20), and no double count when his recent games were already without him.
- **Skew:** P(over) now uses a negative binomial with the player's own spread plus ~4 min of minutes uncertainty. A normal around the mean had overstated every over by ~9 pts.
- **Slate lean:** the engine still sits ~+3 to +5 pts over the market on the first slate, because base rates run above the lines. `--slate` reports that lean and ranks **relative** disagreements (gap minus the lean), starters only (24+ min). The shadow grading will fit a proper level correction.
- **Lesson from the first slate:** the biggest disagreements were bench guards (Daniss Jenkins 8.5 pts → engine 15) driven by *who's out* inputs (Ausar Thompson questionable was passed as OUT). Minutes and availability decide most props; the zone and play-type matchup moves a projection by about ±1 point. **A gap built on an uncertain availability is not a pick.**

## Known limits (v1)
- Minutes come from recent games. It doesn't yet know about a new starter or a teammate who is out: use `opportunity.py` (vacated usage, with/without splits) alongside it.
- Early season: 3–4 games, shrunk toward last season (player k = 8, team k = 10). Roster changes make last season's team defense a weak prior.
- Defensive scheme (drop vs switch, double-team rate) is inferred from zone / play-type allowed, not measured directly.
- No in-game coaching adjustments.
