---
tags: [record, shadow]
---

# Shadow grading: every priced prop vs result and market

Written by `engine/shadow.py` (morning settlement runs it). Rules §9 uses this to decide when the model-health gate relaxes and when NFL/MLB go live.

## NBA
Graded props: **7644** over 29 day(s). Over hit rate 0.481 vs market's average 0.493 vs model's 0.456.
Brier: model 0.2539 · market 0.2466 · blend 0.2474 → **model skill vs market -3.0%**, blend skill -0.3% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| ast | 1772 | 0.484 | 0.495 | 0.457 | -2.0% |
| fg3m | 1319 | 0.489 | 0.484 | 0.450 | -2.8% |
| pts | 2276 | 0.475 | 0.498 | 0.452 | -4.3% |
| reb | 2277 | 0.479 | 0.491 | 0.464 | -2.5% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 484 | 0.251 | 0.444 | 0.467 |
| (0.3, 0.4] | 1727 | 0.359 | 0.450 | 0.464 |
| (0.4, 0.5] | 2877 | 0.450 | 0.464 | 0.486 |
| (0.5, 0.6] | 1964 | 0.543 | 0.520 | 0.518 |
| (0.6, 0.7] | 507 | 0.639 | 0.554 | 0.543 |
| (0.7, 1.0] | 85 | 0.735 | 0.529 | 0.546 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 1669 | 0.480 | 0.496 | -1.6 pts |
| (-0.1, -0.05] | 1518 | 0.479 | 0.493 | -1.4 pts |
| (-0.05, 0.0] | 1848 | 0.464 | 0.492 | -2.9 pts |
| (0.0, 0.05] | 1433 | 0.492 | 0.491 | +0.1 pts |
| (0.05, 0.1] | 745 | 0.490 | 0.488 | +0.2 pts |
| (0.1, 1.0] | 431 | 0.513 | 0.489 | +2.4 pts |

Noise check: with 7644 props one standard error on a hit rate is about ±0.6 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

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
Graded props: **9063** over 25 day(s). Over hit rate 0.478 vs market's average 0.490 vs model's 0.480.
Brier: model 0.2551 · market 0.2455 · blend 0.2459 → **model skill vs market -3.9%**, blend skill -0.2% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| assists | 2108 | 0.488 | 0.491 | 0.483 | -2.8% |
| points | 2589 | 0.475 | 0.501 | 0.489 | -5.9% |
| rebounds | 2446 | 0.473 | 0.489 | 0.486 | -4.1% |
| threes | 1920 | 0.476 | 0.475 | 0.456 | -2.0% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 606 | 0.233 | 0.408 | 0.433 |
| (0.3, 0.4] | 1597 | 0.358 | 0.422 | 0.451 |
| (0.4, 0.5] | 2816 | 0.452 | 0.471 | 0.482 |
| (0.5, 0.6] | 2682 | 0.547 | 0.513 | 0.510 |
| (0.6, 0.7] | 1122 | 0.639 | 0.508 | 0.537 |
| (0.7, 1.0] | 240 | 0.748 | 0.567 | 0.532 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 1499 | 0.470 | 0.487 | -1.7 pts |
| (-0.1, -0.05] | 1412 | 0.458 | 0.488 | -3.0 pts |
| (-0.05, 0.0] | 1934 | 0.487 | 0.488 | -0.1 pts |
| (0.0, 0.05] | 1805 | 0.483 | 0.492 | -1.0 pts |
| (0.05, 0.1] | 1308 | 0.478 | 0.494 | -1.6 pts |
| (0.1, 1.0] | 1105 | 0.489 | 0.489 | -0.1 pts |

Noise check: with 9063 props one standard error on a hit rate is about ±0.5 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

(price-edge grading failed: 'DataFrame' object has no attribute 'over')

(steam grading failed: 'DataFrame' object has no attribute 'over')
