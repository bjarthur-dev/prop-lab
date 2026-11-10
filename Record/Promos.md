---
tags: [record, promos]
---
# Promos

The audit showed promos are where the profit is, so each one gets a row. "Cost" is what the qualifying bets are expected to lose at fair prices; "credit" is what the promo pays; "worth" is credit minus cost, counting bonus credit at about 55-70% of face value until it is turned into cash.

| Date | App | Promo | Staked | Expected cost of the slips | Credit | Worth | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-09 | Betr | Play $20, get $25 Betr Bucks; discounted Cook and Sengun lines | $20 | about -$0.30 (fair.py) | $25 Betr Bucks (in account) | about +$13 to +$17 | slips returned $29.00 on $20 (+$9.00); Bucks unused as of 11-10 |

Earlier promo days (11-06 to 11-08: DraftKings boosts, ESPN bet-and-get, Moonshot bet-and-get) are written up in `Slates/2026-11-07 promos.md` and `Slates/2026-11-08 promos.md`; they were not costed with the new pricer.

Rules: take a promo only when the slips price at or near fair in `engine/fair.py`; never add a weak leg to reach a minimum; write the terms (expiry, play-through) here before using bonus credit.

## Betr Bucks terms (from the app, 2026-11-10)
- Non-redeemable: they cannot be withdrawn or converted directly.
- Entries played with Betr Bucks pay **cash** prizes when they win.
- No expiry date shown on the wallet screen. Not confirmed whether a winning entry pays the full prize or the prize minus the entry; check the first settled one.
- Balance: $25.00 Betr Bucks, $29.00 cash (11-10).
