# Line Movement

Opening = first saved snapshot, closing = last saved snapshot before start (no-vig consensus, Pinnacle 2x, FanDuel 1.5x).

## Game moneylines (ncaab 644, ncaaf 69, nfl 6)
549 games with 2+ snapshots. Brier (lower = more accurate): open 0.1497, close 0.1475 -> close more accurate.

| moved toward a side by | n | open said | close said | that side won | won - open | noise ± |
|---|---|---|---|---|---|---|
| 1-2 pts | 107 | 49.4% | 50.9% | 56.1% | +6.7 | 3.9 |
| 2-4 pts | 99 | 51.1% | 54.0% | 63.6% | +12.5 | 4.5 |
| 4-8 pts | 52 | 50.0% | 55.4% | 53.8% | +3.8 | 6.4 |
| 8-100 pts | 19 | 55.3% | 66.3% | 68.4% | +13.1 | 10.9 |

## NBA player props (over side, same line at open and close)
190 props with 2+ snapshots. Brier (lower = more accurate): open 0.2444, close 0.2486 -> open more accurate.

| moved toward a side by | n | open said | close said | that side won | won - open | noise ± |
|---|---|---|---|---|---|---|
| 1-2 pts | 43 | 50.7% | 52.1% | 53.5% | +2.8 | 7.6 |
| 2-4 pts | 45 | 50.0% | 52.8% | 46.7% | -3.4 | 7.4 |
| 4-8 pts | 22 | 47.5% | 52.6% | 36.4% | -11.1 | 10.6 |
| 8-100 pts | 6 | 46.3% | 56.2% | 16.7% | -29.7 | 20.3 |

Read: if 'that side won' beats 'open said' by more than ~2x noise, line moves carry information -> bet early with the move / avoid betting against it. If close is more accurate than open, our prices should always come from the latest snapshot.
## NBA props by implied mean (line changes included)
8952 player-stat-days with an open and a close snapshot (median gap 5.2 h).
Average miss: open mean 3.05, close mean 3.05 (close more accurate).

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

### Forward test (from Nov 15, 2479 so far)
| stat | mean moved by | n | avg move | result vs open, in move direction | share of move realised |
|---|---|---|---|---|---|
| ast | 0.25-0.75 | 60 | 0.38 | +0.91 ± 0.26 | 244% |
| pra | 0.25-0.75 | 112 | 0.45 | +0.09 ± 0.83 | 19% |
| pra | 0.75-1.5 | 25 | 0.96 | +1.62 ± 1.36 | 168% |
| pts | 0.25-0.75 | 142 | 0.46 | +0.18 ± 0.54 | 38% |
| pts | 0.75-1.5 | 84 | 0.95 | -0.38 ± 0.67 | -40% |
| reb | 0.25-0.75 | 90 | 0.39 | +0.52 ± 0.29 | 136% |
| ALL | 0.25-0.75 | 417 | 0.43 | +0.34 ± 0.30 | 79% |
| ALL | 0.75-1.5 | 125 | 0.94 | +0.09 ± 0.53 | 10% |
| ALL | 1.5-99 | 20 | 2.08 | +0.85 ± 1.08 | 41% |

Share realised ~100% = the move was right and the close is fair; >100% = moves under-react (bet with moves early); <0% = moves are noise/overreaction.