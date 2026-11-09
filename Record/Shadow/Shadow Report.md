---
tags: [record, shadow]
---

# Shadow grading: every priced prop vs result and market

Written by `engine/shadow.py` (morning settlement runs it). Rules §9 uses this to decide when the model-health gate relaxes and when NFL/MLB go live.

## NBA
Graded props: **4077** over 16 day(s). Over hit rate 0.477 vs market's average 0.493 vs model's 0.458.
Brier: model 0.2546 · market 0.2459 · blend 0.2453 → **model skill vs market -3.5%**, blend skill +0.3% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| ast | 970 | 0.478 | 0.495 | 0.456 | -3.2% |
| fg3m | 651 | 0.479 | 0.484 | 0.452 | -2.5% |
| pts | 1194 | 0.464 | 0.497 | 0.455 | -5.2% |
| reb | 1262 | 0.487 | 0.491 | 0.465 | -2.8% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 259 | 0.253 | 0.467 | 0.465 |
| (0.3, 0.4] | 898 | 0.359 | 0.438 | 0.463 |
| (0.4, 0.5] | 1532 | 0.450 | 0.476 | 0.487 |
| (0.5, 0.6] | 1069 | 0.544 | 0.490 | 0.517 |
| (0.6, 0.7] | 267 | 0.640 | 0.554 | 0.543 |
| (0.7, 1.0] | 52 | 0.732 | 0.558 | 0.545 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 876 | 0.487 | 0.496 | -0.8 pts |
| (-0.1, -0.05] | 822 | 0.478 | 0.493 | -1.5 pts |
| (-0.05, 0.0] | 965 | 0.468 | 0.492 | -2.4 pts |
| (0.0, 0.05] | 765 | 0.467 | 0.493 | -2.6 pts |
| (0.05, 0.1] | 410 | 0.476 | 0.488 | -1.2 pts |
| (0.1, 1.0] | 239 | 0.502 | 0.489 | +1.4 pts |

Noise check: with 4077 props one standard error on a hit rate is about ±0.8 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

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
Graded props: **4314** over 12 day(s). Over hit rate 0.469 vs market's average 0.489 vs model's 0.487.
Brier: model 0.2570 · market 0.2453 · blend 0.2461 → **model skill vs market -4.8%**, blend skill -0.3% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| assists | 1041 | 0.482 | 0.492 | 0.494 | -4.4% |
| points | 1183 | 0.452 | 0.501 | 0.501 | -7.5% |
| rebounds | 1204 | 0.486 | 0.488 | 0.487 | -5.3% |
| threes | 886 | 0.454 | 0.470 | 0.459 | -0.7% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 291 | 0.234 | 0.419 | 0.433 |
| (0.3, 0.4] | 714 | 0.358 | 0.410 | 0.451 |
| (0.4, 0.5] | 1275 | 0.453 | 0.461 | 0.482 |
| (0.5, 0.6] | 1299 | 0.548 | 0.512 | 0.506 |
| (0.6, 0.7] | 588 | 0.639 | 0.478 | 0.530 |
| (0.7, 1.0] | 147 | 0.749 | 0.510 | 0.531 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 707 | 0.470 | 0.487 | -1.8 pts |
| (-0.1, -0.05] | 601 | 0.446 | 0.487 | -4.1 pts |
| (-0.05, 0.0] | 865 | 0.468 | 0.489 | -2.0 pts |
| (0.0, 0.05] | 808 | 0.486 | 0.492 | -0.5 pts |
| (0.05, 0.1] | 675 | 0.484 | 0.492 | -0.7 pts |
| (0.1, 1.0] | 658 | 0.454 | 0.487 | -3.3 pts |

Noise check: with 4314 props one standard error on a hit rate is about ±0.8 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.
