---
tags: [record, live]
---

# Live results by method (real money)

Written by `engine/live_report.py` each morning. Tool costs come from `Record/expenses.csv`.

**90 settled bets, staked $353.89, profit $+51.92 (ROI +14.7%). Tool costs $60.00. Net after tools $-8.08.** Bankroll now $21.87.

| method | bets | won | staked | profit | ROI |
|---|---:|---:|---:|---:|---:|
| hedge | 1 | 0 | $16.38 | $-16.38 | -100% |
| long shot | 5 | 2 | $18.86 | $+121.34 | +643% |
| mid | 40 | 8 | $146.81 | $-16.95 | -12% |
| safe | 44 | 13 | $171.84 | $-36.09 | -21% |
| no boost (all tiers) | 45 | 9 | $182.18 | $-94.41 | -52% |
| boosted (all tiers) | 45 | 14 | $171.71 | $+146.33 | +85% |

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
| 2026-11-11 | 4 | $+1.75 | $+62.85 |
| 2026-11-12 | 10 | $-10.93 | $+51.92 |

Without the single biggest win (2026-11-01, $+105.67) profit would be $-53.75: one long shot is carrying the record until the sample grows.

## Next upgrade gate

- Profit last 30 days $+51.92 vs tool costs this month $60.00.
- Odds API paid tier (~$30/mo, confirm price): buy only when the price-edge report shows mean CLV > 0 over 50+ legs, 30-day profit excluding the biggest win >= $60, and bankroll >= $150 (cost <= 15%, bankroll stays >= $60).
- Status: **not yet**

## Targets (tools cost $50/month = about $1.67/day)

| window | bets | profit | minus tools | target | status |
|---|---:|---:|---:|---:|---|
| last 7 days | 64 | $-40.75 | $-52.42 | $100 | behind |
| last 14 days | 87 | $+61.92 | $+38.59 | $100 | behind |

## Tax tracker 2026 (not tax advice; confirm with a tax pro)

- Gross winnings (sum of winning bets' profit): **$319.58**; losses: $267.66; net: $+51.92.
- Indiana 2.95% + county tax applies to gross winnings (no loss deduction for casual bettors): about $14.38 at ~4.5% combined.
- Federal: winnings are income; losses count only if you itemize (capped at 90% of winnings from 2026). Suggested set-aside: ~15-20% of gross winnings = $47.94-$63.92.
- DraftKings issues a W-2G only for a single win of $2,000+ at 300-to-1 or longer; smaller wins are still taxable. Download DK's annual win/loss statement in January.
