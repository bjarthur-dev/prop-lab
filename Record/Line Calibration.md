# Line Calibration

Do the books' prices match what happens? Favourite's no-vig win chance (consensus of all books, Pinnacle 2x, FanDuel 1.5x) from the last saved snapshot before kickoff, vs. how often the favourite actually won.
Games: 632 (ncaab 561, ncaaf 66, nfl 5). Data window: 2026-10-31 to 2026-11-18.

## All sports
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 114 | 54.7% | 43.9% | -10.9 | 4.7 |
| (0.6, 0.7] | 86 | 64.7% | 68.6% | +3.9 | 5.2 |
| (0.7, 0.8] | 80 | 75.1% | 73.8% | -1.4 | 4.8 |
| (0.8, 0.9] | 100 | 85.4% | 84.0% | -1.4 | 3.5 |
| (0.9, 1.0] | 252 | 95.6% | 97.6% | +2.0 | 1.3 |
| **all** | 632 | 79.8% | 78.8% | -1.0 | 1.5 |

## NCAAB
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 97 | 54.8% | 41.2% | -13.5 | 5.1 |
| (0.6, 0.7] | 67 | 65.0% | 71.6% | +6.6 | 5.8 |
| (0.7, 0.8] | 62 | 75.5% | 69.4% | -6.2 | 5.5 |
| (0.8, 0.9] | 83 | 85.5% | 84.3% | -1.2 | 3.9 |
| (0.9, 1.0] | 252 | 95.6% | 97.6% | +2.0 | 1.3 |
| **all** | 561 | 81.2% | 79.7% | -1.5 | 1.5 |

## NCAAF
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 16 | 54.7% | 62.5% | +7.8 | 12.4 |
| (0.6, 0.7] | 16 | 63.6% | 56.2% | -7.3 | 12.0 |
| (0.7, 0.8] | 17 | 74.0% | 88.2% | +14.3 | 10.6 |
| (0.8, 0.9] | 17 | 85.0% | 82.4% | -2.6 | 8.7 |
| **all** | 66 | 69.6% | 72.7% | +3.1 | 5.5 |

## NFL
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 1 | 53.4% | 0.0% | -53.4 | 49.9 |
| (0.6, 0.7] | 3 | 64.4% | 66.7% | +2.2 | 27.6 |
| (0.7, 0.8] | 1 | 70.2% | 100.0% | +29.8 | 45.8 |
| **all** | 5 | 63.4% | 60.0% | -3.4 | 21.4 |

Gap within about 2x the noise column = the prices were right. Small samples: re-run as data grows (results.yml).