---
tags: [record, shadow]
---

# Shadow grading: every priced prop vs result and market

Written by `engine/shadow.py` (morning settlement runs it). Rules §9 uses this to decide when the model-health gate relaxes and when NFL/MLB go live.

## NBA
Graded props: **1472** over 7 day(s). Over hit rate 0.495 vs market's average 0.494 vs model's 0.466.
Brier: model 0.2534 · market 0.2437 · blend 0.2412 → **model skill vs market -4.0%**, blend skill +1.0% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| ast | 350 | 0.483 | 0.494 | 0.461 | -5.6% |
| fg3m | 131 | 0.489 | 0.476 | 0.458 | -2.5% |
| pts | 511 | 0.503 | 0.499 | 0.464 | -4.7% |
| reb | 480 | 0.496 | 0.493 | 0.473 | -2.4% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 95 | 0.250 | 0.484 | 0.479 |
| (0.3, 0.4] | 261 | 0.359 | 0.464 | 0.469 |
| (0.4, 0.5] | 583 | 0.451 | 0.479 | 0.487 |
| (0.5, 0.6] | 385 | 0.543 | 0.488 | 0.510 |
| (0.6, 0.7] | 125 | 0.638 | 0.640 | 0.533 |
| (0.7, 1.0] | 23 | 0.727 | 0.609 | 0.527 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 302 | 0.507 | 0.499 | +0.7 pts |
| (-0.1, -0.05] | 270 | 0.522 | 0.497 | +2.5 pts |
| (-0.05, 0.0] | 328 | 0.451 | 0.491 | -4.0 pts |
| (0.0, 0.05] | 287 | 0.484 | 0.491 | -0.7 pts |
| (0.05, 0.1] | 169 | 0.485 | 0.491 | -0.6 pts |
| (0.1, 1.0] | 116 | 0.560 | 0.490 | +7.0 pts |

Noise check: with 1472 props one standard error on a hit rate is about ±1.3 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

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
Graded props: **964** over 3 day(s). Over hit rate 0.488 vs market's average 0.487 vs model's 0.496.
Brier: model 0.2602 · market 0.2454 · blend 0.2465 → **model skill vs market -6.0%**, blend skill -0.5% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| assists | 207 | 0.483 | 0.492 | 0.514 | -5.5% |
| points | 287 | 0.481 | 0.505 | 0.515 | -7.7% |
| rebounds | 248 | 0.520 | 0.484 | 0.490 | -6.2% |
| threes | 222 | 0.464 | 0.462 | 0.459 | -4.1% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 76 | 0.224 | 0.434 | 0.426 |
| (0.3, 0.4] | 140 | 0.359 | 0.436 | 0.453 |
| (0.4, 0.5] | 254 | 0.453 | 0.492 | 0.478 |
| (0.5, 0.6] | 286 | 0.549 | 0.490 | 0.501 |
| (0.6, 0.7] | 158 | 0.641 | 0.544 | 0.520 |
| (0.7, 1.0] | 50 | 0.743 | 0.500 | 0.531 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 162 | 0.475 | 0.485 | -0.9 pts |
| (-0.1, -0.05] | 100 | 0.480 | 0.481 | -0.1 pts |
| (-0.05, 0.0] | 169 | 0.467 | 0.489 | -2.1 pts |
| (0.0, 0.05] | 172 | 0.552 | 0.488 | +6.4 pts |
| (0.05, 0.1] | 155 | 0.484 | 0.488 | -0.4 pts |
| (0.1, 1.0] | 206 | 0.466 | 0.488 | -2.2 pts |

Noise check: with 964 props one standard error on a hit rate is about ±1.6 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.
