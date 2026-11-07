---
tags: [record, shadow]
---

# Shadow grading: every priced prop vs result and market

Written by `engine/shadow.py` (morning settlement runs it). Rules §9 uses this to decide when the model-health gate relaxes and when NFL/MLB go live.

## NBA
Graded props: **3516** over 14 day(s). Over hit rate 0.478 vs market's average 0.493 vs model's 0.459.
Brier: model 0.2545 · market 0.2459 · blend 0.2447 → **model skill vs market -3.5%**, blend skill +0.5% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| ast | 849 | 0.479 | 0.495 | 0.457 | -3.5% |
| fg3m | 521 | 0.478 | 0.483 | 0.453 | -2.9% |
| pts | 1035 | 0.467 | 0.498 | 0.456 | -4.8% |
| reb | 1111 | 0.486 | 0.491 | 0.466 | -2.5% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 221 | 0.252 | 0.466 | 0.467 |
| (0.3, 0.4] | 775 | 0.359 | 0.436 | 0.464 |
| (0.4, 0.5] | 1313 | 0.450 | 0.478 | 0.487 |
| (0.5, 0.6] | 929 | 0.544 | 0.489 | 0.516 |
| (0.6, 0.7] | 233 | 0.640 | 0.562 | 0.543 |
| (0.7, 1.0] | 45 | 0.730 | 0.556 | 0.542 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 750 | 0.493 | 0.498 | -0.4 pts |
| (-0.1, -0.05] | 708 | 0.477 | 0.492 | -1.4 pts |
| (-0.05, 0.0] | 816 | 0.458 | 0.492 | -3.4 pts |
| (0.0, 0.05] | 671 | 0.474 | 0.494 | -2.0 pts |
| (0.05, 0.1] | 360 | 0.472 | 0.487 | -1.5 pts |
| (0.1, 1.0] | 211 | 0.517 | 0.489 | +2.7 pts |

Noise check: with 3516 props one standard error on a hit rate is about ±0.8 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

## NFL
Graded props: **590** over 2 day(s). Over hit rate 0.466 vs market's average 0.496 vs model's 0.492.
Brier: model 0.2680 · market 0.2473 · blend 0.2494 → **model skill vs market -8.3%**, blend skill -0.8% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| carries | 7 | 0.429 | 0.513 | 0.539 | -37.4% |
| rec_yds | 325 | 0.446 | 0.500 | 0.499 | -3.3% |
| receptions | 155 | 0.484 | 0.485 | 0.467 | -5.7% |
| rush_yds | 103 | 0.505 | 0.498 | 0.500 | -25.9% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 43 | 0.235 | 0.558 | 0.462 |
| (0.3, 0.4] | 101 | 0.355 | 0.495 | 0.490 |
| (0.4, 0.5] | 168 | 0.453 | 0.405 | 0.499 |
| (0.5, 0.6] | 162 | 0.550 | 0.457 | 0.499 |
| (0.6, 0.7] | 77 | 0.645 | 0.506 | 0.501 |
| (0.7, 1.0] | 39 | 0.748 | 0.513 | 0.514 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 146 | 0.514 | 0.496 | +1.8 pts |
| (-0.1, -0.05] | 70 | 0.329 | 0.495 | -16.6 pts |
| (-0.05, 0.0] | 89 | 0.449 | 0.502 | -5.2 pts |
| (0.0, 0.05] | 86 | 0.442 | 0.490 | -4.8 pts |
| (0.05, 0.1] | 86 | 0.523 | 0.501 | +2.2 pts |
| (0.1, 1.0] | 113 | 0.478 | 0.493 | -1.5 pts |

Noise check: with 590 props one standard error on a hit rate is about ±2.1 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

## NBA matchup engine v1 (context vs market)
Graded props: **3616** over 10 day(s). Over hit rate 0.470 vs market's average 0.489 vs model's 0.488.
Brier: model 0.2577 · market 0.2460 · blend 0.2467 → **model skill vs market -4.8%**, blend skill -0.3% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| assists | 881 | 0.481 | 0.493 | 0.496 | -4.5% |
| points | 979 | 0.458 | 0.502 | 0.502 | -7.4% |
| rebounds | 1021 | 0.488 | 0.488 | 0.490 | -5.5% |
| threes | 735 | 0.450 | 0.468 | 0.459 | -0.4% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 244 | 0.230 | 0.414 | 0.432 |
| (0.3, 0.4] | 586 | 0.358 | 0.418 | 0.451 |
| (0.4, 0.5] | 1061 | 0.454 | 0.462 | 0.481 |
| (0.5, 0.6] | 1085 | 0.548 | 0.509 | 0.505 |
| (0.6, 0.7] | 509 | 0.639 | 0.481 | 0.529 |
| (0.7, 1.0] | 131 | 0.751 | 0.519 | 0.532 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 584 | 0.478 | 0.486 | -0.9 pts |
| (-0.1, -0.05] | 480 | 0.444 | 0.487 | -4.3 pts |
| (-0.05, 0.0] | 722 | 0.456 | 0.489 | -3.3 pts |
| (0.0, 0.05] | 688 | 0.484 | 0.491 | -0.7 pts |
| (0.05, 0.1] | 564 | 0.491 | 0.492 | -0.0 pts |
| (0.1, 1.0] | 578 | 0.467 | 0.487 | -2.0 pts |

Noise check: with 3616 props one standard error on a hit rate is about ±0.8 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.
