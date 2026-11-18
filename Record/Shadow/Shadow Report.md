---
tags: [record, shadow]
---

# Shadow grading: every priced prop vs result and market

Written by `engine/shadow.py` (morning settlement runs it). Rules §9 uses this to decide when the model-health gate relaxes and when NFL/MLB go live.

## NBA
Graded props: **6452** over 25 day(s). Over hit rate 0.482 vs market's average 0.493 vs model's 0.459.
Brier: model 0.2540 · market 0.2469 · blend 0.2475 → **model skill vs market -2.9%**, blend skill -0.3% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| ast | 1490 | 0.483 | 0.496 | 0.459 | -2.1% |
| fg3m | 1089 | 0.490 | 0.485 | 0.454 | -2.5% |
| pts | 1922 | 0.475 | 0.498 | 0.456 | -4.3% |
| reb | 1951 | 0.483 | 0.491 | 0.466 | -2.2% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 375 | 0.252 | 0.464 | 0.467 |
| (0.3, 0.4] | 1422 | 0.359 | 0.449 | 0.464 |
| (0.4, 0.5] | 2436 | 0.450 | 0.463 | 0.486 |
| (0.5, 0.6] | 1703 | 0.543 | 0.515 | 0.517 |
| (0.6, 0.7] | 443 | 0.640 | 0.564 | 0.543 |
| (0.7, 1.0] | 73 | 0.732 | 0.548 | 0.546 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 1353 | 0.482 | 0.496 | -1.5 pts |
| (-0.1, -0.05] | 1275 | 0.478 | 0.494 | -1.6 pts |
| (-0.05, 0.0] | 1566 | 0.464 | 0.493 | -2.9 pts |
| (0.0, 0.05] | 1223 | 0.490 | 0.492 | -0.2 pts |
| (0.05, 0.1] | 652 | 0.502 | 0.489 | +1.3 pts |
| (0.1, 1.0] | 383 | 0.512 | 0.489 | +2.3 pts |

Noise check: with 6452 props one standard error on a hit rate is about ±0.6 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

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
Graded props: **7433** over 21 day(s). Over hit rate 0.478 vs market's average 0.490 vs model's 0.482.
Brier: model 0.2559 · market 0.2459 · blend 0.2463 → **model skill vs market -4.1%**, blend skill -0.2% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| assists | 1738 | 0.484 | 0.491 | 0.486 | -3.6% |
| points | 2098 | 0.470 | 0.501 | 0.492 | -6.2% |
| rebounds | 2018 | 0.482 | 0.490 | 0.488 | -3.9% |
| threes | 1579 | 0.477 | 0.473 | 0.456 | -1.9% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 498 | 0.233 | 0.430 | 0.433 |
| (0.3, 0.4] | 1293 | 0.358 | 0.419 | 0.451 |
| (0.4, 0.5] | 2261 | 0.453 | 0.465 | 0.482 |
| (0.5, 0.6] | 2225 | 0.547 | 0.518 | 0.509 |
| (0.6, 0.7] | 943 | 0.639 | 0.504 | 0.536 |
| (0.7, 1.0] | 213 | 0.751 | 0.554 | 0.530 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 1215 | 0.479 | 0.487 | -0.8 pts |
| (-0.1, -0.05] | 1122 | 0.457 | 0.488 | -3.0 pts |
| (-0.05, 0.0] | 1577 | 0.476 | 0.488 | -1.2 pts |
| (0.0, 0.05] | 1464 | 0.480 | 0.492 | -1.3 pts |
| (0.05, 0.1] | 1089 | 0.484 | 0.493 | -0.9 pts |
| (0.1, 1.0] | 966 | 0.496 | 0.489 | +0.7 pts |

Noise check: with 7433 props one standard error on a hit rate is about ±0.6 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

(price-edge grading failed: 'DataFrame' object has no attribute 'over')

(steam grading failed: 'DataFrame' object has no attribute 'over')
