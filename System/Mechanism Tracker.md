---
tags: [system, tracker]
version: v2
updated: 2026-10-23
data: Record/mechanism_tracker.csv
grader: engine/tracker.py
evidence: "[[Research - Advanced NBA mechanisms]]"
---

# Mechanism Tracker v2 — how we test prop theories with zero money

Every theory gets **frozen before tip-off** (definition, price, timestamp) and graded against the market's own devigged probability. The question is never "did it hit?", it's **did it beat its matched control by more than the noise?**

## The test
- **edge** = hit rate − average p_market for the theory's entries.
- **control** = the same calculation for a matched control arm: **same side, same stat, price within ±10 cents, same night, no mechanism.**
- **net = edge − control edge.** Clustered by game (two entries from one game are not two independent tests).
- Until a theory has controls, the grader subtracts the documented side bias instead: **unders +1.5 pts, overs −1.5 pts** (SickFade, 396k NBA props at close: unders −3.4% ROI vs overs −9.2%). Otherwise an under theory gets credit for "unders lose less".
- **Noise floor:** about ±4 pts at 150 entries. A real 5-pt edge needs about 400 entries, and a 3-pt edge about 1,100. **No theory graduates to the engine before ~400 entries and net > 2 SE.**
- Also log `p_model` (engine) and the closing price when available. CLV and log-loss vs close converge much faster than hit rate.

## The theories (pre-registrable definitions)
| ID | Theory | Trigger (computed in the morning, frozen before tip) | Side | Evidence grade |
|---|---|---|---|---|
| **H1a** | Vacated usage → main creator | The **single highest-usage remaining creator** on a team missing ≥ 1 starter (≥ 15% team usage). Log minutes since the news broke. | PTS over | Usage concentrates in creators (sourced); efficiency costs −0.8 to −1.7 ORtg per +1 USG (sourced); the market prices news within ~15 s at books (sourced), so the edge, if any, is staleness |
| **H1b** | Vacated usage → other beneficiaries | Every other projected beneficiary in the same games | PTS over | Weaker: absorbed usage costs efficiency |
| **H2** | Replacement center → rebounds | **Confirmed start** + projected minutes ≥ season average + 8; log the co-big's status | REB over | Lineup-dependent rebounding (sourced) |
| **H3** | Blowout minutes | **Spread ≥ 10 only** (7.5–9.5 is worth ~2 pts of probability and likely priced); later split by coach pull-speed tercile | PTS under | Weak: one dated trend study, "very marginal" |
| **H4** | 3P% regression | Season or last-15 3P% ≥ padded expectation + 6 pts on ≥ 40 3PA, with 3PA/min and minutes stable (±10%); line ≥ 1.5 | 3PM under (mirror: cold → over) | Shooting luck is real (sourced); market overreaction untested |
| **H5** | Assist conversion luck | Last-10 AST − PotAST × expected conversion ≤ −1.0/game, PotAST/min stable | AST over (mirror ≥ +1.0 → under) | Data sourced; regression inferred |
| **H6** | Opponent rebounding environment | Center with REB line ≥ 8.5 vs a top-5 opponent in regressed OREB% | REB under (mirror: weak DREB opp → over) | Opponent reb% matters more than misses (sourced) |
| **H7** | Co-big out (less cannibalization) | Team's other big (≥ 15% DREB share, ≥ 20 MPG) OUT; remaining big's minutes rise ≤ 4 (isolates share, not minutes) | REB over | Cannibalization measured (sourced) |
| **H8** | Opponent 3PA rate allowed | Shooter ≥ 6 3PA/g vs a top-5 opponent in regressed 3PA-rate-allowed index | 3PM over (mirror → under) | Defenses control 3PA, not 3P% (sourced) |
| **P1** | Placebo: DvP tables | Bottom-5 raw DvP vs position, but H6/H8 indices neutral | Over | Expected to fail; proves DvP adds nothing |

**H4–H8 and P1 triggers are computed by code** (engine data: nba_api tracking endpoints), not by an LLM. Until the PC data pull is running, only H1–H3 can be logged.

## Daily routine
1. The Scout's Job C includes a **broad board** (see [[Perplexity Prompt]]), so controls can be picked from players with no mechanism.
2. Claude freezes theory entries plus one control each in `Record/mechanism_tracker.csv` before the first tip.
3. Job A next morning pulls the stat lines. Claude fills in `actual`/`hit` and runs `python engine/tracker.py`.
4. Weekly: running table into [[Market Intel]].

## 2026-10-23 (first night) caveats
15 entries: H1a ×5, H1b ×2, H2 ×3, H3-legacy ×5. **No controls** (the board only covered teams with mechanisms), so they're graded against the side-bias prior. The H2 confirmed-start rule wasn't checked. H3 entries are below the new 10-point threshold and are kept as "legacy" for the record only.
