---
tags: [record, shadow]
---

# Shadow grading: every priced prop vs result and market

Written by `engine/shadow.py` (morning settlement runs it). Rules §9 uses this to decide when the model-health gate relaxes and when NFL/MLB go live.

## NBA
Graded props: **6238** over 24 day(s). Over hit rate 0.480 vs market's average 0.493 vs model's 0.458.
Brier: model 0.2536 · market 0.2469 · blend 0.2466 → **model skill vs market -2.7%**, blend skill +0.1% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| ast | 1445 | 0.478 | 0.496 | 0.458 | -2.1% |
| fg3m | 1040 | 0.489 | 0.484 | 0.453 | -2.2% |
| pts | 1860 | 0.474 | 0.498 | 0.455 | -4.0% |
| reb | 1893 | 0.483 | 0.491 | 0.465 | -2.2% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 370 | 0.252 | 0.462 | 0.467 |
| (0.3, 0.4] | 1386 | 0.359 | 0.449 | 0.465 |
| (0.4, 0.5] | 2364 | 0.450 | 0.461 | 0.486 |
| (0.5, 0.6] | 1633 | 0.543 | 0.511 | 0.517 |
| (0.6, 0.7] | 416 | 0.639 | 0.575 | 0.543 |
| (0.7, 1.0] | 69 | 0.732 | 0.565 | 0.547 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 1323 | 0.479 | 0.496 | -1.7 pts |
| (-0.1, -0.05] | 1241 | 0.477 | 0.494 | -1.7 pts |
| (-0.05, 0.0] | 1520 | 0.458 | 0.493 | -3.5 pts |
| (0.0, 0.05] | 1166 | 0.488 | 0.491 | -0.3 pts |
| (0.05, 0.1] | 626 | 0.506 | 0.489 | +1.8 pts |
| (0.1, 1.0] | 362 | 0.519 | 0.488 | +3.1 pts |

Noise check: with 6238 props one standard error on a hit rate is about ±0.6 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

## NFL
Graded props: **1490** over 5 day(s). Over hit rate 0.485 vs market's average 0.495 vs model's 0.471.
Brier: model 0.2670 · market 0.2477 · blend 0.2492 → **model skill vs market -7.8%**, blend skill -0.6% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| carries | 75 | 0.453 | 0.497 | 0.466 | -30.2% |
| rec_yds | 712 | 0.487 | 0.500 | 0.479 | -2.6% |
| receptions | 484 | 0.488 | 0.486 | 0.452 | -4.1% |
| rush_yds | 219 | 0.484 | 0.498 | 0.492 | -24.9% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 145 | 0.240 | 0.538 | 0.466 |
| (0.3, 0.4] | 319 | 0.355 | 0.470 | 0.487 |
| (0.4, 0.5] | 423 | 0.453 | 0.468 | 0.496 |
| (0.5, 0.6] | 370 | 0.548 | 0.468 | 0.502 |
| (0.6, 0.7] | 152 | 0.645 | 0.526 | 0.509 |
| (0.7, 1.0] | 81 | 0.762 | 0.543 | 0.519 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 437 | 0.499 | 0.495 | +0.4 pts |
| (-0.1, -0.05] | 202 | 0.421 | 0.496 | -7.6 pts |
| (-0.05, 0.0] | 246 | 0.512 | 0.499 | +1.3 pts |
| (0.0, 0.05] | 200 | 0.420 | 0.494 | -7.4 pts |
| (0.05, 0.1] | 175 | 0.566 | 0.496 | +6.9 pts |
| (0.1, 1.0] | 230 | 0.483 | 0.492 | -0.9 pts |

Noise check: with 1490 props one standard error on a hit rate is about ±1.3 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

## NBA matchup engine v1 (context vs market)
Graded props: **7166** over 20 day(s). Over hit rate 0.477 vs market's average 0.489 vs model's 0.482.
Brier: model 0.2559 · market 0.2459 · blend 0.2464 → **model skill vs market -4.1%**, blend skill -0.2% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| assists | 1674 | 0.481 | 0.491 | 0.487 | -3.7% |
| points | 2021 | 0.469 | 0.501 | 0.493 | -6.2% |
| rebounds | 1949 | 0.482 | 0.489 | 0.488 | -4.0% |
| threes | 1522 | 0.476 | 0.473 | 0.456 | -1.7% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 481 | 0.232 | 0.430 | 0.433 |
| (0.3, 0.4] | 1232 | 0.358 | 0.417 | 0.450 |
| (0.4, 0.5] | 2172 | 0.453 | 0.462 | 0.482 |
| (0.5, 0.6] | 2162 | 0.547 | 0.519 | 0.509 |
| (0.6, 0.7] | 908 | 0.639 | 0.499 | 0.535 |
| (0.7, 1.0] | 211 | 0.751 | 0.555 | 0.530 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 1159 | 0.479 | 0.487 | -0.8 pts |
| (-0.1, -0.05] | 1072 | 0.455 | 0.488 | -3.2 pts |
| (-0.05, 0.0] | 1518 | 0.475 | 0.488 | -1.3 pts |
| (0.0, 0.05] | 1414 | 0.475 | 0.492 | -1.7 pts |
| (0.05, 0.1] | 1062 | 0.486 | 0.493 | -0.7 pts |
| (0.1, 1.0] | 941 | 0.495 | 0.489 | +0.6 pts |

Noise check: with 7166 props one standard error on a hit rate is about ±0.6 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

(steam grading failed: 'DataFrame' object has no attribute 'over')
