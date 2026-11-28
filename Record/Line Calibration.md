# Line Calibration

Do the books' prices match what happens? Favourite's no-vig win chance (consensus of all books, Pinnacle 2x, FanDuel 1.5x) from the last saved snapshot before kickoff, vs. how often the favourite actually won.
Games: 934 (ncaab 828, ncaaf 94, nfl 12). Data window: 2026-10-31 to 2026-11-27.

## All sports
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 207 | 54.8% | 48.3% | -6.5 | 3.5 |
| (0.6, 0.7] | 145 | 64.3% | 66.9% | +2.6 | 4.0 |
| (0.7, 0.8] | 133 | 75.0% | 74.4% | -0.5 | 3.8 |
| (0.8, 0.9] | 136 | 85.5% | 83.1% | -2.4 | 3.0 |
| (0.9, 1.0] | 313 | 95.5% | 98.4% | +2.9 | 1.2 |
| **all** | 934 | 77.3% | 76.8% | -0.5 | 1.3 |

## NCAAB
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 180 | 54.7% | 46.1% | -8.6 | 3.7 |
| (0.6, 0.7] | 119 | 64.4% | 67.2% | +2.8 | 4.4 |
| (0.7, 0.8] | 106 | 75.3% | 71.7% | -3.6 | 4.2 |
| (0.8, 0.9] | 111 | 85.5% | 82.9% | -2.6 | 3.3 |
| (0.9, 1.0] | 312 | 95.5% | 98.4% | +2.9 | 1.2 |
| **all** | 828 | 78.2% | 77.1% | -1.2 | 1.3 |

## NCAAF
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 23 | 55.1% | 60.9% | +5.7 | 10.4 |
| (0.6, 0.7] | 22 | 64.0% | 63.6% | -0.4 | 10.2 |
| (0.7, 0.8] | 24 | 73.9% | 91.7% | +17.8 | 9.0 |
| (0.8, 0.9] | 24 | 85.5% | 83.3% | -2.2 | 7.2 |
| (0.9, 1.0] | 1 | 90.6% | 100.0% | +9.4 | 29.2 |
| **all** | 94 | 70.1% | 75.5% | +5.4 | 4.6 |

## NFL
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 4 | 55.5% | 75.0% | +19.5 | 24.9 |
| (0.6, 0.7] | 4 | 64.5% | 75.0% | +10.5 | 23.9 |
| (0.7, 0.8] | 3 | 73.9% | 33.3% | -40.5 | 25.4 |
| (0.8, 0.9] | 1 | 84.7% | 100.0% | +15.3 | 36.0 |
| **all** | 12 | 65.5% | 66.7% | +1.1 | 13.4 |

Gap within about 2x the noise column = the prices were right. Small samples: re-run as data grows (results.yml).