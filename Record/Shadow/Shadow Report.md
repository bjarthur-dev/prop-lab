---
tags: [record, shadow]
---

# Shadow grading: every priced prop vs result and market

Written by `engine/shadow.py` (morning settlement runs it). Rules §9 uses this to decide when the model-health gate relaxes and when NFL/MLB go live.

## NBA
Graded props: **8309** over 31 day(s). Over hit rate 0.483 vs market's average 0.493 vs model's 0.456.
Brier: model 0.2540 · market 0.2468 · blend 0.2477 → **model skill vs market -2.9%**, blend skill -0.3% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| ast | 1907 | 0.491 | 0.495 | 0.457 | -2.1% |
| fg3m | 1476 | 0.490 | 0.484 | 0.450 | -2.4% |
| pts | 2469 | 0.477 | 0.498 | 0.452 | -4.4% |
| reb | 2457 | 0.480 | 0.490 | 0.464 | -2.4% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 518 | 0.251 | 0.444 | 0.466 |
| (0.3, 0.4] | 1887 | 0.359 | 0.452 | 0.464 |
| (0.4, 0.5] | 3152 | 0.450 | 0.469 | 0.486 |
| (0.5, 0.6] | 2110 | 0.543 | 0.522 | 0.518 |
| (0.6, 0.7] | 549 | 0.638 | 0.554 | 0.544 |
| (0.7, 1.0] | 93 | 0.735 | 0.548 | 0.551 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 1802 | 0.477 | 0.496 | -1.9 pts |
| (-0.1, -0.05] | 1659 | 0.480 | 0.493 | -1.3 pts |
| (-0.05, 0.0] | 2023 | 0.470 | 0.492 | -2.3 pts |
| (0.0, 0.05] | 1570 | 0.499 | 0.492 | +0.7 pts |
| (0.05, 0.1] | 801 | 0.497 | 0.488 | +0.9 pts |
| (0.1, 1.0] | 454 | 0.507 | 0.490 | +1.6 pts |

Noise check: with 8309 props one standard error on a hit rate is about ±0.5 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

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
Graded props: **9716** over 27 day(s). Over hit rate 0.480 vs market's average 0.490 vs model's 0.480.
Brier: model 0.2549 · market 0.2457 · blend 0.2460 → **model skill vs market -3.8%**, blend skill -0.1% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| assists | 2254 | 0.493 | 0.492 | 0.484 | -2.7% |
| points | 2770 | 0.476 | 0.501 | 0.488 | -5.7% |
| rebounds | 2626 | 0.473 | 0.489 | 0.485 | -3.8% |
| threes | 2066 | 0.479 | 0.476 | 0.457 | -2.1% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 643 | 0.234 | 0.407 | 0.433 |
| (0.3, 0.4] | 1712 | 0.358 | 0.422 | 0.451 |
| (0.4, 0.5] | 3026 | 0.452 | 0.475 | 0.482 |
| (0.5, 0.6] | 2885 | 0.547 | 0.515 | 0.511 |
| (0.6, 0.7] | 1187 | 0.639 | 0.511 | 0.538 |
| (0.7, 1.0] | 263 | 0.748 | 0.567 | 0.534 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 1612 | 0.470 | 0.487 | -1.7 pts |
| (-0.1, -0.05] | 1513 | 0.462 | 0.488 | -2.6 pts |
| (-0.05, 0.0] | 2085 | 0.487 | 0.489 | -0.1 pts |
| (0.0, 0.05] | 1936 | 0.483 | 0.492 | -0.9 pts |
| (0.05, 0.1] | 1390 | 0.484 | 0.494 | -1.0 pts |
| (0.1, 1.0] | 1180 | 0.494 | 0.490 | +0.4 pts |

Noise check: with 9716 props one standard error on a hit rate is about ±0.5 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

(price-edge grading failed: 'DataFrame' object has no attribute 'over')

(steam grading failed: 'DataFrame' object has no attribute 'over')
