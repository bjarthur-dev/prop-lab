---
tags: [record, shadow]
---

# Shadow grading: every priced prop vs result and market

Written by `engine/shadow.py` (morning settlement runs it). Rules §9 uses this to decide when the model-health gate relaxes and when NFL/MLB go live.

## NBA
Graded props: **3785** over 15 day(s). Over hit rate 0.477 vs market's average 0.493 vs model's 0.459.
Brier: model 0.2552 · market 0.2459 · blend 0.2448 → **model skill vs market -3.8%**, blend skill +0.4% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| ast | 909 | 0.479 | 0.495 | 0.457 | -3.7% |
| fg3m | 582 | 0.474 | 0.484 | 0.453 | -3.0% |
| pts | 1111 | 0.461 | 0.498 | 0.456 | -5.0% |
| reb | 1183 | 0.493 | 0.491 | 0.466 | -3.0% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 235 | 0.251 | 0.477 | 0.466 |
| (0.3, 0.4] | 831 | 0.359 | 0.438 | 0.463 |
| (0.4, 0.5] | 1419 | 0.450 | 0.477 | 0.487 |
| (0.5, 0.6] | 1003 | 0.544 | 0.488 | 0.517 |
| (0.6, 0.7] | 249 | 0.640 | 0.554 | 0.543 |
| (0.7, 1.0] | 48 | 0.731 | 0.542 | 0.542 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 805 | 0.497 | 0.497 | +0.0 pts |
| (-0.1, -0.05] | 760 | 0.478 | 0.493 | -1.5 pts |
| (-0.05, 0.0] | 893 | 0.464 | 0.492 | -2.9 pts |
| (0.0, 0.05] | 719 | 0.466 | 0.493 | -2.7 pts |
| (0.05, 0.1] | 382 | 0.474 | 0.488 | -1.4 pts |
| (0.1, 1.0] | 226 | 0.500 | 0.489 | +1.1 pts |

Noise check: with 3785 props one standard error on a hit rate is about ±0.8 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

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
Graded props: **3966** over 11 day(s). Over hit rate 0.470 vs market's average 0.489 vs model's 0.489.
Brier: model 0.2574 · market 0.2456 · blend 0.2464 → **model skill vs market -4.8%**, blend skill -0.3% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| assists | 960 | 0.479 | 0.492 | 0.495 | -4.7% |
| points | 1084 | 0.453 | 0.502 | 0.503 | -7.4% |
| rebounds | 1112 | 0.493 | 0.488 | 0.490 | -5.5% |
| threes | 810 | 0.451 | 0.469 | 0.460 | -0.4% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 257 | 0.231 | 0.409 | 0.431 |
| (0.3, 0.4] | 649 | 0.358 | 0.416 | 0.450 |
| (0.4, 0.5] | 1161 | 0.454 | 0.463 | 0.481 |
| (0.5, 0.6] | 1207 | 0.548 | 0.510 | 0.506 |
| (0.6, 0.7] | 552 | 0.639 | 0.482 | 0.530 |
| (0.7, 1.0] | 140 | 0.749 | 0.500 | 0.532 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 631 | 0.474 | 0.487 | -1.3 pts |
| (-0.1, -0.05] | 532 | 0.451 | 0.487 | -3.6 pts |
| (-0.05, 0.0] | 793 | 0.462 | 0.489 | -2.7 pts |
| (0.0, 0.05] | 756 | 0.487 | 0.491 | -0.5 pts |
| (0.05, 0.1] | 630 | 0.487 | 0.491 | -0.4 pts |
| (0.1, 1.0] | 624 | 0.455 | 0.487 | -3.2 pts |

Noise check: with 3966 props one standard error on a hit rate is about ±0.8 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.
