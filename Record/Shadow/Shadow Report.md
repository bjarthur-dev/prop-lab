---
tags: [record, shadow]
---

# Shadow grading: every priced prop vs result and market

Written by `engine/shadow.py` (morning settlement runs it). Rules §9 uses this to decide when the model-health gate relaxes and when NFL/MLB go live.

## NBA
Graded props: **2201** over 10 day(s). Over hit rate 0.476 vs market's average 0.493 vs model's 0.464.
Brier: model 0.2545 · market 0.2450 · blend 0.2422 → **model skill vs market -3.9%**, blend skill +1.1% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| ast | 502 | 0.472 | 0.495 | 0.463 | -5.3% |
| fg3m | 291 | 0.460 | 0.476 | 0.454 | -4.0% |
| pts | 742 | 0.473 | 0.499 | 0.463 | -4.6% |
| reb | 666 | 0.488 | 0.492 | 0.470 | -1.9% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 141 | 0.253 | 0.468 | 0.470 |
| (0.3, 0.4] | 427 | 0.359 | 0.438 | 0.465 |
| (0.4, 0.5] | 838 | 0.450 | 0.475 | 0.486 |
| (0.5, 0.6] | 592 | 0.544 | 0.471 | 0.512 |
| (0.6, 0.7] | 170 | 0.640 | 0.571 | 0.538 |
| (0.7, 1.0] | 33 | 0.728 | 0.606 | 0.541 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 444 | 0.505 | 0.498 | +0.7 pts |
| (-0.1, -0.05] | 421 | 0.485 | 0.495 | -1.0 pts |
| (-0.05, 0.0] | 491 | 0.440 | 0.490 | -5.0 pts |
| (0.0, 0.05] | 438 | 0.461 | 0.491 | -3.0 pts |
| (0.05, 0.1] | 248 | 0.476 | 0.490 | -1.4 pts |
| (0.1, 1.0] | 159 | 0.522 | 0.489 | +3.3 pts |

Noise check: with 2201 props one standard error on a hit rate is about ±1.1 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

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
Graded props: **2031** over 6 day(s). Over hit rate 0.463 vs market's average 0.486 vs model's 0.489.
Brier: model 0.2592 · market 0.2444 · blend 0.2458 → **model skill vs market -6.1%**, blend skill -0.6% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| assists | 449 | 0.457 | 0.491 | 0.501 | -5.5% |
| points | 604 | 0.462 | 0.503 | 0.507 | -8.4% |
| rebounds | 518 | 0.485 | 0.485 | 0.487 | -6.5% |
| threes | 460 | 0.448 | 0.462 | 0.455 | -2.9% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 140 | 0.230 | 0.400 | 0.426 |
| (0.3, 0.4] | 351 | 0.357 | 0.419 | 0.451 |
| (0.4, 0.5] | 577 | 0.454 | 0.470 | 0.480 |
| (0.5, 0.6] | 576 | 0.548 | 0.484 | 0.502 |
| (0.6, 0.7] | 301 | 0.640 | 0.492 | 0.524 |
| (0.7, 1.0] | 86 | 0.754 | 0.465 | 0.531 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 342 | 0.468 | 0.485 | -1.7 pts |
| (-0.1, -0.05] | 265 | 0.453 | 0.483 | -3.0 pts |
| (-0.05, 0.0] | 377 | 0.440 | 0.485 | -4.5 pts |
| (0.0, 0.05] | 364 | 0.505 | 0.488 | +1.7 pts |
| (0.05, 0.1] | 319 | 0.470 | 0.489 | -1.9 pts |
| (0.1, 1.0] | 364 | 0.442 | 0.486 | -4.4 pts |

Noise check: with 2031 props one standard error on a hit rate is about ±1.1 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.
