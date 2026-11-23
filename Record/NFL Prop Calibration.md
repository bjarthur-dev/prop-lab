# NFL Prop Calibration
4006 player-lines (2+ books, last pregame quote) joined to play-by-play, 2026-10-25 to 2026-11-22.
Over side. 'Books said' = no-vig consensus chance of the over.

| stat | n | books said (over) | over hit | gap | noise ± |
|---|---|---|---|---|---|
| pass_att | 55 | 50.2% | 43.6% | -6.6 | 6.7 |
| pass_yds | 195 | 50.0% | 54.4% | +4.4 | 3.6 |
| rec | 778 | 48.6% | 46.4% | -2.2 | 1.8 |
| rec_yds | 1895 | 50.0% | 46.8% | -3.2 | 1.1 |
| rush_att | 178 | 49.9% | 43.3% | -6.6 | 3.7 |
| rush_yds | 905 | 50.0% | 45.4% | -4.5 | 1.7 |
| ALL | 4006 | 49.7% | 46.6% | -3.1 | 0.8 |

| priced (over) | n | books said | over hit | gap |
|---|---|---|---|---|
| (0.3, 0.4] | 89 | 37.6% | 41.6% | +4.0 |
| (0.4, 0.45] | 225 | 42.8% | 38.2% | -4.5 |
| (0.45, 0.55] | 3494 | 50.0% | 46.5% | -3.4 |
| (0.55, 0.6] | 139 | 56.9% | 57.6% | +0.6 |
| (0.6, 0.7] | 58 | 62.5% | 63.8% | +1.3 |
| (0.7, 1.0] | 1 | 71.2% | 0.0% | -71.2 |

Zero-stat games assumed (player known, no touch/target that day; true inactives would have voided): 176 of 4006. Results below with them counted as 0; 'matched only' excludes them (upper bound for overs).
- matched only pass_att: n=54, said 50.2%, over hit 44.4%
- matched only pass_yds: n=194, said 50.0%, over hit 54.6%
- matched only rec: n=728, said 48.6%, over hit 49.6%
- matched only rec_yds: n=1800, said 50.0%, over hit 49.3%
- matched only rush_att: n=176, said 49.9%, over hit 43.8%
- matched only rush_yds: n=878, said 50.0%, over hit 46.8%

Low lines (rec <=2.5, yards <20): n=1490, books said over 49.6%, over hit 49.3% (-0.3).