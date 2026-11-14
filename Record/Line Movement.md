# Line Movement

Opening = first saved snapshot, closing = last saved snapshot before start (no-vig consensus, Pinnacle 2x, FanDuel 1.5x).

## Game moneylines (ncaab 396, ncaaf 37, nfl 3)
332 games with 2+ snapshots. Brier (lower = more accurate): open 0.1314, close 0.1307 -> close more accurate.

| moved toward a side by | n | open said | close said | that side won | won - open | noise ± |
|---|---|---|---|---|---|---|
| 1-2 pts | 55 | 49.2% | 50.6% | 58.2% | +9.0 | 5.2 |
| 2-4 pts | 47 | 49.6% | 52.5% | 61.7% | +12.1 | 6.4 |
| 4-8 pts | 22 | 55.4% | 60.9% | 59.1% | +3.7 | 9.7 |
| 8-100 pts | 7 | 54.0% | 64.0% | 42.9% | -11.1 | 17.5 |

## NBA player props (over side, same line at open and close)
78 props with 2+ snapshots. Brier (lower = more accurate): open 0.2481, close 0.2515 -> open more accurate.

| moved toward a side by | n | open said | close said | that side won | won - open | noise ± |
|---|---|---|---|---|---|---|
| 1-2 pts | 28 | 51.2% | 52.7% | 50.0% | -1.2 | 9.4 |
| 2-4 pts | 16 | 48.4% | 50.9% | 50.0% | +1.6 | 12.5 |
| 4-8 pts | 6 | 49.5% | 54.3% | 33.3% | -16.2 | 20.4 |

Read: if 'that side won' beats 'open said' by more than ~2x noise, line moves carry information -> bet early with the move / avoid betting against it. If close is more accurate than open, our prices should always come from the latest snapshot.
## NBA props by implied mean (line changes included)
6245 player-stat-days with an open and a close snapshot (median gap 4.8 h).
Average miss: open mean 2.99, close mean 2.98 (close more accurate).

| stat | mean moved by | n | avg move | result vs open, in move direction | share of move realised |
|---|---|---|---|---|---|
| 3pm | 0.25-0.75 | 23 | 0.32 | -0.20 ± 0.31 | -60% |
| ast | 0.25-0.75 | 126 | 0.41 | +0.57 ± 0.21 | 141% |
| pra | 0.25-0.75 | 165 | 0.48 | +0.41 ± 0.65 | 85% |
| pra | 0.75-1.5 | 86 | 1.03 | +2.90 ± 0.90 | 282% |
| pra | 1.5-99 | 44 | 2.51 | +0.72 ± 1.27 | 29% |
| pts | 0.25-0.75 | 398 | 0.46 | +0.90 ± 0.32 | 195% |
| pts | 0.75-1.5 | 133 | 1.01 | +0.54 ± 0.54 | 53% |
| pts | 1.5-99 | 55 | 2.24 | +2.31 ± 0.97 | 103% |
| reb | 0.25-0.75 | 171 | 0.39 | +0.75 ± 0.19 | 193% |
| reb | 0.75-1.5 | 16 | 1.01 | -0.47 ± 0.57 | -47% |

Share realised ~100% = the move was right and the close is fair; >100% = moves under-react (bet with moves early); <0% = moves are noise/overreaction.