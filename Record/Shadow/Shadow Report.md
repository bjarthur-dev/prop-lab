---
tags: [record, shadow]
---

# Shadow grading: every priced prop vs result and market

Written by `engine/shadow.py` (morning settlement runs it). Rules §9 uses this to decide when the model-health gate relaxes and when NFL/MLB go live.

## NBA
Graded props: **1693** over 8 day(s). Over hit rate 0.488 vs market's average 0.493 vs model's 0.465.
Brier: model 0.2542 · market 0.2442 · blend 0.2420 → **model skill vs market -4.1%**, blend skill +0.9% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| ast | 393 | 0.481 | 0.494 | 0.461 | -6.2% |
| fg3m | 172 | 0.483 | 0.475 | 0.451 | -2.1% |
| pts | 598 | 0.492 | 0.499 | 0.464 | -4.8% |
| reb | 530 | 0.491 | 0.493 | 0.472 | -2.5% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 112 | 0.250 | 0.473 | 0.475 |
| (0.3, 0.4] | 317 | 0.359 | 0.457 | 0.468 |
| (0.4, 0.5] | 650 | 0.451 | 0.475 | 0.486 |
| (0.5, 0.6] | 450 | 0.544 | 0.489 | 0.511 |
| (0.6, 0.7] | 139 | 0.639 | 0.597 | 0.535 |
| (0.7, 1.0] | 25 | 0.726 | 0.640 | 0.524 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 347 | 0.516 | 0.500 | +1.6 pts |
| (-0.1, -0.05] | 317 | 0.498 | 0.496 | +0.2 pts |
| (-0.05, 0.0] | 373 | 0.450 | 0.490 | -3.9 pts |
| (0.0, 0.05] | 333 | 0.474 | 0.491 | -1.7 pts |
| (0.05, 0.1] | 192 | 0.484 | 0.490 | -0.6 pts |
| (0.1, 1.0] | 131 | 0.534 | 0.490 | +4.4 pts |

Noise check: with 1693 props one standard error on a hit rate is about ±1.2 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

## NFL
Graded props: **160** over 1 day(s). Over hit rate 0.444 vs market's average 0.500 vs model's 0.520.
Brier: model 0.2576 · market 0.2505 · blend 0.2490 → **model skill vs market -2.8%**, blend skill +0.6% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| carries | 7 | 0.429 | 0.513 | 0.539 | -37.4% |
| rec_yds | 118 | 0.424 | 0.500 | 0.513 | +1.6% |
| rush_yds | 35 | 0.514 | 0.498 | 0.539 | -10.3% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 7 | 0.234 | 0.429 | 0.502 |
| (0.3, 0.4] | 21 | 0.364 | 0.476 | 0.497 |
| (0.4, 0.5] | 49 | 0.460 | 0.367 | 0.501 |
| (0.5, 0.6] | 43 | 0.554 | 0.419 | 0.500 |
| (0.6, 0.7] | 21 | 0.634 | 0.429 | 0.496 |
| (0.7, 1.0] | 19 | 0.746 | 0.684 | 0.505 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 31 | 0.452 | 0.501 | -4.9 pts |
| (-0.1, -0.05] | 16 | 0.188 | 0.501 | -31.3 pts |
| (-0.05, 0.0] | 28 | 0.464 | 0.500 | -3.6 pts |
| (0.0, 0.05] | 18 | 0.389 | 0.498 | -10.9 pts |
| (0.05, 0.1] | 28 | 0.429 | 0.500 | -7.1 pts |
| (0.1, 1.0] | 39 | 0.564 | 0.500 | +6.4 pts |

Noise check: with 160 props one standard error on a hit rate is about ±4.0 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.

## NBA matchup engine v1 (context vs market)
Graded props: **1444** over 4 day(s). Over hit rate 0.478 vs market's average 0.486 vs model's 0.488.
Brier: model 0.2563 · market 0.2441 · blend 0.2449 → **model skill vs market -5.0%**, blend skill -0.3% (positive = better than the market).

| market | n | over hit | market p | model p | model skill vs mkt |
|---|---:|---:|---:|---:|---:|
| assists | 316 | 0.459 | 0.490 | 0.499 | -4.2% |
| points | 430 | 0.484 | 0.503 | 0.508 | -6.9% |
| rebounds | 368 | 0.497 | 0.484 | 0.482 | -6.0% |
| threes | 330 | 0.467 | 0.463 | 0.456 | -2.1% |

Model calibration (P(over)):

| model p bin | n | predicted | actual | market p |
|---|---:|---:|---:|---:|
| (0.0, 0.3] | 101 | 0.227 | 0.406 | 0.423 |
| (0.3, 0.4] | 253 | 0.358 | 0.407 | 0.452 |
| (0.4, 0.5] | 401 | 0.454 | 0.494 | 0.480 |
| (0.5, 0.6] | 417 | 0.548 | 0.492 | 0.503 |
| (0.6, 0.7] | 215 | 0.641 | 0.544 | 0.525 |
| (0.7, 1.0] | 57 | 0.739 | 0.456 | 0.529 |

Does disagreeing with the market pay? (over hit vs market p, by model−market gap)

| gap bin | n | over hit | market p | hit − market |
|---|---:|---:|---:|---:|
| (-1.0, -0.1] | 244 | 0.467 | 0.485 | -1.8 pts |
| (-0.1, -0.05] | 189 | 0.455 | 0.481 | -2.6 pts |
| (-0.05, 0.0] | 267 | 0.449 | 0.485 | -3.6 pts |
| (0.0, 0.05] | 262 | 0.527 | 0.490 | +3.7 pts |
| (0.05, 0.1] | 222 | 0.505 | 0.488 | +1.7 pts |
| (0.1, 1.0] | 260 | 0.462 | 0.487 | -2.5 pts |

Noise check: with 1444 props one standard error on a hit rate is about ±1.3 pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference.
