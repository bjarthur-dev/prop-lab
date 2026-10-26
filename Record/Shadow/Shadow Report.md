---
tags: [record, shadow]
---

# Shadow grading: every priced prop vs result and market

Written by `engine/shadow.py` (morning settlement runs it). Rules §9 uses this to decide when the model-health gate relaxes and when NFL/MLB go live.

## NBA
Graded props: **492** over 3 day(s). Over hit rate 0.494 vs market's average 0.493 vs model's 0.445.
Brier: model 0.2558 · market 0.2440 · blend 0.2396 → **model skill vs market -4.8%**, blend skill +1.8% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| ast | 132 | 0.462 | 0.493 | 0.443 | -5.9% |
| pts | 185 | 0.530 | 0.499 | 0.445 | -6.9% |
| reb | 175 | 0.480 | 0.486 | 0.446 | -1.7% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 45 | 0.253 | 0.444 | 0.485 |
| (0.3, 0.4] | 107 | 0.358 | 0.486 | 0.478 |
| (0.4, 0.5] | 209 | 0.452 | 0.483 | 0.490 |
| (0.5, 0.6] | 98 | 0.543 | 0.490 | 0.508 |
| (0.6, 0.7] | 27 | 0.637 | 0.704 | 0.527 |
| (0.7, 1.0] | 6 | 0.731 | 0.500 | 0.527 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 127 | 0.457 | 0.496 | -3.9 pts |
| (-0.1, -0.05] | 112 | 0.562 | 0.497 | +6.6 pts |
| (-0.05, 0.0] | 111 | 0.505 | 0.495 | +1.0 pts |
| (0.0, 0.05] | 71 | 0.465 | 0.489 | -2.4 pts |
| (0.05, 0.1] | 41 | 0.439 | 0.482 | -4.3 pts |
| (0.1, 1.0] | 30 | 0.500 | 0.483 | +1.7 pts |

Noise check: with 492 props one standard error on a hit rate is about ±2.3 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

## NFL
Graded props: **160** over 1 day(s). Over hit rate 0.444 vs market's average 0.500 vs model's 0.520.
Brier: model 0.2576 · market 0.2505 · blend 0.2490 → **model skill vs market -2.8%**, blend skill +0.6% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| carries | 7 | 0.429 | 0.513 | 0.539 | -37.4% |
| rec_yds | 118 | 0.424 | 0.500 | 0.513 | +1.6% |
| rush_yds | 35 | 0.514 | 0.498 | 0.539 | -10.3% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 7 | 0.234 | 0.429 | 0.502 |
| (0.3, 0.4] | 21 | 0.364 | 0.476 | 0.497 |
| (0.4, 0.5] | 49 | 0.460 | 0.367 | 0.501 |
| (0.5, 0.6] | 43 | 0.554 | 0.419 | 0.500 |
| (0.6, 0.7] | 21 | 0.634 | 0.429 | 0.496 |
| (0.7, 1.0] | 19 | 0.746 | 0.684 | 0.505 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 31 | 0.452 | 0.501 | -4.9 pts |
| (-0.1, -0.05] | 16 | 0.188 | 0.501 | -31.3 pts |
| (-0.05, 0.0] | 28 | 0.464 | 0.500 | -3.6 pts |
| (0.0, 0.05] | 18 | 0.389 | 0.498 | -10.9 pts |
| (0.05, 0.1] | 28 | 0.429 | 0.500 | -7.1 pts |
| (0.1, 1.0] | 39 | 0.564 | 0.500 | +6.4 pts |

Noise check: with 160 props one standard error on a hit rate is about ±4.0 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.
