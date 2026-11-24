# Line Calibration

Do the books' prices match what happens? Favourite's no-vig win chance (consensus of all books, Pinnacle 2x, FanDuel 1.5x) from the last saved snapshot before kickoff, vs. how often the favourite actually won.
Games: 890 (ncaab 748, ncaaf 125, nfl 17). Data window: 2026-10-31 to 2026-11-23.

## All sports
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 188 | 54.8% | 48.9% | -5.8 | 3.6 |
| (0.6, 0.7] | 145 | 64.6% | 66.2% | +1.6 | 4.0 |
| (0.7, 0.8] | 126 | 74.8% | 76.2% | +1.4 | 3.9 |
| (0.8, 0.9] | 134 | 85.4% | 85.1% | -0.4 | 3.0 |
| (0.9, 1.0] | 297 | 95.6% | 98.0% | +2.4 | 1.2 |
| **all** | 890 | 77.4% | 77.4% | -0.0 | 1.3 |

## NCAAB
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 155 | 54.7% | 47.1% | -7.6 | 4.0 |
| (0.6, 0.7] | 110 | 64.8% | 68.2% | +3.4 | 4.6 |
| (0.7, 0.8] | 92 | 75.1% | 72.8% | -2.2 | 4.5 |
| (0.8, 0.9] | 101 | 85.5% | 84.2% | -1.3 | 3.5 |
| (0.9, 1.0] | 290 | 95.7% | 98.3% | +2.6 | 1.2 |
| **all** | 748 | 78.7% | 78.2% | -0.5 | 1.4 |

## NCAAF
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 31 | 54.9% | 58.1% | +3.1 | 8.9 |
| (0.6, 0.7] | 28 | 64.2% | 60.7% | -3.5 | 9.1 |
| (0.7, 0.8] | 31 | 74.2% | 87.1% | +12.9 | 7.9 |
| (0.8, 0.9] | 29 | 85.3% | 86.2% | +0.9 | 6.6 |
| (0.9, 1.0] | 6 | 92.4% | 83.3% | -9.1 | 10.8 |
| **all** | 125 | 70.6% | 73.6% | +3.0 | 3.9 |

## NFL
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 2 | 54.6% | 50.0% | -4.6 | 35.2 |
| (0.6, 0.7] | 7 | 64.1% | 57.1% | -6.9 | 18.1 |
| (0.7, 0.8] | 3 | 71.9% | 66.7% | -5.2 | 26.0 |
| (0.8, 0.9] | 4 | 85.5% | 100.0% | +14.5 | 17.6 |
| (0.9, 1.0] | 1 | 91.1% | 100.0% | +8.9 | 28.5 |
| **all** | 17 | 71.0% | 70.6% | -0.4 | 10.7 |

Gap within about 2x the noise column = the prices were right. Small samples: re-run as data grows (results.yml).