---
tags: [record, shadow]
---

# Shadow grading: every priced prop vs result and market

Written by `engine/shadow.py` (morning settlement runs it). Rules §9 uses this to decide when the model-health gate relaxes and when NFL/MLB go live.

## NBA
Graded props: **5928** over 23 day(s). Over hit rate 0.478 vs market's average 0.493 vs model's 0.458.
Brier: model 0.2535 · market 0.2466 · blend 0.2468 → **model skill vs market -2.8%**, blend skill -0.0% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| ast | 1383 | 0.479 | 0.496 | 0.458 | -1.7% |
| fg3m | 965 | 0.488 | 0.484 | 0.452 | -2.7% |
| pts | 1771 | 0.472 | 0.498 | 0.454 | -4.1% |
| reb | 1809 | 0.478 | 0.491 | 0.464 | -2.3% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 360 | 0.252 | 0.464 | 0.466 |
| (0.3, 0.4] | 1324 | 0.359 | 0.442 | 0.465 |
| (0.4, 0.5] | 2236 | 0.450 | 0.463 | 0.486 |
| (0.5, 0.6] | 1558 | 0.543 | 0.510 | 0.518 |
| (0.6, 0.7] | 382 | 0.639 | 0.563 | 0.542 |
| (0.7, 1.0] | 68 | 0.732 | 0.574 | 0.547 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 1266 | 0.479 | 0.496 | -1.6 pts |
| (-0.1, -0.05] | 1196 | 0.471 | 0.494 | -2.3 pts |
| (-0.05, 0.0] | 1442 | 0.458 | 0.493 | -3.4 pts |
| (0.0, 0.05] | 1095 | 0.489 | 0.492 | -0.3 pts |
| (0.05, 0.1] | 589 | 0.499 | 0.488 | +1.1 pts |
| (0.1, 1.0] | 340 | 0.515 | 0.488 | +2.7 pts |

Noise check: with 5928 props one standard error on a hit rate is about ±0.6 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

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
Graded props: **6886** over 19 day(s). Over hit rate 0.476 vs market's average 0.490 vs model's 0.482.
Brier: model 0.2563 · market 0.2459 · blend 0.2464 → **model skill vs market -4.2%**, blend skill -0.2% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| assists | 1613 | 0.482 | 0.491 | 0.487 | -3.8% |
| points | 1945 | 0.468 | 0.501 | 0.493 | -6.4% |
| rebounds | 1872 | 0.479 | 0.490 | 0.487 | -4.3% |
| threes | 1456 | 0.477 | 0.473 | 0.456 | -1.7% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 473 | 0.231 | 0.433 | 0.433 |
| (0.3, 0.4] | 1186 | 0.358 | 0.415 | 0.451 |
| (0.4, 0.5] | 2080 | 0.453 | 0.463 | 0.482 |
| (0.5, 0.6] | 2069 | 0.547 | 0.519 | 0.509 |
| (0.6, 0.7] | 874 | 0.639 | 0.495 | 0.535 |
| (0.7, 1.0] | 204 | 0.750 | 0.539 | 0.531 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 1134 | 0.480 | 0.487 | -0.7 pts |
| (-0.1, -0.05] | 1032 | 0.452 | 0.487 | -3.6 pts |
| (-0.05, 0.0] | 1446 | 0.476 | 0.488 | -1.2 pts |
| (0.0, 0.05] | 1349 | 0.473 | 0.492 | -1.9 pts |
| (0.05, 0.1] | 1021 | 0.490 | 0.493 | -0.3 pts |
| (0.1, 1.0] | 904 | 0.487 | 0.489 | -0.3 pts |

Noise check: with 6886 props one standard error on a hit rate is about ±0.6 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.
