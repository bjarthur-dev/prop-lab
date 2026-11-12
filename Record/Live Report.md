---
tags: [record, live]
---

# Live results by method (real money)

Written by `engine/live_report.py` each morning. Tool costs come from `Record/expenses.csv`.

**80 settled bets, staked $301.09, profit $+62.85 (ROI +20.9%). Tool costs $60.00. Net after tools $+2.85.** Bankroll now $31.80.

| method | bets | won | staked | profit | ROI |
|---|---:|---:|---:|---:|---:|
| hedge | 1 | 0 | $16.38 | $-16.38 | -100% |
| long shot | 5 | 2 | $18.86 | $+121.34 | +643% |
| mid | 36 | 7 | $130.81 | $-36.82 | -28% |
| safe | 38 | 12 | $135.04 | $-5.29 | -4% |
| no boost (all tiers) | 39 | 8 | $145.38 | $-63.61 | -44% |
| boosted (all tiers) | 41 | 13 | $155.71 | $+126.46 | +81% |

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

Without the single biggest win (2026-11-01, $+105.67) profit would be $-42.82: one long shot is carrying the record until the sample grows.

## Next upgrade gate

- Profit last 30 days $+62.85 vs tool costs this month $60.00.
- Odds API paid tier (~$30/mo, confirm price): buy only when the price-edge report shows mean CLV > 0 over 50+ legs, 30-day profit excluding the biggest win >= $60, and bankroll >= $150 (cost <= 15%, bankroll stays >= $60).
- Status: **not yet**

## Targets (tools cost $50/month = about $1.67/day)

| window | bets | profit | minus tools | target | status |
|---|---:|---:|---:|---:|---|
| last 7 days | 57 | $-54.82 | $-66.49 | $100 | behind |
| last 14 days | 77 | $+72.85 | $+49.52 | $100 | behind |

## Tax tracker 2026 (not tax advice; confirm with a tax pro)

- Gross winnings (sum of winning bets' profit): **$284.71**; losses: $221.86; net: $+62.85.
- Indiana 2.95% + county tax applies to gross winnings (no loss deduction for casual bettors): about $12.81 at ~4.5% combined.
- Federal: winnings are income; losses count only if you itemize (capped at 90% of winnings from 2026). Suggested set-aside: ~15-20% of gross winnings = $42.71-$56.94.
- DraftKings issues a W-2G only for a single win of $2,000+ at 300-to-1 or longer; smaller wins are still taxable. Download DK's annual win/loss statement in January.
