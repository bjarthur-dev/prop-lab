# NFL Prop Calibration
2896 player-lines (2+ books, last pregame quote) joined to play-by-play, 2026-10-25 to 2026-11-15.
Over side. 'Books said' = no-vig consensus chance of the over.

| stat | n | books said (over) | over hit | gap | noise ± |
|---|---|---|---|---|---|
| pass_att | 25 | 50.4% | 40.0% | -10.4 | 10.0 |
| pass_yds | 99 | 50.1% | 58.6% | +8.5 | 5.0 |
| rec | 581 | 48.5% | 46.0% | -2.6 | 2.1 |
| rec_yds | 1410 | 50.0% | 46.7% | -3.4 | 1.3 |
| rush_att | 112 | 49.9% | 45.5% | -4.4 | 4.7 |
| rush_yds | 669 | 49.9% | 45.7% | -4.2 | 1.9 |
| ALL | 2896 | 49.7% | 46.6% | -3.1 | 0.9 |

| priced (over) | n | books said | over hit | gap |
|---|---|---|---|---|
| (0.3, 0.4] | 68 | 37.5% | 42.6% | +5.1 |
| (0.4, 0.45] | 169 | 42.8% | 37.3% | -5.5 |
| (0.45, 0.55] | 2510 | 50.0% | 46.7% | -3.3 |
| (0.55, 0.6] | 107 | 57.0% | 55.1% | -1.9 |
| (0.6, 0.7] | 42 | 62.5% | 64.3% | +1.8 |

Zero-stat games assumed (player known, no touch/target that day; true inactives would have voided): 132 of 2896. Results below with them counted as 0; 'matched only' excludes them (upper bound for overs).
- matched only pass_att: n=25, said 50.4%, over hit 40.0%
- matched only pass_yds: n=99, said 50.1%, over hit 58.6%
- matched only rec: n=542, said 48.6%, over hit 49.3%
- matched only rec_yds: n=1338, said 50.1%, over hit 49.2%
- matched only rush_att: n=111, said 50.0%, over hit 45.9%
- matched only rush_yds: n=649, said 49.9%, over hit 47.1%

Low lines (rec <=2.5, yards <20): n=1089, books said over 49.6%, over hit 50.4% (+0.8).