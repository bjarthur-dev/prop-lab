# Line Calibration

Do the books' prices match what happens? Favourite's no-vig win chance (consensus of all books, Pinnacle 2x, FanDuel 1.5x) from the last saved snapshot before kickoff, vs. how often the favourite actually won.
Games: 718 (ncaab 643, ncaaf 69, nfl 6). Data window: 2026-10-31 to 2026-11-20.

## All sports
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 141 | 54.8% | 46.1% | -8.7 | 4.2 |
| (0.6, 0.7] | 98 | 64.6% | 68.4% | +3.8 | 4.8 |
| (0.7, 0.8] | 94 | 75.0% | 73.4% | -1.6 | 4.5 |
| (0.8, 0.9] | 108 | 85.4% | 84.3% | -1.2 | 3.4 |
| (0.9, 1.0] | 277 | 95.6% | 98.2% | +2.6 | 1.2 |
| **all** | 718 | 79.1% | 78.6% | -0.6 | 1.4 |

## NCAAB
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 121 | 54.8% | 44.6% | -10.2 | 4.5 |
| (0.6, 0.7] | 79 | 64.8% | 70.9% | +6.1 | 5.4 |
| (0.7, 0.8] | 76 | 75.3% | 69.7% | -5.5 | 4.9 |
| (0.8, 0.9] | 90 | 85.5% | 84.4% | -1.1 | 3.7 |
| (0.9, 1.0] | 277 | 95.6% | 98.2% | +2.6 | 1.2 |
| **all** | 643 | 80.3% | 79.5% | -0.9 | 1.4 |

## NCAAF
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 19 | 55.1% | 57.9% | +2.8 | 11.4 |
| (0.6, 0.7] | 16 | 63.6% | 56.2% | -7.3 | 12.0 |
| (0.7, 0.8] | 17 | 74.0% | 88.2% | +14.3 | 10.6 |
| (0.8, 0.9] | 17 | 85.0% | 82.4% | -2.6 | 8.7 |
| **all** | 69 | 69.1% | 71.0% | +1.9 | 5.4 |

## NFL
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 1 | 53.4% | 0.0% | -53.4 | 49.9 |
| (0.6, 0.7] | 3 | 64.4% | 66.7% | +2.2 | 27.6 |
| (0.7, 0.8] | 1 | 70.2% | 100.0% | +29.8 | 45.8 |
| (0.8, 0.9] | 1 | 84.7% | 100.0% | +15.3 | 36.0 |
| **all** | 6 | 66.9% | 66.7% | -0.3 | 18.8 |

Gap within about 2x the noise column = the prices were right. Small samples: re-run as data grows (results.yml).