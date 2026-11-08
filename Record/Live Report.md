---
tags: [record, live]
---

# Live results by method (real money)

Written by `engine/live_report.py` each morning. Tool costs come from `Record/expenses.csv`.

**38 settled bets, staked $193.00, profit $+83.49 (ROI +43.3%). Tool costs $60.00. Net after tools $+23.49.** Bankroll now $59.49.

| method | bets | won | staked | profit | ROI |
|---|---:|---:|---:|---:|---:|
| hedge | 1 | 0 | $16.38 | $-16.38 | -100% |
| long shot | 4 | 2 | $15.81 | $+124.39 | +787% |
| mid | 18 | 2 | $99.81 | $-37.02 | -37% |
| safe | 15 | 7 | $61.00 | $+12.50 | +20% |
| no boost (all tiers) | 11 | 1 | $68.38 | $-52.58 | -77% |
| boosted (all tiers) | 27 | 10 | $124.62 | $+136.07 | +109% |

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

Without the single biggest win (2026-11-01, $+105.67) profit would be $-22.18: one long shot is carrying the record until the sample grows.

## Next upgrade gate

- Profit last 30 days $+83.49 vs tool costs this month $60.00.
- Odds API paid tier (~$30/mo, confirm price): buy only when the price-edge report shows mean CLV > 0 over 50+ legs, 30-day profit excluding the biggest win >= $60, and bankroll >= $150 (cost <= 15%, bankroll stays >= $60).
- Status: **not yet**

## Targets (tools cost $50/month = about $1.67/day)

| window | bets | profit | minus tools | target | status |
|---|---:|---:|---:|---:|---|
| last 7 days | 24 | $-1.32 | $-12.99 | $100 | behind |
| last 14 days | 38 | $+83.49 | $+60.16 | $100 | behind |

## Tax tracker 2026 (not tax advice; confirm with a tax pro)

- Gross winnings (sum of winning bets' profit): **$232.26**; losses: $148.77; net: $+83.49.
- Indiana 2.95% + county tax applies to gross winnings (no loss deduction for casual bettors): about $10.45 at ~4.5% combined.
- Federal: winnings are income; losses count only if you itemize (capped at 90% of winnings from 2026). Suggested set-aside: ~15-20% of gross winnings = $34.84-$46.45.
- DraftKings issues a W-2G only for a single win of $2,000+ at 300-to-1 or longer; smaller wins are still taxable. Download DK's annual win/loss statement in January.
