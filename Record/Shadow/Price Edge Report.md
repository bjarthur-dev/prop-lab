---
tags: [record, shadow, price-edge]
---

# Price-edge method: every qualifying leg, graded

Written by `engine/edge_grade.py` (morning settlement). Qualifying = DK beats the sharp fair by >= 2% EV and the all-book consensus. Profit is per 1-unit single at the DK price. CLV uses the last sharp snapshot before tip (a true close only when one was taken).

**99 legs over 17 days: 52-47, ROI -3.9% per unit (expected at scan +6.3%).** CLV: 57 legs with a later snapshot, mean +3.2%, positive on 84%.

One standard error on ROI at this sample is about ±10%: CLV is the faster signal.

| market | n | record | ROI | mean CLV |
|---|---:|---:|---:|---:|
| alt_ast | 15 | 6-9 | -30.0% | n/a |
| alt_pts | 22 | 12-10 | -24.3% | n/a |
| alt_reb | 5 | 2-3 | -50.2% | n/a |
| assists | 14 | 8-6 | +15.2% | +2.5% |
| points | 15 | 9-6 | +19.5% | +3.3% |
| rebounds | 15 | 8-7 | +11.3% | +2.9% |
| threes | 13 | 7-6 | +13.3% | +4.3% |

| date | n | record | ROI | mean CLV |
|---|---:|---:|---:|---:|
| 2026-10-24 | 2 | 0-2 | -100.0% | +3.8% |
| 2026-10-25 | 1 | 1-0 | +110.0% | +2.0% |
| 2026-10-26 | 27 | 15-12 | -27.1% | +5.4% |
| 2026-10-27 | 20 | 7-13 | -29.7% | +3.3% |
| 2026-10-28 | 3 | 1-2 | -34.3% | +3.3% |
| 2026-10-29 | 3 | 3-0 | +112.3% | +2.6% |
| 2026-10-30 | 1 | 1-0 | +123.0% | +2.5% |
| 2026-10-31 | 1 | 0-1 | -100.0% | +2.3% |
| 2026-11-01 | 1 | 0-1 | -100.0% | -5.7% |
| 2026-11-02 | 10 | 6-4 | +25.6% | +3.6% |
| 2026-11-04 | 3 | 2-1 | +37.0% | +2.9% |
| 2026-11-06 | 3 | 1-2 | -32.0% | -0.8% |
| 2026-11-08 | 1 | 1-0 | +87.7% | +3.5% |
| 2026-11-09 | 5 | 4-1 | +53.3% | +3.3% |
| 2026-11-10 | 10 | 6-4 | +21.8% | +6.2% |
| 2026-11-11 | 6 | 3-3 | +0.8% | +1.1% |
| 2026-11-12 | 2 | 1-1 | +11.0% | +2.6% |
