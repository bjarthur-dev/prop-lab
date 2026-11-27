# Line Calibration

Do the books' prices match what happens? Favourite's no-vig win chance (consensus of all books, Pinnacle 2x, FanDuel 1.5x) from the last saved snapshot before kickoff, vs. how often the favourite actually won.
Games: 918 (ncaab 820, ncaaf 88, nfl 10). Data window: 2026-10-31 to 2026-11-26.

## All sports
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 200 | 54.7% | 48.0% | -6.7 | 3.5 |
| (0.6, 0.7] | 145 | 64.3% | 64.8% | +0.5 | 4.0 |
| (0.7, 0.8] | 130 | 75.0% | 74.6% | -0.4 | 3.8 |
| (0.8, 0.9] | 132 | 85.5% | 82.6% | -3.0 | 3.1 |
| (0.9, 1.0] | 311 | 95.5% | 98.4% | +2.9 | 1.2 |
| **all** | 918 | 77.4% | 76.5% | -0.9 | 1.3 |

## NCAAB
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 176 | 54.7% | 46.0% | -8.6 | 3.8 |
| (0.6, 0.7] | 120 | 64.4% | 65.0% | +0.6 | 4.4 |
| (0.7, 0.8] | 105 | 75.4% | 71.4% | -3.9 | 4.2 |
| (0.8, 0.9] | 109 | 85.5% | 82.6% | -3.0 | 3.4 |
| (0.9, 1.0] | 310 | 95.5% | 98.4% | +2.9 | 1.2 |
| **all** | 820 | 78.3% | 76.7% | -1.6 | 1.3 |

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
| (0.5, 0.6] | 3 | 54.1% | 66.7% | +12.6 | 28.8 |
| (0.6, 0.7] | 4 | 64.5% | 75.0% | +10.5 | 23.9 |
| (0.7, 0.8] | 2 | 71.2% | 50.0% | -21.2 | 32.0 |
| (0.8, 0.9] | 1 | 84.7% | 100.0% | +15.3 | 36.0 |
| **all** | 10 | 64.8% | 70.0% | +5.2 | 14.8 |

Gap within about 2x the noise column = the prices were right. Small samples: re-run as data grows (results.yml).