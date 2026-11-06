---
tags: [record, shadow]
---

# Shadow grading: every priced prop vs result and market

Written by `engine/shadow.py` (morning settlement runs it). Rules §9 uses this to decide when the model-health gate relaxes and when NFL/MLB go live.

## NBA
Graded props: **3160** over 13 day(s). Over hit rate 0.477 vs market's average 0.493 vs model's 0.460.
Brier: model 0.2544 · market 0.2458 · blend 0.2441 → **model skill vs market -3.5%**, blend skill +0.7% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| ast | 770 | 0.479 | 0.495 | 0.457 | -4.2% |
| fg3m | 444 | 0.480 | 0.483 | 0.456 | -3.7% |
| pts | 933 | 0.463 | 0.498 | 0.458 | -4.5% |
| reb | 1013 | 0.487 | 0.491 | 0.466 | -2.1% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 198 | 0.252 | 0.455 | 0.467 |
| (0.3, 0.4] | 676 | 0.360 | 0.439 | 0.464 |
| (0.4, 0.5] | 1196 | 0.451 | 0.477 | 0.487 |
| (0.5, 0.6] | 833 | 0.544 | 0.486 | 0.515 |
| (0.6, 0.7] | 213 | 0.640 | 0.563 | 0.542 |
| (0.7, 1.0] | 44 | 0.730 | 0.568 | 0.543 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 656 | 0.498 | 0.498 | +0.1 pts |
| (-0.1, -0.05] | 640 | 0.478 | 0.492 | -1.4 pts |
| (-0.05, 0.0] | 733 | 0.454 | 0.492 | -3.8 pts |
| (0.0, 0.05] | 606 | 0.469 | 0.494 | -2.5 pts |
| (0.05, 0.1] | 327 | 0.471 | 0.486 | -1.5 pts |
| (0.1, 1.0] | 198 | 0.520 | 0.489 | +3.1 pts |

Noise check: with 3160 props one standard error on a hit rate is about ±0.9 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

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
Graded props: **3173** over 9 day(s). Over hit rate 0.470 vs market's average 0.488 vs model's 0.489.
Brier: model 0.2578 · market 0.2461 · blend 0.2468 → **model skill vs market -4.8%**, blend skill -0.3% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| assists | 782 | 0.481 | 0.492 | 0.496 | -4.9% |
| points | 845 | 0.453 | 0.502 | 0.504 | -7.5% |
| rebounds | 907 | 0.490 | 0.487 | 0.490 | -5.1% |
| threes | 639 | 0.451 | 0.467 | 0.459 | -0.5% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 205 | 0.227 | 0.410 | 0.432 |
| (0.3, 0.4] | 520 | 0.358 | 0.415 | 0.451 |
| (0.4, 0.5] | 930 | 0.454 | 0.459 | 0.480 |
| (0.5, 0.6] | 953 | 0.549 | 0.513 | 0.505 |
| (0.6, 0.7] | 445 | 0.640 | 0.481 | 0.528 |
| (0.7, 1.0] | 120 | 0.750 | 0.508 | 0.531 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 500 | 0.468 | 0.487 | -1.9 pts |
| (-0.1, -0.05] | 429 | 0.445 | 0.485 | -4.0 pts |
| (-0.05, 0.0] | 620 | 0.453 | 0.489 | -3.5 pts |
| (0.0, 0.05] | 612 | 0.497 | 0.491 | +0.6 pts |
| (0.05, 0.1] | 488 | 0.494 | 0.490 | +0.3 pts |
| (0.1, 1.0] | 524 | 0.458 | 0.486 | -2.8 pts |

Noise check: with 3173 props one standard error on a hit rate is about ±0.9 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.
