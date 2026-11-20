---
tags: [record, shadow]
---

# Shadow grading: every priced prop vs result and market

Written by `engine/shadow.py` (morning settlement runs it). Rules §9 uses this to decide when the model-health gate relaxes and when NFL/MLB go live.

## NBA
Graded props: **7085** over 27 day(s). Over hit rate 0.480 vs market's average 0.493 vs model's 0.457.
Brier: model 0.2542 · market 0.2468 · blend 0.2481 → **model skill vs market -3.0%**, blend skill -0.5% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| ast | 1642 | 0.484 | 0.495 | 0.457 | -2.3% |
| fg3m | 1194 | 0.492 | 0.484 | 0.451 | -2.9% |
| pts | 2120 | 0.475 | 0.498 | 0.453 | -4.3% |
| reb | 2129 | 0.476 | 0.490 | 0.464 | -2.2% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 450 | 0.250 | 0.458 | 0.467 |
| (0.3, 0.4] | 1583 | 0.359 | 0.449 | 0.465 |
| (0.4, 0.5] | 2662 | 0.450 | 0.463 | 0.486 |
| (0.5, 0.6] | 1832 | 0.543 | 0.517 | 0.517 |
| (0.6, 0.7] | 478 | 0.639 | 0.554 | 0.542 |
| (0.7, 1.0] | 80 | 0.735 | 0.537 | 0.545 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 1549 | 0.479 | 0.496 | -1.7 pts |
| (-0.1, -0.05] | 1394 | 0.474 | 0.493 | -1.9 pts |
| (-0.05, 0.0] | 1707 | 0.465 | 0.492 | -2.7 pts |
| (0.0, 0.05] | 1319 | 0.492 | 0.492 | +0.0 pts |
| (0.05, 0.1] | 704 | 0.491 | 0.488 | +0.3 pts |
| (0.1, 1.0] | 412 | 0.515 | 0.489 | +2.6 pts |

Noise check: with 7085 props one standard error on a hit rate is about ±0.6 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

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
Graded props: **8296** over 23 day(s). Over hit rate 0.478 vs market's average 0.490 vs model's 0.481.
Brier: model 0.2556 · market 0.2458 · blend 0.2463 → **model skill vs market -4.0%**, blend skill -0.2% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| assists | 1934 | 0.488 | 0.491 | 0.484 | -3.1% |
| points | 2359 | 0.475 | 0.501 | 0.491 | -6.0% |
| rebounds | 2246 | 0.471 | 0.489 | 0.488 | -4.0% |
| threes | 1757 | 0.480 | 0.475 | 0.457 | -2.1% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 545 | 0.234 | 0.420 | 0.434 |
| (0.3, 0.4] | 1448 | 0.358 | 0.421 | 0.451 |
| (0.4, 0.5] | 2555 | 0.452 | 0.470 | 0.482 |
| (0.5, 0.6] | 2480 | 0.547 | 0.513 | 0.510 |
| (0.6, 0.7] | 1039 | 0.639 | 0.507 | 0.536 |
| (0.7, 1.0] | 229 | 0.748 | 0.555 | 0.532 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 1356 | 0.475 | 0.488 | -1.3 pts |
| (-0.1, -0.05] | 1274 | 0.456 | 0.488 | -3.2 pts |
| (-0.05, 0.0] | 1764 | 0.484 | 0.488 | -0.4 pts |
| (0.0, 0.05] | 1646 | 0.482 | 0.492 | -1.0 pts |
| (0.05, 0.1] | 1210 | 0.477 | 0.494 | -1.7 pts |
| (0.1, 1.0] | 1046 | 0.492 | 0.489 | +0.3 pts |

Noise check: with 8296 props one standard error on a hit rate is about ±0.5 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

(price-edge grading failed: 'DataFrame' object has no attribute 'over')

(steam grading failed: 'DataFrame' object has no attribute 'over')
