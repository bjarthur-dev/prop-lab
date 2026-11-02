---
tags: [record, live]
---

# Live results by method (real money)

Written by `engine/live_report.py` each morning. Tool costs come from `Record/expenses.csv`.

**14 settled bets, staked $63.52, profit $+84.81 (ROI +133.5%). Tool costs $30.00. Net after tools $+54.81.** Bankroll now $90.81.

| method | bets | won | staked | profit | ROI |
|---|---:|---:|---:|---:|---:|
| hedge | 1 | 0 | $16.38 | $-16.38 | -100% |
| long shot | 1 | 1 | $5.14 | $+105.67 | +2056% |
| mid | 6 | 1 | $28.00 | $-11.62 | -42% |
| safe | 6 | 4 | $14.00 | $+7.14 | +51% |
| no boost (all tiers) | 3 | 0 | $26.38 | $-21.38 | -81% |
| boosted (all tiers) | 11 | 6 | $37.14 | $+106.19 | +286% |

| date | bets | profit | running |
|---|---:|---:|---:|
| 2026-10-26 | 1 | $+0.00 | $+0.00 |
| 2026-10-27 | 1 | $-5.00 | $-5.00 |
| 2026-10-28 | 1 | $-5.00 | $-10.00 |
| 2026-10-31 | 6 | $+0.14 | $-9.86 |
| 2026-11-01 | 5 | $+94.67 | $+84.81 |

Without the single biggest win (2026-11-01, $+105.67) profit would be $-20.86: one long shot is carrying the record until the sample grows.

## Next upgrade gate

- Profit last 30 days $+84.81 vs tool costs this month $30.00.
- Odds API paid tier (~$30/mo, confirm price): buy only when the price-edge report shows mean CLV > 0 over 50+ legs, 30-day profit excluding the biggest win >= $60, and bankroll >= $150 (cost <= 15%, bankroll stays >= $60).
- Status: **not yet**
