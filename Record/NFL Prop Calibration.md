# NFL Prop Calibration
2123 player-lines (2+ books, last pregame quote) joined to play-by-play, 2026-10-25 to 2026-11-12.
Over side. 'Books said' = no-vig consensus chance of the over.

| stat | n | books said (over) | over hit | gap | noise ± |
|---|---|---|---|---|---|
| pass_yds | 55 | 50.0% | 60.0% | +10.0 | 6.7 |
| rec | 408 | 48.5% | 47.8% | -0.7 | 2.4 |
| rec_yds | 1083 | 50.0% | 46.3% | -3.8 | 1.5 |
| rush_att | 64 | 49.7% | 46.9% | -2.8 | 6.2 |
| rush_yds | 513 | 50.0% | 45.0% | -4.9 | 2.2 |
| ALL | 2123 | 49.7% | 46.6% | -3.1 | 1.1 |

| priced (over) | n | books said | over hit | gap |
|---|---|---|---|---|
| (0.3, 0.4] | 51 | 37.8% | 41.2% | +3.4 |
| (0.4, 0.45] | 113 | 42.7% | 38.9% | -3.8 |
| (0.45, 0.55] | 1860 | 50.0% | 46.5% | -3.5 |
| (0.55, 0.6] | 72 | 56.9% | 61.1% | +4.2 |
| (0.6, 0.7] | 27 | 62.5% | 63.0% | +0.5 |

Zero-stat games assumed (player known, no touch/target that day; true inactives would have voided): 104 of 2123. Results below with them counted as 0; 'matched only' excludes them (upper bound for overs).
- matched only pass_yds: n=55, said 50.0%, over hit 60.0%
- matched only rec: n=379, said 48.5%, over hit 51.5%
- matched only rec_yds: n=1029, said 50.0%, over hit 48.7%
- matched only rush_att: n=63, said 49.8%, over hit 47.6%
- matched only rush_yds: n=493, said 50.0%, over hit 46.9%

Low lines (rec <=2.5, yards <20): n=829, books said over 49.6%, over hit 49.8% (+0.3).