# Line Calibration

Do the books' prices match what happens? Favourite's no-vig win chance (consensus of all books, Pinnacle 2x, FanDuel 1.5x) from the last saved snapshot before kickoff, vs. how often the favourite actually won.
Games: 613 (ncaab 534, ncaaf 63, nfl 16). Data window: 2026-10-31 to 2026-11-17.

## All sports
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 108 | 54.9% | 42.6% | -12.3 | 4.8 |
| (0.6, 0.7] | 89 | 64.6% | 68.5% | +3.9 | 5.1 |
| (0.7, 0.8] | 80 | 75.1% | 72.5% | -2.6 | 4.8 |
| (0.8, 0.9] | 97 | 85.3% | 86.6% | +1.3 | 3.6 |
| (0.9, 1.0] | 239 | 95.7% | 97.9% | +2.2 | 1.3 |
| **all** | 613 | 79.7% | 78.8% | -0.9 | 1.5 |

## NCAAB
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 88 | 55.0% | 39.8% | -15.2 | 5.3 |
| (0.6, 0.7] | 66 | 64.9% | 71.2% | +6.3 | 5.9 |
| (0.7, 0.8] | 62 | 75.5% | 67.7% | -7.7 | 5.5 |
| (0.8, 0.9] | 79 | 85.5% | 87.3% | +1.8 | 4.0 |
| (0.9, 1.0] | 239 | 95.7% | 97.9% | +2.2 | 1.3 |
| **all** | 534 | 81.3% | 80.0% | -1.3 | 1.5 |

## NCAAF
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 16 | 54.7% | 62.5% | +7.8 | 12.4 |
| (0.6, 0.7] | 16 | 63.6% | 56.2% | -7.3 | 12.0 |
| (0.7, 0.8] | 15 | 73.6% | 86.7% | +13.0 | 11.4 |
| (0.8, 0.9] | 16 | 85.0% | 81.2% | -3.8 | 8.9 |
| **all** | 63 | 69.2% | 71.4% | +2.3 | 5.6 |

## NFL
| favourite priced | games | books said | actually won | gap (pts) | noise ± |
|---|---|---|---|---|---|
| (0.5, 0.6] | 4 | 54.9% | 25.0% | -29.9 | 24.9 |
| (0.6, 0.7] | 7 | 64.2% | 71.4% | +7.2 | 18.1 |
| (0.7, 0.8] | 3 | 73.7% | 100.0% | +26.3 | 25.4 |
| (0.8, 0.9] | 2 | 81.5% | 100.0% | +18.5 | 27.4 |
| **all** | 16 | 65.8% | 68.8% | +2.9 | 11.6 |

Gap within about 2x the noise column = the prices were right. Small samples: re-run as data grows (results.yml).