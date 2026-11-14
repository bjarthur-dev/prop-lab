# Line Calibration

Do the books' prices match what happens? Favourite's no-vig win chance (consensus of all books, Pinnacle 2x, FanDuel 1.5x) from the last saved snapshot before kickoff, vs. how often the favourite actually won.
Games: 451 (ncaab 411, ncaaf 37, nfl 3). Data window: 2026-10-31 to 2026-11-12.

## All sports
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 67 | 54.8% | 41.8% | -13.0 | 6.1 |
| (0.6, 0.7] | 61 | 65.0% | 67.2% | +2.2 | 6.1 |
| (0.7, 0.8] | 58 | 75.2% | 75.9% | +0.7 | 5.7 |
| (0.8, 0.9] | 69 | 85.5% | 85.5% | -0.0 | 4.2 |
| (0.9, 1.0] | 196 | 95.7% | 98.0% | +2.2 | 1.4 |
| **all** | 451 | 81.3% | 80.7% | -0.6 | 1.7 |

## NCAAB
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 59 | 54.9% | 39.0% | -15.9 | 6.5 |
| (0.6, 0.7] | 48 | 65.3% | 68.8% | +3.4 | 6.9 |
| (0.7, 0.8] | 50 | 75.5% | 72.0% | -3.5 | 6.1 |
| (0.8, 0.9] | 58 | 85.6% | 84.5% | -1.2 | 4.6 |
| (0.9, 1.0] | 196 | 95.7% | 98.0% | +2.2 | 1.4 |
| **all** | 411 | 82.4% | 81.0% | -1.4 | 1.7 |

## NCAAF
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 7 | 54.0% | 71.4% | +17.4 | 18.8 |
| (0.6, 0.7] | 12 | 63.7% | 58.3% | -5.4 | 13.9 |
| (0.7, 0.8] | 7 | 73.6% | 100.0% | +26.4 | 16.7 |
| (0.8, 0.9] | 11 | 84.8% | 90.9% | +6.1 | 10.8 |
| **all** | 37 | 70.0% | 78.4% | +8.4 | 7.3 |

## NFL
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 1 | 53.4% | 0.0% | -53.4 | 49.9 |
| (0.6, 0.7] | 1 | 63.6% | 100.0% | +36.4 | 48.1 |
| (0.7, 0.8] | 1 | 70.2% | 100.0% | +29.8 | 45.8 |
| **all** | 3 | 62.4% | 66.7% | +4.3 | 27.7 |

Gap within about 2x the noise column = the prices were right. Small samples: re-run as data grows (results.yml).