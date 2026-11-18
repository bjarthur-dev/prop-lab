# Line Movement

Opening = first saved snapshot, closing = last saved snapshot before start (no-vig consensus, Pinnacle 2x, FanDuel 1.5x).

## Game moneylines (ncaab 527, ncaaf 63, nfl 16)
460 games with 2+ snapshots. Brier (lower = more accurate): open 0.1446, close 0.1429 -> close more accurate.

| moved toward a side by | n | open said | close said | that side won | won - open | noise ± |
|---|---|---|---|---|---|---|
| 1-2 pts | 86 | 50.5% | 52.0% | 58.1% | +7.6 | 4.3 |
| 2-4 pts | 76 | 50.4% | 53.3% | 59.2% | +8.8 | 5.1 |
| 4-8 pts | 37 | 54.0% | 59.4% | 59.5% | +5.4 | 7.5 |
| 8-100 pts | 18 | 56.7% | 67.4% | 66.7% | +9.9 | 11.2 |

## NBA player props (over side, same line at open and close)
158 props with 2+ snapshots. Brier (lower = more accurate): open 0.2477, close 0.2522 -> open more accurate.

| moved toward a side by | n | open said | close said | that side won | won - open | noise ± |
|---|---|---|---|---|---|---|
| 1-2 pts | 42 | 50.7% | 52.0% | 54.8% | +4.1 | 7.7 |
| 2-4 pts | 38 | 49.8% | 52.6% | 47.4% | -2.4 | 8.1 |
| 4-8 pts | 15 | 48.3% | 53.3% | 33.3% | -15.0 | 12.9 |
| 8-100 pts | 6 | 46.3% | 56.2% | 16.7% | -29.7 | 20.3 |

Read: if 'that side won' beats 'open said' by more than ~2x noise, line moves carry information -> bet early with the move / avoid betting against it. If close is more accurate than open, our prices should always come from the latest snapshot.
## NBA props by implied mean (line changes included)
7586 player-stat-days with an open and a close snapshot (median gap 4.8 h).
Average miss: open mean 3.03, close mean 3.02 (close more accurate).

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

### Forward test (from Nov 15, 1113 so far)
| stat | mean moved by | n | avg move | result vs open, in move direction | share of move realised |
|---|---|---|---|---|---|
| ast | 0.25-0.75 | 27 | 0.36 | +0.69 ± 0.36 | 188% |
| pra | 0.25-0.75 | 64 | 0.47 | -0.48 ± 1.12 | -103% |
| pra | 0.75-1.5 | 21 | 0.97 | +0.75 ± 1.45 | 77% |
| pts | 0.25-0.75 | 67 | 0.45 | -0.00 ± 0.82 | -0% |
| pts | 0.75-1.5 | 33 | 0.94 | -0.23 ± 1.14 | -24% |
| reb | 0.25-0.75 | 36 | 0.39 | +0.85 ± 0.40 | 217% |
| ALL | 0.25-0.75 | 199 | 0.43 | +0.09 ± 0.46 | 21% |
| ALL | 0.75-1.5 | 57 | 0.95 | +0.17 ± 0.85 | 18% |

Share realised ~100% = the move was right and the close is fair; >100% = moves under-react (bet with moves early); <0% = moves are noise/overreaction.