---
tags: [record, live]
---

# Live results by method (real money)

Written by `engine/live_report.py` each morning. Tool costs come from `Record/expenses.csv`.

**16 settled bets, staked $67.52, profit $+80.81 (ROI +119.7%). Tool costs $30.00. Net after tools $+50.81.** Bankroll now $86.81.

| method | bets | won | staked | profit | ROI |
|---|---:|---:|---:|---:|---:|
| hedge | 1 | 0 | $16.38 | $-16.38 | -100% |
| long shot | 2 | 1 | $7.14 | $+103.67 | +1452% |
| mid | 6 | 1 | $28.00 | $-11.62 | -42% |
| safe | 7 | 4 | $16.00 | $+5.14 | +32% |
| no boost (all tiers) | 4 | 0 | $28.38 | $-23.38 | -82% |
| boosted (all tiers) | 12 | 6 | $39.14 | $+104.19 | +266% |

| date | bets | profit | running |
|---|---:|---:|---:|
| 2026-10-26 | 1 | $+0.00 | $+0.00 |
| 2026-10-27 | 1 | $-5.00 | $-5.00 |
| 2026-10-28 | 1 | $-5.00 | $-10.00 |
| 2026-10-31 | 6 | $+0.14 | $-9.86 |
| 2026-11-01 | 5 | $+94.67 | $+84.81 |
| 2026-11-02 | 2 | $-4.00 | $+80.81 |

Without the single biggest win (2026-11-01, $+105.67) profit would be $-24.86: one long shot is carrying the record until the sample grows.

## Next upgrade gate

- Profit last 30 days $+80.81 vs tool costs this month $30.00.
- Odds API paid tier (~$30/mo, confirm price): buy only when the price-edge report shows mean CLV > 0 over 50+ legs, 30-day profit excluding the biggest win >= $60, and bankroll >= $150 (cost <= 15%, bankroll stays >= $60).
- Status: **not yet**
