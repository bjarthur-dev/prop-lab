---
tags: [record, shadow]
---

# Shadow grading: every priced prop vs result and market

Written by `engine/shadow.py` (morning settlement runs it). Rules §9 uses this to decide when the model-health gate relaxes and when NFL/MLB go live.

## NBA
Graded props: **909** over 5 day(s). Over hit rate 0.503 vs market's average 0.495 vs model's 0.462.
Brier: model 0.2549 · market 0.2431 · blend 0.2383 → **model skill vs market -4.9%**, blend skill +2.0% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| ast | 240 | 0.483 | 0.491 | 0.452 | -7.8% |
| pts | 346 | 0.526 | 0.499 | 0.461 | -6.0% |
| reb | 323 | 0.492 | 0.492 | 0.470 | -1.4% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 70 | 0.247 | 0.543 | 0.485 |
| (0.3, 0.4] | 162 | 0.359 | 0.469 | 0.477 |
| (0.4, 0.5] | 354 | 0.451 | 0.466 | 0.488 |
| (0.5, 0.6] | 236 | 0.541 | 0.500 | 0.508 |
| (0.6, 0.7] | 72 | 0.639 | 0.694 | 0.528 |
| (0.7, 1.0] | 15 | 0.733 | 0.667 | 0.523 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 208 | 0.505 | 0.497 | +0.8 pts |
| (-0.1, -0.05] | 173 | 0.543 | 0.499 | +4.5 pts |
| (-0.05, 0.0] | 185 | 0.459 | 0.496 | -3.6 pts |
| (0.0, 0.05] | 172 | 0.471 | 0.491 | -2.0 pts |
| (0.05, 0.1] | 99 | 0.505 | 0.493 | +1.2 pts |
| (0.1, 1.0] | 72 | 0.583 | 0.488 | +9.6 pts |

Noise check: with 909 props one standard error on a hit rate is about ±1.7 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

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
Graded props: **201** over 1 day(s). Over hit rate 0.562 vs market's average 0.485 vs model's 0.527.
Brier: model 0.2510 · market 0.2482 · blend 0.2462 → **model skill vs market -1.1%**, blend skill +0.8% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| assists | 43 | 0.581 | 0.497 | 0.536 | -10.4% |
| points | 56 | 0.607 | 0.504 | 0.555 | -6.9% |
| rebounds | 54 | 0.537 | 0.481 | 0.528 | +4.9% |
| threes | 48 | 0.521 | 0.458 | 0.485 | +6.8% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 6 | 0.233 | 0.167 | 0.382 |
| (0.3, 0.4] | 19 | 0.366 | 0.526 | 0.439 |
| (0.4, 0.5] | 59 | 0.444 | 0.525 | 0.466 |
| (0.5, 0.6] | 65 | 0.548 | 0.600 | 0.494 |
| (0.6, 0.7] | 31 | 0.644 | 0.710 | 0.532 |
| (0.7, 1.0] | 21 | 0.753 | 0.476 | 0.515 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 20 | 0.500 | 0.496 | +0.4 pts |
| (-0.1, -0.05] | 18 | 0.333 | 0.491 | -15.8 pts |
| (-0.05, 0.0] | 28 | 0.500 | 0.489 | +1.1 pts |
| (0.0, 0.05] | 46 | 0.674 | 0.479 | +19.5 pts |
| (0.05, 0.1] | 39 | 0.564 | 0.480 | +8.4 pts |
| (0.1, 1.0] | 50 | 0.600 | 0.487 | +11.3 pts |

Noise check: with 201 props one standard error on a hit rate is about ±3.5 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.
