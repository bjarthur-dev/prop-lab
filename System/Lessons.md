---
tags: [system, lessons]
---

# Lessons from the data (study of 2026-11-02, covers 10-24 → 11-01)

Samples: 3,970 NBA props with sharp prices graded vs box scores; 385 NFL props graded vs play-by-play (players with no touches counted as 0); 1,609 matchup-engine projections; 14 real-money bets.

## 1. Sharp prices are accurate; the edge is in favorites, moves and boosts
- **Calibration:** Pinnacle/FanDuel devig fair is honest. NBA legs priced 45–55% win 50.0%; 55–65% legs win **60.6%** (fair 57.8%, n=497). NFL 55–70% legs win **66%** (fair 59%, n=68). Long shots under 45% underperform (NBA 39.6% vs 42.3%; NFL 34% vs 41%).
- So: **build from sharp favorites (fair >= 55%) and never from sharp underdogs.** The 11-01 winners were all 55–62% legs.

## 2. STEAM: corrected 2026-11-02 17:50 (bug fix) — NOT a proven edge yet
- The first study (55.6% / "DK lagging 61.5%, +16%") had a bug: it priced DK from a line DraftKings had already moved off (e.g. Roschon Johnson U12.5 after DK moved to 9.5). Those bets were not available.
- Re-graded with DK's CURRENT line only: 114 bettable steam legs, 50.0% win vs last fair 51.5%, ROI −7.4%; "DK lagging" 14 legs, 35.7%. No edge so far.
- What still holds: the sharp line itself tends to keep moving the way it moved (sharp-only, same line: the steamed side won ~55.8% vs ~52% fair), but by the time we see it DK has usually moved too.
- Use steam only as a VETO/confirm: drop a card leg whose sharp line moved >= 2 pts against it; do not add new legs from the steam list until Record/Shadow/Steam Report.md shows the bettable version winning over 100+ legs.

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
2. 18:18 pregame snapshot → `steam_scan.py`: drop legs whose sharp line moved >= 2 pts against us (veto only; steam is not yet a source of new legs, see #2).
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
- A pick must win on its own BEFORE the boost: sharp fair >= 55%, or DK beats the sharp price (EV >= 2% unboosted). The boost only makes a winning pick pay more. A bet that is +EV only because of the boost is NOT placed.
- Underdogs / upsets are allowed only with a stated, checkable reason that the market has not priced: DK price better than the sharp fair (unboosted EV >= 2%), the sharp line moving toward the dog (steam), or confirmed news (injury, lineup, rest) with source and time that the price has not caught up to. "Could happen" is not a reason.
- Combos (alternates, multi-sport parlays, SGPx) are built only from legs that qualify on their own; more legs are added only when each one does.

## 11-02 night (−$4): concentration, not the picks
- 3 of tonight's 5 real-money exposures sat in ONE game (Brown U1.5 3PM single, Brown + Giddey inside the SGPx). Brown hit 2 threes and Giddey went over 7.5 ast in the same game, so one game sank both tickets.
- Rule: across ALL tickets of the day, at most 1 exposure per player and 2 legs per game. When a promo requires 2 legs from one game, pick that game so it holds no other ticket's legs; if none qualifies, skip the promo.
- A leg added only to satisfy a promo's structure (Giddey, added at 19:00 from a 17:36 price) needs the same checks as any other leg, at a fresh price.
- Checked: game total vs under win rate (3,114 graded NBA props): no consistent pattern by total bucket. Not a rule.

## 11-02 graded (morning review 11-03)
- The card's SGPx (Anunoby/Brunson/Vassell reb unders) went 3/3 and the Carter Jr. under won (6 pts). The placed slip lost only on the two legs added for the promo structure (Giddey 10 ast, Brown 4 threes): concentration rule confirmed.
- MNF skips were right: sharp-favorite catch unders went 1-4 at DK's overpriced numbers (Loveland 7, Burden 7, Odunze 4, Charbonnet 3; Raymond 2 won), Caleb Williams ran once for 2 yds (the scramble angle failed), Swift 2 catches / 69 rush yds, Bears won 34-17. Horton O1.5 (3) and JSN U7.5 (6) would have won.
- CBB promo games: Purdue ML lost (Gonzaga 78-72), Florida -5.5 covered (77-67), Fla-Mia UNDER 160.5 won (144), UCLA +4.5 won outright. One night of CBB lines = noise; keep tracking.
- Credits: the 18:18 pregame was skipped by the guard (592 left for 28 days), so there was no real close for CLV. Low-credit mode added: when credits < 40/day for the rest of the month, the NBA board carries only rebounds + assists (our under markets), halving its cost.

## Volume (user, 2026-11-03): no cap on the NUMBER of bets
- Every qualifying bet goes on the card, across all sports; there is no daily count limit. Sizing still protects the bankroll: singles ~2% each, boosted parlays ~2-5%, and the day's total at most ~15% of the bankroll (if more qualify, scale every stake down evenly rather than dropping bets).
- College basketball every day it's in season: dispatch odds tag `cbb` (3 credits, every game) and run `python engine/game_scan.py D ncaab` (spreads, totals, moneylines; DK vs Pinnacle at the same number, EV >= 2% sharp and >= 0 consensus). Same scan for nba/nfl/ncaaf games files when present. Sharp underdogs below 45% (big moneyline dogs) stay excluded by rule #1 even when the scan flags them.

## Confidence tiers and sizing (user, 2026-11-03): bet more when the edge is bigger, small bankroll
Stake = a fraction of the CURRENT bankroll, set by the edge, never by feel (quarter-Kelly: stake% ≈ edge ÷ (decimal odds − 1) ÷ 4, then capped by tier).
| tier | what qualifies | stake |
|---|---|---|
| **A: high confidence** | price edge >= 4% vs Pinnacle AND sharp fair >= 58% AND clean story (role stable, no availability doubt, nothing in news against it); or a boosted parlay whose every leg is tier A/B | **4–5%** single; boosted long shot 3% |
| **B: standard** | price edge 2–4% or sharp fair >= 55% at a fair DK price, story checks out | **2%** |
| **C: lean** | qualifies but thin (one sharp book, a story question, near the worst price) | **1%** or paper |
| no bet | fails any rule | 0 |
- Long-shot rule: one boosted long shot a day, built only from tier A/B legs, 2–3% of bankroll. It is the "one bet that wins big" (11-01: $5 → $110) and it is +EV only because every leg already is. Most days it loses; that is priced in.
- Daily total <= ~15% of bankroll. After a losing day stakes shrink automatically (they're % of the new bankroll); after a win they grow. That compounding is how $100 becomes $500 without adding money.
- The card states each bet's tier and the one-line reason it is that tier.

## 11-04 (−$16.81)
- The card's best plays (Reid, Edey, Buzelis singles) were never placed: the games tipped before the user saw the final list. Final list must be placed right at ~18:20.
- The parlay lost on the coin-flip leg added only to reach the boost's +300 minimum (Giannis U11.5, 51%): MIA erased a 15-point deficit and the game went to OT. Harper U5.5 (5) and Sabonis 11+ hit. Rule: a leg added to reach a promo minimum must be >= 55% sharp itself; a 50/50 filler is not allowed (the price-edge exception doesn't apply to filler legs).
- Stakes: Pick6 $10 vs $4 suggested; the day's total was 19% of the bankroll. Stick to card stakes.

## 11-05 TNF: Pick6 paid (JAX 33-10)
- Two Pick6 entries won and paid far above their listed multipliers through a Pick6 winnings boost: 3-pick $27.30 → $46.41, 2-pick $14.98 → $32.26. Pick6 promos (free/gimme lines, 1.3x boost picks, winnings boosts) can be worth more than sportsbook boosts: always price Pick6 when the user reports promos there.
- The script call held: JAX blew out a rookie-QB BAL; Henry 57 rush yds (under), Lane 0 rec yds, Lawrence 242 (the 199.5 promo line was easy). The Henry MORE entry lost, as the lean said.
- Lane LESS 17.5 (the one 58% Pick6 pick) and Henry LESS (the story pick) both hit: the story + sharp combination worked, even with Henry at 50% sharp. Still one night; keep tracking Pick6 promo picks separately.

## Paid Odds API (2026-11-06): 20,000 credits/month, key in ODDS_API_KEY_1
- The snapshot script auto-detects the paid plan (>= 5,000 credits on key 1): no budget guard, NBA board adds points+rebounds+assists combos, NFL board every day it has games, game lines for NBA/CBB/NFL/CFB on board and pregame, open snapshot + scores at 10:37, closes for all games near tip. Expect ~400-600 credits a normal day.
- More snapshots = real closing lines for CLV and more stale-DK chances. Routines no longer need force=1.
- $30/month is logged in Record/expenses.csv; the 30-day review in Live Report.md decides whether it stays.
