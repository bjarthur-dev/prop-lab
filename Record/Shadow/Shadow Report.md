---
tags: [record, shadow]
---

# Shadow grading: every priced prop vs result and market

Written by `engine/shadow.py` (morning settlement runs it). Rules §9 uses this to decide when the model-health gate relaxes and when NFL/MLB go live.

## NBA
Graded props: **5439** over 21 day(s). Over hit rate 0.476 vs market's average 0.493 vs model's 0.457.
Brier: model 0.2534 · market 0.2466 · blend 0.2469 → **model skill vs market -2.8%**, blend skill -0.1% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| ast | 1279 | 0.476 | 0.496 | 0.457 | -1.6% |
| fg3m | 855 | 0.489 | 0.484 | 0.451 | -2.5% |
| pts | 1630 | 0.469 | 0.497 | 0.453 | -4.2% |
| reb | 1675 | 0.475 | 0.491 | 0.463 | -2.3% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 344 | 0.251 | 0.465 | 0.467 |
| (0.3, 0.4] | 1222 | 0.359 | 0.438 | 0.465 |
| (0.4, 0.5] | 2046 | 0.450 | 0.461 | 0.487 |
| (0.5, 0.6] | 1414 | 0.543 | 0.508 | 0.518 |
| (0.6, 0.7] | 351 | 0.640 | 0.558 | 0.542 |
| (0.7, 1.0] | 62 | 0.732 | 0.565 | 0.543 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 1176 | 0.479 | 0.496 | -1.7 pts |
| (-0.1, -0.05] | 1113 | 0.465 | 0.493 | -2.8 pts |
| (-0.05, 0.0] | 1308 | 0.460 | 0.493 | -3.3 pts |
| (0.0, 0.05] | 1003 | 0.480 | 0.492 | -1.3 pts |
| (0.05, 0.1] | 528 | 0.500 | 0.488 | +1.2 pts |
| (0.1, 1.0] | 311 | 0.514 | 0.488 | +2.7 pts |

Noise check: with 5439 props one standard error on a hit rate is about ±0.7 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

## NFL
Graded props: **1073** over 4 day(s). Over hit rate 0.495 vs market's average 0.495 vs model's 0.476.
Brier: model 0.2620 · market 0.2477 · blend 0.2484 → **model skill vs market -5.8%**, blend skill -0.3% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| carries | 45 | 0.489 | 0.494 | 0.464 | -23.7% |
| rec_yds | 533 | 0.486 | 0.500 | 0.484 | -1.3% |
| receptions | 337 | 0.510 | 0.486 | 0.457 | -2.3% |
| rush_yds | 158 | 0.494 | 0.498 | 0.491 | -22.8% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 87 | 0.243 | 0.506 | 0.464 |
| (0.3, 0.4] | 222 | 0.356 | 0.473 | 0.486 |
| (0.4, 0.5] | 330 | 0.454 | 0.479 | 0.497 |
| (0.5, 0.6] | 261 | 0.549 | 0.490 | 0.503 |
| (0.6, 0.7] | 117 | 0.644 | 0.547 | 0.507 |
| (0.7, 1.0] | 56 | 0.753 | 0.571 | 0.519 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 293 | 0.502 | 0.495 | +0.6 pts |
| (-0.1, -0.05] | 152 | 0.388 | 0.496 | -10.8 pts |
| (-0.05, 0.0] | 185 | 0.524 | 0.500 | +2.4 pts |
| (0.0, 0.05] | 144 | 0.451 | 0.490 | -3.9 pts |
| (0.05, 0.1] | 134 | 0.582 | 0.497 | +8.5 pts |
| (0.1, 1.0] | 165 | 0.515 | 0.493 | +2.2 pts |

Noise check: with 1073 props one standard error on a hit rate is about ±1.5 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

## NBA matchup engine v1 (context vs market)
Graded props: **6245** over 17 day(s). Over hit rate 0.473 vs market's average 0.489 vs model's 0.482.
Brier: model 0.2556 · market 0.2458 · blend 0.2462 → **model skill vs market -4.0%**, blend skill -0.2% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| assists | 1477 | 0.475 | 0.491 | 0.487 | -3.7% |
| points | 1759 | 0.466 | 0.501 | 0.494 | -6.2% |
| rebounds | 1697 | 0.476 | 0.490 | 0.487 | -4.1% |
| threes | 1312 | 0.475 | 0.471 | 0.455 | -1.1% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 423 | 0.235 | 0.416 | 0.432 |
| (0.3, 0.4] | 1087 | 0.357 | 0.415 | 0.451 |
| (0.4, 0.5] | 1884 | 0.453 | 0.462 | 0.482 |
| (0.5, 0.6] | 1876 | 0.547 | 0.514 | 0.508 |
| (0.6, 0.7] | 792 | 0.639 | 0.499 | 0.534 |
| (0.7, 1.0] | 183 | 0.750 | 0.519 | 0.531 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 1037 | 0.473 | 0.487 | -1.4 pts |
| (-0.1, -0.05] | 935 | 0.444 | 0.486 | -4.2 pts |
| (-0.05, 0.0] | 1303 | 0.479 | 0.487 | -0.8 pts |
| (0.0, 0.05] | 1198 | 0.470 | 0.493 | -2.3 pts |
| (0.05, 0.1] | 939 | 0.492 | 0.492 | +0.0 pts |
| (0.1, 1.0] | 833 | 0.475 | 0.489 | -1.3 pts |

Noise check: with 6245 props one standard error on a hit rate is about ±0.6 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.
