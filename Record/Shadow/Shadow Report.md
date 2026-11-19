---
tags: [record, shadow]
---

# Shadow grading: every priced prop vs result and market

Written by `engine/shadow.py` (morning settlement runs it). Rules §9 uses this to decide when the model-health gate relaxes and when NFL/MLB go live.

## NBA
Graded props: **6961** over 26 day(s). Over hit rate 0.481 vs market's average 0.493 vs model's 0.457.
Brier: model 0.2541 · market 0.2469 · blend 0.2481 → **model skill vs market -2.9%**, blend skill -0.5% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| ast | 1604 | 0.484 | 0.496 | 0.457 | -2.1% |
| fg3m | 1194 | 0.492 | 0.484 | 0.451 | -2.9% |
| pts | 2077 | 0.474 | 0.498 | 0.452 | -4.3% |
| reb | 2086 | 0.478 | 0.490 | 0.464 | -2.2% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 448 | 0.250 | 0.455 | 0.467 |
| (0.3, 0.4] | 1555 | 0.359 | 0.450 | 0.464 |
| (0.4, 0.5] | 2619 | 0.450 | 0.463 | 0.486 |
| (0.5, 0.6] | 1796 | 0.543 | 0.517 | 0.518 |
| (0.6, 0.7] | 466 | 0.639 | 0.556 | 0.543 |
| (0.7, 1.0] | 77 | 0.733 | 0.545 | 0.546 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 1527 | 0.479 | 0.496 | -1.7 pts |
| (-0.1, -0.05] | 1372 | 0.474 | 0.493 | -2.0 pts |
| (-0.05, 0.0] | 1682 | 0.466 | 0.492 | -2.7 pts |
| (0.0, 0.05] | 1291 | 0.491 | 0.492 | -0.1 pts |
| (0.05, 0.1] | 689 | 0.492 | 0.488 | +0.4 pts |
| (0.1, 1.0] | 400 | 0.517 | 0.489 | +2.9 pts |

Noise check: with 6961 props one standard error on a hit rate is about ±0.6 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

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
Graded props: **8067** over 22 day(s). Over hit rate 0.478 vs market's average 0.490 vs model's 0.481.
Brier: model 0.2554 · market 0.2458 · blend 0.2462 → **model skill vs market -3.9%**, blend skill -0.2% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| assists | 1886 | 0.487 | 0.491 | 0.485 | -3.0% |
| points | 2289 | 0.474 | 0.501 | 0.491 | -6.1% |
| rebounds | 2182 | 0.474 | 0.489 | 0.486 | -3.8% |
| threes | 1710 | 0.480 | 0.475 | 0.457 | -2.0% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 537 | 0.234 | 0.423 | 0.434 |
| (0.3, 0.4] | 1409 | 0.358 | 0.417 | 0.450 |
| (0.4, 0.5] | 2478 | 0.452 | 0.469 | 0.482 |
| (0.5, 0.6] | 2410 | 0.547 | 0.516 | 0.510 |
| (0.6, 0.7] | 1010 | 0.639 | 0.507 | 0.536 |
| (0.7, 1.0] | 223 | 0.749 | 0.561 | 0.532 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 1325 | 0.473 | 0.488 | -1.4 pts |
| (-0.1, -0.05] | 1243 | 0.457 | 0.488 | -3.1 pts |
| (-0.05, 0.0] | 1715 | 0.481 | 0.488 | -0.7 pts |
| (0.0, 0.05] | 1589 | 0.483 | 0.492 | -1.0 pts |
| (0.05, 0.1] | 1175 | 0.481 | 0.494 | -1.3 pts |
| (0.1, 1.0] | 1020 | 0.496 | 0.489 | +0.7 pts |

Noise check: with 8067 props one standard error on a hit rate is about ±0.6 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

(price-edge grading failed: 'DataFrame' object has no attribute 'over')

(steam grading failed: 'DataFrame' object has no attribute 'over')
