---
tags: [record, shadow]
---

# Shadow grading: every priced prop vs result and market

Written by `engine/shadow.py` (morning settlement runs it). Rules §9 uses this to decide when the model-health gate relaxes and when NFL/MLB go live.

## NBA
Graded props: **4873** over 19 day(s). Over hit rate 0.472 vs market's average 0.493 vs model's 0.457.
Brier: model 0.2528 · market 0.2461 · blend 0.2461 → **model skill vs market -2.7%**, blend skill +0.0% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| ast | 1153 | 0.468 | 0.495 | 0.456 | -1.4% |
| fg3m | 722 | 0.483 | 0.483 | 0.450 | -2.5% |
| pts | 1471 | 0.465 | 0.497 | 0.453 | -4.1% |
| reb | 1527 | 0.475 | 0.491 | 0.464 | -2.5% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 312 | 0.250 | 0.455 | 0.468 |
| (0.3, 0.4] | 1084 | 0.359 | 0.435 | 0.465 |
| (0.4, 0.5] | 1840 | 0.450 | 0.458 | 0.487 |
| (0.5, 0.6] | 1270 | 0.544 | 0.499 | 0.517 |
| (0.6, 0.7] | 312 | 0.639 | 0.561 | 0.541 |
| (0.7, 1.0] | 55 | 0.732 | 0.582 | 0.544 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 1054 | 0.475 | 0.496 | -2.1 pts |
| (-0.1, -0.05] | 981 | 0.466 | 0.493 | -2.7 pts |
| (-0.05, 0.0] | 1178 | 0.458 | 0.492 | -3.5 pts |
| (0.0, 0.05] | 910 | 0.469 | 0.493 | -2.4 pts |
| (0.05, 0.1] | 473 | 0.486 | 0.488 | -0.2 pts |
| (0.1, 1.0] | 277 | 0.520 | 0.488 | +3.2 pts |

Noise check: with 4873 props one standard error on a hit rate is about ±0.7 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

## NFL
Graded props: **1039** over 3 day(s). Over hit rate 0.490 vs market's average 0.495 vs model's 0.475.
Brier: model 0.2620 · market 0.2476 · blend 0.2483 → **model skill vs market -5.8%**, blend skill -0.3% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| carries | 41 | 0.463 | 0.495 | 0.475 | -19.0% |
| rec_yds | 520 | 0.483 | 0.500 | 0.483 | -1.5% |
| receptions | 324 | 0.503 | 0.486 | 0.455 | -2.9% |
| rush_yds | 154 | 0.494 | 0.498 | 0.493 | -23.0% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 86 | 0.242 | 0.500 | 0.463 |
| (0.3, 0.4] | 214 | 0.356 | 0.467 | 0.486 |
| (0.4, 0.5] | 320 | 0.453 | 0.472 | 0.497 |
| (0.5, 0.6] | 250 | 0.549 | 0.492 | 0.503 |
| (0.6, 0.7] | 115 | 0.644 | 0.539 | 0.506 |
| (0.7, 1.0] | 54 | 0.749 | 0.556 | 0.518 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 286 | 0.493 | 0.495 | -0.2 pts |
| (-0.1, -0.05] | 149 | 0.383 | 0.496 | -11.3 pts |
| (-0.05, 0.0] | 178 | 0.522 | 0.500 | +2.2 pts |
| (0.0, 0.05] | 138 | 0.464 | 0.490 | -2.6 pts |
| (0.05, 0.1] | 126 | 0.571 | 0.498 | +7.3 pts |
| (0.1, 1.0] | 162 | 0.506 | 0.493 | +1.3 pts |

Noise check: with 1039 props one standard error on a hit rate is about ±1.6 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

## NBA matchup engine v1 (context vs market)
Graded props: **5511** over 15 day(s). Over hit rate 0.471 vs market's average 0.489 vs model's 0.484.
Brier: model 0.2556 · market 0.2457 · blend 0.2461 → **model skill vs market -4.0%**, blend skill -0.2% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| assists | 1314 | 0.477 | 0.491 | 0.489 | -3.5% |
| points | 1531 | 0.459 | 0.501 | 0.496 | -6.6% |
| rebounds | 1514 | 0.476 | 0.490 | 0.487 | -4.4% |
| threes | 1152 | 0.473 | 0.470 | 0.456 | -0.8% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 377 | 0.235 | 0.416 | 0.435 |
| (0.3, 0.4] | 942 | 0.357 | 0.412 | 0.451 |
| (0.4, 0.5] | 1634 | 0.453 | 0.457 | 0.482 |
| (0.5, 0.6] | 1669 | 0.547 | 0.516 | 0.507 |
| (0.6, 0.7] | 724 | 0.639 | 0.494 | 0.533 |
| (0.7, 1.0] | 165 | 0.749 | 0.509 | 0.532 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 907 | 0.472 | 0.487 | -1.6 pts |
| (-0.1, -0.05] | 811 | 0.439 | 0.487 | -4.8 pts |
| (-0.05, 0.0] | 1122 | 0.467 | 0.488 | -2.1 pts |
| (0.0, 0.05] | 1053 | 0.483 | 0.493 | -1.0 pts |
| (0.05, 0.1] | 849 | 0.492 | 0.491 | +0.1 pts |
| (0.1, 1.0] | 769 | 0.468 | 0.488 | -2.0 pts |

Noise check: with 5511 props one standard error on a hit rate is about ±0.7 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.
