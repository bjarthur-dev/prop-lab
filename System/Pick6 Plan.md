---
tags: [system, plan, pick6]
updated: 2026-10-26
---

# Pick6 Plan — $30 → $60

> **11-09 pricing rule (overrides older steps below):** price every slip with `python engine/fair.py --payout X sport:player:market:side:line ...`; run `python engine/consensus_scan.py` for price edges (6%+ only). No Poisson scripts. Evidence and rules: [[Lessons]] "11-09 System audit", `Record/Audit.md`, `Record/Market Backtest.md`.

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

## Pick6 multiplier tiers = DraftKings sportsbook price of that side (found 2026-11-23)
User observation + check vs 11-21 NHL SOG board (56 picks) and 11-23 MNF board (4 picks); every point fits:

| DK sportsbook price of the side | Pick6 multiplier on that side |
|---|---|
| -124 or better (both sides <= ~-125) | 1x |
| ~-125/-130 to -145 | 0.9x |
| ~-145/-150 to -190 | 0.8x |
| -195 or worse | 0.7x |

Boundary at -125 is fuzzy (snapshot timing). Breakeven per pick: 2-pick 3x -> 57.7%; 3-pick 6x -> 55.0%; 4-pick 10x -> 56.2%.

Value rules:
- 1x is the value tier. Target: DK at -115 to -124 on the side while sharps (Pinnacle/FanDuel devig) put it >= 56-58% (about -130 to -140). DK caps it at 1x, so the extra probability is free.
- A reduced pick is worth taking over a typical 1x pick (~53-55%) only if multiplier x sharp fair > that: 0.9x needs >= ~60-61% fair (sharps ~-155 while DK still <= -145); 0.8x needs >= ~68-69% (sharps ~-220 while DK <= -190); 0.7x needs >= ~77-79%. At DK's own price the reduced tiers are always worse than a boundary 1x pick (0.9 x 58% = 52%; 0.8 x 64% = 51%).
- Scanner: rank candidates by multiplier x sharp fair; build entries from the top, one sport per entry, one promo/discount pick per entry.
