---
tags: [system, engine, nfl]
version: v1.2
updated: 2026-10-24
code: engine/nfl/
status: fitted to 2023-26 nflverse pbp + walk-forward backtest (v1.1); PAPER/WATCH until CLV record builds
---

# NFL Engine v1.1

Built from [[Research - Advanced NFL and MLB mechanisms]]: **project the denominator (plays, dropbacks, carries), regress the numerator, price from the simulated distribution, never the mean.**

## Chain (one shared draw per simulation)
1. **Game state:** final margin ~ Normal(−spread, 13.5); implied team points = (total ∓ spread)/2.
2. **Plays:** 63 + 0.25 × (total − 44), SD 6.
3. **Pass rate:** 0.585 + PROE (50% this season / 50% prior) + **0.5 pp per point of spread** (underdogs throw more) − script term from the realized margin.
4. **Attempts** = dropbacks − sacks − scrambles; **rushes** = plays − dropbacks.
5. **Players:** targets ~ Binomial(attempts, Beta(target share)), catches ~ Binomial(targets, catch rate), yards = sum of per-catch gamma draws (WR 12.5 / TE 10.5 / RB 7.5 mean), longest reception = max of simulated catches. Carries ~ Binomial(rushes, Beta(carry share)); per-carry yards = core + 7% explosive tail.
6. **Anytime TD:** team TDs = implied points × 0.70 / 7, split 42% rush / 58% pass, × the player's inside-10 carry share / end-zone target share → Poisson. Benchmark against the **Kalshi mid** (yes-only books hold 25–45%).
7. **Weather:** passing-yard haircuts at ≥ 12 mph wind (−8.4%), rain (−15%); dome = none.
8. **Decision:** same guards as [[Rules]] §3 (shrunk ≥ 3, model−market 3–10 pts, blend ≥ 2). **v1 can only output PAPER/WATCH.**

## Sanity checks (`engine/nfl/tests/test_nfl.py`)
- 7-pt underdog throws **+1.8** more passes than a 7-pt favorite in the model (real data: +0.9).
- WR1 receiving yards: mean 66.7 > median 60.4 (skew); RB receiving: mean 17.6 vs median 12.5. That gap is the N1/N2 under mechanism.
- RB1 at 26 implied points, 60% inside-10 share: **P(ATD) 54%** (research worked example: 55%).

## v1.1 (2026-10-24): fitted to real data
Data on the laptop: nflverse play-by-play 2023, 2024, 2025 (285 games each) + 2026 through Week 7 TNF (94 games). `engine/nfl/calibrate.py` fits the team constants on 1,820 regular-season team-games; `engine/nfl/backtest.py` projects every player-game in 2024 wk 3 → 2026 wk 7 (37 weeks, 542 games) **from earlier games only**.

**Constants that changed (guess → fitted):**
| | v1 guess | fitted |
|---|---|---|
| plays at a 44 total | 63 + 0.25/pt | **61.3 + 0.08/pt**, SD 8 |
| final margin SD | 13.5 | **12.6** |
| base pass rate | 0.585 | **0.606** |
| pass rate per point of spread | +0.5 pp | **+0.24 pp** |
| scramble rate | 4% | **5.6%** |
| offensive TD share of points | 0.70 | **0.736** |
| rushing share of TDs | 42% | **38.5%** |
| explosive carries | 7% × 18 yds | **4.3% go 15+ (avg 24.4)** |

- **Myth check:** a 7-pt underdog throws only **+0.9** more passes than a 7-pt favorite (33.1 vs 32.3); the favorite runs **+3.5** more times. The script effect is mostly in *rushing* volume, so RB carry overs for big favorites are the cleaner side of it.
- **TD fix:** 51% of passing TDs and 23% of rushing TDs start **outside the 10**, so those are now split by overall target/carry share, not red-zone share. Plus a fitted correction λ' = 0.80·λ^0.75.
- **Variance:** target shares are steady game to game (Beta concentration 80); **carry shares swing a lot** (concentration 8). The 10/90 bands hit target after this (rush yds 11.9%/11.3%, carries 9.6%/8.1%, rec yds 8.8%/9.9%).
- **Weights:** recency half-life 3 games; last season counts **0.1 per game** (0.3 was worse for every yardage market; roles change between seasons).

