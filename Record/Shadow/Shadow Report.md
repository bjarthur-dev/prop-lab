---
tags: [record, shadow]
---

# Shadow grading: every priced prop vs result and market

Written by `engine/shadow.py` (morning settlement runs it). Rules §9 uses this to decide when the model-health gate relaxes and when NFL/MLB go live.

## NBA
Graded props: **2766** over 11 day(s). Over hit rate 0.478 vs market's average 0.493 vs model's 0.461.
Brier: model 0.2535 · market 0.2453 · blend 0.2441 → **model skill vs market -3.3%**, blend skill +0.5% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| ast | 628 | 0.481 | 0.495 | 0.460 | -4.4% |
| fg3m | 417 | 0.482 | 0.481 | 0.454 | -3.1% |
| pts | 901 | 0.465 | 0.498 | 0.459 | -4.3% |
| reb | 820 | 0.487 | 0.492 | 0.469 | -1.5% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 172 | 0.252 | 0.442 | 0.468 |
| (0.3, 0.4] | 579 | 0.359 | 0.428 | 0.464 |
| (0.4, 0.5] | 1045 | 0.450 | 0.483 | 0.487 |
| (0.5, 0.6] | 734 | 0.544 | 0.488 | 0.515 |
| (0.6, 0.7] | 197 | 0.640 | 0.569 | 0.542 |
| (0.7, 1.0] | 39 | 0.728 | 0.564 | 0.539 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 566 | 0.493 | 0.497 | -0.4 pts |
| (-0.1, -0.05] | 557 | 0.479 | 0.493 | -1.4 pts |
| (-0.05, 0.0] | 637 | 0.454 | 0.492 | -3.8 pts |
| (0.0, 0.05] | 535 | 0.473 | 0.494 | -2.1 pts |
| (0.05, 0.1] | 288 | 0.486 | 0.488 | -0.2 pts |
| (0.1, 1.0] | 183 | 0.508 | 0.488 | +2.0 pts |

Noise check: with 2766 props one standard error on a hit rate is about ±1.0 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

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
Graded props: **2733** over 7 day(s). Over hit rate 0.466 vs market's average 0.487 vs model's 0.487.
Brier: model 0.2574 · market 0.2454 · blend 0.2461 → **model skill vs market -4.9%**, blend skill -0.3% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| assists | 612 | 0.471 | 0.490 | 0.494 | -4.2% |
| points | 812 | 0.456 | 0.502 | 0.504 | -7.5% |
| rebounds | 698 | 0.486 | 0.487 | 0.488 | -6.4% |
| threes | 611 | 0.453 | 0.466 | 0.458 | -0.4% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 188 | 0.225 | 0.383 | 0.430 |
| (0.3, 0.4] | 461 | 0.357 | 0.416 | 0.453 |
| (0.4, 0.5] | 797 | 0.454 | 0.458 | 0.480 |
| (0.5, 0.6] | 788 | 0.548 | 0.509 | 0.503 |
| (0.6, 0.7] | 391 | 0.640 | 0.488 | 0.526 |
| (0.7, 1.0] | 108 | 0.751 | 0.491 | 0.529 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 459 | 0.451 | 0.486 | -3.5 pts |
| (-0.1, -0.05] | 369 | 0.442 | 0.486 | -4.4 pts |
| (-0.05, 0.0] | 523 | 0.459 | 0.487 | -2.8 pts |
| (0.0, 0.05] | 498 | 0.498 | 0.488 | +1.0 pts |
| (0.05, 0.1] | 415 | 0.489 | 0.490 | -0.1 pts |
| (0.1, 1.0] | 469 | 0.454 | 0.486 | -3.2 pts |

Noise check: with 2733 props one standard error on a hit rate is about ±1.0 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.
