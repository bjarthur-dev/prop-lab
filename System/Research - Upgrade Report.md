# Rebuild Prop-Lab around enforcement, not more doctrine

Tonight's slate (2026-10-22, Patriots @ Bears on TNF plus Nuggets @ Thunder) broke almost every rule the Prop-Lab vault writes down. The Guide's math is right. Nearly every worked number in it recomputes correctly, and its key ideas are sound: the LLM handles facts, code handles math, EV accounts for settlement rules, CLV is treated as a diagnostic, and the A/B/C judgment test is well designed. The problem is that tonight's nine paper bets ignored all of that. They staked **10% of bankroll per bet against a documented 1–2% cap, putting 90% of the bankroll on two games**. All five NBA entries were overs in one game. Five of the nine were "priced" at media sites (Sports Betting Dime and StatMuse) that take no bets. The 3-leg same-game parlay (SGP) was logged at a price nobody quoted, which creates a **phantom +29% EV**. Two bets failed the vault's own "1–2 points = no edge" pass rule. And no bet came from an actual projection model: Math Engine.md says outright that it does not produce probabilities. So the upgrade is mostly about enforcement, in this order:

1. Make the record trustworthy.
2. Hard-code exposure caps and pass rules.
3. Build the minutes-first (NBA) and volume-first (NFL) projection layers the Guide already describes.
4. Measure skill against the devigged closing market instead of with P&L.
5. Automate the deterministic steps with Python on a Windows scheduler, and limit AI agents to sourced fact-gathering and adversarial review.

Slate size should change how many bets you make and how much total money is exposed. It should not change the edge threshold. On a one-game night like tonight, the right output is usually zero to three small positions.

**How to read this report.** Claims with a web link are sourced. Claims that cite a vault file (`[Vault: …]`) are taken from the user's own notes. Numbers marked **[computed]** come from the research team's own calculations or simulations. Recommendations marked **(heuristic)** are synthesized judgment that has not been validated empirically, and should be tested against your own logs before they are hard-coded.

## Nine paper bets, two games, 90% of bankroll: tonight versus the vault's own rules

The audit recomputed every entry in `bets.csv`. The arithmetic in the CSV holds up (its `ev_pct` values match to rounding), so the failures are about which bets were selected, which prices were used, and how much was staked.

| # | Bet | "Book" | Blend − break-even | Logged EV | Main problem |
|---|---|---|---:|---:|---|
| 1 | Swift o14.5 rush att | SBD | +5.1 pts | +9.7% | Not a real book; built on first-order news ("Monangai OUT") that the NFL prompt says is already priced |
| 2 | Douglas o3.5 rec | SBD | +4.0 | +8.2% | Not a real book (second-order thesis is reasonable) |
| 3 | Stevenson u42.5 rush yds | SBD | +1.6 | +3.0% | **Fails the vault's own 1–2 pt pass rule**; evidence is one game |
| 4 | 3-leg SGP | DK | — | +29.2% | **Price never quoted** (7.38× is just the product of the singles); duplicates bets 1–3 |
| 5 | Gordon 6+ reb | Polymarket | +4.0 | +7.4% | Logged as line 6 instead of 5.5; DNP resolves "No"; edge rests on a 21-game head-to-head sample |
| 6 | SGA o30.5 pts | StatMuse | +2.7 | +5.4% | Not a real book; edge driven by the last 3 games |
| 7 | J. Williams o18.5 | StatMuse | +1.9 | +3.8% | **Fails pass rule**; rationale rests on an unresolved roster fact; the source's angle was the **under** |
| 8 | Jokic o24.5 pts | BetMGM | +3.1 | +6.0% | Blend inputs can't be reproduced; the research file had already marked this "correctly passed" |
| 9 | Jokic o9.5 ast | DK | +4.2 | +8.8% | Correlated with #8; the "disagreement" is against a quote with 12% overround |

