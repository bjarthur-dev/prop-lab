---
tags: [system, lessons]
---

# Lessons from the data (study of 2026-11-02, covers 10-24 → 11-01)

Samples: 3,970 NBA props with sharp prices graded vs box scores; 385 NFL props graded vs play-by-play (players with no touches counted as 0); 1,609 matchup-engine projections; 14 real-money bets.

## 1. Sharp prices are accurate; the edge is in favorites, moves and boosts
- **Calibration:** Pinnacle/FanDuel devig fair is honest. NBA legs priced 45–55% win 50.0%; 55–65% legs win **60.6%** (fair 57.8%, n=497). NFL 55–70% legs win **66%** (fair 59%, n=68). Long shots under 45% underperform (NBA 39.6% vs 42.3%; NFL 34% vs 41%).
- So: **build from sharp favorites (fair >= 55%) and never from sharp underdogs.** The 11-01 winners were all 55–62% legs.

## 2. STEAM: follow the sharp line move (strongest signal found)
- When the sharp line moves between the morning/afternoon snapshot and the 18:18 pregame snapshot, the side it moved toward won **55.6%** vs its last fair of 52.4% (342 NBA props with a >= 2-pt move; positive on 6 of 8 days).
- **If DraftKings has not moved yet (DK price still >= the new fair): 96 legs, 61.5% win, +16% ROI as singles.**
- Unders that steamed: 57% (n=223). Example: Garland u7.5 ast moved 54% → 57% before the 11-01 win.
- Tool: `python engine/steam_scan.py [date] [nba|nfl]` after the pregame snapshot. Steam legs are the first choice for safe singles and parlay legs.

## 3. Unders, mostly
- NBA: assists unders 53.4% vs fair 51.1% (n=388); unders on 6.5–12.5 lines 55.2% vs fair 50.6% (n=373).
- NFL: receptions unders 53.9% vs fair 51.8% (n=141), receiving-yards unders 53.2% (n=156). Rushing yards: the over did better (53.4%, n=88).
- The public bets overs; books shade overs. Default lean is the under unless the role is growing (injury to a teammate) or the line steamed up.

