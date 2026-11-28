# Line Movement

Opening = first saved snapshot, closing = last saved snapshot before start (no-vig consensus, Pinnacle 2x, FanDuel 1.5x).

## Game moneylines (ncaab 825, ncaaf 94, nfl 12)
723 games with 2+ snapshots. Brier (lower = more accurate): open 0.1581, close 0.1560 -> close more accurate.

| moved toward a side by | n | open said | close said | that side won | won - open | noise ± |
|---|---|---|---|---|---|---|
| 1-2 pts | 144 | 48.5% | 50.0% | 50.7% | +2.2 | 3.4 |
| 2-4 pts | 120 | 51.1% | 54.0% | 59.2% | +8.0 | 4.1 |
| 4-8 pts | 81 | 48.0% | 53.4% | 51.9% | +3.9 | 5.2 |
| 8-100 pts | 26 | 49.5% | 61.5% | 65.4% | +15.9 | 9.2 |

## NBA player props (over side, same line at open and close)
199 props with 2+ snapshots. Brier (lower = more accurate): open 0.2437, close 0.2470 -> open more accurate.

| moved toward a side by | n | open said | close said | that side won | won - open | noise ± |
|---|---|---|---|---|---|---|
| 1-2 pts | 46 | 50.8% | 52.2% | 54.3% | +3.5 | 7.3 |
| 2-4 pts | 47 | 50.4% | 53.2% | 48.9% | -1.5 | 7.2 |
| 4-8 pts | 24 | 47.6% | 52.8% | 41.7% | -6.0 | 10.2 |
| 8-100 pts | 6 | 46.3% | 56.2% | 16.7% | -29.7 | 20.3 |

Read: if 'that side won' beats 'open said' by more than ~2x noise, line moves carry information -> bet early with the move / avoid betting against it. If close is more accurate than open, our prices should always come from the latest snapshot.
## NBA props by implied mean (line changes included)
11273 player-stat-days with an open and a close snapshot (median gap 5.2 h).
Average miss: open mean 3.05, close mean 3.04 (close more accurate).

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

### Forward test (from Nov 15, 4800 so far)
| stat | mean moved by | n | avg move | result vs open, in move direction | share of move realised |
|---|---|---|---|---|---|
| 3pm | 0.25-0.75 | 16 | 0.31 | +0.44 ± 0.30 | 140% |
| ast | 0.25-0.75 | 98 | 0.38 | +0.49 ± 0.22 | 130% |
| pra | 0.25-0.75 | 183 | 0.45 | -0.14 ± 0.60 | -31% |
| pra | 0.75-1.5 | 49 | 0.96 | +0.86 ± 0.96 | 90% |
| pra | 1.5-99 | 16 | 2.07 | +2.36 ± 1.80 | 114% |
| pts | 0.25-0.75 | 251 | 0.45 | +0.18 ± 0.42 | 39% |
| pts | 0.75-1.5 | 127 | 0.97 | +0.07 ± 0.55 | 7% |
| pts | 1.5-99 | 27 | 2.07 | +2.44 ± 0.90 | 118% |
| reb | 0.25-0.75 | 131 | 0.39 | +0.29 ± 0.24 | 74% |
| ALL | 0.25-0.75 | 679 | 0.42 | +0.17 ± 0.23 | 39% |
| ALL | 0.75-1.5 | 195 | 0.96 | +0.32 ± 0.43 | 34% |
| ALL | 1.5-99 | 45 | 2.06 | +2.38 ± 0.83 | 116% |

Share realised ~100% = the move was right and the close is fair; >100% = moves under-react (bet with moves early); <0% = moves are noise/overreaction.