# Line Calibration

Do the books' prices match what happens? Favourite's no-vig win chance (consensus of all books, Pinnacle 2x, FanDuel 1.5x) from the last saved snapshot before kickoff, vs. how often the favourite actually won.
Games: 619 (ncaab 520, ncaaf 95, nfl 4). Data window: 2026-10-31 to 2026-11-15.

## All sports
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 114 | 54.7% | 46.5% | -8.2 | 4.7 |
| (0.6, 0.7] | 87 | 64.7% | 65.5% | +0.8 | 5.1 |
| (0.7, 0.8] | 87 | 75.3% | 72.4% | -2.9 | 4.6 |
| (0.8, 0.9] | 97 | 85.3% | 85.6% | +0.3 | 3.6 |
| (0.9, 1.0] | 234 | 95.7% | 98.3% | +2.6 | 1.3 |
| **all** | 619 | 79.3% | 78.5% | -0.8 | 1.5 |

## NCAAB
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 88 | 54.8% | 42.0% | -12.8 | 5.3 |
| (0.6, 0.7] | 64 | 65.1% | 68.8% | +3.7 | 6.0 |
| (0.7, 0.8] | 63 | 75.7% | 68.3% | -7.4 | 5.4 |
| (0.8, 0.9] | 73 | 85.5% | 86.3% | +0.8 | 4.1 |
| (0.9, 1.0] | 232 | 95.7% | 98.3% | +2.5 | 1.3 |
| **all** | 520 | 81.2% | 79.8% | -1.4 | 1.6 |

## NCAAF
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 24 | 54.3% | 62.5% | +8.2 | 10.2 |
| (0.6, 0.7] | 22 | 63.7% | 54.5% | -9.1 | 10.3 |
| (0.7, 0.8] | 23 | 74.3% | 82.6% | +8.3 | 9.1 |
| (0.8, 0.9] | 24 | 84.6% | 83.3% | -1.3 | 7.4 |
| (0.9, 1.0] | 2 | 93.7% | 100.0% | +6.3 | 17.2 |
| **all** | 95 | 69.8% | 71.6% | +1.8 | 4.5 |

## NFL
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 2 | 55.7% | 50.0% | -5.7 | 35.1 |
| (0.6, 0.7] | 1 | 63.6% | 100.0% | +36.4 | 48.1 |
| (0.7, 0.8] | 1 | 70.2% | 100.0% | +29.8 | 45.8 |
| **all** | 4 | 61.3% | 75.0% | +13.7 | 24.2 |

Gap within about 2x the noise column = the prices were right. Small samples: re-run as data grows (results.yml).