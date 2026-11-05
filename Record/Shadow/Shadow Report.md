---
tags: [record, shadow]
---

# Shadow grading: every priced prop vs result and market

Written by `engine/shadow.py` (morning settlement runs it). Rules §9 uses this to decide when the model-health gate relaxes and when NFL/MLB go live.

## NBA
Graded props: **3070** over 12 day(s). Over hit rate 0.477 vs market's average 0.493 vs model's 0.461.
Brier: model 0.2537 · market 0.2458 · blend 0.2440 → **model skill vs market -3.2%**, blend skill +0.7% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| ast | 750 | 0.479 | 0.495 | 0.459 | -3.8% |
| fg3m | 423 | 0.478 | 0.481 | 0.454 | -3.1% |
| pts | 908 | 0.465 | 0.498 | 0.459 | -4.4% |
| reb | 989 | 0.485 | 0.491 | 0.467 | -1.8% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 188 | 0.252 | 0.447 | 0.466 |
| (0.3, 0.4] | 652 | 0.360 | 0.434 | 0.464 |
| (0.4, 0.5] | 1162 | 0.451 | 0.479 | 0.487 |
| (0.5, 0.6] | 816 | 0.544 | 0.485 | 0.515 |
| (0.6, 0.7] | 209 | 0.640 | 0.565 | 0.542 |
| (0.7, 1.0] | 43 | 0.730 | 0.581 | 0.543 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 627 | 0.494 | 0.497 | -0.3 pts |
| (-0.1, -0.05] | 617 | 0.475 | 0.492 | -1.7 pts |
| (-0.05, 0.0] | 718 | 0.458 | 0.492 | -3.4 pts |
| (0.0, 0.05] | 589 | 0.467 | 0.494 | -2.7 pts |
| (0.05, 0.1] | 323 | 0.474 | 0.486 | -1.3 pts |
| (0.1, 1.0] | 196 | 0.526 | 0.489 | +3.7 pts |

Noise check: with 3070 props one standard error on a hit rate is about ±0.9 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

## NFL
Graded props: **590** over 2 day(s). Over hit rate 0.466 vs market's average 0.496 vs model's 0.492.
Brier: model 0.2680 · market 0.2473 · blend 0.2494 → **model skill vs market -8.3%**, blend skill -0.8% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| carries | 7 | 0.429 | 0.513 | 0.539 | -37.4% |
| rec_yds | 325 | 0.446 | 0.500 | 0.499 | -3.3% |
| receptions | 155 | 0.484 | 0.485 | 0.467 | -5.7% |
| rush_yds | 103 | 0.505 | 0.498 | 0.500 | -25.9% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 43 | 0.235 | 0.558 | 0.462 |
| (0.3, 0.4] | 101 | 0.355 | 0.495 | 0.490 |
| (0.4, 0.5] | 168 | 0.453 | 0.405 | 0.499 |
| (0.5, 0.6] | 162 | 0.550 | 0.457 | 0.499 |
| (0.6, 0.7] | 77 | 0.645 | 0.506 | 0.501 |
| (0.7, 1.0] | 39 | 0.748 | 0.513 | 0.514 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 146 | 0.514 | 0.496 | +1.8 pts |
| (-0.1, -0.05] | 70 | 0.329 | 0.495 | -16.6 pts |
| (-0.05, 0.0] | 89 | 0.449 | 0.502 | -5.2 pts |
| (0.0, 0.05] | 86 | 0.442 | 0.490 | -4.8 pts |
| (0.05, 0.1] | 86 | 0.523 | 0.501 | +2.2 pts |
| (0.1, 1.0] | 113 | 0.478 | 0.493 | -1.5 pts |

Noise check: with 590 props one standard error on a hit rate is about ±2.1 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

## NBA matchup engine v1 (context vs market)
Graded props: **3077** over 8 day(s). Over hit rate 0.469 vs market's average 0.488 vs model's 0.489.
Brier: model 0.2579 · market 0.2463 · blend 0.2470 → **model skill vs market -4.7%**, blend skill -0.3% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| assists | 759 | 0.477 | 0.491 | 0.496 | -4.5% |
| points | 819 | 0.454 | 0.502 | 0.504 | -7.5% |
| rebounds | 882 | 0.488 | 0.487 | 0.491 | -5.2% |
| threes | 617 | 0.451 | 0.466 | 0.458 | -0.3% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 203 | 0.226 | 0.404 | 0.432 |
| (0.3, 0.4] | 501 | 0.358 | 0.413 | 0.451 |
| (0.4, 0.5] | 896 | 0.453 | 0.462 | 0.479 |
| (0.5, 0.6] | 925 | 0.549 | 0.509 | 0.504 |
| (0.6, 0.7] | 433 | 0.640 | 0.478 | 0.527 |
| (0.7, 1.0] | 119 | 0.750 | 0.513 | 0.530 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 493 | 0.460 | 0.486 | -2.6 pts |
| (-0.1, -0.05] | 409 | 0.447 | 0.485 | -3.8 pts |
| (-0.05, 0.0] | 591 | 0.453 | 0.488 | -3.5 pts |
| (0.0, 0.05] | 589 | 0.492 | 0.490 | +0.2 pts |
| (0.05, 0.1] | 476 | 0.494 | 0.490 | +0.4 pts |
| (0.1, 1.0] | 519 | 0.461 | 0.486 | -2.6 pts |

Noise check: with 3077 props one standard error on a hit rate is about ±0.9 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.
