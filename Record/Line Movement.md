# Line Movement

Opening = first saved snapshot, closing = last saved snapshot before start (no-vig consensus, Pinnacle 2x, FanDuel 1.5x).

## Game moneylines (ncaab 819, ncaaf 88, nfl 10)
710 games with 2+ snapshots. Brier (lower = more accurate): open 0.1578, close 0.1561 -> close more accurate.

| moved toward a side by | n | open said | close said | that side won | won - open | noise ± |
|---|---|---|---|---|---|---|
| 1-2 pts | 144 | 48.5% | 50.0% | 51.4% | +2.9 | 3.5 |
| 2-4 pts | 121 | 51.6% | 54.5% | 60.3% | +8.7 | 4.1 |
| 4-8 pts | 71 | 48.4% | 53.9% | 53.5% | +5.1 | 5.6 |
| 8-100 pts | 22 | 52.4% | 63.4% | 63.6% | +11.3 | 10.0 |

## NBA player props (over side, same line at open and close)
198 props with 2+ snapshots. Brier (lower = more accurate): open 0.2436, close 0.2472 -> open more accurate.

| moved toward a side by | n | open said | close said | that side won | won - open | noise ± |
|---|---|---|---|---|---|---|
| 1-2 pts | 46 | 50.8% | 52.2% | 54.3% | +3.5 | 7.3 |
| 2-4 pts | 47 | 50.4% | 53.2% | 48.9% | -1.5 | 7.2 |
| 4-8 pts | 23 | 47.6% | 52.8% | 39.1% | -8.5 | 10.4 |
| 8-100 pts | 6 | 46.3% | 56.2% | 16.7% | -29.7 | 20.3 |

Read: if 'that side won' beats 'open said' by more than ~2x noise, line moves carry information -> bet early with the move / avoid betting against it. If close is more accurate than open, our prices should always come from the latest snapshot.
## NBA props by implied mean (line changes included)
10610 player-stat-days with an open and a close snapshot (median gap 5.3 h).
Average miss: open mean 3.07, close mean 3.06 (close more accurate).

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

### Forward test (from Nov 15, 4137 so far)
| stat | mean moved by | n | avg move | result vs open, in move direction | share of move realised |
|---|---|---|---|---|---|
| 3pm | 0.25-0.75 | 16 | 0.31 | +0.44 ± 0.30 | 140% |
| ast | 0.25-0.75 | 88 | 0.37 | +0.58 ± 0.23 | 156% |
| pra | 0.25-0.75 | 160 | 0.45 | -0.12 ± 0.68 | -27% |
| pra | 0.75-1.5 | 39 | 0.99 | +0.70 ± 1.12 | 71% |
| pts | 0.25-0.75 | 230 | 0.45 | +0.14 ± 0.44 | 32% |
| pts | 0.75-1.5 | 116 | 0.97 | -0.18 ± 0.58 | -19% |
| pts | 1.5-99 | 25 | 2.11 | +2.37 ± 0.97 | 112% |
| reb | 0.25-0.75 | 122 | 0.39 | +0.32 ± 0.26 | 83% |
| ALL | 0.25-0.75 | 616 | 0.42 | +0.18 ± 0.25 | 43% |
| ALL | 0.75-1.5 | 173 | 0.97 | +0.10 ± 0.47 | 11% |
| ALL | 1.5-99 | 39 | 2.11 | +2.23 ± 0.90 | 106% |

Share realised ~100% = the move was right and the close is fair; >100% = moves under-react (bet with moves early); <0% = moves are noise/overreaction.