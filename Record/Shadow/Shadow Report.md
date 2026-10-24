---
tags: [record, shadow]
---

# Shadow grading: every priced prop vs result and market

Written by `engine/shadow.py` (morning settlement runs it). Rules §9 uses this to decide when the model-health gate relaxes and when NFL/MLB go live.

## NBA
Graded props: **74** over 1 day(s). Over hit rate 0.365 vs market's average 0.496 vs model's 0.440.
Brier: model 0.2390 · market 0.2361 · blend 0.2316 → **model skill vs market -1.3%**, blend skill +1.9% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| ast | 14 | 0.429 | 0.501 | 0.413 | -30.0% |
| pts | 30 | 0.333 | 0.502 | 0.449 | +9.7% |
| reb | 30 | 0.367 | 0.488 | 0.444 | -0.1% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 8 | 0.263 | 0.500 | 0.518 |
| (0.3, 0.4] | 17 | 0.362 | 0.235 | 0.474 |
| (0.4, 0.5] | 29 | 0.445 | 0.241 | 0.491 |
| (0.5, 0.6] | 15 | 0.543 | 0.600 | 0.512 |
| (0.6, 0.7] | 4 | 0.641 | 0.750 | 0.528 |
| (0.7, 1.0] | 1 | 0.711 | 0.000 | 0.500 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 22 | 0.455 | 0.506 | -5.2 pts |
| (-0.1, -0.05] | 18 | 0.222 | 0.497 | -27.5 pts |
| (-0.05, 0.0] | 12 | 0.333 | 0.486 | -15.3 pts |
| (0.0, 0.05] | 12 | 0.333 | 0.489 | -15.6 pts |
| (0.05, 0.1] | 6 | 0.667 | 0.502 | +16.4 pts |
| (0.1, 1.0] | 4 | 0.250 | 0.479 | -22.9 pts |

Noise check: with 74 props one standard error on a hit rate is about ±5.8 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.
