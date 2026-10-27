---
tags: [record, shadow]
---

# Shadow grading: every priced prop vs result and market

Written by `engine/shadow.py` (morning settlement runs it). Rules §9 uses this to decide when the model-health gate relaxes and when NFL/MLB go live.

## NBA
Graded props: **782** over 4 day(s). Over hit rate 0.495 vs market's average 0.495 vs model's 0.461.
Brier: model 0.2523 · market 0.2424 · blend 0.2360 → **model skill vs market -4.1%**, blend skill +2.6% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| ast | 207 | 0.464 | 0.492 | 0.453 | -6.3% |
| pts | 296 | 0.517 | 0.499 | 0.459 | -5.1% |
| reb | 279 | 0.495 | 0.492 | 0.469 | -1.4% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 60 | 0.245 | 0.467 | 0.487 |
| (0.3, 0.4] | 141 | 0.359 | 0.482 | 0.477 |
| (0.4, 0.5] | 310 | 0.452 | 0.461 | 0.489 |
| (0.5, 0.6] | 201 | 0.541 | 0.488 | 0.507 |
| (0.6, 0.7] | 57 | 0.638 | 0.719 | 0.530 |
| (0.7, 1.0] | 13 | 0.736 | 0.692 | 0.523 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 176 | 0.483 | 0.497 | -1.4 pts |
| (-0.1, -0.05] | 153 | 0.536 | 0.499 | +3.7 pts |
| (-0.05, 0.0] | 163 | 0.479 | 0.496 | -1.8 pts |
| (0.0, 0.05] | 147 | 0.456 | 0.492 | -3.6 pts |
| (0.05, 0.1] | 84 | 0.488 | 0.488 | -0.0 pts |
| (0.1, 1.0] | 59 | 0.576 | 0.488 | +8.8 pts |

Noise check: with 782 props one standard error on a hit rate is about ±1.8 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

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
