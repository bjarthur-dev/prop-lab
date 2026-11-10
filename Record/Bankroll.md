---
tags: [record, bankroll]
---

# Bankroll (live pilot, Rules §9)

starting_bankroll: 30.00     # USD, set 2026-10-24 by the user
current_bankroll: 41.60
balances: {draftkings: 41.60, betr: 0.00, betr_bucks: 25.00}   # 2026-11-10 08:58: user moved the $29 from Betr to DraftKings; Betr Bucks are bonus credit, not counted in current_bankroll
withdrawn_total: 60.00   # 11-06: +$30 Odds API plan; 2026-11-01: AI subscriptions (Claude + Perplexity), logged in Record/expenses.csv
venues: [DraftKings Sportsbook, DraftKings Pick6, Betr Picks]   # Betr added 2026-10-27; Betr is NOT in The Odds API -> card gives 'take on Betr only if line is at or better than X'
pilot_start: 2026-10-24
stake_straight_usd: 2.00     # tier B (2%); tier A 4-5%, tier C 1% (System/Lessons.md "Confidence tiers"); $1 floor if bankroll < $60
stake_pick6_entry_usd: 1.00
stake_cash_slip_usd: 5.00     # one boosted long-shot parlay per day (>= 25% boost only, System/Lessons.md); daily total <= ~10% of bankroll
cash_slip_rule: "under $15 bankroll -> $3 slips until back over $20; at $60+ set $30 aside"
max_bets_per_day: 3          # $3/day max = 10% of bankroll
per_game_max_usd: 2.00
per_player_max_usd: 1.00
promo_tokens: 0   # user 2026-10-27: no no-sweat tokens left. Do not build token slips.
kill_switch: "back to paper if current_bankroll < 20.00, or mean CLV <= 0 after 50 live bets, or a bet placed that wasn't on the card"
user_preference_noted: "user asked for 4 x $5 bets; capped at 3 x $1 because $20/day on a $30 roll risks ruin in 1-2 bad days. Revisit at 50 live bets with CLV data."

Cards show $ stakes from these numbers. Update current_bankroll after each settlement (the morning task does it).

## Goal + plan (user, 2026-10-26)
goal: "+$30 profit as fast as possible: DK $60 (from $30) / combined $74 (DK + Betr $12 assumed new money)"
venue: DraftKings Pick6 only
entry_rule: "one $5 Pick6 entry per day (two on a strong day), STANDARD picks only (no discounted/lowered lines), every pick >= 58-60% by the sharp sportsbook market at Pick6's line; 2-pick (3x) or 3-pick (6x, check app) - whichever has higher EV. Under $15 -> $3 entries. At $60 -> goal hit, set $30 aside."
method: "engine/pick6_scan.py (Pick6 line vs sharp books) + engine/opportunity.py (minutes/usage/who's out/script) - see System/Pick6 Plan.md"

## Funding rule for tools (user, 2026-11-01)
Every subscription or upgrade (Odds API tier, data, anything) is paid out of the DraftKings bankroll. It has to pay for itself.
Gate before buying anything:
1. **Evidence first:** the method the tool would scale must show positive results on paper or live (price edge: mean CLV > 0 over 50+ legs).
2. **Pays 2x:** expected monthly profit it adds >= 2x its monthly cost, using real stake sizes (not hopes).
3. **Affordable:** cost <= 15% of current bankroll, and the bankroll stays >= $60 after paying.
4. **Review after 30 days:** if the added profit didn't cover the cost, cancel.
Log each purchase as a row in bets.csv (type=expense) so the record shows net profit after tools.
