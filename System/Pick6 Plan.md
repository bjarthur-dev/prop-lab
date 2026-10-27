---
tags: [system, plan, pick6]
updated: 2026-10-26
---

# Pick6 Plan — $30 → $60

The user has **no DraftKings Sportsbook access**, so everything goes through **DraftKings Pick6**. The sportsbook no-sweat tokens and DK-price edges no longer apply.

## Where the edge is on Pick6
Pick6 posts one line per player (standard pick, x1). Sportsbooks move their lines all day; Pick6 lags. When Pick6's line is **a half point or more off the sharp books' line**, one side becomes a 58–65% pick at a flat payout. That is the only repeatable edge on a pick'em app.
- **Standard picks only.** Lowered ("discounted") lines pay so much less that they almost never beat the math. Example, Oct 26: Miller 20+ / JJJ 15+ paid **1.47x**, so it needed **68%** to break even; our estimate was ~48%.
- **Break-evens:** a 2-pick at 3x needs each pick at **57.7%**; a 3-pick at 6x needs **55%** each. Always use the payout the app shows: break-even = (1/payout)^(1/picks).
- **Some picks are one-way** (only More offered). The scan respects that.

## Daily routine (automated)
1. **14:52 afternoon card:** odds snapshot with the `pick6` tag (Pick6 lines + 9 sportsbooks for every game today, same credits as before). Then `python engine/pick6_scan.py D` lists picks at ≥ 58%.
2. **Opportunity filter:** run `engine/opportunity.py` on each candidate. Keep a pick only if minutes, usage, who's out, game script and back-to-backs support the side.
3. **Entry:** the best 2-pick, or a 3-pick if three picks are all ≥ 58% and the EV is higher. Use different games. $5.
4. **18:17 late update:** re-pulls `pick6`, re-checks lines (Pick6 moves too) and lineups, and confirms or swaps picks.
5. **08:17 settlement:** grades the entry and every scanned pick, so we learn which kinds of line gaps actually hit.

## Honest math
At +20–35% EV per $5 entry, the average gain is about **$1–2 a day**. Reaching $60 inside a week still needs a hot run, because a 2-pick wins only about 40% of the time. Bigger entries (4–5 picks) win more when they hit but miss far more often. We stay at 2–3 picks until the record shows the line gaps convert.

## Rules
- Never a discounted pick. Never more than one pick from the same game, unless correlated on purpose and noted.
- Bankroll under $15: $3 entries. At $60: goal reached, set $30 aside.
- Check the Pick6 promos tab daily (deposit matches, boosted picks, free entries). A real boost on a pick we already like is the best play available.
