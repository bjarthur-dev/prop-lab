---
tags: [system, engine, nba]
version: v1.4
updated: 2026-10-23
code: engine/nba/
status: real-data backtest done (2025-26); calibrated v1.3; paper/watch only until CLV record builds
---

# NBA Engine v1

Takes [[Upgrade Roadmap]] #8 from "nothing" to a working, tested engine. **Code does the math; the Scout's files are the inputs; [[Rules]] makes the decisions.**

## How a projection is built
1. **Minutes:** a recency-weighted average of this season's minutes (half-life 6 games), anchored by last season's average (worth 4 games). With no game yet this season, last season × 0.9. Caps from coach or beat-reporter quotes go in `engine/out/DATE/min_caps.csv` (e.g. Zach Collins 16).
2. **OUT players are removed** (OUT + Doubtful from the official report; updates from Job C R6). Their minutes go to the remaining rotation, normalized to 241 team minutes, max 38 per player.
3. **Blowout risk:** past a 6-point spread, starters (28+ min) lose 0.25 min per extra point and the bench absorbs it.
4. **Per-minute rates** for points, rebounds, assists and threes: recency-weighted over both seasons (half-life 40 games, last season at 0.7×) and shrunk toward the league rate (worth 100–300 minutes).
5. **Market anchoring:** each team's projected points are scaled to the **implied team total** from the spread and total (clipped 0.8–1.25). Pace, opponent defense and the market's own read of the injuries come in this way. Assists scale with it (^0.8); rebounds scale with the game total.
6. **Joint simulation:** one minutes draw per simulation drives every stat, so points, rebounds, assists and PRA move together. Counts are negative binomial, with dispersion **fitted from the logs** each run.

## How a side is decided (code version of [[Rules]] §3)
Two ways to qualify, and both must pass the **blend check**: market-weighted (0.75) p beats break-even by ≥ 2 pts.
- **Path A, model edge:** shrunk edge ≥ 3, model beats the sharp consensus by 3–10 pts. **More than 10 pts = WATCH:** a disagreement that big with sharp books usually means we're missing information.
- **Path B, stale price:** consensus of the *other* books (≥ 2) beats our book's break-even by ≥ 2.5 pts, and the model doesn't say the side is more than 3 pts below break-even.
- **Decisions:**
  - **PAPER/BET:** staked, under [[Rules]] §2 caps.
  - **WATCH:** tracked, no stake.
  - **PASS.**

## Test results (synthetic leagues with known truth, 7 seeds)
- Rates recovered within **4–7%**; projected points MAE **0.7–0.85**; calibration-in-the-large **0.2–1.2 pts**.
- **Fair-priced board: 0 false bets on 6 seeds, 1 on 1 seed.** Before the blend and 10-pt guards this was 2–3 per 40 sides, which would have meant ~15 fake bets on a 300-side night. Those two guards came out of this test.
- A planted stale price (+150 vs three fair books) was **caught on every seed**.
- What the synthetic test can't prove: real role changes, real injuries, real market sharpness. **That's what the backtest is for.**

## Run it (Windows)
1. **Once:** install Python 3.11+ (tick "Add to PATH"), then double-click `engine/setup_windows.bat`. It installs packages, runs the tests, pulls 2025-26 and 2026-27 logs (`nba_api`), and writes `engine/out/backtest_report.txt`. **Send me that report**; it's how we tune the half-lives and shrinkage on real data.
2. **Daily:** after the Scout's Job C file is in `Inbox/Perplexity/`, double-click `engine/run_nba_slate.bat` and enter the date. Output: `engine/out/DATE/summary.md` (+ `candidates.csv`, `projections.csv`).
3. Until your PC runs it on a schedule, the same files can be run by Claude whenever the logs are in the vault.

## v1.1 fixes (2026-10-23, from the advanced-mechanisms research)
- **Blowout rule no longer undone.** The starter→bench transfer now happens *after* normalizing to 241 minutes and is zero-sum. Test: at −9.5 a star loses 0.88 min (rule: 0.875). Before the fix: 0.26.
- **Vacated minutes go to the replacement, not the stars.** Bench players absorb first (weight 1.0 vs starters 0.2); starters can rise at most +2 min. With positions (`engine/data/positions.csv`, pulled by `fetch.py`), 70% of an OUT player's minutes go to same-position bench players. Test: starting C out → backup C 18 → 30 min, star +1.3. Before: backup +2.6, stars to the 38 cap.
- **`min_set.csv`** (player, minutes) for Scout-confirmed replacement starters, alongside `min_caps.csv`.
- Tests: `engine/nba/tests/test_minutes.py` (new) + `test_synthetic.py` (still passes).

