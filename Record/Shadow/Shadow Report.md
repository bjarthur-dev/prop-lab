---
tags: [record, shadow]
---

# Shadow grading: every priced prop vs result and market

Written by `engine/shadow.py` (morning settlement runs it). Rules §9 uses this to decide when the model-health gate relaxes and when NFL/MLB go live.

## NBA
Graded props: **282** over 2 day(s). Over hit rate 0.493 vs market's average 0.492 vs model's 0.434.
Brier: model 0.2488 · market 0.2410 · blend 0.2303 → **model skill vs market -3.2%**, blend skill +4.4% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| ast | 76 | 0.526 | 0.492 | 0.437 | -3.7% |
| pts | 105 | 0.495 | 0.500 | 0.435 | -5.0% |
| reb | 101 | 0.465 | 0.483 | 0.432 | -1.1% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 28 | 0.259 | 0.429 | 0.483 |
| (0.3, 0.4] | 69 | 0.355 | 0.449 | 0.478 |
| (0.4, 0.5] | 124 | 0.452 | 0.468 | 0.489 |
| (0.5, 0.6] | 48 | 0.545 | 0.583 | 0.511 |
| (0.6, 0.7] | 10 | 0.639 | 0.800 | 0.549 |
| (0.7, 1.0] | 3 | 0.725 | 0.667 | 0.514 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 82 | 0.451 | 0.493 | -4.2 pts |
| (-0.1, -0.05] | 68 | 0.529 | 0.495 | +3.5 pts |
| (-0.05, 0.0] | 61 | 0.459 | 0.495 | -3.6 pts |
| (0.0, 0.05] | 43 | 0.535 | 0.485 | +5.0 pts |
| (0.05, 0.1] | 17 | 0.529 | 0.490 | +3.9 pts |
| (0.1, 1.0] | 11 | 0.545 | 0.471 | +7.4 pts |

Noise check: with 282 props one standard error on a hit rate is about ±3.0 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.
