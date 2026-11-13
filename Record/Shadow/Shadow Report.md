---
tags: [record, shadow]
---

# Shadow grading: every priced prop vs result and market

Written by `engine/shadow.py` (morning settlement runs it). Rules §9 uses this to decide when the model-health gate relaxes and when NFL/MLB go live.

## NBA
Graded props: **5030** over 20 day(s). Over hit rate 0.474 vs market's average 0.493 vs model's 0.457.
Brier: model 0.2528 · market 0.2461 · blend 0.2459 → **model skill vs market -2.8%**, blend skill +0.1% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| ast | 1188 | 0.474 | 0.496 | 0.456 | -1.4% |
| fg3m | 757 | 0.485 | 0.484 | 0.451 | -2.4% |
| pts | 1516 | 0.466 | 0.497 | 0.453 | -4.2% |
| reb | 1569 | 0.476 | 0.491 | 0.464 | -2.5% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 319 | 0.250 | 0.461 | 0.468 |
| (0.3, 0.4] | 1117 | 0.359 | 0.434 | 0.465 |
| (0.4, 0.5] | 1897 | 0.450 | 0.461 | 0.487 |
| (0.5, 0.6] | 1316 | 0.543 | 0.502 | 0.518 |
| (0.6, 0.7] | 323 | 0.640 | 0.567 | 0.541 |
| (0.7, 1.0] | 58 | 0.732 | 0.586 | 0.543 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 1088 | 0.477 | 0.497 | -2.0 pts |
| (-0.1, -0.05] | 1020 | 0.467 | 0.493 | -2.7 pts |
| (-0.05, 0.0] | 1205 | 0.459 | 0.493 | -3.4 pts |
| (0.0, 0.05] | 942 | 0.475 | 0.493 | -1.8 pts |
| (0.05, 0.1] | 487 | 0.485 | 0.488 | -0.4 pts |
| (0.1, 1.0] | 288 | 0.528 | 0.488 | +4.0 pts |

Noise check: with 5030 props one standard error on a hit rate is about ±0.7 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

## NFL
Graded props: **1073** over 4 day(s). Over hit rate 0.495 vs market's average 0.495 vs model's 0.476.
Brier: model 0.2620 · market 0.2477 · blend 0.2484 → **model skill vs market -5.8%**, blend skill -0.3% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| carries | 45 | 0.489 | 0.494 | 0.464 | -23.7% |
| rec_yds | 533 | 0.486 | 0.500 | 0.484 | -1.3% |
| receptions | 337 | 0.510 | 0.486 | 0.457 | -2.3% |
| rush_yds | 158 | 0.494 | 0.498 | 0.491 | -22.8% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 87 | 0.243 | 0.506 | 0.464 |
| (0.3, 0.4] | 222 | 0.356 | 0.473 | 0.486 |
| (0.4, 0.5] | 330 | 0.454 | 0.479 | 0.497 |
| (0.5, 0.6] | 261 | 0.549 | 0.490 | 0.503 |
| (0.6, 0.7] | 117 | 0.644 | 0.547 | 0.507 |
| (0.7, 1.0] | 56 | 0.753 | 0.571 | 0.519 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 293 | 0.502 | 0.495 | +0.6 pts |
| (-0.1, -0.05] | 152 | 0.388 | 0.496 | -10.8 pts |
| (-0.05, 0.0] | 185 | 0.524 | 0.500 | +2.4 pts |
| (0.0, 0.05] | 144 | 0.451 | 0.490 | -3.9 pts |
| (0.05, 0.1] | 134 | 0.582 | 0.497 | +8.5 pts |
| (0.1, 1.0] | 165 | 0.515 | 0.493 | +2.2 pts |

Noise check: with 1073 props one standard error on a hit rate is about ±1.5 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

## NBA matchup engine v1 (context vs market)
Graded props: **5726** over 16 day(s). Over hit rate 0.472 vs market's average 0.489 vs model's 0.483.
Brier: model 0.2553 · market 0.2456 · blend 0.2460 → **model skill vs market -3.9%**, blend skill -0.1% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| assists | 1360 | 0.479 | 0.491 | 0.488 | -3.6% |
| points | 1602 | 0.461 | 0.501 | 0.495 | -6.3% |
| rebounds | 1567 | 0.476 | 0.490 | 0.488 | -4.1% |
| threes | 1197 | 0.475 | 0.471 | 0.456 | -0.8% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 388 | 0.235 | 0.418 | 0.434 |
| (0.3, 0.4] | 978 | 0.357 | 0.413 | 0.451 |
| (0.4, 0.5] | 1713 | 0.453 | 0.457 | 0.482 |
| (0.5, 0.6] | 1731 | 0.547 | 0.517 | 0.508 |
| (0.6, 0.7] | 748 | 0.639 | 0.500 | 0.533 |
| (0.7, 1.0] | 168 | 0.749 | 0.518 | 0.531 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 943 | 0.471 | 0.487 | -1.6 pts |
| (-0.1, -0.05] | 853 | 0.442 | 0.487 | -4.5 pts |
| (-0.05, 0.0] | 1176 | 0.471 | 0.488 | -1.7 pts |
| (0.0, 0.05] | 1092 | 0.482 | 0.493 | -1.1 pts |
| (0.05, 0.1] | 874 | 0.493 | 0.492 | +0.2 pts |
| (0.1, 1.0] | 788 | 0.473 | 0.488 | -1.5 pts |

Noise check: with 5726 props one standard error on a hit rate is about ±0.7 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

(steam grading failed: [Errno 32] Broken pipe)

(live_report failed: [Errno 32] Broken pipe)

(stat_sheet failed: [Errno 32] Broken pipe)

(health failed: [Errno 32] Broken pipe)
