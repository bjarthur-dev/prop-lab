---
tags: [record, shadow]
---

# Shadow grading: every priced prop vs result and market

Written by `engine/shadow.py` (morning settlement runs it). Rules §9 uses this to decide when the model-health gate relaxes and when NFL/MLB go live.

## NBA
Graded props: **4599** over 18 day(s). Over hit rate 0.473 vs market's average 0.493 vs model's 0.456.
Brier: model 0.2539 · market 0.2462 · blend 0.2463 → **model skill vs market -3.1%**, blend skill -0.0% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| ast | 1085 | 0.468 | 0.495 | 0.455 | -1.9% |
| fg3m | 722 | 0.483 | 0.483 | 0.450 | -2.5% |
| pts | 1365 | 0.464 | 0.497 | 0.453 | -4.8% |
| reb | 1427 | 0.480 | 0.491 | 0.464 | -2.7% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 302 | 0.249 | 0.457 | 0.467 |
| (0.3, 0.4] | 1026 | 0.359 | 0.440 | 0.464 |
| (0.4, 0.5] | 1715 | 0.450 | 0.464 | 0.487 |
| (0.5, 0.6] | 1207 | 0.544 | 0.495 | 0.517 |
| (0.6, 0.7] | 297 | 0.640 | 0.552 | 0.541 |
| (0.7, 1.0] | 52 | 0.732 | 0.558 | 0.545 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 997 | 0.481 | 0.496 | -1.4 pts |
| (-0.1, -0.05] | 928 | 0.469 | 0.493 | -2.4 pts |
| (-0.05, 0.0] | 1103 | 0.461 | 0.492 | -3.1 pts |
| (0.0, 0.05] | 856 | 0.467 | 0.493 | -2.5 pts |
| (0.05, 0.1] | 449 | 0.481 | 0.488 | -0.7 pts |
| (0.1, 1.0] | 266 | 0.508 | 0.487 | +2.0 pts |

Noise check: with 4599 props one standard error on a hit rate is about ±0.7 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

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
Graded props: **4968** over 14 day(s). Over hit rate 0.469 vs market's average 0.489 vs model's 0.485.
Brier: model 0.2561 · market 0.2455 · blend 0.2461 → **model skill vs market -4.3%**, blend skill -0.2% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| assists | 1192 | 0.475 | 0.492 | 0.492 | -3.8% |
| points | 1363 | 0.454 | 0.501 | 0.499 | -6.8% |
| rebounds | 1378 | 0.481 | 0.490 | 0.488 | -4.9% |
| threes | 1035 | 0.465 | 0.471 | 0.457 | -0.9% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 337 | 0.234 | 0.412 | 0.435 |
| (0.3, 0.4] | 834 | 0.357 | 0.409 | 0.450 |
| (0.4, 0.5] | 1457 | 0.454 | 0.458 | 0.482 |
| (0.5, 0.6] | 1516 | 0.548 | 0.512 | 0.507 |
| (0.6, 0.7] | 668 | 0.639 | 0.490 | 0.531 |
| (0.7, 1.0] | 156 | 0.749 | 0.506 | 0.533 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 815 | 0.471 | 0.488 | -1.7 pts |
| (-0.1, -0.05] | 698 | 0.440 | 0.486 | -4.6 pts |
| (-0.05, 0.0] | 1011 | 0.464 | 0.489 | -2.5 pts |
| (0.0, 0.05] | 949 | 0.482 | 0.493 | -1.1 pts |
| (0.05, 0.1] | 771 | 0.489 | 0.491 | -0.2 pts |
| (0.1, 1.0] | 724 | 0.463 | 0.488 | -2.5 pts |

Noise check: with 4968 props one standard error on a hit rate is about ±0.7 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.
