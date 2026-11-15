---
tags: [record, shadow]
---

# Shadow grading: every priced prop vs result and market

Written by `engine/shadow.py` (morning settlement runs it). Rules §9 uses this to decide when the model-health gate relaxes and when NFL/MLB go live.

## NBA
Graded props: **5587** over 22 day(s). Over hit rate 0.477 vs market's average 0.493 vs model's 0.457.
Brier: model 0.2536 · market 0.2465 · blend 0.2465 → **model skill vs market -2.9%**, blend skill -0.0% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| ast | 1311 | 0.477 | 0.496 | 0.456 | -1.8% |
| fg3m | 886 | 0.486 | 0.484 | 0.451 | -2.5% |
| pts | 1674 | 0.471 | 0.497 | 0.453 | -4.3% |
| reb | 1716 | 0.477 | 0.491 | 0.463 | -2.5% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 351 | 0.251 | 0.467 | 0.467 |
| (0.3, 0.4] | 1257 | 0.359 | 0.440 | 0.465 |
| (0.4, 0.5] | 2105 | 0.450 | 0.463 | 0.487 |
| (0.5, 0.6] | 1452 | 0.543 | 0.506 | 0.518 |
| (0.6, 0.7] | 358 | 0.639 | 0.561 | 0.542 |
| (0.7, 1.0] | 64 | 0.733 | 0.562 | 0.547 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 1212 | 0.479 | 0.496 | -1.7 pts |
| (-0.1, -0.05] | 1142 | 0.468 | 0.494 | -2.5 pts |
| (-0.05, 0.0] | 1345 | 0.462 | 0.493 | -3.1 pts |
| (0.0, 0.05] | 1028 | 0.481 | 0.492 | -1.2 pts |
| (0.05, 0.1] | 541 | 0.497 | 0.488 | +0.9 pts |
| (0.1, 1.0] | 319 | 0.511 | 0.488 | +2.3 pts |

Noise check: with 5587 props one standard error on a hit rate is about ±0.7 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

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
Graded props: **6481** over 18 day(s). Over hit rate 0.474 vs market's average 0.489 vs model's 0.482.
Brier: model 0.2564 · market 0.2458 · blend 0.2464 → **model skill vs market -4.3%**, blend skill -0.2% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| assists | 1527 | 0.477 | 0.491 | 0.486 | -4.0% |
| points | 1828 | 0.468 | 0.501 | 0.494 | -6.6% |
| rebounds | 1762 | 0.477 | 0.490 | 0.486 | -4.4% |
| threes | 1364 | 0.475 | 0.472 | 0.456 | -1.4% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 450 | 0.231 | 0.427 | 0.433 |
| (0.3, 0.4] | 1124 | 0.357 | 0.413 | 0.451 |
| (0.4, 0.5] | 1951 | 0.453 | 0.464 | 0.482 |
| (0.5, 0.6] | 1944 | 0.547 | 0.516 | 0.508 |
| (0.6, 0.7] | 823 | 0.639 | 0.496 | 0.534 |
| (0.7, 1.0] | 189 | 0.750 | 0.524 | 0.531 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 1078 | 0.475 | 0.487 | -1.2 pts |
| (-0.1, -0.05] | 968 | 0.449 | 0.486 | -3.7 pts |
| (-0.05, 0.0] | 1355 | 0.481 | 0.488 | -0.7 pts |
| (0.0, 0.05] | 1255 | 0.469 | 0.493 | -2.3 pts |
| (0.05, 0.1] | 974 | 0.493 | 0.492 | +0.0 pts |
| (0.1, 1.0] | 851 | 0.476 | 0.489 | -1.3 pts |

Noise check: with 6481 props one standard error on a hit rate is about ±0.6 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.