## 4. The matchup engine adds nothing over the market (yet)
- Log loss: market 0.682; any blend with the engine is worse (0.684 at 20%, 0.714 alone). Where the engine was 20+ pts above the market the over hit **32%** (n=53).
- Use it for the *story* (role, minutes, who's out, shot diet), never to pick a side against the sharp price. Stop citing "context %" as a reason.

## 5. Parlays only with a boost
- A 3-leg parlay of 58% legs at DK prices is about −10% EV. With a 30% profit boost it's about +11%; with 50%, about +26%. Real money agrees: boosted bets +$106 over 11, unboosted −$21 over 3.
- Rule: no parlay without a >= 25% boost. Legs must each be sharp >= 55% (prefer steam legs). SGPs: the book prices correlation, so pick legs whose correlation helps (e.g. two same-team assist unders in a slow game) and avoid legs that fight (two overs competing for the same targets).

## 6. Live management
- Never cash out a boosted ticket (it removes the boost). Cash out only if the offer beats (live chance × full payout).
- Hedge the last weak leg with a live bet when a loss would hurt; the cost is roughly the book's margin, not 30–50% like a cash-out.

## 7. Process errors to stop repeating
- Check the player's team and the last 5–7 game logs before writing a leg (Diggs is on WAS; McKee went over in both starts).
- Re-check role changes when a starter is out: compare games without him (WAS without McLaurin, PHI without DeVonta Smith) before taking a catches under.
- NFL zero-catch games must count as 0 in grading (fixed in the study; the earlier NFL shadow grading dropped them and inflated overs).
- One huge long shot carries the live record (without it −$21). Judge methods by leg win rate and CLV, not by one ticket.

## Daily recipe
1. Afternoon card: price-edge legs (DK beats sharp) + sharp favorites >= 55% that fit the story; lean under.
2. 18:18 pregame snapshot → `steam_scan.py`: promote legs that steamed >= 2 pts with DK lagging; drop legs that steamed against us.
3. Safe slips from the top steam/price-edge legs; one boosted parlay (>= 25% boost) from 3–5 favorites.
4. Log everything; the morning report grades legs, steam, CLV and the live tiers.

## Card standard (user, 2026-11-02): most PROFIT, every pick fully explained
- Rank candidates by expected profit per $1 at the DK price (sharp fair × payout − 1), not by win %. A 45% leg at +150 can beat a 65% leg at −250; a parlay is ranked by its EV after the day's boost.
- Every pick on the card states: (1) the probability and where it comes from (sharp devig, steam move), (2) the price edge or boost that makes it +EV, (3) the role/minutes/matchup story with numbers, (4) **why it beats the next-best alternative** (name that alternative and its EV), (5) what would kill it (minutes cap, blowout, a teammate returning).
- Every parlay states why these legs together: each leg's fair %, the combined win %, payout with and without the boost, EV, and whether the correlation helps or hurts.
- "Near misses": list up to 5 legs considered and skipped with the reason (e.g. Boozer o8.5 reb +104 on 10-31: sharp had the over at 44%, so +104 was −EV even though it hit). The morning settlement grades near misses too, so skipped-but-hit legs are judged by price, not by one result.

## Running without the laptop (2026-11-02)
- Everything that decides picks runs in the cloud: odds (GitHub Actions), NBA game logs (API-NBA in results.yml + morning web gap fill), NFL data (nflverse in results.yml), scans, cards, settlement, reports.
- The laptop only refreshes the stats.nba.com matchup context (cloud servers are blocked by that site). Per lesson #4 the context never moves a pick, so a stale context changes the WHY text only. Refresh it when the laptop is on; the health check flags it after 14 days.

## Promos (2026-11-02)
- If Slates/"D precheck.md" exists, read it first: its hypotheses are tested against prices (never bet without a qualifying price).
- If Slates/"D promos.md" exists, the afternoon card and late update build the best play for EACH listed promo (or say why to skip it), ranked by EV at the sharp fair including the boost.
- A profit boost multiplies profit, so it is worth most on longer prices: a 30% boost turns a sharp-fair +190 into about +12-18% EV, a -110 into about +9-11%. Pick by EV, mention win %.
- NBA 1st-quarter props: dispatch odds tag nbaq1 (player_points_q1/rebounds_q1/assists_q1) after ~16:00 ET. College basketball game lines: tag cbb (3 credits for every game).

## No forcing (user, 2026-11-02)
- We place a bet only when we believe it wins money: sharp fair >= 55% for props/legs (or a clear price edge / steam), and positive EV after any boost. A promo that has no such play is skipped; skipping is normal.
- Everything else is TRACKED, not bet: every scanned prop (edge scans, steam lists), every game line we snapshot (college basketball, NFL, college football via `cbb`/`lines`/board/pregame tags) and final scores (`scores`, run in the free-tier 10:37 slot) are graded each morning (Record/Shadow/*Report.md). New methods earn real money only after their report shows them winning.
- Promo picks list the "would place" play and a plain "skip" when nothing qualifies. A long shot whose only edge is the boost (e.g. a 33% moneyline) is listed as optional, not as a must-place.

## The boost is never the reason (user, 2026-11-02)
- A pick must win on its own BEFORE the boost: sharp fair >= 55%, or DK beats the sharp price (EV >= 2% unboosted), or the sharp line steamed toward it with DK lagging. The boost only makes a winning pick pay more. A bet that is +EV only because of the boost is NOT placed.
- Underdogs / upsets are allowed only with a stated, checkable reason that the market has not priced: DK price better than the sharp fair (unboosted EV >= 2%), the sharp line moving toward the dog (steam), or confirmed news (injury, lineup, rest) with source and time that the price has not caught up to. "Could happen" is not a reason.
- Combos (alternates, multi-sport parlays, SGPx) are built only from legs that qualify on their own; more legs are added only when each one does.
