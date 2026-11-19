# Line Movement

Opening = first saved snapshot, closing = last saved snapshot before start (no-vig consensus, Pinnacle 2x, FanDuel 1.5x).

## Game moneylines (ncaab 557, ncaaf 66, nfl 5)
479 games with 2+ snapshots. Brier (lower = more accurate): open 0.1477, close 0.1463 -> close more accurate.

| moved toward a side by | n | open said | close said | that side won | won - open | noise ± |
|---|---|---|---|---|---|---|
| 1-2 pts | 93 | 50.3% | 51.8% | 55.9% | +5.6 | 4.1 |
| 2-4 pts | 81 | 51.4% | 54.3% | 63.0% | +11.6 | 4.9 |
| 4-8 pts | 39 | 51.6% | 57.1% | 53.8% | +2.2 | 7.4 |
| 8-100 pts | 17 | 55.5% | 66.1% | 64.7% | +9.2 | 11.4 |

## NBA player props (over side, same line at open and close)
169 props with 2+ snapshots. Brier (lower = more accurate): open 0.2464, close 0.2501 -> open more accurate.

| moved toward a side by | n | open said | close said | that side won | won - open | noise ± |
|---|---|---|---|---|---|---|
| 1-2 pts | 43 | 50.7% | 52.1% | 53.5% | +2.8 | 7.6 |
| 2-4 pts | 41 | 50.1% | 52.9% | 46.3% | -3.8 | 7.8 |
| 4-8 pts | 19 | 47.8% | 52.9% | 42.1% | -5.7 | 11.4 |
| 8-100 pts | 6 | 46.3% | 56.2% | 16.7% | -29.7 | 20.3 |

Read: if 'that side won' beats 'open said' by more than ~2x noise, line moves carry information -> bet early with the move / avoid betting against it. If close is more accurate than open, our prices should always come from the latest snapshot.
## NBA props by implied mean (line changes included)
8237 player-stat-days with an open and a close snapshot (median gap 5.1 h).
Average miss: open mean 3.04, close mean 3.03 (close more accurate).

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

### Forward test (from Nov 15, 1764 so far)
| stat | mean moved by | n | avg move | result vs open, in move direction | share of move realised |
|---|---|---|---|---|---|
| ast | 0.25-0.75 | 43 | 0.38 | +1.05 ± 0.32 | 276% |
| pra | 0.25-0.75 | 87 | 0.45 | -0.20 ± 0.91 | -43% |
| pra | 0.75-1.5 | 22 | 0.97 | +1.18 ± 1.45 | 122% |
| pts | 0.25-0.75 | 105 | 0.46 | +0.55 ± 0.66 | 119% |
| pts | 0.75-1.5 | 56 | 0.96 | -0.86 ± 0.80 | -89% |
| reb | 0.25-0.75 | 67 | 0.39 | +0.61 ± 0.33 | 156% |
| ALL | 0.25-0.75 | 310 | 0.43 | +0.41 ± 0.35 | 95% |
| ALL | 0.75-1.5 | 87 | 0.96 | -0.23 ± 0.64 | -24% |
| ALL | 1.5-99 | 19 | 2.11 | +1.03 ± 1.12 | 49% |

Share realised ~100% = the move was right and the close is fair; >100% = moves under-react (bet with moves early); <0% = moves are noise/overreaction.