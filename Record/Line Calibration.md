# Line Calibration

Do the books' prices match what happens? Favourite's no-vig win chance (consensus of all books, Pinnacle 2x, FanDuel 1.5x) from the last saved snapshot before kickoff, vs. how often the favourite actually won.
Games: 689 (ncaab 616, ncaaf 68, nfl 5). Data window: 2026-10-31 to 2026-11-19.

## All sports
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 126 | 54.8% | 46.0% | -8.8 | 4.4 |
| (0.6, 0.7] | 95 | 64.6% | 70.5% | +5.9 | 4.9 |
| (0.7, 0.8] | 91 | 75.0% | 73.6% | -1.4 | 4.5 |
| (0.8, 0.9] | 104 | 85.5% | 83.7% | -1.8 | 3.5 |
| (0.9, 1.0] | 273 | 95.6% | 97.8% | +2.2 | 1.2 |
| **all** | 689 | 79.6% | 79.2% | -0.4 | 1.4 |

## NCAAB
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 107 | 54.8% | 43.9% | -10.9 | 4.8 |
| (0.6, 0.7] | 76 | 64.9% | 73.7% | +8.8 | 5.5 |
| (0.7, 0.8] | 73 | 75.3% | 69.9% | -5.5 | 5.0 |
| (0.8, 0.9] | 87 | 85.5% | 83.9% | -1.6 | 3.8 |
| (0.9, 1.0] | 273 | 95.6% | 97.8% | +2.2 | 1.2 |
| **all** | 616 | 80.9% | 80.2% | -0.7 | 1.4 |

## NCAAF
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 18 | 55.0% | 61.1% | +6.1 | 11.7 |
| (0.6, 0.7] | 16 | 63.6% | 56.2% | -7.3 | 12.0 |
| (0.7, 0.8] | 17 | 74.0% | 88.2% | +14.3 | 10.6 |
| (0.8, 0.9] | 17 | 85.0% | 82.4% | -2.6 | 8.7 |
| **all** | 68 | 69.3% | 72.1% | +2.8 | 5.4 |

## NFL
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 1 | 53.4% | 0.0% | -53.4 | 49.9 |
| (0.6, 0.7] | 3 | 64.4% | 66.7% | +2.2 | 27.6 |
| (0.7, 0.8] | 1 | 70.2% | 100.0% | +29.8 | 45.8 |
| **all** | 5 | 63.4% | 60.0% | -3.4 | 21.4 |

Gap within about 2x the noise column = the prices were right. Small samples: re-run as data grows (results.yml).