## v1.2 (2026-10-23): threes = attempts × padded 3P%
- 3PA/min with light padding (100 min) × 3P% padded **240 attempts toward the player's own prior**, the prior padded **750 attempts toward league** (Medvedovsky / Blackport). Simulated as Binomial(3PA, p) with 3PA overdispersed and p uncertain (Beta, n=400).
- Synthetic test: padded 3P% lands **2.1 pts** from the truth vs **7.5 pts** for raw season-to-date 3P% (234 players). That gap is the H4 mechanism.
- Outputs `p3`, `p3_raw_cur` and `fg3a_cur` per player, which is everything needed to compute H4 triggers.

## v1.3 (2026-10-23): first real-data backtest + calibration fix
Data pulled on the laptop: 26,651 player-games (2025-26), 640 (2026-27 so far), 519 roster positions. Walk-forward backtest: 18 dates, 5,856 player-games, each projected from games *before* that date only.
- **Points:** MAE 4.97 vs naive season average 5.07 (**+1.9%**); calibrated.
- **Rebounds / assists:** mean accuracy = naive (no gain yet; v1.5's opportunity models are the fix), but v1.2 was **overconfident by ~5 pts** at p ≥ 0.55 (fitted dispersion 1.04/1.05 was too tight).
- **Fix (tuned on that backtest):** dispersion floors (reb 1.5, ast 1.35) + 10% true-rate uncertainty per simulation. Result in the 55–65% bin: reb **58.3% predicted vs 58.2% actual**, ast 59.0 vs 60.5, pts 59.4 vs 59.7. Brier improved (reb .2458 → .2446, ast .2435 → .2431). Report: `engine/out/backtest_report_v1.3.txt`.
- Meaning: probabilities are now trustworthy as probabilities. Whether they beat *the market* is a separate question that only the CLV record answers.

## v1.4 (2026-10-24): fixes found by the first live card
The first cloud card found the model leaning under on the whole board (−11 pts on overs across 213 DraftKings sides). Three bugs, all in steps the v1.3 backtest never exercised (it tested baselines, not `project_game`):
1. **Ghost players:** players with no game this season (injured, released, traded) stayed in their old team's rotation and took starters' minutes (PHI: Payne/Martin/Watford ate ~45 min; Maxey 33 → 37 after the fix). Now excluded once the team has played, unless the Scout confirms a role (`min_set`).
2. **Double-counted absences:** an OUT player's minutes were re-routed to his backups even when he'd already been missing games (DEN: Bagley/Brazile 18 → 27, Jokic cut to 28). Now only a **fresh** absence (he played the team's last game) is routed, and trimming a team above 241 min comes mostly off the bench (`STARTER_TRIM` 0.25).
3. **Shrinkage toward the wrong average:** every player was pulled toward the all-rotation scoring rate, which inflated 10–20-min players by **14%**; the team-total scaling then cut stars. Now each player is pulled toward his **role tier** (0–12 / 12–20 / 20–28 / 28+ min). 2025-26 check (15 dates): bench points bias 1.143 → 1.042, stars 0.974 → 0.980, rebounds/assists within ±2.5% in every tier.
- **Model-health gate:** if model-minus-market on overs averages beyond ±4 pts across the board, every BET/PAPER becomes WATCH. After the fixes the lean is −7.4 (pts), −5 (reb/ast); means now sit within 0.7 pts of the lines, so the remaining gap is the **shape** of the distribution (our ranges are wide and right-skewed). That can only be settled with CLV and tracker data, not by tuning tonight.
- **Next:** backtest the full `project_game` pipeline (not just baselines) and refit the dispersion floors on live tracker outcomes.

## Next (v1.5 plan, in order, from [[Research - Advanced NBA mechanisms]])
1. ~~Threes~~ done in v1.2.
2. Usage redistribution ∝ usage^k (k ≈ 1.5–2) with an efficiency cost, replacing the uniform team factor.
3. Rebounds = DREB/OREB pools × lineup-aware share × opponent reb% (team-rebound deductions 5.6% / 25.1%).
4. Assists = potential assists × receivers' expected conversion (fixes: shooter out should *lower* a passer's assists).
5. Final-margin draw per simulation with coach pull curves, OT and late-FT branches (replaces the linear blowout rule).
6. Opponent 3PA-rate and rim-frequency indices (regressed 40%); ignore opponent 3P% allowed.

## Known limits (v1)
- No position or matchup data yet (rebounds don't know who guards whom); no referee or rest effects. All of it is deliberately left out until the backtest shows the base is calibrated.
- 3PM is modeled as a rate, not 3PA × shrunk 3P% (v2).
- Name matching is by normalized name. Mismatches show up in the summary's "no projection" list.
