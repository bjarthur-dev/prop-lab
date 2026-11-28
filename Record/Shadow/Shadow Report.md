---
tags: [record, shadow]
---

# Shadow grading: every priced prop vs result and market

Written by `engine/shadow.py` (morning settlement runs it). Rules §9 uses this to decide when the model-health gate relaxes and when NFL/MLB go live.

## NBA
Graded props: **9289** over 34 day(s). Over hit rate 0.484 vs market's average 0.493 vs model's 0.457.
Brier: model 0.2538 · market 0.2467 · blend 0.2473 → **model skill vs market -2.9%**, blend skill -0.3% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| ast | 2130 | 0.491 | 0.495 | 0.457 | -2.3% |
| fg3m | 1702 | 0.488 | 0.485 | 0.452 | -2.2% |
| pts | 2744 | 0.477 | 0.498 | 0.452 | -4.4% |
| reb | 2713 | 0.483 | 0.490 | 0.464 | -2.2% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 595 | 0.251 | 0.439 | 0.465 |
| (0.3, 0.4] | 2090 | 0.359 | 0.456 | 0.464 |
| (0.4, 0.5] | 3507 | 0.451 | 0.464 | 0.486 |
| (0.5, 0.6] | 2364 | 0.543 | 0.524 | 0.518 |
| (0.6, 0.7] | 628 | 0.638 | 0.561 | 0.546 |
| (0.7, 1.0] | 105 | 0.734 | 0.562 | 0.554 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 2034 | 0.478 | 0.496 | -1.8 pts |
| (-0.1, -0.05] | 1829 | 0.476 | 0.493 | -1.7 pts |
| (-0.05, 0.0] | 2234 | 0.471 | 0.492 | -2.1 pts |
| (0.0, 0.05] | 1766 | 0.501 | 0.492 | +0.9 pts |
| (0.05, 0.1] | 917 | 0.494 | 0.489 | +0.5 pts |
| (0.1, 1.0] | 509 | 0.511 | 0.490 | +2.1 pts |

Noise check: with 9289 props one standard error on a hit rate is about ±0.5 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

## NFL
Graded props: **2004** over 8 day(s). Over hit rate 0.488 vs market's average 0.495 vs model's 0.476.
Brier: model 0.2640 · market 0.2475 · blend 0.2484 → **model skill vs market -6.7%**, blend skill -0.4% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| carries | 111 | 0.441 | 0.496 | 0.453 | -23.4% |
| rec_yds | 942 | 0.494 | 0.500 | 0.482 | -2.3% |
| receptions | 668 | 0.481 | 0.485 | 0.462 | -3.9% |
| rush_yds | 283 | 0.505 | 0.498 | 0.496 | -21.1% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 177 | 0.237 | 0.508 | 0.469 |
| (0.3, 0.4] | 411 | 0.356 | 0.470 | 0.485 |
| (0.4, 0.5] | 585 | 0.454 | 0.477 | 0.494 |
| (0.5, 0.6] | 509 | 0.548 | 0.473 | 0.500 |
| (0.6, 0.7] | 208 | 0.644 | 0.510 | 0.509 |
| (0.7, 1.0] | 114 | 0.763 | 0.605 | 0.522 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 544 | 0.493 | 0.495 | -0.2 pts |
| (-0.1, -0.05] | 263 | 0.456 | 0.497 | -4.0 pts |
| (-0.05, 0.0] | 348 | 0.503 | 0.499 | +0.4 pts |
| (0.0, 0.05] | 284 | 0.447 | 0.492 | -4.5 pts |
| (0.05, 0.1] | 234 | 0.543 | 0.496 | +4.7 pts |
| (0.1, 1.0] | 331 | 0.486 | 0.490 | -0.3 pts |

Noise check: with 2004 props one standard error on a hit rate is about ±1.1 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

## NBA matchup engine v1 (context vs market)
Graded props: **10894** over 30 day(s). Over hit rate 0.481 vs market's average 0.491 vs model's 0.481.
Brier: model 0.2546 · market 0.2454 · blend 0.2458 → **model skill vs market -3.7%**, blend skill -0.1% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| assists | 2531 | 0.494 | 0.493 | 0.485 | -2.8% |
| points | 3109 | 0.477 | 0.500 | 0.488 | -5.6% |
| rebounds | 2926 | 0.479 | 0.489 | 0.488 | -3.9% |
| threes | 2328 | 0.476 | 0.477 | 0.459 | -2.0% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 698 | 0.235 | 0.413 | 0.431 |
| (0.3, 0.4] | 1916 | 0.358 | 0.426 | 0.451 |
| (0.4, 0.5] | 3396 | 0.452 | 0.469 | 0.482 |
| (0.5, 0.6] | 3223 | 0.547 | 0.518 | 0.511 |
| (0.6, 0.7] | 1361 | 0.638 | 0.519 | 0.539 |
| (0.7, 1.0] | 300 | 0.747 | 0.577 | 0.539 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 1784 | 0.478 | 0.487 | -0.9 pts |
| (-0.1, -0.05] | 1686 | 0.461 | 0.488 | -2.8 pts |
| (-0.05, 0.0] | 2358 | 0.485 | 0.489 | -0.4 pts |
| (0.0, 0.05] | 2193 | 0.482 | 0.493 | -1.1 pts |
| (0.05, 0.1] | 1564 | 0.488 | 0.495 | -0.8 pts |
| (0.1, 1.0] | 1309 | 0.500 | 0.491 | +0.8 pts |

Noise check: with 10894 props one standard error on a hit rate is about ±0.5 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

(price-edge grading failed: 'DataFrame' object has no attribute 'over')

(steam grading failed: 'DataFrame' object has no attribute 'over')
