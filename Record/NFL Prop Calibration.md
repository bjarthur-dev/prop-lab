# NFL Prop Calibration
4396 player-lines (2+ books, last pregame quote) joined to play-by-play, 2026-10-25 to 2026-11-26.
Over side. 'Books said' = no-vig consensus chance of the over.

| stat | n | books said (over) | over hit | gap | noise ± |
|---|---|---|---|---|---|
| pass_att | 55 | 50.2% | 43.6% | -6.6 | 6.7 |
| pass_yds | 222 | 50.0% | 53.6% | +3.6 | 3.4 |
| rec | 858 | 48.6% | 45.1% | -3.5 | 1.7 |
| rec_yds | 2088 | 50.0% | 45.5% | -4.6 | 1.1 |
| rush_att | 195 | 49.8% | 42.6% | -7.3 | 3.6 |
| rush_yds | 978 | 49.9% | 46.0% | -3.9 | 1.6 |
| ALL | 4396 | 49.7% | 45.8% | -3.9 | 0.8 |

| priced (over) | n | books said | over hit | gap |
|---|---|---|---|---|
| (0.3, 0.4] | 100 | 37.6% | 39.0% | +1.4 |
| (0.4, 0.45] | 251 | 42.8% | 36.3% | -6.5 |
| (0.45, 0.55] | 3827 | 50.0% | 45.9% | -4.1 |
| (0.55, 0.6] | 153 | 57.0% | 55.6% | -1.4 |
| (0.6, 0.7] | 64 | 62.4% | 62.5% | +0.1 |
| (0.7, 1.0] | 1 | 71.2% | 0.0% | -71.2 |

Zero-stat games assumed (player known, no touch/target that day; true inactives would have voided): 201 of 4396. Results below with them counted as 0; 'matched only' excludes them (upper bound for overs).
- matched only pass_att: n=54, said 50.2%, over hit 44.4%
- matched only pass_yds: n=221, said 50.0%, over hit 53.8%
- matched only rec: n=800, said 48.6%, over hit 48.4%
- matched only rec_yds: n=1979, said 50.0%, over hit 48.0%
- matched only rush_att: n=193, said 49.9%, over hit 43.0%
- matched only rush_yds: n=948, said 49.9%, over hit 47.5%

Low lines (rec <=2.5, yards <20): n=1630, books said over 49.6%, over hit 48.3% (-1.3).