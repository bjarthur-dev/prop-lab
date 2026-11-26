---
tags: [record, shadow]
---

# Shadow grading: every priced prop vs result and market

Written by `engine/shadow.py` (morning settlement runs it). Rules §9 uses this to decide when the model-health gate relaxes and when NFL/MLB go live.

## NBA
Graded props: **8777** over 33 day(s). Over hit rate 0.484 vs market's average 0.493 vs model's 0.457.
Brier: model 0.2539 · market 0.2468 · blend 0.2476 → **model skill vs market -2.9%**, blend skill -0.4% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| ast | 2007 | 0.492 | 0.495 | 0.458 | -2.3% |
| fg3m | 1583 | 0.488 | 0.485 | 0.451 | -2.4% |
| pts | 2606 | 0.478 | 0.498 | 0.453 | -4.3% |
| reb | 2581 | 0.482 | 0.490 | 0.464 | -2.2% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 538 | 0.252 | 0.442 | 0.466 |
| (0.3, 0.4] | 1980 | 0.359 | 0.456 | 0.464 |
| (0.4, 0.5] | 3341 | 0.451 | 0.466 | 0.486 |
| (0.5, 0.6] | 2235 | 0.543 | 0.523 | 0.518 |
| (0.6, 0.7] | 584 | 0.638 | 0.557 | 0.544 |
| (0.7, 1.0] | 99 | 0.734 | 0.556 | 0.553 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 1887 | 0.479 | 0.496 | -1.7 pts |
| (-0.1, -0.05] | 1751 | 0.481 | 0.493 | -1.2 pts |
| (-0.05, 0.0] | 2138 | 0.470 | 0.492 | -2.2 pts |
| (0.0, 0.05] | 1659 | 0.499 | 0.492 | +0.7 pts |
| (0.05, 0.1] | 862 | 0.491 | 0.488 | +0.3 pts |
| (0.1, 1.0] | 480 | 0.515 | 0.491 | +2.4 pts |

Noise check: with 8777 props one standard error on a hit rate is about ±0.5 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

## NFL
Graded props: **1945** over 7 day(s). Over hit rate 0.492 vs market's average 0.495 vs model's 0.476.
Brier: model 0.2650 · market 0.2479 · blend 0.2489 → **model skill vs market -6.9%**, blend skill -0.4% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| carries | 107 | 0.439 | 0.496 | 0.459 | -24.2% |
| rec_yds | 918 | 0.497 | 0.500 | 0.482 | -2.5% |
| receptions | 644 | 0.489 | 0.486 | 0.462 | -3.8% |
| rush_yds | 276 | 0.504 | 0.499 | 0.497 | -21.9% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 173 | 0.238 | 0.514 | 0.468 |
| (0.3, 0.4] | 400 | 0.356 | 0.477 | 0.485 |
| (0.4, 0.5] | 563 | 0.454 | 0.483 | 0.495 |
| (0.5, 0.6] | 489 | 0.548 | 0.472 | 0.501 |
| (0.6, 0.7] | 207 | 0.644 | 0.507 | 0.509 |
| (0.7, 1.0] | 113 | 0.763 | 0.611 | 0.521 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 530 | 0.498 | 0.495 | +0.3 pts |
| (-0.1, -0.05] | 258 | 0.457 | 0.496 | -3.9 pts |
| (-0.05, 0.0] | 335 | 0.507 | 0.499 | +0.8 pts |
| (0.0, 0.05] | 273 | 0.454 | 0.492 | -3.8 pts |
| (0.05, 0.1] | 225 | 0.538 | 0.496 | +4.2 pts |
| (0.1, 1.0] | 324 | 0.494 | 0.490 | +0.4 pts |

Noise check: with 1945 props one standard error on a hit rate is about ±1.1 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

## NBA matchup engine v1 (context vs market)
Graded props: **10312** over 29 day(s). Over hit rate 0.482 vs market's average 0.490 vs model's 0.481.
Brier: model 0.2548 · market 0.2456 · blend 0.2460 → **model skill vs market -3.8%**, blend skill -0.1% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| assists | 2388 | 0.495 | 0.492 | 0.485 | -2.7% |
| points | 2945 | 0.479 | 0.501 | 0.489 | -5.6% |
| rebounds | 2781 | 0.477 | 0.489 | 0.487 | -3.9% |
| threes | 2198 | 0.478 | 0.477 | 0.458 | -2.2% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 662 | 0.235 | 0.411 | 0.432 |
| (0.3, 0.4] | 1813 | 0.358 | 0.425 | 0.451 |
| (0.4, 0.5] | 3216 | 0.452 | 0.474 | 0.482 |
| (0.5, 0.6] | 3050 | 0.547 | 0.516 | 0.510 |
| (0.6, 0.7] | 1287 | 0.639 | 0.517 | 0.538 |
| (0.7, 1.0] | 284 | 0.748 | 0.570 | 0.537 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 1693 | 0.473 | 0.487 | -1.4 pts |
| (-0.1, -0.05] | 1605 | 0.464 | 0.488 | -2.4 pts |
| (-0.05, 0.0] | 2205 | 0.488 | 0.489 | -0.1 pts |
| (0.0, 0.05] | 2068 | 0.484 | 0.492 | -0.8 pts |
| (0.05, 0.1] | 1487 | 0.487 | 0.495 | -0.8 pts |
| (0.1, 1.0] | 1254 | 0.498 | 0.491 | +0.7 pts |

Noise check: with 10312 props one standard error on a hit rate is about ±0.5 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

(price-edge grading failed: 'DataFrame' object has no attribute 'over')

(steam grading failed: 'DataFrame' object has no attribute 'over')
