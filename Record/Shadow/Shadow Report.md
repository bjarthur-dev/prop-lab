---
tags: [record, shadow]
---

# Shadow grading: every priced prop vs result and market

Written by `engine/shadow.py` (morning settlement runs it). Rules §9 uses this to decide when the model-health gate relaxes and when NFL/MLB go live.

## NBA
Graded props: **7471** over 28 day(s). Over hit rate 0.481 vs market's average 0.493 vs model's 0.457.
Brier: model 0.2538 · market 0.2467 · blend 0.2474 → **model skill vs market -2.9%**, blend skill -0.3% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| ast | 1730 | 0.485 | 0.495 | 0.457 | -2.1% |
| fg3m | 1282 | 0.491 | 0.484 | 0.450 | -2.8% |
| pts | 2228 | 0.477 | 0.498 | 0.453 | -4.0% |
| reb | 2231 | 0.476 | 0.490 | 0.464 | -2.4% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 471 | 0.250 | 0.448 | 0.467 |
| (0.3, 0.4] | 1684 | 0.359 | 0.448 | 0.464 |
| (0.4, 0.5] | 2806 | 0.450 | 0.465 | 0.486 |
| (0.5, 0.6] | 1929 | 0.543 | 0.519 | 0.518 |
| (0.6, 0.7] | 499 | 0.639 | 0.555 | 0.543 |
| (0.7, 1.0] | 82 | 0.734 | 0.549 | 0.546 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 1628 | 0.478 | 0.496 | -1.8 pts |
| (-0.1, -0.05] | 1480 | 0.480 | 0.493 | -1.3 pts |
| (-0.05, 0.0] | 1801 | 0.464 | 0.492 | -2.8 pts |
| (0.0, 0.05] | 1402 | 0.491 | 0.492 | -0.0 pts |
| (0.05, 0.1] | 737 | 0.491 | 0.488 | +0.3 pts |
| (0.1, 1.0] | 423 | 0.518 | 0.489 | +2.9 pts |

Noise check: with 7471 props one standard error on a hit rate is about ±0.6 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

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
Graded props: **8754** over 24 day(s). Over hit rate 0.478 vs market's average 0.490 vs model's 0.481.
Brier: model 0.2552 · market 0.2456 · blend 0.2460 → **model skill vs market -3.9%**, blend skill -0.2% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| assists | 2040 | 0.491 | 0.491 | 0.484 | -2.9% |
| points | 2495 | 0.475 | 0.501 | 0.490 | -5.8% |
| rebounds | 2367 | 0.470 | 0.489 | 0.486 | -4.1% |
| threes | 1852 | 0.479 | 0.475 | 0.457 | -2.0% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 572 | 0.234 | 0.416 | 0.433 |
| (0.3, 0.4] | 1540 | 0.358 | 0.420 | 0.450 |
| (0.4, 0.5] | 2712 | 0.452 | 0.470 | 0.482 |
| (0.5, 0.6] | 2602 | 0.547 | 0.513 | 0.510 |
| (0.6, 0.7] | 1091 | 0.639 | 0.509 | 0.537 |
| (0.7, 1.0] | 237 | 0.748 | 0.565 | 0.532 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 1429 | 0.475 | 0.487 | -1.2 pts |
| (-0.1, -0.05] | 1365 | 0.453 | 0.488 | -3.4 pts |
| (-0.05, 0.0] | 1868 | 0.487 | 0.488 | -0.1 pts |
| (0.0, 0.05] | 1740 | 0.480 | 0.492 | -1.3 pts |
| (0.05, 0.1] | 1274 | 0.480 | 0.494 | -1.4 pts |
| (0.1, 1.0] | 1078 | 0.492 | 0.490 | +0.2 pts |

Noise check: with 8754 props one standard error on a hit rate is about ±0.5 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

(price-edge grading failed: 'DataFrame' object has no attribute 'over')

(steam grading failed: 'DataFrame' object has no attribute 'over')
