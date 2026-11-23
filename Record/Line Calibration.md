# Line Calibration

Do the books' prices match what happens? Favourite's no-vig win chance (consensus of all books, Pinnacle 2x, FanDuel 1.5x) from the last saved snapshot before kickoff, vs. how often the favourite actually won.
Games: 876 (ncaab 739, ncaaf 130, nfl 7). Data window: 2026-10-31 to 2026-11-22.

## All sports
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 181 | 54.8% | 47.5% | -7.3 | 3.7 |
| (0.6, 0.7] | 140 | 64.4% | 66.4% | +2.0 | 4.0 |
| (0.7, 0.8] | 123 | 74.8% | 75.6% | +0.8 | 3.9 |
| (0.8, 0.9] | 134 | 85.5% | 83.6% | -1.9 | 3.0 |
| (0.9, 1.0] | 298 | 95.5% | 97.7% | +2.1 | 1.2 |
| **all** | 876 | 77.7% | 77.1% | -0.6 | 1.3 |

## NCAAB
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 148 | 54.8% | 45.9% | -8.9 | 4.1 |
| (0.6, 0.7] | 109 | 64.5% | 67.9% | +3.4 | 4.6 |
| (0.7, 0.8] | 91 | 75.1% | 71.4% | -3.7 | 4.5 |
| (0.8, 0.9] | 100 | 85.5% | 83.0% | -2.5 | 3.5 |
| (0.9, 1.0] | 291 | 95.6% | 97.9% | +2.4 | 1.2 |
| **all** | 739 | 78.9% | 77.8% | -1.1 | 1.4 |

## NCAAF
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 32 | 54.8% | 56.2% | +1.4 | 8.8 |
| (0.6, 0.7] | 28 | 64.2% | 60.7% | -3.5 | 9.1 |
| (0.7, 0.8] | 31 | 74.2% | 87.1% | +12.9 | 7.9 |
| (0.8, 0.9] | 32 | 85.2% | 84.4% | -0.8 | 6.3 |
| (0.9, 1.0] | 7 | 92.3% | 85.7% | -6.6 | 10.1 |
| **all** | 130 | 71.0% | 73.1% | +2.1 | 3.8 |

## NFL
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 1 | 53.4% | 0.0% | -53.4 | 49.9 |
| (0.6, 0.7] | 3 | 64.4% | 66.7% | +2.2 | 27.6 |
| (0.7, 0.8] | 1 | 70.2% | 100.0% | +29.8 | 45.8 |
| (0.8, 0.9] | 2 | 87.3% | 100.0% | +12.7 | 23.6 |
| **all** | 7 | 70.2% | 71.4% | +1.2 | 16.7 |

Gap within about 2x the noise column = the prices were right. Small samples: re-run as data grows (results.yml).