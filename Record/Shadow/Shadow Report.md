---
tags: [record, shadow]
---

# Shadow grading: every priced prop vs result and market

Written by `engine/shadow.py` (morning settlement runs it). Rules §9 uses this to decide when the model-health gate relaxes and when NFL/MLB go live.

## NBA
Graded props: **1836** over 9 day(s). Over hit rate 0.482 vs market's average 0.493 vs model's 0.464.
Brier: model 0.2538 · market 0.2443 · blend 0.2414 → **model skill vs market -3.9%**, blend skill +1.2% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| ast | 427 | 0.475 | 0.495 | 0.462 | -6.1% |
| fg3m | 204 | 0.456 | 0.473 | 0.450 | -2.1% |
| pts | 637 | 0.485 | 0.498 | 0.462 | -4.4% |
| reb | 568 | 0.493 | 0.493 | 0.472 | -2.3% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 124 | 0.251 | 0.452 | 0.474 |
| (0.3, 0.4] | 350 | 0.360 | 0.449 | 0.466 |
| (0.4, 0.5] | 696 | 0.450 | 0.477 | 0.487 |
| (0.5, 0.6] | 493 | 0.544 | 0.481 | 0.512 |
| (0.6, 0.7] | 148 | 0.640 | 0.588 | 0.535 |
| (0.7, 1.0] | 25 | 0.726 | 0.640 | 0.524 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 379 | 0.504 | 0.499 | +0.5 pts |
| (-0.1, -0.05] | 344 | 0.491 | 0.495 | -0.4 pts |
| (-0.05, 0.0] | 407 | 0.455 | 0.490 | -3.6 pts |
| (0.0, 0.05] | 360 | 0.469 | 0.491 | -2.2 pts |
| (0.05, 0.1] | 208 | 0.471 | 0.489 | -1.8 pts |
| (0.1, 1.0] | 138 | 0.529 | 0.490 | +3.9 pts |

Noise check: with 1836 props one standard error on a hit rate is about ±1.2 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

## NFL
Graded props: **160** over 1 day(s). Over hit rate 0.444 vs market's average 0.500 vs model's 0.520.
Brier: model 0.2576 · market 0.2505 · blend 0.2490 → **model skill vs market -2.8%**, blend skill +0.6% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| carries | 7 | 0.429 | 0.513 | 0.539 | -37.4% |
| rec_yds | 118 | 0.424 | 0.500 | 0.513 | +1.6% |
| rush_yds | 35 | 0.514 | 0.498 | 0.539 | -10.3% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 7 | 0.234 | 0.429 | 0.502 |
| (0.3, 0.4] | 21 | 0.364 | 0.476 | 0.497 |
| (0.4, 0.5] | 49 | 0.460 | 0.367 | 0.501 |
| (0.5, 0.6] | 43 | 0.554 | 0.419 | 0.500 |
| (0.6, 0.7] | 21 | 0.634 | 0.429 | 0.496 |
| (0.7, 1.0] | 19 | 0.746 | 0.684 | 0.505 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 31 | 0.452 | 0.501 | -4.9 pts |
| (-0.1, -0.05] | 16 | 0.188 | 0.501 | -31.3 pts |
| (-0.05, 0.0] | 28 | 0.464 | 0.500 | -3.6 pts |
| (0.0, 0.05] | 18 | 0.389 | 0.498 | -10.9 pts |
| (0.05, 0.1] | 28 | 0.429 | 0.500 | -7.1 pts |
| (0.1, 1.0] | 39 | 0.564 | 0.500 | +6.4 pts |

Noise check: with 160 props one standard error on a hit rate is about ±4.0 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

## NBA matchup engine v1 (context vs market)
Graded props: **1609** over 5 day(s). Over hit rate 0.472 vs market's average 0.487 vs model's 0.491.
Brier: model 0.2584 · market 0.2446 · blend 0.2457 → **model skill vs market -5.6%**, blend skill -0.5% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| assists | 354 | 0.455 | 0.492 | 0.505 | -5.4% |
| points | 483 | 0.480 | 0.503 | 0.511 | -7.3% |
| rebounds | 409 | 0.499 | 0.486 | 0.483 | -6.6% |
| threes | 363 | 0.449 | 0.464 | 0.460 | -2.5% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 105 | 0.227 | 0.400 | 0.425 |
| (0.3, 0.4] | 268 | 0.358 | 0.410 | 0.453 |
| (0.4, 0.5] | 458 | 0.454 | 0.487 | 0.480 |
| (0.5, 0.6] | 474 | 0.549 | 0.489 | 0.504 |
| (0.6, 0.7] | 237 | 0.641 | 0.519 | 0.525 |
| (0.7, 1.0] | 67 | 0.749 | 0.448 | 0.526 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 261 | 0.471 | 0.486 | -1.5 pts |
| (-0.1, -0.05] | 208 | 0.462 | 0.485 | -2.3 pts |
| (-0.05, 0.0] | 299 | 0.455 | 0.487 | -3.2 pts |
| (0.0, 0.05] | 302 | 0.510 | 0.490 | +2.0 pts |
| (0.05, 0.1] | 247 | 0.478 | 0.488 | -1.1 pts |
| (0.1, 1.0] | 292 | 0.455 | 0.486 | -3.1 pts |

Noise check: with 1609 props one standard error on a hit rate is about ±1.2 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.
