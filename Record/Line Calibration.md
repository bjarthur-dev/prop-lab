# Line Calibration

Do the books' prices match what happens? Favourite's no-vig win chance (consensus of all books, Pinnacle 2x, FanDuel 1.5x) from the last saved snapshot before kickoff, vs. how often the favourite actually won.
Games: 847 (ncaab 743, ncaaf 86, nfl 18). Data window: 2026-10-31 to 2026-11-24.

## All sports
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 180 | 54.7% | 50.0% | -4.7 | 3.7 |
| (0.6, 0.7] | 127 | 64.5% | 65.4% | +0.9 | 4.2 |
| (0.7, 0.8] | 121 | 74.9% | 75.2% | +0.3 | 3.9 |
| (0.8, 0.9] | 126 | 85.5% | 84.1% | -1.3 | 3.1 |
| (0.9, 1.0] | 293 | 95.6% | 98.3% | +2.7 | 1.2 |
| **all** | 847 | 77.8% | 77.7% | -0.1 | 1.3 |

## NCAAB
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 157 | 54.7% | 48.4% | -6.3 | 4.0 |
| (0.6, 0.7] | 101 | 64.6% | 66.3% | +1.7 | 4.8 |
| (0.7, 0.8] | 94 | 75.2% | 72.3% | -2.9 | 4.5 |
| (0.8, 0.9] | 100 | 85.4% | 84.0% | -1.4 | 3.5 |
| (0.9, 1.0] | 291 | 95.6% | 98.3% | +2.7 | 1.2 |
| **all** | 743 | 78.8% | 78.2% | -0.6 | 1.4 |

## NCAAF
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 21 | 55.1% | 61.9% | +6.8 | 10.9 |
| (0.6, 0.7] | 19 | 63.8% | 63.2% | -0.6 | 11.0 |
| (0.7, 0.8] | 23 | 74.0% | 91.3% | +17.3 | 9.1 |
| (0.8, 0.9] | 22 | 85.6% | 81.8% | -3.8 | 7.5 |
| (0.9, 1.0] | 1 | 90.6% | 100.0% | +9.4 | 29.2 |
| **all** | 86 | 70.3% | 75.6% | +5.3 | 4.8 |

## NFL
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 2 | 54.6% | 50.0% | -4.6 | 35.2 |
| (0.6, 0.7] | 7 | 64.1% | 57.1% | -6.9 | 18.1 |
| (0.7, 0.8] | 4 | 72.0% | 50.0% | -22.0 | 22.5 |
| (0.8, 0.9] | 4 | 85.5% | 100.0% | +14.5 | 17.6 |
| (0.9, 1.0] | 1 | 91.1% | 100.0% | +8.9 | 28.5 |
| **all** | 18 | 71.0% | 66.7% | -4.4 | 10.4 |

Gap within about 2x the noise column = the prices were right. Small samples: re-run as data grows (results.yml).