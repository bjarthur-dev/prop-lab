---
tags: [system, engine, nfl]
version: v1
updated: 2026-10-23
code: engine/nfl/
status: built + sanity-tested; PAPER/WATCH only until a 2023-25 nflverse backtest exists
---

# NFL Engine v1

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
- 7-pt underdog throws **+3.9** more passes than a 7-pt favorite (sourced slope ≈ +0.5 pp per point).
- WR1 receiving yards: mean 66.7 > median 60.4 (skew); RB receiving: mean 17.6 vs median 12.5. That gap is the N1/N2 under mechanism.
- RB1 at 26 implied points, 60% inside-10 share: **P(ATD) 54%** (research worked example: 55%).

## Run it
`python engine/nfl/run_nfl.py 2026-10-25` with three CSVs in `engine/out/DATE/`: `nfl_games.csv`, `nfl_shares.csv`, `nfl_board.csv` (columns in the script header). Claude builds them from the Scout's Job files until nflverse data runs on the PC.

## Known limits (v1) / next
- Shares are inputs (Scout or nflverse), not yet estimated from routes/TPRR. Next: nflverse pbp → target share per dropback, carry share, inside-10 share, shrunk toward 2025.
- Pass attempts run slightly low (~31–35); refit plays/pass rate on 2023–25.
- No coverage-shell multiplier (sourced effect only ±1–3%), no QB sack/scramble splits yet, no injury route re-solve.
