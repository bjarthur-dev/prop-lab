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

## Profit targets and sizing (user, 2026-11-06)
- Costs: $50/month (Claude $20 + Odds API $30). Targets: at least $100 profit every 2 weeks after costs; aim for $100/week (~$20/day). Tracked in Record/Live Report.md "Targets".
- Honest math at a ~$125 bankroll: expected profit is mostly from promos (boosts on qualifying legs, Pick6 gimmes/1.3x/winnings boosts), roughly $5-10/day on average with big swings. $100/2 weeks is realistic; $100/week needs either a hit long shot or a bigger bankroll. Stakes grow automatically as the bankroll grows (they are % of the current bankroll).
- Sizing (half-Kelly, capped by the promo max and tiers): stake% ≈ 0.5 × EV ÷ (decimal payout − 1).
  - 50% boost on 3-4 legs of 58-60% (EV ~+30%, ~+450 boosted): ~3.5% → $4-5 at $125; reaches the $10 max at ~$280.
  - 30% boost, same legs (EV ~+15%): ~2% → $2-3.
  - Pick6 entries with a gimme/free pick or 1.3x boost on qualifying picks: 3-5%.
  - Tier A single 4-5%, tier B 2%, tier C 1%. Daily total <= ~20% of bankroll on promo-heavy days, 15% otherwise.
- Go big only through the boosted long shots built from qualifying legs (the 11-01 +2056 type), never by raising stakes on coin flips or chasing.

