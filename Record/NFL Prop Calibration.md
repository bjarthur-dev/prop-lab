# NFL Prop Calibration
3002 player-lines (2+ books, last pregame quote) joined to play-by-play, 2026-10-25 to 2026-11-16.
Over side. 'Books said' = no-vig consensus chance of the over.

| stat | n | books said (over) | over hit | gap | noise ± |
|---|---|---|---|---|---|
| pass_att | 28 | 50.4% | 42.9% | -7.6 | 9.4 |
| pass_yds | 105 | 50.1% | 58.1% | +8.0 | 4.9 |
| rec | 600 | 48.5% | 46.3% | -2.2 | 2.0 |
| rec_yds | 1458 | 50.0% | 47.1% | -2.9 | 1.3 |
| rush_att | 120 | 49.9% | 45.8% | -4.1 | 4.6 |
| rush_yds | 691 | 49.9% | 45.0% | -4.9 | 1.9 |
| ALL | 3002 | 49.7% | 46.8% | -2.9 | 0.9 |

| priced (over) | n | books said | over hit | gap |
|---|---|---|---|---|
| (0.3, 0.4] | 74 | 37.5% | 44.6% | +7.1 |
| (0.4, 0.45] | 171 | 42.7% | 38.0% | -4.7 |
| (0.45, 0.55] | 2601 | 50.0% | 46.7% | -3.3 |
| (0.55, 0.6] | 112 | 57.0% | 56.2% | -0.7 |
| (0.6, 0.7] | 44 | 62.6% | 63.6% | +1.0 |

Zero-stat games assumed (player known, no touch/target that day; true inactives would have voided): 144 of 3002. Results below with them counted as 0; 'matched only' excludes them (upper bound for overs).
- matched only pass_att: n=28, said 50.4%, over hit 42.9%
- matched only pass_yds: n=105, said 50.1%, over hit 58.1%
- matched only rec: n=558, said 48.5%, over hit 49.8%
- matched only rec_yds: n=1377, said 50.1%, over hit 49.9%
- matched only rush_att: n=119, said 50.0%, over hit 46.2%
- matched only rush_yds: n=671, said 49.9%, over hit 46.3%

Low lines (rec <=2.5, yards <20): n=1144, books said over 49.6%, over hit 49.8% (+0.2).