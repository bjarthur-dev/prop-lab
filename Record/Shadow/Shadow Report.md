---
tags: [record, shadow]
---

# Shadow grading: every priced prop vs result and market

Written by `engine/shadow.py` (morning settlement runs it). Rules §9 uses this to decide when the model-health gate relaxes and when NFL/MLB go live.

## NBA
Graded props: **7926** over 30 day(s). Over hit rate 0.481 vs market's average 0.492 vs model's 0.456.
Brier: model 0.2537 · market 0.2467 · blend 0.2474 → **model skill vs market -2.8%**, blend skill -0.3% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| ast | 1827 | 0.486 | 0.495 | 0.457 | -1.9% |
| fg3m | 1385 | 0.488 | 0.483 | 0.449 | -2.5% |
| pts | 2359 | 0.475 | 0.498 | 0.453 | -3.9% |
| reb | 2355 | 0.480 | 0.490 | 0.464 | -2.5% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 499 | 0.251 | 0.443 | 0.466 |
| (0.3, 0.4] | 1790 | 0.359 | 0.448 | 0.464 |
| (0.4, 0.5] | 2996 | 0.450 | 0.466 | 0.486 |
| (0.5, 0.6] | 2031 | 0.543 | 0.521 | 0.518 |
| (0.6, 0.7] | 522 | 0.638 | 0.552 | 0.543 |
| (0.7, 1.0] | 88 | 0.735 | 0.545 | 0.546 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 1714 | 0.475 | 0.496 | -2.1 pts |
| (-0.1, -0.05] | 1582 | 0.480 | 0.493 | -1.3 pts |
| (-0.05, 0.0] | 1922 | 0.467 | 0.492 | -2.5 pts |
| (0.0, 0.05] | 1497 | 0.493 | 0.491 | +0.2 pts |
| (0.05, 0.1] | 771 | 0.492 | 0.488 | +0.4 pts |
| (0.1, 1.0] | 440 | 0.511 | 0.490 | +2.2 pts |

Noise check: with 7926 props one standard error on a hit rate is about ±0.6 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

## NFL
Graded props: **1912** over 6 day(s). Over hit rate 0.492 vs market's average 0.495 vs model's 0.477.
Brier: model 0.2644 · market 0.2478 · blend 0.2487 → **model skill vs market -6.7%**, blend skill -0.4% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| carries | 104 | 0.442 | 0.496 | 0.455 | -23.6% |
| rec_yds | 905 | 0.496 | 0.500 | 0.483 | -2.3% |
| receptions | 631 | 0.491 | 0.486 | 0.463 | -3.5% |
| rush_yds | 272 | 0.500 | 0.499 | 0.495 | -22.3% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 166 | 0.237 | 0.524 | 0.469 |
| (0.3, 0.4] | 392 | 0.356 | 0.477 | 0.485 |
| (0.4, 0.5] | 558 | 0.454 | 0.478 | 0.495 |
| (0.5, 0.6] | 482 | 0.548 | 0.473 | 0.501 |
| (0.6, 0.7] | 205 | 0.644 | 0.507 | 0.509 |
| (0.7, 1.0] | 109 | 0.763 | 0.624 | 0.520 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 519 | 0.499 | 0.495 | +0.4 pts |
| (-0.1, -0.05] | 252 | 0.448 | 0.497 | -4.8 pts |
| (-0.05, 0.0] | 334 | 0.509 | 0.500 | +0.9 pts |
| (0.0, 0.05] | 268 | 0.455 | 0.492 | -3.7 pts |
| (0.05, 0.1] | 222 | 0.536 | 0.497 | +4.0 pts |
| (0.1, 1.0] | 317 | 0.498 | 0.490 | +0.9 pts |

Noise check: with 1912 props one standard error on a hit rate is about ±1.1 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

## NBA matchup engine v1 (context vs market)
Graded props: **9295** over 26 day(s). Over hit rate 0.478 vs market's average 0.490 vs model's 0.479.
Brier: model 0.2547 · market 0.2456 · blend 0.2459 → **model skill vs market -3.7%**, blend skill -0.1% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| assists | 2156 | 0.489 | 0.491 | 0.483 | -2.7% |
| points | 2656 | 0.474 | 0.501 | 0.488 | -5.7% |
| rebounds | 2512 | 0.473 | 0.489 | 0.485 | -3.9% |
| threes | 1971 | 0.477 | 0.475 | 0.455 | -1.9% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 629 | 0.234 | 0.407 | 0.433 |
| (0.3, 0.4] | 1655 | 0.358 | 0.421 | 0.451 |
| (0.4, 0.5] | 2891 | 0.452 | 0.470 | 0.482 |
| (0.5, 0.6] | 2739 | 0.547 | 0.516 | 0.510 |
| (0.6, 0.7] | 1136 | 0.639 | 0.510 | 0.537 |
| (0.7, 1.0] | 245 | 0.747 | 0.571 | 0.533 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 1563 | 0.466 | 0.487 | -2.0 pts |
| (-0.1, -0.05] | 1448 | 0.459 | 0.488 | -2.9 pts |
| (-0.05, 0.0] | 1993 | 0.486 | 0.488 | -0.2 pts |
| (0.0, 0.05] | 1840 | 0.483 | 0.492 | -1.0 pts |
| (0.05, 0.1] | 1328 | 0.482 | 0.494 | -1.2 pts |
| (0.1, 1.0] | 1123 | 0.492 | 0.490 | +0.3 pts |

Noise check: with 9295 props one standard error on a hit rate is about ±0.5 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

(price-edge grading failed: 'DataFrame' object has no attribute 'over')

(steam grading failed: 'DataFrame' object has no attribute 'over')
