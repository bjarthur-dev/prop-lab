# Line Calibration

Do the books' prices match what happens? Favourite's no-vig win chance (consensus of all books, Pinnacle 2x, FanDuel 1.5x) from the last saved snapshot before kickoff, vs. how often the favourite actually won.
Games: 778 (ncaab 690, ncaaf 82, nfl 6). Data window: 2026-10-31 to 2026-11-21.

## All sports
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 156 | 54.8% | 46.8% | -8.0 | 4.0 |
| (0.6, 0.7] | 114 | 64.4% | 66.7% | +2.2 | 4.5 |
| (0.7, 0.8] | 103 | 74.9% | 73.8% | -1.1 | 4.3 |
| (0.8, 0.9] | 117 | 85.3% | 82.9% | -2.4 | 3.3 |
| (0.9, 1.0] | 288 | 95.6% | 97.9% | +2.4 | 1.2 |
| **all** | 778 | 78.5% | 77.6% | -0.9 | 1.4 |

## NCAAB
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 133 | 54.8% | 45.9% | -8.9 | 4.3 |
| (0.6, 0.7] | 92 | 64.5% | 69.6% | +5.1 | 5.0 |
| (0.7, 0.8] | 84 | 75.1% | 70.2% | -4.8 | 4.7 |
| (0.8, 0.9] | 95 | 85.5% | 83.2% | -2.3 | 3.6 |
| (0.9, 1.0] | 286 | 95.6% | 97.9% | +2.3 | 1.2 |
| **all** | 690 | 79.7% | 78.7% | -1.0 | 1.4 |

## NCAAF
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 22 | 55.1% | 54.5% | -0.6 | 10.6 |
| (0.6, 0.7] | 19 | 64.2% | 52.6% | -11.6 | 11.0 |
| (0.7, 0.8] | 18 | 74.1% | 88.9% | +14.8 | 10.3 |
| (0.8, 0.9] | 21 | 84.7% | 81.0% | -3.7 | 7.9 |
| (0.9, 1.0] | 2 | 91.2% | 100.0% | +8.8 | 20.0 |
| **all** | 82 | 69.8% | 69.5% | -0.3 | 4.9 |

## NFL
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 1 | 53.4% | 0.0% | -53.4 | 49.9 |
| (0.6, 0.7] | 3 | 64.4% | 66.7% | +2.2 | 27.6 |
| (0.7, 0.8] | 1 | 70.2% | 100.0% | +29.8 | 45.8 |
| (0.8, 0.9] | 1 | 84.7% | 100.0% | +15.3 | 36.0 |
| **all** | 6 | 66.9% | 66.7% | -0.3 | 18.8 |

Gap within about 2x the noise column = the prices were right. Small samples: re-run as data grows (results.yml).