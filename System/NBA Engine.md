---
tags: [system, engine, nba]
version: v1
updated: 2026-10-23
code: engine/nba/
status: built and tested on synthetic leagues; awaiting first real-data run + backtest on your PC
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

## Known limits (v1)
- No position or matchup data yet (rebounds don't know who guards whom); no referee or rest effects. All of it is deliberately left out until the backtest shows the base is calibrated.
- 3PM is modeled as a rate, not 3PA × shrunk 3P% (v2).
- Name matching is by normalized name. Mismatches show up in the summary's "no projection" list.