## Pick6 math (researched 11-06)
- How it pays: Pick6 is peer-to-peer. You get a **Base Payout = stake x base multiplier x every pick multiplier** (0.7x, 0.8x, 0.9x, 1.3x...), plus **Extra Winnings** from the contest pool, split among winners at the same pick level by Standings Points. Pick multipliers also change Standings Points. Rules: at least 2 teams per set; 1 stat per player; an exact-line result or a DNP voids that pick and drops the entry to the next-lower pick level; all but one pick void = refund.
- Base multipliers (receipts + the app's 11-06 screens): 2 picks 3x, 3 picks 6x, 4 picks 10x, 6 picks 25x (5: read the app). The 6-pick break-even at 1.0x is 58.5% per pick. "Ride the upside" = DK's name for Extra Winnings (the app's example: a 10x base plus 8x extra). Treat Extra Winnings as a small bonus, never the reason.
- 11-06 check: George LESS 6.5 ast showed **0.8x** and Murray-Boyles LESS 2.5 ast showed **0.9x**, so a 2-pick paid 2.16x. That needs 46% to hit both; sharp gave 35% (EV -24%). SKIPPED. Pick6 discounts the picks our sharp favorites point to, so check the multiplier before adding any pick.
- **Break-even per pick at 1.0x:** 2-pick 57.7%, 3-pick 55.0%, 4-pick 56.2%. A pick with multiplier m needs break-even / m: at the 4-pick level, a 0.8x pick needs **70%** and a 0.7x pick needs **80%**, while a 1.3x pick needs only **43%**.
- **Stacking 0.8x picks is not an exploit.** Four 0.8x picks pay 10 x 0.41 = 4.1x, which needs a 24% all-hit rate, so each pick has to be about 70%. DK puts 0.8x on the picks it knows are popular and likely. Only use one if the sharp fair is >= 70% (gimme or promo lines).
- **Where the value is:** (1) 1.0x picks that are sharp favorites (>= 57-59%), since Pick6 charges no per-pick vig: three 59% picks at 6x = +23% EV before Extra Winnings; (2) 1.3x picks with a sharp fair of 50%+; (3) Pick6 lines that are stale vs the sharp line (same player, better number); (4) winnings boosts and free picks. Extra Winnings are a bonus on top; contrarian winners get a bigger share.
- The cloud odds feed has had 0 Pick6 rows since 11-06. The user screenshots the Pick6 board, and Claude prices each pick vs sharp.

## 11-06: promo night over-staked (-$25)
- Three promo bets at the max ($10 boosted SGPx, $10 SGA live most points, $5 Pick6) = 30% of the bankroll in one night, after the user said "no rules tonight". All three lost: the SGPx on Burries's 2nd three, SGA trailing Mitchell in a 22-pt blowout (a starter sitting the 4th is the real risk on a live points-leader bet when the team is already well ahead), and the Pick6 entry.
- The EV was positive on each, but max-promo stakes on 20-55% shots swing the bankroll too hard. Size promo bets by half-Kelly, not by the promo max, and keep the day <= 20% even on promo nights. The day after a loss uses normal stakes (no chasing).

## 11-07: promo Saturday, 93% of the bankroll in one day (about -$15)
- 13 live bets, $63.67 staked on a $68.67 start. Every bet was +EV on paper (sum of EVs about +$10), result about -$15 (-$9 if the Rossi Pick6 hits). Wins: the 4-leg CFB 30% (ASU/La Tech/Texas/UCLA, +$25.72) and Georgia ML 50% (+$4.30). Losses: LSU -3.5 and Tailgate (LSU and Ohio State both lost; LSU was on two tickets), App+Baylor, WKU live, ESPN (Liberty-NMSU finished 44 vs O46.5), NHL Pick6 (Suzuki 0 ast), NBA Pick6 (Durant 1 three), DEN SGP (Zubac 12 reb), SGPx (Draymond 13 ast, Mitchell 5 3s, VanVleet 4 3s).
- The process was right (sharp favorites, boosts on qualifying legs, Ole Miss +3.5 corrected to Georgia ML), but the sizing was wrong. +EV only pays if the bankroll survives to keep taking the daily promos. Most tickets were 12-20% shots, so a 0-for-10 night is ordinary.
- New rules: (1) daily stake <= 25% of bankroll, <= 35% on promo-heavy days; fill promos by EV per dollar (gimmes, odds boosts, 50% boosts on favorites first) until the cap, then stop. (2) Bankroll under $100: prefer 2-3 leg structures (20-35% hit) over 4+ legs. (3) One team per day across tickets. (4) Stake about $3, never the $10 max, until the bankroll is back over $100.
- Tracked, not placed: Pick6 MacKinnon MORE 2.5 SOG + Pickard MORE 21.5 saves + Oettinger MORE 19.5 saves (0.7x each, 2.06x) would have won (4 SOG, 30 saves, 20 saves). Estimated about -24% EV; one hit doesn't change that, but keep tracking Pick6 0.7x discount-line picks: if they hit about 80%+ over 30+ picks, our probability estimates for them are too low.

## Pick6 "discount-steepness" method (user's idea, 11-07)
- How it works: for each player, note the multiplier at the main line (e.g. MORE 3.5 SOG at 0.9x), then the multiplier after Pick6 moves the line down (MORE 2.5 at 0.7x). Players whose multiplier drops LESS for the same cushion (0.9 -> 0.7 instead of 0.9 -> 0.6) are the cheapest discounts. Pick those. The 11-07 NHL slip built this way (MacKinnon SOG, Pickard and Oettinger saves) went 3/3.
- How to check it against the market: Pick6's implied chance per pick is roughly 0.5 / multiplier (0.9x ~ 55%, 0.7x ~ 71%, 0.6x ~ 83%). The true chance at the lowered line comes from sportsbook ALTERNATE lines (Pinnacle/FanDuel alt SOG/saves/points) or a Poisson fit from the main line. Edge = true chance - implied chance. Rank by edge, and play only if every pick in the entry clears the entry's break-even (3-pick at 0.7x each = 2.06x -> needs ~79% per pick).
- Tooling: the nhlprops tag now also pulls alternate markets (SOG, points, assists, saves). The user screenshots the multipliers at both lines; Claude prices each against the alt lines and ranks them.

## 11-08 Moonshot (crash game)
- The user played 3 Moonshot rounds: $5 at 1.2x (+$1, which earned the $5 bonus bet), $15 lost, and $40 cashed at 1.4x (+$16). Net +$2, but $40 was 67% of the bankroll on a game with a house edge and no way to price it. Rule: Moonshot only for a Bet & Get qualifier, at the minimum stake, once.
- The 30% parlay was cashed out for $3.83, which forfeited the boost. Don't cash out boosted tickets unless the offer beats the ticket's fair value.

## Sizing (user handed sizing to Claude, 11-08)
- Stake = half-Kelly from the hit chance and the (boosted) payout: f = 0.5 x (p x b - (1-p)) / b, where b = decimal payout - 1. Then cap by hit chance, so likely bets get more money and long shots get less:
  | hit chance | max % of bankroll |
  |---|---|
  | >= 55% | 6% |
  | 30-55% | 4% |
  | 15-30% | 2% |
  | < 15% | 1% |
- Daily total <= 25% (35% on promo-heavy days). Stakes grow with the bankroll. That compounding is the route to "winning big", not bigger long shots.
- Every card lists the exact stake per slip. The user places what's listed (no default $5).

## Moonshot simulation (11-08): engine/nfl/moonshot_sim.py
- Rules from the DK help page, replayed on every 2025-26 regular-season play (nflverse full pbp; 394 games, 7,609 live rounds).
- Result (assuming an incompletion/turnover before the round's first qualifying play VOIDS the bet, per DK: "occurs before a round starts... voided"):
  | target | hit | EV |
  |---|---|---|
  | 1.2x | 66% | -20% |
  | 1.5x | 56% | -14% |
  | 2x | 47% | -3% |
  | 2.5x | 41% | +5% |
  | **3x** | 35% | **+8%** (90% CI +5 to +11) |
  | 4x | 26% | +8% |
  | 5x | 19-20% | +4 to +9% |
  | 10x+ | | -11% or worse |
- Best spots: 2H rounds (3x +12%) and early rounds ("Before 1st-3rd" incompletion, 3x +16%). Late rounds (9th+) are about 0.
- If that first-play ender instead counts as a LOSS, every target is -18% or worse. VERIFIED 11-08: LV@SF '1H Before 8th' was VOIDED, stake returned (the ender came before the round started), so the void reading holds. Until verified: $1-2 stakes, 3x target, 2H early rounds, track every round.
- Low targets (1.1-1.5x) are the trap: they hit often but lose 14-25%.
- Moonshot entry rules (3x target, by situation when the round starts): >= 5 min left in the half +12 to +17%; 2-5 min about -1%; under 2 min -27% (two-minute drill means incompletions). Run-leaning offense (xpass < 0.6) +10 to +15%, pass-heavy +2%. Offense tied/leading +11 to +13%, trailing +4%. 2H +12%, 1H +4%.
- Checklist: 3x auto-target; only rounds likely to start with 5+ min left in the half; skip when the trailing team is in hurry-up; cash out under ~1:30 left if the offer is close to the current multiplier.

## 11-09 Pick6 0.8x main-line entries are -EV (priced)
- 12 user $1 NBA entries (mostly 3-picks of 0.8x picks at the market's own line) priced vs the sharp main line (Poisson) and the alt ladders: each pick 55-67%, but a 3-pick at 0.8x^3 x 6 = 3.07x needs 68.8% per pick. Entry EVs -26% to -44% (one ~+6% with a missing price). Sum about -$4 on $12.
- Rule: Pick6 only with 1.0x+ picks at >= 57% sharp, a promo or boost, or a discounted line the alt ladder prices clearly above Pick6's implied odds. Never volume entries of 0.8x main-line picks.

## 11-09 System audit: what the data says works (read this before building any slip)
Evidence: `Record/Audit.md` (real money) and `Record/Market Backtest.md` (37,821 NBA book-lines over 15 dates, joined to box scores).
- Real money: 50 settled bets, +$69. Without the one $105.67 parlay: **-$37**. One hit carried the record.
- Stated hit chances were too high: 19 bets added up to 7.3 expected wins; 3 won (2% chance that is luck).
- Singles had no edge: 31 with a recorded close averaged **-1.4% CLV** and beat the close 32% of the time.
- Cause found: **Poisson overstates lowered lines.** Points lowered two steps: Poisson said 81%, 67% hit. Assists, rebounds, threes lowered one step: Poisson 67-76%, actual 64-72%. This inflated every Pick6 discount pick, alt line and Betr promo line we priced.
- The books' no-vig consensus is calibrated to 1-2 points. We cannot out-predict it; we can only find prices that disagree with it.
- Overs hit about 1.5 points under their no-vig price (47.4% vs 49.0%). Not proven (1.4 sigma by day), so: haircut overs, give unders no bonus.
- "Book X is off the others" under 4% claimed EV **lost** 6-13%. At 6%+ it hit 63% (n=48). About 3 such lines a day across all books; DraftKings had 12 at 4%+ in 15 days.
- Pick6 standard 1.0x lines: the market had the pick at 55%+ on 11 of 1,183. Standard Pick6 lines are not an edge.

Rules from this (they override earlier notes where they conflict):
1. Price every slip with `python engine/fair.py` (negative binomial with fitted spread, consensus at the exact line when it exists). No more Poisson scripts.
2. A pick-based bet needs 6%+ EV against the other books at the same line (`python engine/consensus_scan.py`). 2-5% is noise: pass.
3. Profit comes from **promos priced at fair value** (discounted lines, profit boosts, bet-and-gets, bonus credit). A promo slip must still show +EV in fair.py after the boost; the legs must be near fair on their own.
4. No un-boosted singles or parlays at standard prices. They cost 3-10% per bet.
5. If fair.py says the stake is under $5, the honest options are pass or $5 knowing it is over-sized. Say which.
6. Re-check `Record/Audit.md` weekly. If stated chances still run above results after 30 more bets, shrink again.

## 11-10 Betr: shielded "safe" partners cost more than they add
- Tkachuk promo MORE 2.5 SOG (63%) + Scheifele shielded MORE 0.5 points (64%) paid **2x**: 40% x 2 = -19%. The shield cut the payout from 3x to 2x.
- Rule: partner a Betr promo pick with an **unshielded standard line** (full payout) the market has at 60%+ (e.g. LESS 1.5 threes on low-volume shooters), not a shielded low line. Check the payout: break-even is 1 / (product of the two chances).

## 11-11 DraftKings "Stepped Up" college parlay boost (105% at 11+ legs)
- DK college prices vs the other books (48 games): moneylines about -2.7% per leg, alt spreads -4.4%, alt totals -6.1%. But big-underdog alt spreads (dog getting +25 to +45 at about -360 to -400) were close to fair, some slightly positive.
- With 105% on the profit, 11 near-fair legs at about -380 each: about 8% to hit, about +100% EV. Hand-picked favourites/alts (user's first slip) were about 4.5% and +35%.
- Method: pull tag=cbbalt, run engine/cbb_alt.py, pick one leg per game at -360 to -400 with the highest fair chance and leg EV of -4% or better. Max bet was $5.

## 11-12 Live in-game bets: the leak to close
- System bets that day: 6 bets, $21 staked, $41.87 back (Bet & Earn parlay hit, Likely/Daniels Pick6 hit). The system was up.
- Then three live "next field goal type" bets at the IU game: $2, $3, then **$23** (72% of the bankroll on one coin flip). All lost: -$28.
- Live micro-markets carry a big margin and settle in minutes, which makes chasing easy. Rule: **no live in-game bets**, and no single bet over 10% of the bankroll for any reason.
- Near misses that day: Diggs U41.5 lost by 1 yard (42); Aho U1.5 pts lost to 2 goals.
