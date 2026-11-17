# Line Movement

Opening = first saved snapshot, closing = last saved snapshot before start (no-vig consensus, Pinnacle 2x, FanDuel 1.5x).

## Game moneylines (ncaab 532, ncaaf 96, nfl 15)
494 games with 2+ snapshots. Brier (lower = more accurate): open 0.1470, close 0.1454 -> close more accurate.

| moved toward a side by | n | open said | close said | that side won | won - open | noise ± |
|---|---|---|---|---|---|---|
| 1-2 pts | 89 | 50.1% | 51.6% | 59.6% | +9.4 | 4.3 |
| 2-4 pts | 86 | 52.5% | 55.4% | 55.8% | +3.4 | 4.8 |
| 4-8 pts | 48 | 54.6% | 60.1% | 62.5% | +7.9 | 6.6 |
| 8-100 pts | 18 | 56.6% | 67.1% | 66.7% | +10.0 | 11.2 |

## NBA player props (over side, same line at open and close)
138 props with 2+ snapshots. Brier (lower = more accurate): open 0.2480, close 0.2528 -> open more accurate.

| moved toward a side by | n | open said | close said | that side won | won - open | noise ± |
|---|---|---|---|---|---|---|
| 1-2 pts | 38 | 50.8% | 52.2% | 50.0% | -0.8 | 8.1 |
| 2-4 pts | 33 | 49.8% | 52.6% | 48.5% | -1.3 | 8.7 |
| 4-8 pts | 13 | 48.7% | 53.7% | 30.8% | -18.0 | 13.8 |
| 8-100 pts | 5 | 47.0% | 57.0% | 20.0% | -27.0 | 22.3 |

Read: if 'that side won' beats 'open said' by more than ~2x noise, line moves carry information -> bet early with the move / avoid betting against it. If close is more accurate than open, our prices should always come from the latest snapshot.
## NBA props by implied mean (line changes included)
7337 player-stat-days with an open and a close snapshot (median gap 4.8 h).
Average miss: open mean 3.01, close mean 3.00 (close more accurate).

### Found on (Oct 24 - Nov 14)
| stat | mean moved by | n | avg move | result vs open, in move direction | share of move realised |
|---|---|---|---|---|---|
| 3pm | 0.25-0.75 | 23 | 0.32 | -0.20 ± 0.31 | -60% |
| ast | 0.25-0.75 | 130 | 0.41 | +0.54 ± 0.20 | 134% |
| pra | 0.25-0.75 | 174 | 0.48 | +0.33 ± 0.63 | 69% |
| pra | 0.75-1.5 | 89 | 1.03 | +2.72 ± 0.89 | 265% |
| pra | 1.5-99 | 50 | 2.48 | +0.95 ± 1.19 | 38% |
| pts | 0.25-0.75 | 412 | 0.46 | +0.89 ± 0.32 | 194% |
| pts | 0.75-1.5 | 138 | 1.02 | +0.63 ± 0.53 | 62% |
| pts | 1.5-99 | 58 | 2.21 | +2.07 ± 0.93 | 93% |
| reb | 0.25-0.75 | 177 | 0.39 | +0.68 ± 0.19 | 176% |
| reb | 0.75-1.5 | 17 | 1.03 | -0.23 ± 0.59 | -22% |
| ALL | 0.25-0.75 | 916 | 0.44 | +0.67 ± 0.19 | 152% |
| ALL | 0.75-1.5 | 251 | 1.02 | +1.36 ± 0.44 | 133% |
| ALL | 1.5-99 | 111 | 2.32 | +1.47 ± 0.73 | 63% |

### Forward test (from Nov 15, 864 so far)
| stat | mean moved by | n | avg move | result vs open, in move direction | share of move realised |
|---|---|---|---|---|---|
| ast | 0.25-0.75 | 16 | 0.38 | +0.04 ± 0.39 | 11% |
| pra | 0.25-0.75 | 55 | 0.48 | -0.93 ± 1.22 | -196% |
| pra | 0.75-1.5 | 19 | 0.98 | +1.10 ± 1.59 | 112% |
| pts | 0.25-0.75 | 48 | 0.47 | +0.13 ± 1.00 | 27% |
| pts | 0.75-1.5 | 25 | 0.92 | -1.64 ± 1.32 | -179% |
| reb | 0.25-0.75 | 24 | 0.38 | +0.95 ± 0.44 | 249% |
| ALL | 0.25-0.75 | 145 | 0.44 | -0.16 ± 0.58 | -36% |
| ALL | 0.75-1.5 | 45 | 0.95 | -0.45 ± 1.00 | -47% |

Share realised ~100% = the move was right and the close is fair; >100% = moves under-react (bet with moves early); <0% = moves are noise/overreaction.