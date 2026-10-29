---
tags: [record, shadow]
---

# Shadow grading: every priced prop vs result and market

Written by `engine/shadow.py` (morning settlement runs it). Rules §9 uses this to decide when the model-health gate relaxes and when NFL/MLB go live.

## NBA
Graded props: **1346** over 6 day(s). Over hit rate 0.490 vs market's average 0.493 vs model's 0.465.
Brier: model 0.2537 · market 0.2439 · blend 0.2415 → **model skill vs market -4.0%**, blend skill +1.0% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| ast | 325 | 0.477 | 0.492 | 0.459 | -5.5% |
| fg3m | 101 | 0.455 | 0.474 | 0.457 | -2.9% |
| pts | 475 | 0.501 | 0.499 | 0.463 | -4.9% |
| reb | 445 | 0.497 | 0.493 | 0.472 | -2.2% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 90 | 0.250 | 0.478 | 0.481 |
| (0.3, 0.4] | 242 | 0.358 | 0.467 | 0.469 |
| (0.4, 0.5] | 529 | 0.450 | 0.473 | 0.487 |
| (0.5, 0.6] | 349 | 0.542 | 0.481 | 0.509 |
| (0.6, 0.7] | 116 | 0.638 | 0.638 | 0.532 |
| (0.7, 1.0] | 20 | 0.728 | 0.600 | 0.525 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 279 | 0.498 | 0.498 | -0.0 pts |
| (-0.1, -0.05] | 253 | 0.514 | 0.496 | +1.8 pts |
| (-0.05, 0.0] | 293 | 0.464 | 0.492 | -2.7 pts |
| (0.0, 0.05] | 261 | 0.475 | 0.490 | -1.5 pts |
| (0.05, 0.1] | 154 | 0.468 | 0.492 | -2.5 pts |
| (0.1, 1.0] | 106 | 0.557 | 0.489 | +6.8 pts |

Noise check: with 1346 props one standard error on a hit rate is about ±1.4 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

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
Graded props: **795** over 2 day(s). Over hit rate 0.484 vs market's average 0.488 vs model's 0.488.
Brier: model 0.2614 · market 0.2461 · blend 0.2472 → **model skill vs market -6.2%**, blend skill -0.5% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| assists | 167 | 0.479 | 0.493 | 0.508 | -5.9% |
| points | 239 | 0.473 | 0.505 | 0.505 | -9.5% |
| rebounds | 207 | 0.531 | 0.483 | 0.481 | -5.2% |
| threes | 182 | 0.451 | 0.464 | 0.456 | -3.4% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 67 | 0.224 | 0.433 | 0.435 |
| (0.3, 0.4] | 129 | 0.359 | 0.434 | 0.455 |
| (0.4, 0.5] | 220 | 0.454 | 0.500 | 0.482 |
| (0.5, 0.6] | 218 | 0.548 | 0.482 | 0.501 |
| (0.6, 0.7] | 120 | 0.643 | 0.542 | 0.523 |
| (0.7, 1.0] | 41 | 0.746 | 0.488 | 0.527 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 150 | 0.473 | 0.488 | -1.4 pts |
| (-0.1, -0.05] | 92 | 0.467 | 0.481 | -1.4 pts |
| (-0.05, 0.0] | 142 | 0.479 | 0.490 | -1.1 pts |
| (0.0, 0.05] | 137 | 0.547 | 0.487 | +6.1 pts |
| (0.05, 0.1] | 116 | 0.474 | 0.487 | -1.2 pts |
| (0.1, 1.0] | 158 | 0.462 | 0.491 | -2.9 pts |

Noise check: with 795 props one standard error on a hit rate is about ±1.8 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.
