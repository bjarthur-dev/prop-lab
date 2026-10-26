---
tags: [record, bankroll]
---

# Bankroll (live pilot, Rules §9)

starting_bankroll: 30.00     # USD, set 2026-10-24 by the user
current_bankroll: 30.00
venues: [DraftKings Sportsbook, DraftKings Pick6]
pilot_start: 2026-10-24
stake_straight_usd: 1.00     # app minimum; % rules (0.5%) would be $0.15, below what the apps take
stake_pick6_entry_usd: 1.00
stake_cash_slip_usd: 5.00     # user decision 2026-10-26: one $5 cash slip per day (doubling plan), plus no-sweat tokens on slips
cash_slip_rule: "under $15 bankroll -> $3 slips until back over $20; at $60+ set $30 aside"
max_bets_per_day: 3          # $3/day max = 10% of bankroll
per_game_max_usd: 2.00
per_player_max_usd: 1.00
promo_tokens: 4 x $5 no-sweat (DraftKings; check eligible markets, max refund, expiry in app)
kill_switch: "back to paper if current_bankroll < 20.00, or mean CLV <= 0 after 50 live bets, or a bet placed that wasn't on the card"
user_preference_noted: "user asked for 4 x $5 bets; capped at 3 x $1 because $20/day on a $30 roll risks ruin in 1-2 bad days. Revisit at 50 live bets with CLV data."

Cards show $ stakes from these numbers. Update current_bankroll after each settlement (the morning task does it).
