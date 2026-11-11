---
tags: [record, live]
---

# Live results by method (real money)

Written by `engine/live_report.py` each morning. Tool costs come from `Record/expenses.csv`.

**76 settled bets, staked $292.04, profit $+61.10 (ROI +20.9%). Tool costs $60.00. Net after tools $+1.10.** Bankroll now $51.65.

| method | bets | won | staked | profit | ROI |
|---|---:|---:|---:|---:|---:|
| hedge | 1 | 0 | $16.38 | $-16.38 | -100% |
| long shot | 4 | 2 | $15.81 | $+124.39 | +787% |
| mid | 34 | 6 | $124.81 | $-41.62 | -33% |
| safe | 37 | 12 | $135.04 | $-5.29 | -4% |
| no boost (all tiers) | 38 | 8 | $145.38 | $-63.61 | -44% |
| boosted (all tiers) | 38 | 12 | $146.66 | $+124.71 | +85% |

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
| 2026-11-06 | 3 | $-25.00 | $+92.67 |
| 2026-11-07 | 12 | $-9.18 | $+83.49 |
| 2026-11-08 | 7 | $-29.00 | $+54.49 |
| 2026-11-09 | 27 | $-3.44 | $+51.05 |
| 2026-11-10 | 4 | $+10.05 | $+61.10 |

Without the single biggest win (2026-11-01, $+105.67) profit would be $-44.57: one long shot is carrying the record until the sample grows.

## Next upgrade gate

- Profit last 30 days $+61.10 vs tool costs this month $60.00.
- Odds API paid tier (~$30/mo, confirm price): buy only when the price-edge report shows mean CLV > 0 over 50+ legs, 30-day profit excluding the biggest win >= $60, and bankroll >= $150 (cost <= 15%, bankroll stays >= $60).
- Status: **not yet**

## Targets (tools cost $50/month = about $1.67/day)

| window | bets | profit | minus tools | target | status |
|---|---:|---:|---:|---:|---|
| last 7 days | 58 | $-2.90 | $-14.57 | $100 | behind |
| last 14 days | 73 | $+71.10 | $+47.77 | $100 | behind |

## Tax tracker 2026 (not tax advice; confirm with a tax pro)

- Gross winnings (sum of winning bets' profit): **$276.91**; losses: $215.81; net: $+61.10.
- Indiana 2.95% + county tax applies to gross winnings (no loss deduction for casual bettors): about $12.46 at ~4.5% combined.
- Federal: winnings are income; losses count only if you itemize (capped at 90% of winnings from 2026). Suggested set-aside: ~15-20% of gross winnings = $41.54-$55.38.
- DraftKings issues a W-2G only for a single win of $2,000+ at 300-to-1 or longer; smaller wins are still taxable. Download DK's annual win/loss statement in January.
