# NFL Prop Calibration
3106 player-lines (2+ books, last pregame quote) joined to play-by-play, 2026-10-25 to 2026-11-19.
Over side. 'Books said' = no-vig consensus chance of the over.

| stat | n | books said (over) | over hit | gap | noise ± |
|---|---|---|---|---|---|
| pass_att | 31 | 50.4% | 38.7% | -11.7 | 9.0 |
| pass_yds | 120 | 50.0% | 50.8% | +0.8 | 4.6 |
| rec | 615 | 48.5% | 46.0% | -2.5 | 2.0 |
| rec_yds | 1505 | 50.0% | 46.7% | -3.3 | 1.3 |
| rush_att | 124 | 50.0% | 45.2% | -4.8 | 4.5 |
| rush_yds | 711 | 49.9% | 45.3% | -4.7 | 1.9 |
| ALL | 3106 | 49.7% | 46.3% | -3.5 | 0.9 |

| priced (over) | n | books said | over hit | gap |
|---|---|---|---|---|
| (0.3, 0.4] | 75 | 37.5% | 44.0% | +6.5 |
| (0.4, 0.45] | 176 | 42.7% | 37.5% | -5.2 |
| (0.45, 0.55] | 2692 | 50.0% | 46.2% | -3.7 |
| (0.55, 0.6] | 118 | 56.9% | 55.1% | -1.8 |
| (0.6, 0.7] | 45 | 62.5% | 62.2% | -0.3 |

Zero-stat games assumed (player known, no touch/target that day; true inactives would have voided): 144 of 3106. Results below with them counted as 0; 'matched only' excludes them (upper bound for overs).
- matched only pass_att: n=31, said 50.4%, over hit 38.7%
- matched only pass_yds: n=120, said 50.0%, over hit 50.8%
- matched only rec: n=573, said 48.5%, over hit 49.4%
- matched only rec_yds: n=1424, said 50.1%, over hit 49.4%
- matched only rush_att: n=123, said 50.0%, over hit 45.5%
- matched only rush_yds: n=691, said 49.9%, over hit 46.6%

Low lines (rec <=2.5, yards <20): n=1172, books said over 49.6%, over hit 50.1% (+0.5).