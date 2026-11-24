# NFL Prop Calibration
4098 player-lines (2+ books, last pregame quote) joined to play-by-play, 2026-10-25 to 2026-11-23.
Over side. 'Books said' = no-vig consensus chance of the over.

| stat | n | books said (over) | over hit | gap | noise ± |
|---|---|---|---|---|---|
| pass_att | 55 | 50.2% | 43.6% | -6.6 | 6.7 |
| pass_yds | 204 | 50.0% | 54.9% | +4.9 | 3.5 |
| rec | 793 | 48.5% | 46.2% | -2.4 | 1.8 |
| rec_yds | 1945 | 50.0% | 46.6% | -3.4 | 1.1 |
| rush_att | 181 | 49.9% | 43.1% | -6.8 | 3.7 |
| rush_yds | 920 | 50.0% | 45.5% | -4.4 | 1.6 |
| ALL | 4098 | 49.7% | 46.5% | -3.2 | 0.8 |

| priced (over) | n | books said | over hit | gap |
|---|---|---|---|---|
| (0.3, 0.4] | 92 | 37.6% | 41.3% | +3.7 |
| (0.4, 0.45] | 229 | 42.8% | 38.0% | -4.8 |
| (0.45, 0.55] | 3577 | 50.0% | 46.5% | -3.5 |
| (0.55, 0.6] | 140 | 56.9% | 57.1% | +0.2 |
| (0.6, 0.7] | 59 | 62.5% | 62.7% | +0.2 |
| (0.7, 1.0] | 1 | 71.2% | 0.0% | -71.2 |

Zero-stat games assumed (player known, no touch/target that day; true inactives would have voided): 186 of 4098. Results below with them counted as 0; 'matched only' excludes them (upper bound for overs).
- matched only pass_att: n=54, said 50.2%, over hit 44.4%
- matched only pass_yds: n=203, said 50.0%, over hit 55.2%
- matched only rec: n=741, said 48.5%, over hit 49.4%
- matched only rec_yds: n=1844, said 50.0%, over hit 49.2%
- matched only rush_att: n=179, said 49.9%, over hit 43.6%
- matched only rush_yds: n=891, said 50.0%, over hit 47.0%

Low lines (rec <=2.5, yards <20): n=1522, books said over 49.6%, over hit 48.9% (-0.7).