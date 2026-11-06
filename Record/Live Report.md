---
tags: [record, live]
---

# Live results by method (real money)

Written by `engine/live_report.py` each morning. Tool costs come from `Record/expenses.csv`.

**23 settled bets, staked $109.33, profit $+117.67 (ROI +107.6%). Tool costs $60.00. Net after tools $+57.67.** Bankroll now $123.67.

| method | bets | won | staked | profit | ROI |
|---|---:|---:|---:|---:|---:|
| hedge | 1 | 0 | $16.38 | $-16.38 | -100% |
| long shot | 2 | 1 | $7.14 | $+103.67 | +1452% |
| mid | 12 | 2 | $64.81 | $-2.02 | -3% |
| safe | 8 | 5 | $21.00 | $+32.40 | +154% |
| no boost (all tiers) | 7 | 0 | $48.38 | $-43.38 | -90% |
| boosted (all tiers) | 16 | 8 | $60.95 | $+161.05 | +264% |

| date | bets | profit | running |
|---|---:|---:|---:|
| 2026-10-26 | 1 | $+0.00 | $+0.00 |
| 2026-10-27 | 1 | $-5.00 | $-5.00 |
| 2026-10-28 | 1 | $-5.00 | $-10.00 |
| 2026-10-31 | 6 | $+0.14 | $-9.86 |
| 2026-11-01 | 5 | $+94.67 | $+84.81 |
| 2026-11-02 | 2 | $-4.00 | $+80.81 |
| 2026-11-04 | 2 | $-16.81 | $+64.00 |
| 2026-11-05 | 5 | $+53.67 | $+117.67 |

Without the single biggest win (2026-11-01, $+105.67) profit would be $+12.00: one long shot is carrying the record until the sample grows.

## Next upgrade gate

- Profit last 30 days $+117.67 vs tool costs this month $60.00.
- Odds API paid tier (~$30/mo, confirm price): buy only when the price-edge report shows mean CLV > 0 over 50+ legs, 30-day profit excluding the biggest win >= $60, and bankroll >= $150 (cost <= 15%, bankroll stays >= $60).
- Status: **not yet**

## Targets (tools cost $50/month = about $1.67/day)

| window | bets | profit | minus tools | target | status |
|---|---:|---:|---:|---:|---|
| last 7 days | 20 | $+127.67 | $+116.00 | $100 | on track |
| last 14 days | 23 | $+117.67 | $+94.34 | $100 | behind |
