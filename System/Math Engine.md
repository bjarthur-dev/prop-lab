# prop-engine — the Section 11 probability engine

The companion tool to the player-prop guide: **the LLM researches context, this code does the math.** Every number it produces is auditable, and the guide's own verified examples are baked in as tests.

## What it is (and is not)

An optional arithmetic and paper-testing prototype. It computes what happens **if** your probability estimates are right — devig, distribution pricing, EV, Kelly sizing, pick'em payouts, and a bet log that tracks closing lines, two separate CLV diagnostics, calibration, and Brier score. It does **not** produce the probabilities: those come from your modeling (guide Sections 4-6) and the AI-research layer (Section 11). It does not generate calibrated player projections, and nothing here establishes suitability for real-money sizing — that is what the paper-trading record is for.

Scope of the bet log: sportsbook singles and fixed all-correct entries (including pick'em/parlay tickets by payout multiplier). Flex/partial-payout entries can be recorded with an explicit `--profit` override, but the report's calibration treats the logged result as the modeled event's outcome — evaluate flex entries with `pickem_flex_ev` in the library instead. Paper and live records are reported separately; passes are logged as part of your discipline record.

## Quick start

```bash
python3 tests.py        # all guide-verified numbers must pass before anything else
```

## Core usage

### 1. Devig a market to find the fair probability

```python
from prop_engine import devig, implied_prob

# -110/-110 market: both sides 52.38% -> overround 4.76%
p_over, p_under = devig(-110, -110)

# lopsided market: use power or shin
p_over, p_under = devig(-140, +105, method="shin")
```

### 2. Price a prop from a forecast (pick the right distribution)

```python
from prop_engine import PropForecast, poisson_over, binomial_over

# MLB hits, projected mean 1.35 (guide 4.3): over 0.5 = 74.1%, over 1.5 = 39.1%
hits = PropForecast(kind="poisson", mean=1.35)
hits.p_over(0.5)   # 0.7410

# cleaner: hits in N plate appearances (binomial, PA uncertainty on top)
binomial_over(n=4, p_hit=0.31, line=0.5)   # over 0.5 hits in 4 PAs

# NFL/NBA yards & points: normal, mean + SD from your simulation
yds = PropForecast(kind="normal", mean=62.0, sd=28.0)
yds.p_over(65.5)

# correlated combos (HRR): NEVER Poisson — negative binomial (guide 3.1)
PropForecast(kind="negbin", mean=1.5, vmr=2.06).p_over(1.5)
```

Distribution rules of thumb (guide 3.1 — candidates to test, not defaults):
- **Normal** — high-volume continuous stats (receiving yards, star points)
- **Poisson** — low-volume counts, variance ≈ mean (VMR ≤ ~1.3)
- **Binomial / Poisson-binomial** — successes in a known number of trials (hits in N PAs, catches on N targets)
- **Negative binomial** — overdispersed counts (VMR > 1.3), e.g., HRR, clustered outcomes
- **Simulation** — anything with dependent components (same-game legs)

### 3. EV and sizing

```python
from prop_engine import ev, ev_settlement, kelly, boost_decimal, ev_parlay

ev(0.55, -110)                      # +5.0%
ev_settlement(0.575, 0.425, -118)   # +6.2% (p_win + p_loss = 1 here; add a void slice by scaling both down)
kelly(0.575, -118, fraction=0.25, cap=0.01)   # 1.84% -> capped at 1%

# parlays: only under independence + multiplicative pricing (guide 16.1)
ev_parlay([0.55, 0.55, 0.55, 0.55], [-110]*4)    # four legs -> +21.55%
ev_parlay([0.70]*6, [-250]*6)                     # six -250 legs -> -11.4%
```

**Parlay rule:** a leg may enter only if you would bet it as a single at that price. Same-game legs need a shared simulation, not multiplication.

### 4. Pick'em apps (Pick6 / PrizePicks / Underdog — guide 16.9)

```python
from prop_engine import pickem_leg_break_even, ev_pickem_from_legs, pickem_flex_ev

pickem_leg_break_even(37.5, 6)      # 54.7% per leg required on a 6-pick 37.5x
ev_pickem_from_legs([0.55]*6, 37.5)  # +3.8% (vs +34% at -110 parlay pricing)
pickem_flex_ev([0.55]*3, {3: 3.0, 2: 1.0})   # 3-pick flex enumeration
```

Remember: pick'em pricing doesn't move with betting money the way sportsbook odds do, but the per-leg break-even is higher (~55-58% vs 52.4% at -110) — whether the softer lines outweigh it is an empirical question for your logs.

### 5. The bet log — where the method becomes science

```bash
# log a paper bet (virtual 10-unit stake) the moment you make the call
python3 bet_log.py add --date 2026-10-23 --sport NBA --player "Jalen Brunson" \
    --market points --line 26.5 --selection over --book DraftKings --odds -118 \
    --odds-ts "2026-10-23T18:32Z" --model-prob 0.575 --decision paper

# after the game: settle by outcome, with BOTH closing sides, the closing
# threshold, and the closing snapshot timestamp (CLV needs all of them)
python3 bet_log.py settle 1 win --close-odds -110 --close-odds-opp -102 \
    --close-line 26.5 --close-ts "2026-10-23T19:05Z"

# the record: separate paper/live ROI, two CLV diagnostics, calibration, Brier
python3 bet_log.py report
```

The log is the whole game (guide Sections 12 and 17.5): log **passes too**, log every override with its reason and timestamp, and let calibration + CLV + a large logged ROI sample — not any hot streak — decide whether the system is real.

## The daily workflow (guide 11.4)

1. **Morning:** pull slate + odds; run forecasts; devig a sharp book; compute EV on every prop and alternate; log candidates.
2. **News window:** on injury/lineup news, re-run with updated availability; compare against prices that haven't moved yet.
3. **Final check:** re-devig, line-shop, size with fractional Kelly under the cap, log with odds timestamp.
4. **Always:** settle with the closing line; read the report before changing anything.

## Files

- `prop_engine.py` — the math (odds, devig, distributions, EV, Kelly, pick'em)
- `bet_log.py` — CLI bet log + validation report (ROI, CLV, calibration, Brier)
- `tests.py` — selected arithmetic examples and known mathematical cases, asserted (independent oracles, not guide-copied numbers where avoidable)
- `bets.csv` — your record (starts empty; the first row is the start of your out-of-sample test)
