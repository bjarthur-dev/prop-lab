# Line Calibration

Do the books' prices match what happens? Favourite's no-vig win chance (consensus of all books, Pinnacle 2x, FanDuel 1.5x) from the last saved snapshot before kickoff, vs. how often the favourite actually won.
Games: 657 (ncaab 546, ncaaf 96, nfl 15). Data window: 2026-10-31 to 2026-11-16.

## All sports
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 123 | 54.8% | 47.2% | -7.7 | 4.5 |
| (0.6, 0.7] | 95 | 64.5% | 66.3% | +1.8 | 4.9 |
| (0.7, 0.8] | 94 | 75.2% | 72.3% | -2.8 | 4.5 |
| (0.8, 0.9] | 106 | 85.2% | 86.8% | +1.6 | 3.4 |
| (0.9, 1.0] | 239 | 95.7% | 98.3% | +2.7 | 1.3 |
| **all** | 657 | 78.9% | 78.5% | -0.4 | 1.5 |

## NCAAB
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 94 | 54.9% | 43.6% | -11.3 | 5.1 |
| (0.6, 0.7] | 67 | 64.9% | 68.7% | +3.8 | 5.8 |
| (0.7, 0.8] | 68 | 75.5% | 67.6% | -7.9 | 5.2 |
| (0.8, 0.9] | 80 | 85.5% | 87.5% | +2.0 | 3.9 |
| (0.9, 1.0] | 237 | 95.7% | 98.3% | +2.6 | 1.3 |
| **all** | 546 | 80.9% | 79.9% | -1.0 | 1.5 |

## NCAAF
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 25 | 54.4% | 64.0% | +9.6 | 10.0 |
| (0.6, 0.7] | 22 | 63.7% | 54.5% | -9.1 | 10.3 |
| (0.7, 0.8] | 23 | 74.3% | 82.6% | +8.3 | 9.1 |
| (0.8, 0.9] | 24 | 84.6% | 83.3% | -1.3 | 7.4 |
| (0.9, 1.0] | 2 | 93.7% | 100.0% | +6.3 | 17.2 |
| **all** | 96 | 69.7% | 71.9% | +2.2 | 4.5 |

## NFL
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 4 | 54.9% | 25.0% | -29.9 | 24.9 |
| (0.6, 0.7] | 6 | 63.9% | 83.3% | +19.5 | 19.6 |
| (0.7, 0.8] | 3 | 73.7% | 100.0% | +26.3 | 25.4 |
| (0.8, 0.9] | 2 | 81.5% | 100.0% | +18.5 | 27.4 |
| **all** | 15 | 65.8% | 73.3% | +7.6 | 12.0 |

Gap within about 2x the noise column = the prices were right. Small samples: re-run as data grows (results.yml).