Source: [Vault: bets.csv](file:///mnt/user-data/uploads/Prop-Lab/Record/bets.csv), recomputed by the auditor.

**Sizing was off by 5–10×.** The vault states its per-bet cap four different ways: 1% in the Guide's §13 and Math Engine's `cap=0.01`, 0.5–1% in Guide §12.5, and a 2% cap with 5–10% per night in Daily Workflow §3. The Guide also says to "concentrate stakes only in the strongest 1–2 edges; cap total exposure to the single game" ([Vault: The Guide › 11.4](file:///mnt/user-data/uploads/Prop-Lab/System/The%20Guide.md)). Tonight staked $10 on each of nine bets against a $100 bankroll: 40% on one NFL game and 50% on one NBA game. Flat paper stakes are fine for grading probabilities. But the Guide also says to evaluate "the selected betting policy… at what size," and this record cannot test the sizing policy it claims to follow. Under the vault's own 1% cap, with a 2–3% per-game cap, the night would have been about two NFL and two NBA positions of $1 each. Stevenson, J. Williams and the SGP would have been passes.

**The exposure was one bet in disguise.** The three NFL singles and the SGP built from those same three legs all depend on one script: Bears lead, Patriots pass. All five NBA entries are overs in DEN@OKC, so they share pace, overtime risk and blowout risk (OKC −8.5), and bets #8 and #9 share Jokic's minutes. The Guide warns that "all your bets share one game's scenario distribution — a wrong game-script read loses them together," and says teammate dependence has to be estimated pair by pair ([Vault: The Guide › 11.4, 16.6](file:///mnt/user-data/uploads/Prop-Lab/System/The%20Guide.md)). No joint simulation was run.

**Five of the nine prices could not actually be bet.** Sports Betting Dime's footer says "We are not a sportsbook and do not take any wagers" ([SBD](https://www.sportsbettingdime.com/nba/)). StatMuse's two-way pairs imply overrounds of **0.96% (SGA) and 2.44% (J. Williams)**. A single executable book's prop market carries far more vig than that, so the sub-1% figure points to best-of-several-books aggregation or stale quotes (the aggregation is an inference). Meanwhile the Jokic assists quote that bet #9 was measured against carries a **12% overround**, which suggests it was stale. The Guide requires returns "using the price actually taken" ([Vault: The Guide › 12.1–12.2](file:///mnt/user-data/uploads/Prop-Lab/System/The%20Guide.md)). Closing line value (CLV) can never be graded on these rows, because no book exists whose close could be recorded.

**The SGP and Gordon rows are wrong as written.** The SGP's 7.38× is 1.9009 × 2.05 × 1.8929, the product of the three singles' prices. The Guide says SGPs carry a correlation adjustment plus margin and must be evaluated at the quoted payout ([Vault: The Guide › 8.2](file:///mnt/user-data/uploads/Prop-Lab/System/The%20Guide.md)). The note's own "16.9%" product of model probabilities actually works out to 16.57%. Gordon was logged as `line=6, over` for Polymarket's "6+" contract. "6+" is the over-5.5 event. Under sportsbook rules "over 6" pushes on exactly 6, and Market Intel itself says P(exactly N) is about 13–14 points. Polymarket's NBA rules also resolve a player who never takes the court as "No" ([Polyguana mirror of a Polymarket market](https://polyguana.com/market/2039593)), so a DNP is a loss, not the void DraftKings would give. The same mirrored market showed **$111 of 24-hour volume and $2.5K of liquidity**, so a fractional quote like 54.18¢ is probably a mid or last trade, not the ask you could fill at.

**The timestamps undermine the record.** Rows 5–7 were logged at 01:01:34Z with odds stamped at 01:10Z, a quote nine minutes after logging. The SGP was logged at 00:20:03Z, five minutes after the 8:15 PM ET kickoff, using pre-game prices. The slate note gives NBA tip as 9:30 PM ET while the research file says 10:30 PM ET.

**The evidence behind each bet was third-party and small-sample.** Four of the five NBA bets map one-for-one onto "angles" from SBD, Covers and DK Network that were pasted into the research file. Bet #7 flipped the sign of SBD's Jalen Williams *under* recommendation. Gordon's edge rests on "8.0 rpg in 21 games vs OKC." The standard error of a 66.7% hit rate on 21 games is about ±10.3 points, larger than the claimed edge. SGA's rests on "34/36/35 last 3 vs DEN." The independent model probability was never stored, because the `model_prob` column holds the blend, so the Guide's A/B/C test cannot be run on this record. The model's distribution parameters were recorded for only one of the nine bets.

This record can still be useful. The audit recommends keeping all nine rows but flagging SBD and StatMuse rows `executable=false` and the SGP `quoted=false`. Those rows then count toward calibration but are excluded from ROI and CLV. Gordon's row should be corrected to line 5.5 with a `dnp_rule=loss`. The slate note also expects "strong positive CLV" on SGA's move from +102 to −111, but the close source was never recorded and every close field in the CSV is blank, so that claim can't be verified yet.

## The doctrine is right; its application and seventeen contradictions are not

Several parts of the vault are worth keeping as they are:

- **Settlement-aware EV.** EV = P(win)(D−1) − P(loss), with voids counted as zero.
- **Parlay rule.** "A leg may enter only if you would bet it as a single."
- **Kelly for parlay books.** The claim that Kelly-optimal parlay books factorize into single-event solutions matches [Long, arXiv 2603.26620](https://arxiv.org/html/2603.26620v1) and [Whitrow 2007](https://ideas.repec.org/a/bla/jorssc/v56y2007i5p607-623.html).
- **Form and streaks.** The chapter pairs Miller and Sanjurjo's hot-hand correction with evidence that markets already price momentum.
- **CLV caution.** The Guide treats CLV as a diagnostic, not proof. Whelan's 3,670-game NBA moneyline study supports that: only the top CLV decile earned meaningfully (**+11.4%**), and the 9th decile averaged +5% CLV but only **+0.2%** return ([Whelan](https://www.karlwhelan.com/?p=2595)).
- **Worked math.** Every Guide example recomputes, including the Brunson ¼-Kelly of 1.84%, the Poisson λ=1.35 tails, the parlay variance table and the pick'em break-evens. The only miss is a rounding slip: −118 breaks even at 54.13%, not 54.2%.

The errors are in how that math gets applied.

**The blend is done in probability space.** Guide §5.3 warns against averaging probabilities and says to "blend central estimates… and derive alternate-line probabilities from a coherent distribution." Daily Workflow says "blend 50/50." The 50/50 weight is also untested, and the evidence favors the market. Across 479,440 soccer games, consensus bookmaker probabilities regressed on outcomes gave R² ≈ 0.995–0.999 with slopes of 1.003–1.081 ([Kaunitz et al., arXiv:1710.02824](https://arxiv.org/pdf/1710.02824)). Selection makes it worse. Bets are chosen *because* the model beats the market, so halving the deviation scales the winner's-curse bias but does not remove it. The audit's fix (heuristic):

1. Blend the distribution's parameters (its mean and spread), not the final probabilities.
2. Store both the independent model probability and the market probability.
3. Start with a market weight of 0.7–0.8.
4. After about 200 settled bets, fit the weight by regressing outcome on logit(model) and logit(devigged market).

**"Brier < 0.25" tells you nothing.** A perfectly calibrated forecaster at p = 0.55 has expected Brier 0.2475 **[computed]**, so any near-coin-flip forecaster passes. The meaningful number is Brier or log-loss *skill* against the devigged close on the same bets.

**The vault's sample-size guidance is far too small to prove ROI.** The Guide's 300–500-bet "practical minimum" cannot separate a 3% edge from zero. At −110 (per-bet SD ≈ 0.95u), a two-sided 95% test needs about **3,900 bets for a 3% ROI edge, 1,400 for 5%, and 8,700 for 2%** **[computed]**. Props from one game are not independent, which pushes the requirement higher still.

**Kelly treats the point estimate as exact.** [Baker & McHale (2013)](https://ideas.repec.org/a/inm/ordeca/v10y2013i3p189-199.html) show stakes should be shrunk for parameter uncertainty. The vault's only protection is a flat ¼ multiplier plus a cap. It also describes portfolio sizing ("simulate the slate's shared outcomes and cap total exposure to any one game") without implementing it: Math Engine has only a single-bet `kelly()`.

**The vault contradicts itself in at least 17 places.** The most consequential:

- The per-bet cap is 1% in two places and 2% in another.
- One place blends means, another blends probabilities.
- Distributions are called "candidates to test" in one note and "never Poisson on combos" rules in another.
- Market Intel calls CLV "the skill," while the Guide calls it a diagnostic.
- Reverse line movement (RLM) on a spread is called "the free sharp signal" for props without any test.
- The workflow says to "devig a sharp book" but devigs StatMuse quotes.
- Home says the Guide has 16 chapters; it has 17.

The fix (heuristic) is one `System/Rules.md`, or a set of frontmatter constants, holding the cap, game cap, nightly cap, pass margin, blend weight and the allowed-book whitelist. Every other note links to it instead of restating the numbers.

**Neither "Master Prompt" works as a prompt.** The NFL file is hard-coded to one game, with a "verified facts — do not re-research" table that has no URLs or timestamps. It locks in facts that may be stale while forbidding anyone to check them. It also asks the LLM to output "model probability (mean + SD)" when no model exists, which breaks its own rule "you never invent a number." The NBA file is a game-prep dossier: no operating rules, no output schema, no default to PASS. It is packed with head-to-head splits, ATS (against-the-spread) trivia ("DEN covered 19 of 24 as dog vs OKC") and affiliate picks.

The replacement (heuristic) is one sport-agnostic researcher prompt:

- It outputs only structured facts (JSON with URL, retrieved_at and as_of) and *feature deltas* such as minutes, usage or role changes, each with a source and a magnitude.
- It never outputs probabilities.
- It bans head-to-head splits under about 50 player-games, ATS/O-U trends, and raw last-N-game stats, unless code applies shrinkage to them.
- It moves third-party picks into a separate sentiment field the model cannot use as a feature.

## Projecting each spot: minutes first in the NBA, volume first in the NFL, batters faced in MLB

### NBA: model minutes, then usage, then shrunk per-possession rates

Practitioner sources agree that NBA production is "heavily minutes-based." Minutes are where projection sources disagree most, and a star's absence moves usage to his teammates ([amicsta](https://amicsta.substack.com/p/how-to-beat-nba-props)). RotoWire builds minutes from historical usage, teammate injuries, blowout probability, schedule density and rotation context. It does not model foul trouble. For a sense of how tight star minutes are, Anthony Edwards averaged 36.3 mpg and landed between **33 and 39 minutes in 53 of 79 games** ([RotoWire](https://www.rotowire.com/basketball/article/nba-projected-minutes-explained-fantasy-basketball-97473)).

The recommended chain (heuristic, standard practitioner structure) is:

E[stat] = E[minutes | availability, rotation, spread, back-to-back] × per-possession rate (time-decayed, shrunk to a prior) × game pace ÷ player's baseline pace × a heavily shrunk opponent factor × a role multiplier when teammates are out.

Copy the DARKO-style architecture of a separate decay rate per stat rather than one "last N games" window. That design is general knowledge and unverified here.

**How fast stats stabilize decides how hard to shrink them.** Rebounds, assists and blocks are stable, highly discriminating skills, largely because they track role and position. **3P% is the least stable common metric: more than half of the between-player variation within a season is chance**, and empirical-Bayes shrinkage toward the player's career average improves it. FT% is very stable from year to year ([Franks et al., arXiv 1609.09830](https://arxiv.org/pdf/1609.09830)). So project threes made as a fast-updating 3PA rate times a heavily shrunk 3P% (heuristic). In October and November, use a Bayesian update with a per-stat stabilization constant k: posterior rate = (prior rate × k + current rate × n) / (k + n). Override the prior only when the role has demonstrably changed (heuristic).

**Distributions (heuristic).** Model points as the sum of 2PA, 3PA and FTA counts times make probabilities, or as roughly normal for high-volume scorers. Use negative binomial for rebounds and assists. Use Poisson or NB for threes, steals and blocks at low means, where a normal approximation badly misprices 0.5 and 1.5 lines. The audit confirmed the direction: for mean 1.5 and variance-to-mean ratio (VMR) 2.06, P(≥2) is 37.9% under NB versus 44.2% under Poisson. Simulating at the minutes level produces the right correlations automatically. Same-player stats rise together through minutes, and teammates compete for usage but share pace and overtime. No public source gives NBA prop SDs or correlation matrices, so estimate them from your own logs.

**Which context is real.** Back-to-backs are real but modest. Road teams on the second night were about **3 points per 100 possessions worse** on adjusted net rating ([Grantland](https://grantland.com/the-triangle/the-effects-of-the-compressed-schedule-examining-back-to-backs/)), though that was a small, lockout-compressed sample that probably overstates the modern effect. The bigger prop effect is minutes and availability (heuristic). Referee crews differ by about **4.7 fouls per 100 possessions** between the extremes, Scott Foster at +2.31 versus Intae Hwang at −2.39 ([The F5](https://thef5.substack.com/p/nba-referee-database)). That matters for free-throw-heavy scorers and for foul-prone bigs' minutes.

Vacated usage does not split proportionally. It flows mostly to the next primary creator and to whoever absorbs the minutes. A clear beneficiary typically gains about +2 to +5 usage points, or +1 to +4 points scored (heuristic). Shrink small-sample WOWY (with-or-without-you) splits toward a structural redistribution model. Head-to-head history and last-3 streaks deserve about zero weight beyond what time-decayed rates already capture. That is the opposite of how tonight's NBA bets were built.

### NFL: model team volume, then player shares, then heavily regressed efficiency

Build the chain in this order (heuristic):

1. Team plays.
2. Neutral pass rate over expectation (PROE), plus a game-script adjustment.
3. Dropbacks.
4. Routes, times targets per route run (TPRR), gives targets.
5. Catch rate.
6. Yards.
7. Separately: designed runs times carry share.

The stability numbers set the weights. Year over year, **TPRR has R² 0.41, yards per route run 0.21, and yards per target only 0.08** ([Football Perspective](https://www.footballperspective.com/yards-per-route-run-yards-per-target-and-targets-per-route-run/), 2007–12 data). Rushing yards over expected has a split-half correlation of only 0.17 ([StatsbyLopez](https://statsbylopez.netlify.com/post/assessing-running-back-performance-using-distributions/)). At Weeks 7–8 that suggests roughly 50–70% weight on season-to-date shares and 30% or less on season-to-date efficiency (heuristic). Use route participation, not snap share, for receivers. nflreadr's FTN participation data is confirmed only for 2023–24, and the `qs` format was hard-deprecated in 2026 ([nflreadr NEWS](https://cloud.r-project.org/web/packages/nflreadr/news/news.html)).

**Game script is the largest lever.** League rush rate is **40.5% in neutral situations, 51.5% when leading by 8+, and 28.0% when trailing by 8+**. Coaches' lead-versus-trail sensitivity ranges from 20.4 to 37.7 points ([4for4](https://www.4for4.com/fantasy-football/how-play-calling-tendencies-affect-fantasy-football), dated 2016 data). Simulate script rather than assume one. Draw a margin from about Normal(−spread, 13–14) (heuristic), map it to a pass rate with team-specific sensitivity, then simulate plays and shares. The vault's own 10,000-trial specification already describes this.

**Yardage is right-skewed, so its median sits below its mean.** A receiver averaging 65 yards can have a median under a 50-yard line ([FTN](https://ftnfantasy.com/nfl/betting-nfl-props-using-math-week-1)). Comparing a mean projection to a line set near the median therefore biases you toward overs. Use simulation or a skewed distribution. For anytime TDs, P(≥1) = 1 − e^(−λ): a back at 0.7 expected TDs is about 50%. Books post shorter than that and hold **8–15% on TD markets**, and prices differ by 30+ cents across books ([DeucesCracked](https://www.deucescracked.com/blog/nfl-anytime-touchdown-props-betting-guide)).

**Weather: wind matters, temperature mostly doesn't.** Team passing falls from **227 yards at 0–7 mph wind to 208 at 12–14 mph**. Rain cuts passing yards by about 15%, and rain games went under 57.4% of the time ([Sharp Football Analysis](https://www.sharpfootballanalysis.com/betting/nfl-weather-betting/amp/)). TNF does *not* need a blanket under adjustment: 2019–24 TNF games averaged 45.49 combined points versus 45.69 for other games ([FanDuel Research](https://fanduel.com/research/thursday-night-football-nfl-betting-trends-historical-spread-over-under-analysis)). The real TNF risk is stale injury information. Backup-QB effects are player-specific and only anecdotally documented ([PFF](https://pff.com/news/fantasy-football-how-do-backup-qbs-affect-skill-player-production)).

### MLB: batters faced × matchup K%, with shorter postseason leashes

The Guide already includes MLB hitter and pitcher chains. The upgrade (heuristic) is to model strikeouts as expected batters faced (pitch count ÷ pitches per PA, capped by when the manager pulls the starter) × log5 matchup K% by handedness × park, then simulate. Down-weight pre-2026 umpire K data. The 2026 ABS challenge system uses a slightly smaller zone, running 27% to 53.5% of batter height. It is expected to lower K% a little from 2025's 22.2% and reduce umpire influence ([MLB.com](https://www.mlb.com/news/abs-challenge-system-2026-mlb-season-overview?p=0)).

Postseason starters get pulled about "two innings earlier" ([DeucesCracked](https://www.deucescracked.com/blog/mlb-2026-postseason-pitching-matchups-betting-guide)), which is qualitative. Cutting expected batters faced by 10–20% is a heuristic. Batter props depend on plate appearances by lineup slot, regressed platoon splits, park and weather.

### How day types differ

Sourced quantitative evidence by day type is thin. The framework below is heuristic, built from the mechanisms above:

- **Early season:** stale priors and book mispricing make edges larger, but you also know less, so shrink more, not less. An ETSU paper documents an early-season pricing bias in the NBA ([ETSU](https://dc.etsu.edu/etsu-works/17780)).
- **Back-to-back-heavy NBA nights:** wider minutes distributions and later news. Wait for the news, then hit the stale props.
- **National TV, holidays and playoffs:** micro-slates with peak attention. Expect efficient closes and use micro-slate rules. In the playoffs, edges come from tighter rotations and minutes reallocation.
- **Late season:** tanking and rest create minutes volatility, which favors reacting to news.

## Slate size, game choice and timing change how many bets you place and how much you risk, not the edge threshold

**Bigger slates are softer, but only if you shrink properly.** Books keep prop limits low ($200–300 for winners, sometimes $10) because they "can't keep track of them all." Props go stale for "a short window" after news moves the main markets ([Establish The Run](https://establishtherun.com/miller-why-prop-betting-is-profitable/)). That supports a heuristic: a one-game TNF concentrates attention on about 40–80 props, while a 12-game NBA night spreads it across 1,000+, so softness should rise with slate size. No public study measures this directly.

A Monte Carlo simulation shows the trap **[computed; parameters illustrative]**. True edges were drawn as N(−1%, 2%) and model noise as N(0, 3%), and the top 5 picks by estimated edge were taken. When scanning 20 props (a one-game slate), the top 5 *looked* like 3.4% edges but were truly 0.3%. When scanning 400 props, they looked like 8.3% and were truly 1.9%. Estimated edge overstates true edge by 4–10×, yet the true edge of the best picks rises about 6× with slate size. The implied shrinkage factor is about 0.31. The lesson: stop taking "the best five tonight" on small slates. Hold one constant shrunk-edge threshold and let the number of qualifying plays scale with the slate.

**Sizing simultaneous bets.** For independent bets, exact simultaneous Kelly sizes each one almost exactly at its isolated stake. The deviation is cubic in edge, and adding parlays gains only fourth-order growth ([Long, arXiv 2603.26620](https://arxiv.org/html/2603.26620v1)). So the binding constraints are total exposure, correlation and estimation error. Treat a same-game cluster as roughly *one* bet (heuristic). The recommended scheme below is heuristic throughout, built on sourced payout rules and the Kelly literature:

| Slate class | Games | Expected qualifying legs | Straight bets | Pick'em slips | Max slate exposure | Per-game cap |
|---|---|---|---|---|---|---|
| Micro (TNF/MNF/SNF, single national NBA game, playoffs) | 1–2 | 0–4 | 0–4 | 0–2; 3–5 legs; Flex; deliberate script stacks | ≈3–5% | = slate cap |
| Small | 3–5 | 2–8 | 2–8 | 1–3; 4–6 legs; ≤2 legs per game | ≈5–8% | ≈3% |
| Medium | 6–9 | 5–15 | 5–15 | 2–4 disjoint 5–6-leg slips, 1 leg per game | ≈8–12% | ≈3% |
| Large (NBA 10–15 games, NFL Sunday main) | 10+ | 10–30 | 10–30 | 3–6 disjoint 5–6-leg slips | ≈10–20% | ≈3% |

Two further rules apply to every class (heuristic). Cap each player at about 1.5–2% of bankroll across all props and slips, which mirrors Underdog's **$750 per-player risk cap** ([ETR](https://establishtherun.com/how-to-beat-pick-em-on-underdog-fantasy/)). And never hold singles plus an SGP of the same legs. Tonight's two-game, two-sport night is a micro slate: about 3–5% total exposure, not 90%.

**Pick'em slips work best at 5–6 legs, which brings extreme variance.** These are PrizePicks' published payouts:

| Picks | Power (all correct) | Flex payouts |
|---|---|---|
| 2 | 3× | — |
| 3 | 5× | 3/3 = 2.25× |
| 4 | 10× | 4/4 = 5×, 3/4 = 1.5× |
| 5 | 20× | 5/5 = 10×, 4/5 = 2×, 3/5 = 0.4× |
| 6 | 37.5× | 6/6 = 25×, 5/6 = 2×, 4/6 = 0.4× |

Source: [PrizePicks Help](https://intercom.help/prizepicks/en/articles/9047668-payouts-explained). The per-leg break-evens follow: **54.2% for 6-Flex, 54.7% for 6-Power, 57.7% for 2-Power, and 58.5% for 3-Power** **[computed]**. Underdog's standard 3-pick pays 6× (55.0% break-even), much better than PrizePicks' 5× 3-Power. A 5-pick at a 60% hit rate wins only about 7.8% of the time ([ETR](https://establishtherun.com/how-to-beat-pick-em-on-underdog-fantasy/)). A 6-Power slip hitting about 4% of the time has a 36% chance of 25 straight losses **[computed]**, so size slips at about 0.25–0.5% of bankroll for Power and 0.5–1% for Flex (heuristic).

All three apps require picks from at least two teams. On Underdog, a push that leaves only one team refunds the entry ([ETR](https://establishtherun.com/how-to-beat-pick-em-on-underdog-fantasy/); [TheLines on Pick6](https://www.thelines.com/draftkings-pick6-guide/)). On a one-game slate, that rule means every leg is correlated. Stack deliberately in the projected script direction rather than pretend the legs are independent. PrizePicks reduces multipliers for same-game picks but doesn't publish by how much. On a big slate, build disjoint slips with one leg per game so the binomial math holds. Payout tables change and peer-to-peer formats (PrizePicks Arena, Sleeper, Pick6 pools) vary by entry, so compute break-even from the multiplier actually displayed.

**Timing depends on where the edge comes from** (heuristic, built on sourced mechanisms):

- **Your projection versus the opener:** bet early. Openers have the lowest limits and the most value, and sharps max-bet them ([ETR](https://establishtherun.com/miller-why-prop-betting-is-profitable/)).
- **Pick'em versus a sharp book:** bet late, 60 to 15 minutes before lock. That comparison "works best… closer to game time" ([ETR](https://establishtherun.com/how-to-beat-pick-em-on-underdog-fantasy/)).
- **News:** fire within minutes, using pre-computed scenarios.

The NBA news windows are fixed. The day-before injury report is due at 5 p.m. local (1 p.m. game-day for the second leg of a back-to-back). Since a **Dec 19, 2025 memo**, there is also a mandatory game-day resubmission between 11 a.m. and 1 p.m. local ([NBA Official](https://official.nba.com/nba-injury-report-2025-26/); [AP/News4JAX](https://www.news4jax.com/sports/2025/12/19/nba-tweaks-its-injury-reporting-rules-still-wants-changes-to-prop-betting/)). Whether 2026-27 changes this is unverified. NFL inactives come about 90 minutes before kickoff (general knowledge). Use separate pick'em slips per start window, because Pick6 lineups can't be edited after submission. Early settlement lets you recompute Kelly on updated bankroll, which is exactly the sequential equivalence Long describes.

**The 2026-27 NBA season removed some markets.** At partner sportsbooks the league banned same-player under parlays, opening-tip bets, "miss specific shots" props, and **unders on players projected under 12 minutes**. Prediction markets are not covered ([Covers, Oct 16 2026](https://www.covers.com/industry/nba-bans-certain-bet-types-ahead-of-new-season-oct-16-2026)). The classic "fade the deep bench" under is gone at those books.

## Finding props: devig real two-way books, price prediction markets net of fees, and treat tools as screens

**No book is "the Pinnacle of props."** Practitioners name **FanDuel**, which originates its own prop numbers, and **Caesars**, which takes about $500+ even on openers, as the most efficient US prop books. Pinnacle and Circa post limited prop sheets late. DK, Caesars and MGM reportedly share a source, and many offshore books use the same prop tool ([ETR, 2023](https://establishtherun.com/understanding-the-current-ecosystem-of-nfl-player-props/)). So deduplicate your consensus by price source rather than counting copies as independent votes (heuristic). FanDuel often posts one-way props, which shouldn't be devigged naively ([BetSmart](https://betsmart.beehiiv.com/p/efficient-prop-markets), a promotional source).

**Devig method.** No 2026 source ranks devig methods empirically for props. The theory (background knowledge) is that methods differ by tenths of a point on −110/−110 markets but by 1–2+ points on high-hold or lopsided ones. So screen high-hold markets with the power method or a worst-case across methods, and skip or fixed-haircut one-way markets. Hold itself tells you how reliable a reference is. A 4% two-way market at a sharp-ish book is a benchmark. StatMuse's 0.96% or a 12% stale quote is not.

**Tools and data feeds.** Of the commercial options, only The Odds API's pricing was verified. It runs from free (500 credits, no historical data) to $30, $59, $119 and $249 per month, and all paid plans include historical odds ([the-odds-api.com](https://the-odds-api.com/)). Historical player props start **May 3, 2023, at 5-minute snapshots**, at 10 credits per region per market per event ([historical data page](https://the-odds-api.com/historical-odds-data/)). Polling full prop boards every few minutes probably needs the $119–249 tier; that estimate is unverified. OddsJam, Unabated, Props.cash, Outlier, OpticOdds and SportsGameOdds 2026 pricing **was not verified** and should come from vendor pages. Their marketing (for example, Rotowire's daily "OddsJam EV tool found an edge" posts) is not evidence of returns.

**Prediction markets: fee-adjusted, ask-side, liquidity-checked.** Kalshi's taker fee is roundup(0.07 × C × P × (1−P)), peaking at 1.75¢ per contract at 50¢ ([Allium](https://allium.so/blog/kalshi-fees-why-the-cost-peaks-near-50-cents/)). A 55¢ buy breaks even at **56.74%** ([Stokastic](https://www.stokastic.com/articles/prediction-markets/kalshi-vs-dfs-pickem-apps)). Resting maker orders mostly skip the fee. Kalshi caps NBA props at $10,000 per trade ([Front Office Sports](https://frontofficesports.com/article/kalshi-adds-nba-prop-markets-as-betting-crackdowns-surge/)).

**The research notes conflict on Polymarket's sports fees, and this report does not resolve it.**

- *vault_audit.md* cites Pine Analytics: Polymarket introduced taker fees on Sports markets on **Feb 18, 2026**, peaking around a 0.75% effective rate after a Mar 30 rollout, with makers paying nothing ([Pine Analytics](https://pineanalytics.substack.com/p/polymarket-fee-rollout)).
- *prop_discovery_tools.md* cites River Markets: a Polymarket US fee schedule effective **Jul 1, 2026**, with taker fee = contracts × 5% × P × (1−P) for sports (max $1.25 per 100 contracts at 50¢) and makers at zero ([River Markets](https://www.rivermarkets.com/insights/polymarket-us-fees.html)).

The two may describe different entities, the global Polymarket venue versus the CFTC-licensed Polymarket US, or successive schedules, but neither note confirms which. Neither source mentions player props specifically. The difference is material for the Gordon bet. Under the ~0.75% figure, EV falls from +7.4% to about +6.6%. Under the 5%×P(1−P) formula at 54.18¢, the all-in cost is about 55.4¢ and EV falls to about **+5.0%** **[computed]**. Check the live fee on the order ticket before trusting either figure. Legal access is also in flux. The Third Circuit sided with Kalshi, the Ninth (and apparently the Sixth) against it, and New Jersey petitioned the Supreme Court on Sep 2, 2026 ([Finance Magnates](https://financemagnates.com/fintech/federal-courts-now-disagree-on-kalshis-sports-contracts-new-jersey-wants-the-supreme-court-to-settle-the-fight)). Verify geofencing in your state.

**Pick'em screening recipe** (heuristic, matching what commercial tools sell):

1. Devig the sportsbook market at the same number.
2. If the app's line differs, convert through a distribution.
3. Flag legs above the actual entry's break-even.
4. Build slips from the flagged legs.

A −140 book price can be worth about −122 on Underdog ([ETR](https://establishtherun.com/how-to-beat-pick-em-on-underdog-fantasy/)). Goblins and Demons are not automatically +EV ([Stokastic](https://www.stokastic.com/articles/dfs-strategy/how-prizepicks-multipliers-work)).

**Where to look.** Sourced evidence points to unders on skewed, low-volume NFL markets. PFF's 2020–mid-2022 blind bets returned **+108 units on RB receiving-yard unders** and found receiving-yard overs "very hard to win long-term" ([PFF](https://pff.com/news/nfl-betting-2022-midseason-player-prop-performance-review)); those edges may have decayed. Add TD price shopping and stale lines after news. NBA candidates (practitioner consensus, unmeasured) are role players, rebounds and assists, low-count markets at 0.5/1.5, and alt-line tails. Pre-2026 notes suggest smaller markets such as WNBA have more edge than major-sport props.

## Measuring everything: CLV against the devigged close first, P&L last

**Computing prop CLV properly** ([Whelan](https://www.karlwhelan.com/?p=2595) for the method; the steps are heuristic):

1. Snapshot both sides at bet time and at close, the last snapshot before start.
2. Devig the closing pair from the sharpest available book or a median of several.
3. Compute CLV% = your decimal odds × closing fair probability − 1.
4. If the line moved, convert through your distribution model, or log "line CLV" separately.
5. If no sharp close exists, record "no close" rather than imputing one.

Whelan's lesson sets the bar. Mean CLV must clearly exceed zero *and* the hold, and high-CLV deciles must actually return more. CLV also converges fast. With a per-bet mean of 2% and SD of 5%, about 24 bets reach t ≈ 2 **[computed; use your own SD]**, versus thousands for ROI.

**Calibration and skill** ([Wikipedia: Brier score](https://en.wikipedia.org/wiki/Brier_score) for definitions; the application is heuristic). Store p_model, p_market at bet time and p_market at close for every bet. Report Brier skill and log-loss skill against the close; negative means the market beats you. Expect results within ±1–2% of the market even for a profitable model. Use quantile bins of at least 50 bets for reliability diagrams, since most props sit at 0.45–0.60, and also report calibration-in-the-large. To avoid optional-stopping bias, use either:

- a pre-registered review every 250 bets, or
- an anytime-valid **test martingale** (a running wealth from betting a small Kelly fraction of your edge against the market), rejecting "no edge" once that wealth passes 20 at α = 0.05 ([Shafer, "Testing by betting"](https://www.glennshafer.com/assets/downloads/articles/article104_jrss_shafer-testingbybetting-with-discussion-response.pdf?lang=en-GB)).

Segment by sport, market, book, slate size, minutes to start, side, reason code and executable flag, and cluster standard errors by game_id. Treat segment "wins" as hypotheses: 48 cells will produce about 2 false positives at 5%.

**Paper-to-live graduation** (heuristic; no published criteria were found). All of these must hold:

1. 300–500 timestamped paper bets with both-side snapshots.
2. Mean devigged CLV of at least +1.5–2% with t > 2, or a passed e-value test.
3. Brier skill against the close ≥ 0, at minimum against the bet-time market.
4. Calibration-in-the-large within ±2 points.
5. Positive CLV in at least two independent segments.
6. Zero data-integrity or hallucination incidents in the last 100 bets.
7. Four or more weeks of unattended runs.

Then go live at 1% flat units, with a kill switch if rolling-200 CLV drops to 0 or below, or drawdown exceeds 35%.

Even at quarter-Kelly with a true 3% edge, a simulation of 2,000 bets gives a **23.5% median maximum drawdown, a 37% 90th-percentile drawdown, and an 11% chance of finishing below the starting bankroll** **[computed]**. Full Kelly gives a 71% median drawdown. On $100, quarter-Kelly stakes are under $1.

**The logging schema has to change** before any of this works. Add to bets.csv, or better a database table:

- p_model, p_market, p_market_method, market_source
- dist, mu, sd or VMR
- executable, quoted, dnp_rule
- game_id, corr_group, reason_code, minutes_to_start, slate_class
- model_version, run_id

Add two validation rules: reject a row if `odds_ts > logged_at` or `logged_at > start_time`.

## Automating with Python, scheduled Claude tasks, Obsidian Bases and a reviewer agent

**Code does the math; the LLM finds facts and challenges them.** The architecture (heuristic, built on the sourced tool capabilities below):

| Local time (NBA day) | Runner | Job |
|---|---|---|
| 06:30 | Windows Task Scheduler → `ingest.py` | Pull box scores (nba_api / nflreadpy) into DuckDB; settle bets in code; compute CLV from stored snapshots |
| 10:00, at bet time, T−10 min | Task Scheduler → `odds_snapshot.py` | Append-only odds snapshots for target markets; close = max(ts) < start |
| ~11:00–13:30 local + 30 min pre-tip | Claude Desktop local task "research-agent" | Read slate JSON; gather injury/lineup news; write the slate note with every fact carrying a URL and retrieved_at; output only structured feature deltas |
| After research | `price.py` | Projections + deltas + devigged market → p_model, p_blend, shrunk edge; apply Rules.md caps and pass rule; write candidates |
| Before logging | Claude task "reviewer-agent" (separate context) | Re-check every number against DuckDB or its URL; mark `verified`; block unverified bets |
| Next morning | Python + Claude | Settlement, CLV by reason code, calibration PNGs, daily review note |

**Tool facts that shape the design:**

- **Claude Code Desktop local scheduled tasks** run only while the app is open and the PC is awake. On wake they run **one** catch-up for the most recent missed run. They support custom cron, store prompts at `~/.claude/scheduled-tasks/<name>/SKILL.md`, and stall on any unapproved tool. Cloud tasks run with the machine off but have no local file access ([Claude Code docs](https://code.claude.com/docs/en/desktop-scheduled-tasks)). Use local tasks, put time guards in every prompt ("if after tip-off, create no bets"), turn on "keep computer awake," and do a "Run now / always allow" pass once per tool.
- **The vault is just files.** A local task can read and write it directly. For surgical edits while Obsidian is open, the **Local REST API** plugin offers PATCH by heading, block or frontmatter key, plus a **built-in MCP server at `/mcp/`** with 16 tools. It runs on HTTPS port 27124 with bearer authentication ([GitHub](https://github.com/coddingtonbear/obsidian-local-rest-api)).
- **Obsidian Bases** (core plugin since 1.9) defines `.base` YAML views with filters, formulas and summaries (Average, Sum, Median, Stddev and more) and groupBy ([Obsidian Help](https://obsidian.md/help/bases/syntax)). Bases reads note properties, not CSVs. So generate one note per bet with flat snake_case frontmatter and build these views:
  - open bets
  - exposure by game
  - CLV by market (average clv_pct, sum of pnl)
  - reason-code ledger
  - calibration bins (bucket = round(model_prob×20)/20)
- **Other plugins.** Dataview, Templater, QuickAdd and Obsidian Git are useful, but their 2026 status was not verified. Calibration and CLV charts rendered as PNGs from Python are sturdier than in-vault charting.
- **Data feeds.** nflreadpy returns Polars DataFrames and supports filesystem caching. nba_api needs Python 3.10+, and NBA.com changes endpoints without notice ([nflreadpy](https://github.com/nflverse/nflreadpy); [nba_api](https://github.com/swar/nba_api)). Running both on the home PC sidesteps reported cloud-IP blocking, which is anecdotal.

**Fix the two-sources-of-truth problem.** Home.md says "the cloud sandbox is the live version; this vault is your reading room," with no sync mechanism. Make DuckDB canonical. Make vault notes generated mirrors plus the research log, and keep constants in Rules.md.

**Hallucination guardrails** (heuristic, since no first-party guidance on this was found):

1. LLMs never output probabilities or stat values used in pricing.
2. Every quoted number must exist in a provided data file, or come with a URL and a quoted snippet.
3. The reviewer runs in a separate context and is instructed to falsify.
4. Automated checks confirm the player is on the team, the game exists, and the line exists in the snapshot.
5. Every note logs `run_id` and `model_version`.
6. A hallucination-incident counter is one of the graduation metrics.

## Prioritized upgrade roadmap

The order follows the audit's ranking: fix the record first ("the record is the product"), then risk, then the model. Effort estimates are heuristic.

| Priority | Upgrade | What changes | Why first | Effort |
|---|---|---|---|---|
| 1 | Record integrity | New columns (p_model, p_market, method, source, executable, quoted, dist/params, game_id, corr_group, dnp_rule, reason_code, run_id); timestamp validation; re-flag tonight's rows; Gordon → 5.5 | Every later metric depends on it; tonight's rows can't be graded for CLV | Hours |
| 2 | One Rules.md + hard caps in code | 1% per bet (¼-Kelly on shrunk edge), ≤2–3% per game, slate cap by class, ≤2 positions per game, ban on singles + SGP of the same legs, allowed-book whitelist | Tonight was 90% of bankroll across two correlated clusters | Hours |
| 3 | Pass rule in code | Auto-PASS unless shrunk blend − break-even ≥ ~3 pts *and* model − sharp devig ≥ ~3 pts; no SGP without a quoted payout and timestamp | Two of nine bets failed the existing rule; SGP EV was phantom | Hours |
| 4 | Odds snapshot pipeline | The Odds API → append-only DuckDB at open, bet time and T−10; devig only real two-way books (power or worst-case for high hold) | Makes CLV computable; kills media-site "books" | 1–2 days |
| 5 | Evaluation layer | CLV vs devigged close; Brier/log-loss skill vs close; quantile reliability bins; test martingale; segment report clustered by game | Replaces "Brier < 0.25" and the 300–500-bet ROI myth | 1–2 days |
| 6 | Prediction-market and pick'em chapter | Ask-side price + live fee (resolve the Feb 18 vs Jul 1 Polymarket conflict on the ticket), depth check, DNP-as-No; per-app break-evens from the displayed multipliers; two-team rule | Polymarket was used with none of this modeled | Hours |
| 7 | Researcher + reviewer prompts | Replace both Master Prompts: facts-only JSON with URLs, feature deltas, small-sample bans, quarantined third-party picks; separate falsifying reviewer | The prompts seeded the night's bets almost one-for-one | 1 day |
| 8 | NBA projection engine | Minutes distribution (spread, back-to-back, OT branch) × per-stat time-decayed, shrunk per-possession rates × pace × shrunk opponent; NB/Poisson simulation; scenario pre-computation for questionable players | Currently "model probability" is hand-estimated | 1–3 weeks |
| 9 | NFL projection engine | Script-simulated volume → route/carry shares → regressed efficiency; skewed yardage; Poisson TD λ; wind adjustments | Same | 1–3 weeks |
| 10 | Blend redesign | Blend parameters, not probabilities; market weight 0.7–0.8; refit after ~200 settled bets | Requires stored p_model and p_market (step 1) | After data |
| 11 | Scheduling + Obsidian | Task Scheduler Python jobs; Claude local tasks with time guards; per-bet notes; Bases dashboards; Local REST API/MCP only if needed | Removes manual close capture, which is impossible by hand | 2–4 days |
| 12 | Slate-class playbook and graduation gate | Micro/Small/Medium/Large rules; go-live criteria; kill switch | Needs the evaluation layer and a few hundred logged bets to tune | Ongoing |

MLB slots in after NBA and NFL with the same pattern: a batters-faced × matchup K% strikeout simulation, and lineup-slot plate appearances for batter props.

## Conclusion

The Prop-Lab vault doesn't fail for lack of theory. It reads like the work of someone who has done the reading. It fails because nothing between the doctrine and the bet slip enforces it, so the natural pull of a live slate (affiliate angles, small hot samples, "best five tonight," product-priced parlays) took over. The most valuable upgrades are therefore unglamorous: a log that refuses bad rows, caps that live in code, and a market benchmark that can actually be bet. Without those, a better projection model would only produce more confident versions of the same errors. The second insight is about scale. A one-game national-TV slate is the *least* favorable environment for this system: everything is correlated, attention is at its peak, and selection bias is largest relative to the signal. The system's natural advantage, once automated, is the busy NBA Tuesday or NFL Sunday main slate, where speed after news and broad coverage matter more than clever narratives.

Three questions remain open, and only your own data can settle them. Do prop CLV and closing efficiency really vary with slate size and time-to-start? What market weight in the blend best predicts outcomes? And which "soft market" claims, mostly from 2020–23 practitioner sources, still hold in 2026 after league-driven market restrictions? A timestamped, two-sided, automated log is the instrument that can answer all three. Building it is the upgrade that makes the other upgrades possible.