**Backtest result (v1.1):**
| market | n | MAE vs naive season avg | calibration |
|---|---|---|---|
| receiving yds | 4,251 | **+5.0% better** | over own median: 50.0% pred / 50.0% actual |
| receptions | 4,251 | **+5.6% better** | ~2 pts too high on overs (39.2% vs 41.0%): lean unders at equal edge |
| rushing yds | 1,373 | +1.4% | 48.2% vs 50%: slight over bias |
| carries | 1,373 | +0.5% | 46.6% vs 46.5% |
| anytime TD | 5,103 | Brier .2004 vs .2109 base rate (5% skill) | bins within ~1–3 pts; lowest bin (13% pred) hits 16.5% |

What this proves: the engine's *probabilities* are honest and its means beat a season average. It does **not** prove it beats the market: pbp has no prop lines. That's what the CLV record and N-tracker controls are for. Report: `engine/out/nfl_backtest_report_v1.1.txt`.

## Run it (each NFL Sunday)
1. Double-click `engine/setup_nfl.bat` (or `python engine/nfl/fetch_nfl.py`) to pull the latest games.
2. `python engine/nfl/build_shares.py 2026-10-25 --season 2026 --week 7` → `engine/out/DATE/nfl_shares.csv` (329 players, all 32 teams). Put OUT players in `engine/out/DATE/nfl_out.csv` (column `player`) first; their shares go to teammates in proportion. `missed_last=True` = absent from his team's last game (byes excluded): check the injury report.
3. `nfl_games.csv` (spread, total, weather) + `nfl_board.csv` (lines from the Scout's Job C) → `python engine/nfl/run_nfl.py DATE`.
Names: pbp uses "J.Chase" style; build_shares matches full names by first initial + last name.

## v1.2 (2026-10-25): availability + name fixes from the first NFL Sunday card
- **Stale players dropped:** a player who missed his team's last 2+ games and has **no props today** is treated as unavailable (IR/injured) and removed, without redistributing his share (teammates' recent shares already reflect his absence). Example: De'Von Achane (IR since Week 3) had kept 56% of MIA carries, which made Ollie Gordon look like a 39-pt under.
- **Returning players added:** a player with props today but no 2026 game yet (back from injury) is added at 80% of last season's share, and teammates are scaled down to make room. Example: Josh Jacobs (GB) 51% of carries; Strong/Lloyd reduced. Uses `data/odds/nfl/DATE/board_*.csv` automatically (or `--board`).
- **OUT redistribution only for fresh absences** (he played the team's last game), same rule as NBA v1.4.
- **Name collisions fixed:** `run_nfl.py` keys players by `short|TEAM` and resolves board names (full names + the board's `game` column) to a unique player (Malik Washington MIA ≠ Mike Washington LV).
- **Shadow grading for NFL:** `engine/shadow.py` grades `data/shadow/nfl/` from play-by-play once the results Action refreshes it (Mon/Tue/Fri).
- **Known:** the NFL model leans under on yardage overs too (−5 to −6 pts vs market on Oct 25), the same distribution-shape issue as NBA; shadow grading will measure and correct it.

## Known limits (v1) / next
- Shares come from targets/carries, not routes (no TPRR/participation data yet). Injury redistribution is proportional, not role-aware (v1.2: route-tree / same-position routing like NBA v1.1).
- Backtest conditions on the player appearing; it can't see snap limits or in-game injuries, so live bands should be slightly wider.
- TE vs WR not separated (no roster join yet): per-catch yards come from each player's own padded average.
- No coverage-shell multiplier (sourced effect only ±1–3%), no QB sack/scramble splits yet, no injury route re-solve.
