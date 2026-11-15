# Line Movement

Opening = first saved snapshot, closing = last saved snapshot before start (no-vig consensus, Pinnacle 2x, FanDuel 1.5x).

## Game moneylines (ncaab 504, ncaaf 95, nfl 3)
469 games with 2+ snapshots. Brier (lower = more accurate): open 0.1449, close 0.1442 -> close more accurate.

| moved toward a side by | n | open said | close said | that side won | won - open | noise ± |
|---|---|---|---|---|---|---|
| 1-2 pts | 84 | 49.7% | 51.2% | 59.5% | +9.8 | 4.4 |
| 2-4 pts | 79 | 52.1% | 55.0% | 55.7% | +3.6 | 5.0 |
| 4-8 pts | 46 | 53.8% | 59.3% | 63.0% | +9.3 | 6.7 |
| 8-100 pts | 14 | 55.4% | 66.3% | 50.0% | -5.4 | 12.6 |

## NBA player props (over side, same line at open and close)
131 props with 2+ snapshots. Brier (lower = more accurate): open 0.2491, close 0.2554 -> open more accurate.

| moved toward a side by | n | open said | close said | that side won | won - open | noise ± |
|---|---|---|---|---|---|---|
| 1-2 pts | 38 | 50.8% | 52.2% | 50.0% | -0.8 | 8.1 |
| 2-4 pts | 30 | 49.4% | 52.2% | 43.3% | -6.1 | 9.1 |
| 4-8 pts | 11 | 48.0% | 53.0% | 27.3% | -20.7 | 15.0 |

Read: if 'that side won' beats 'open said' by more than ~2x noise, line moves carry information -> bet early with the move / avoid betting against it. If close is more accurate than open, our prices should always come from the latest snapshot.
## NBA props by implied mean (line changes included)
6473 player-stat-days with an open and a close snapshot (median gap 4.8 h).
Average miss: open mean 2.98, close mean 2.97 (close more accurate).

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

Forward test starts Nov 15.

Share realised ~100% = the move was right and the close is fair; >100% = moves under-react (bet with moves early); <0% = moves are noise/overreaction.