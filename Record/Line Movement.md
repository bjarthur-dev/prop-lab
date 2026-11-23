# Line Movement

Opening = first saved snapshot, closing = last saved snapshot before start (no-vig consensus, Pinnacle 2x, FanDuel 1.5x).

## Game moneylines (ncaab 737, ncaaf 130, nfl 7)
670 games with 2+ snapshots. Brier (lower = more accurate): open 0.1590, close 0.1578 -> close more accurate.

| moved toward a side by | n | open said | close said | that side won | won - open | noise ± |
|---|---|---|---|---|---|---|
| 1-2 pts | 135 | 48.3% | 49.8% | 52.6% | +4.3 | 3.5 |
| 2-4 pts | 132 | 51.8% | 54.6% | 59.1% | +7.3 | 3.9 |
| 4-8 pts | 71 | 51.6% | 57.0% | 50.7% | -0.9 | 5.5 |
| 8-100 pts | 20 | 54.9% | 65.8% | 70.0% | +15.1 | 10.6 |

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
9531 player-stat-days with an open and a close snapshot (median gap 5.1 h).
Average miss: open mean 3.08, close mean 3.07 (close more accurate).

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

### Forward test (from Nov 15, 3058 so far)
| stat | mean moved by | n | avg move | result vs open, in move direction | share of move realised |
|---|---|---|---|---|---|
| ast | 0.25-0.75 | 69 | 0.37 | +0.86 ± 0.24 | 234% |
| pra | 0.25-0.75 | 129 | 0.46 | +0.03 ± 0.75 | 6% |
| pra | 0.75-1.5 | 31 | 0.97 | +1.55 ± 1.20 | 160% |
| pts | 0.25-0.75 | 174 | 0.46 | +0.32 ± 0.52 | 69% |
| pts | 0.75-1.5 | 92 | 0.96 | -0.06 ± 0.65 | -6% |
| pts | 1.5-99 | 16 | 2.15 | +1.76 ± 1.24 | 82% |
| reb | 0.25-0.75 | 101 | 0.39 | +0.43 ± 0.27 | 112% |
| ALL | 0.25-0.75 | 486 | 0.43 | +0.34 ± 0.28 | 79% |
| ALL | 0.75-1.5 | 140 | 0.95 | +0.36 ± 0.50 | 38% |
| ALL | 1.5-99 | 22 | 2.10 | +1.01 ± 1.05 | 48% |

Share realised ~100% = the move was right and the close is fair; >100% = moves under-react (bet with moves early); <0% = moves are noise/overreaction.