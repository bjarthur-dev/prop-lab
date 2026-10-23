---
tags: [system, rules]
version: 1
updated: 2026-10-23
---

# Rules — the single source of constants

> **This file wins.** If any other note (Guide, Daily Workflow, Master Prompts, Market Intel) gives a different number, this file is correct and the other note is stale. Change a rule only here, and log why in the changelog at the bottom.

Background for every number: [[Research - Upgrade Report]]. Items marked *(heuristic)* are reasoned starting points, not validated findings, so tune them from your own record.

## 1. Sizing
- **Unit = 1% of current bankroll** for paper and live. On $100 that's $1, not $10.
- Kelly is only a ceiling: quarter-Kelly on the **shrunk** edge (§3), capped at 1%. Take whichever is smaller.
- Pick'em slips: Power 0.25–0.5%, Flex 0.5–1% per entry *(heuristic)*.
- Re-size after each settlement window (early games settle → recompute on the new bankroll).

## 2. Exposure caps (hard)
| Cap | Limit |
|---|---|
| Per bet | 1% |
| Per game (all singles + slips touching it) | 3% |
| Per player (all props + slips) | 1.5–2% |
| Positions per game | ≤ 2 straight bets |
| Per slate | by class, see [[Slate Playbook]] (micro 3–5% → large 10–20%) |

- **Never hold singles plus an SGP made of the same legs.** Pick one expression of the thesis.
- A same-game cluster counts as **one bet** for exposure.

## 3. The pass rule (enforce before logging)
A leg is a **BET** only if all of these hold:
1. The price is **executable**: a real book, app or exchange you can actually bet into, at the timestamped price. Media and aggregator quotes (SBD, StatMuse, Covers, Action) are *reference only*.
2. **Shrunk edge ≥ 3 percentage points** over break-even. Shrunk edge = 0.3–0.5 × (p_model − break-even) until CLV data justifies more *(heuristic: the winner's-curse simulation implied a shrinkage of about 0.31)*.
3. The model probability beats the devigged sharp price by **≥ 3 pts**. If there's no sharp two-way market, the bet is PAPER at most.
4. No thesis built on: head-to-head history, last 1–5 games, ATS/quarter trends, or an affiliate site's pick.
5. **SGP or parlay:** only with an actual quoted payout and timestamp. Never log "product pricing".

6. **Blend check:** the market-weighted (0.75) probability must beat break-even by **≥ 2 pts**.
7. **Too-good-to-be-true check:** if the model disagrees with the sharp consensus by **> 10 pts**, it's WATCH (investigate missing info), never a bet.
8. **Stale-price path:** a side also qualifies if ≥ 2 *other* books' devigged consensus beats our break-even by ≥ 2.5 pts, the model doesn't say it's > 3 pts below break-even, and check 6 passes.

Anything else → **WATCH** (tracked, no stake) or **PASS**. Log all three. Items 6–8 came from the synthetic test of [[NBA Engine]] (2026-10-23), where they cut fake edges on fair lines from ~6% of sides to ~0.

## 4. Allowed price sources
| Use | Sources |
|---|---|
| Sharp reference (devig) | FanDuel, Caesars, Pinnacle, Circa, Kalshi/Polymarket mid (with depth) |
| Executable | Any regulated book or app you actually hold an account at |
| Never a benchmark | Media sites, one-way FanDuel props, stale quotes, markets with hold > ~10% |

- Treat DraftKings, Caesars and MGM as possibly **one source** when building a consensus (they reportedly share a price feed).
- Devig method: multiplicative for ~4–5% hold; power or worst-case for lopsided or high-hold markets.

## 5. Prediction markets & pick'em
- Price = **ask** + **live fee from the order ticket**. The fee schedule is unresolved: one source says Feb 18 2026 (~0.75% effective), another says 5%·P(1−P) for Polymarket US from Jul 1 2026. Check the ticket.
- Polymarket player props: **DNP resolves "No"** (a loss, not a void). Count that in p.
- Integer lines (6+) = over **5.5**. Log the half-point equivalent.
- Pick'em break-even comes from the multiplier **shown on the actual entry**. Reference: PP 6-Flex 54.2%, 6-Power 54.7%, 3-Power 58.5%, 2-Power 57.7%; Underdog 3-pick 6x 55.0%.
- All the apps need ≥ 2 teams. On a 1-game slate every leg is correlated: stack in the script direction on purpose, or skip.

## 6. Logging (every row)
Required fields: `p_model`, `p_market`, `p_market_method`, `market_source`, `executable`, `quoted`, `dist`, `mu`, `sd_or_vmr`, `game_id`, `corr_group`, `reason_code`, `minutes_to_start`, `slate_class`, `dnp_rule`, `model_version`, `run_id`.
Reject the row if `odds_ts > logged_at` or `logged_at > start_time`.

## 7. Blend
- Blend **parameters** (means), not probabilities.
- Market weight 0.7–0.8 to start *(heuristic)*. Refit after ~200 settled bets with stored p_model and p_market.

## 8. Measurement & graduation
- Order of truth: **CLV vs the devigged close → Brier/log-loss skill vs the close → calibration → ROI last.**
- Delete "Brier < 0.25" as a target. Any coin-flip forecaster passes it.
- Proving ROI needs ~3,900 bets for a 3% edge at −110, so CLV is the only fast signal.
- **Go live only when all hold:** 300–500 timestamped paper bets with both sides captured; mean devigged CLV ≥ +1.5–2% with t > 2 (or test-martingale wealth > 20); Brier skill vs close ≥ 0; calibration-in-the-large within ±2 pts; positive CLV in ≥ 2 independent segments; zero hallucination or integrity incidents in the last 100; ≥ 4 weeks of steady runs.
- **Kill switch:** rolling-200 CLV ≤ 0, or drawdown > 35%, sends you back to paper.

## Changelog
- 2026-10-23 v2: added §3 items 6–8 (blend ≥ 2 pts, >10-pt disagreement = WATCH, stale-price path) and the WATCH decision.
- 2026-10-23 v1: created after the 2026-10-22 audit. Supersedes the Daily Workflow "2% cap", the Guide's "Brier < 0.25" and its 300–500 ROI sample, and the probability-blend.
