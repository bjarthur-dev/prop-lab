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