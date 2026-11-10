---
tags: [record, shadow]
---

# Shadow grading: every priced prop vs result and market

Written by `engine/shadow.py` (morning settlement runs it). Rules §9 uses this to decide when the model-health gate relaxes and when NFL/MLB go live.

## NBA
Graded props: **4400** over 17 day(s). Over hit rate 0.476 vs market's average 0.492 vs model's 0.457.
Brier: model 0.2544 · market 0.2462 · blend 0.2465 → **model skill vs market -3.3%**, blend skill -0.1% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| ast | 1034 | 0.475 | 0.495 | 0.456 | -2.7% |
| fg3m | 722 | 0.483 | 0.483 | 0.450 | -2.5% |
| pts | 1289 | 0.465 | 0.497 | 0.455 | -4.9% |
| reb | 1355 | 0.484 | 0.491 | 0.465 | -2.8% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 277 | 0.253 | 0.473 | 0.465 |
| (0.3, 0.4] | 979 | 0.359 | 0.435 | 0.463 |
| (0.4, 0.5] | 1654 | 0.450 | 0.472 | 0.487 |
| (0.5, 0.6] | 1155 | 0.544 | 0.496 | 0.518 |
| (0.6, 0.7] | 283 | 0.640 | 0.548 | 0.542 |
| (0.7, 1.0] | 52 | 0.732 | 0.558 | 0.545 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 933 | 0.486 | 0.496 | -1.0 pts |
| (-0.1, -0.05] | 898 | 0.471 | 0.493 | -2.2 pts |
| (-0.05, 0.0] | 1062 | 0.469 | 0.492 | -2.3 pts |
| (0.0, 0.05] | 821 | 0.471 | 0.493 | -2.2 pts |
| (0.05, 0.1] | 431 | 0.476 | 0.488 | -1.3 pts |
| (0.1, 1.0] | 255 | 0.506 | 0.488 | +1.8 pts |

Noise check: with 4400 props one standard error on a hit rate is about ±0.8 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

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
Graded props: **4661** over 13 day(s). Over hit rate 0.470 vs market's average 0.489 vs model's 0.487.
Brier: model 0.2567 · market 0.2454 · blend 0.2461 → **model skill vs market -4.6%**, blend skill -0.3% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| assists | 1118 | 0.480 | 0.492 | 0.495 | -4.3% |
| points | 1279 | 0.455 | 0.501 | 0.500 | -7.5% |
| rebounds | 1300 | 0.483 | 0.489 | 0.488 | -5.0% |
| threes | 964 | 0.460 | 0.471 | 0.459 | -0.4% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 308 | 0.235 | 0.422 | 0.434 |
| (0.3, 0.4] | 772 | 0.358 | 0.405 | 0.451 |
| (0.4, 0.5] | 1360 | 0.454 | 0.463 | 0.482 |
| (0.5, 0.6] | 1430 | 0.548 | 0.513 | 0.506 |
| (0.6, 0.7] | 637 | 0.639 | 0.482 | 0.531 |
| (0.7, 1.0] | 154 | 0.749 | 0.506 | 0.532 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 759 | 0.472 | 0.488 | -1.6 pts |
| (-0.1, -0.05] | 640 | 0.444 | 0.487 | -4.3 pts |
| (-0.05, 0.0] | 935 | 0.464 | 0.489 | -2.5 pts |
| (0.0, 0.05] | 893 | 0.493 | 0.492 | +0.0 pts |
| (0.05, 0.1] | 734 | 0.484 | 0.492 | -0.8 pts |
| (0.1, 1.0] | 700 | 0.456 | 0.487 | -3.1 pts |

Noise check: with 4661 props one standard error on a hit rate is about ±0.7 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.
