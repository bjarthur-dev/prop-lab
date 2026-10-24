---
tags: [record, bankroll]
---

# Bankroll (live pilot, Rules §9)

starting_bankroll: UNSET   # the user sets this (the money set aside for betting only)
current_bankroll: UNSET
pilot_start: 2026-10-24
stake_straight_pct: 0.5
stake_slip_entry_pct: 0.25
daily_cap_pct: 2.0
kill_switch: "drawdown >= 15% of starting_bankroll, or mean CLV <= 0 after 50 live bets, or an unlogged bet"

Until starting_bankroll is set, cards show stakes in % only.
