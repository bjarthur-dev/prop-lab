# Line Calibration

Do the books' prices match what happens? Favourite's no-vig win chance (consensus of all books, Pinnacle 2x, FanDuel 1.5x) from the last saved snapshot before kickoff, vs. how often the favourite actually won.
Games: 891 (ncaab 795, ncaaf 88, nfl 8). Data window: 2026-10-31 to 2026-11-25.

## All sports
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 189 | 54.6% | 46.0% | -8.6 | 3.6 |
| (0.6, 0.7] | 139 | 64.6% | 66.9% | +2.3 | 4.1 |
| (0.7, 0.8] | 129 | 74.9% | 75.2% | +0.2 | 3.8 |
| (0.8, 0.9] | 129 | 85.5% | 83.7% | -1.8 | 3.1 |
| (0.9, 1.0] | 305 | 95.5% | 98.4% | +2.8 | 1.2 |
| **all** | 891 | 77.6% | 76.9% | -0.7 | 1.3 |

## NCAAB
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 167 | 54.6% | 44.3% | -10.3 | 3.9 |
| (0.6, 0.7] | 114 | 64.7% | 67.5% | +2.9 | 4.5 |
| (0.7, 0.8] | 104 | 75.2% | 72.1% | -3.1 | 4.2 |
| (0.8, 0.9] | 106 | 85.5% | 84.0% | -1.6 | 3.4 |
| (0.9, 1.0] | 304 | 95.5% | 98.4% | +2.8 | 1.2 |
| **all** | 795 | 78.5% | 77.2% | -1.3 | 1.3 |

## NCAAF
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 21 | 55.1% | 61.9% | +6.8 | 10.9 |
| (0.6, 0.7] | 21 | 64.1% | 61.9% | -2.2 | 10.5 |
| (0.7, 0.8] | 23 | 74.0% | 91.3% | +17.3 | 9.1 |
| (0.8, 0.9] | 22 | 85.6% | 81.8% | -3.8 | 7.5 |
| (0.9, 1.0] | 1 | 90.6% | 100.0% | +9.4 | 29.2 |
| **all** | 88 | 70.2% | 75.0% | +4.8 | 4.7 |

## NFL
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 1 | 53.4% | 0.0% | -53.4 | 49.9 |
| (0.6, 0.7] | 4 | 64.5% | 75.0% | +10.5 | 23.9 |
| (0.7, 0.8] | 2 | 71.2% | 50.0% | -21.2 | 32.0 |
| (0.8, 0.9] | 1 | 84.7% | 100.0% | +15.3 | 36.0 |
| **all** | 8 | 67.3% | 62.5% | -4.8 | 16.3 |

Gap within about 2x the noise column = the prices were right. Small samples: re-run as data grows (results.yml).