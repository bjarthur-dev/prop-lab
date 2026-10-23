# Beating the Books on Player Props: A Complete Research & Modeling Guide (NBA / MLB / NFL)

Deep research report — compiled October 2026

---

## 1. What "Beating the Books" Actually Means

Before any sport-specific strategy, the definition has to be right, because most bettors lose while "winning" picks.

### 1.1 The three numbers that matter

For every prop there are three distinct quantities that casual bettors collapse into one:

1. **The player's projected mean** — e.g., "Jayson Tatum projects for 27.3 points."
2. **The probability of exceeding a specific line** — e.g., "P(over 24.5 points) = 63%."
3. **The expected value (EV) at the offered price** — the only thing that determines long-run profit.

A projection of 27.3 does not mean the over 24.5 is a good bet. The bet is +EV only if your estimated win probability exceeds the **break-even probability of the price you are actually offered** (52.38% at -110, 45.45% at +120). A devigged market benchmark (Section 1.4) is a useful comparison estimate — but it is one model's estimate of fair value, not ground truth. Your edge is against the price you can actually bet, at the moment you can bet it.

### 1.2 The EV formula

For a two-way prop where one side wins and the other loses:

\[
EV = p \times D - 1
\]

where \(p\) is your estimated win probability and \(D\) is the decimal odds. At **-110** the decimal price is 1.909, so the break-even probability is \(1/1.909 = 52.38\%\). If you estimate 55%, your EV is \(0.55 \times 1.909 - 1 = +5.0\%\) — bet. If you estimate 51%, EV is \(-2.6\%\) — pass, no matter how much you like the player ([Circa Sports](https://www.circasports.com/blog/kelly-criterion-for-sports-betting-explained)).

When voids are possible (Section 9), use the settlement-aware form:

\[
EV = P(\text{win}) \times (D-1) - P(\text{loss})
\]

with refunded voids contributing zero net profit. If \(p = P(\text{win} \mid \text{action})\), then \(pD-1\) is the EV conditional on the wager having action; per submitted dollar, EV is \(P(\text{action}) \times (pD-1)\), which equals \(P(\text{win})(D-1) - P(\text{loss})\).

A -110/-110 prop market has an overround of **4.76%** (both sides imply 52.38%, summing to 104.76%) — and a bettor picking sides at random loses about **4.55% of stake per bet**. That margin is the default cost of doing business unless your probabilities beat the price.

### 1.3 The .5 line doesn't help you

Half-point lines (24.5, 1.5, 0.5) exist so there is no push — one side always wins. That guarantees a winner, but it does **not**:

- make the sides equally likely,
- remove the vig,
- or protect you from settlement rules. Injuries, DNP rules, and voids still apply (see Section 9).

### 1.4 Removing the vig to estimate the fair number

You cannot know if you have an edge until you strip the book's margin out of the two-way price. The standard devig methods:

| Method | How it works | When to use |
|---|---|---|
| **Multiplicative (proportional)** | \(p_i = b_i / \sum_j b_j\) where \(b_i = 1/o_i\) | Balanced markets; quick scans |
| **Power** | Find \(k\) so \(\sum_i b_i^k = 1\); then \(p_i = b_i^k\) | Lopsided markets; value scanning |
| **Shin** | Solves for insider-trading fraction \(z\) | Sharp benchmarks; calibrating vs closing lines |

([OddsPapi](https://oddspapi.io/blog/no-vig-odds-api/))

**Practical protocol:** devig a sharp, low-margin book to get a market-implied fair probability, then compare your model's probability against that benchmark — and against the best executable price you can actually get. Books differ; Pinnacle is widely used as the sharp anchor for game lines (margins around 2–3%, vs 5–8% at softer books) ([OddsPapi](https://oddspapi.io/blog/backtest-betting-model-free-historical-odds/)).

### 1.5 "No bet" is a valid output

One odds-vendor's guide illustrates the scale of a modern slate: roughly **10 NBA games × 10 players × 5 prop types = 500 markets** on a typical night — and frames even a 5% hit rate of meaningful edges as ~25 opportunities ([TheOddsAPI](https://theoddsapi.com/guides/player-props)). Treat that arithmetic as illustration, not evidence. The decision framework it implies is correct though: **the default output for most props on most nights should be "pass."** A system that forces a pick on every game manufactures -EV bets.

---

## 2. How Prop Markets Actually Work (and Where They May Be Soft)

### 2.1 How books set the lines

Sportsbooks build prop lines from: team play volume and pace, pass rate, the player's snap share / route participation / target or carry share, historical efficiency, and the expected game script. The projection is converted to a threshold near the middle of the expected range, and the distribution matters — two players with the same mean can warrant different prices. The vig is then attached to both sides ([Prop Lab](https://proplabsports.com/learn/how-sportsbooks-set-prop-lines)).

Structural reasons props may be softer than game lines — treat each as a hypothesis your own CLV tracking must confirm:

- **Lower limits, later posts.** Books cap props lower and post them later because a single piece of information (an inactive teammate) can invalidate a number; relatively little money moves prop markets ([Prop Lab](https://proplabsports.com/learn/how-sportsbooks-set-prop-lines)).
- **Slower updates (vendor claim).** One odds-API vendor states books adjust prop prices **10–30 minutes slower** than game lines after news, and that teammate props (usage inheritors) lag the most ([TheOddsAPI](https://theoddsapi.com/guides/player-props)). Verify against your own timestamps before relying on it.
- **Line and price move independently.** A fixed 54.5 line can silently get more expensive: over -110 → -125 raises implied probability from 52.4% to 55.6% without the number moving ([Prop Lab](https://proplabsports.com/learn/how-sportsbooks-set-prop-lines)).
- **Cross-book disagreement.** One vendor treats a ~5-point (American odds) gap between a US book and a sharp baseline as an edge signal ([TheOddsAPI](https://theoddsapi.com/guides/player-props)) — a screening heuristic, not a validated threshold.

### 2.2 What this means strategically

Star main lines are commonly assumed to be the most efficient markets — treat that as a hypothesis, not a fact, and let your own CLV record tell you where prices are actually beatable. Candidate mechanisms worth researching first, each requiring your own validation:

1. **Speed on news** — practitioner guides report the first hour after injury news as the window where teammate props misprice role changes ([NBA Props Betting](https://nbapropsbetting.com/articles/nba-prop-betting-strategy/)). Test with logged CLV.
2. **Low-attention markets** — secondary players, combo stats, and alternates may get less book attention than main lines (hypothesis, not established fact).
3. **Structural modeling questions** — e.g., whether books systematically misprice MLB plate-appearance opportunity (Section 4). One practitioner guide claims they do ([Baseball Bet System](https://baseballbetsystem.com/articles/mlb-hits-runs-rbis-props/)); verify on your own data.
4. **Price shopping** — the same prop routinely varies across books; always compare prices before betting ([Betting News](https://www.bettingnews.com/sports-betting-guides/mlb-hitter-props/)).

---

## 3. The Universal Modeling Chain

Every sport's props reduce to the same causal chain. Model each stage, in order, and carry **uncertainty through every step** — opportunity uncertainty (will he play? how many minutes/PAs/targets?) usually dwarfs efficiency uncertainty (how well does he perform per opportunity?).

```
AVAILABILITY → OPPORTUNITY VOLUME → RATE/EFFICIENCY → STAT DISTRIBUTION → PRICE
```

### 3.1 Choose candidate distributions per stat — then let held-out fit decide

A projected mean does **not** identify a probability distribution — the same 60-yard projection could come from a steady volume receiver or a boom-bust deep threat with completely different tails. Treat the table below as candidates to test, selected by held-out calibration and tail performance, not as universal defaults:

| Distribution | Candidate for | Notes |
|---|---|---|
| **Normal** | High-volume, roughly symmetric continuous props | One guide uses it for 50+ expected yards or 15+ expected points ([The Prop Bettor's Edge](https://thepropbettorsedge.com/modules/selecting-distribution/sport-specific-guide)) — but check skew and tails; many "normal" props have fatter tails |
| **Poisson** | Low-volume counts with variance ≈ mean | Heuristic from one guide: VMR ≤ ~1.3 makes Poisson a candidate ([The Prop Bettor's Edge](https://thepropbettorsedge.com/modules/selecting-distribution/sport-specific-guide)) |
| **Negative binomial** | Overdispersed counts (VMR > ~1.3) | E.g., clustered outcomes like big-inning run production |
| **Binomial / Poisson-binomial** | Successes in a known number of trials | E.g., hits in N plate appearances, catches on N targets |
| **ZIP / hurdle** | Structural zeros within games where the bet has action | Active players whose opportunity may genuinely not occur (e.g., scripted out of the game plan). Note: a **scratch/DNP is a settlement void (stake refunded), not a statistical zero** — voids live in the settlement rules (Section 9), not in the outcome distribution |
| **Simulation** | Everything with dependent components | The general answer: simulate the opportunity chain and read the empirical distribution |

([The Prop Bettor's Edge](https://thepropbettorsedge.com/modules/selecting-distribution/sport-specific-guide), [Datafield textbook](https://datafield.dev/sports-betting-textbook/part-02/chapter-07/))

The canonical cautionary example is **MLB hits+runs+RBIs (HRR)**. One modeling guide reports that individual hits, runs, and RBIs each have a variance-to-mean ratio near 1.0 (Poisson-like), but their sum has a VMR of roughly **2.06** because the components are positively correlated (a home run contributes 3 HRR at once) — so a naive Poisson fit would overstate the probability of moderate totals and understate the tails ([Prediction Engine](https://predictionengine.app/learn/mlb-player-props-guide)). The specific ratios are that vendor's estimates — the principle (correlated components change the sum's distribution) is what generalizes. Note also that a pure Poisson model cannot have an arbitrary "standard-deviation floor" — that vendor applies the floor to the predictive distribution around its forecast (modeling model error), which is a reasonable calibration hack, not part of Poisson itself.

### 3.2 Regressor + distribution, not classifier

Build a model that predicts the stat value (e.g., 1.35 hits), then run it through the appropriate distribution to get P(over 0.5), P(over 1.5), etc. This gives magnitude information and prices every line and alternate from one coherent forecast ([Prediction Engine](https://predictionengine.app/learn/mlb-player-props-guide)). (A classifier can take the threshold as an input — classification isn't restricted to one line — but a continuous forecast plus distribution is usually more information-efficient.)

---

## 4. MLB: The Opportunity-Modeling Case

MLB is a strong structural candidate for the bettor because the single most important input — **expected plate appearances** — is both predictable and, per one practitioner guide, underweighted by the market ([Baseball Bet System](https://baseballbetsystem.com/articles/mlb-hits-runs-rbis-props/)). Whether that underweighting survives your own out-of-sample testing is the open question.

### 4.1 The hitter modeling chain

```
CONFIRMED LINEUP SLOT → EXPECTED PAs → HITS/PA RATE → DISTRIBUTION → PRICE
```

**Expected PAs — the claimed edge.** The same guide reports that books tend to price hitter lines as though every starter gets 4 PAs, while reality ranges from a road leadoff hitter in a 9.5-run-total game (5–6 PAs) to a home 8-hole hitter in a low-total game (often 3), and that a lineup-position error alone typically swings expected HRR by 0.5+ points ([Baseball Bet System](https://baseballbetsystem.com/articles/mlb-hits-runs-rbis-props/)). Related structural facts it cites: home teams skip the bottom of the ninth when ahead (worth ~30–40 PAs per season to a home leadoff hitter), and higher game totals mean more team PAs for everyone. Model expected PAs from lineup slot, home/road, and projected game total — then check whether the market already reflects it.

**The stat inputs per prop family:**

| Prop | Key inputs |
|---|---|
| **Hits (over 0.5/1.5)** | Expected PAs, contact quality (xBA, xwOBA from Statcast), pitcher's hard-contact allowed, handedness platoon split, batting slot |
| **HRR (over 1.5)** | All of the above plus lineup context — RBI chances depend on who bats ahead of you, run chances on who bats behind you; do **not** fit Poisson to the sum (see Section 3.1) |
| **Home runs / total bases** | Barrels, fly-ball rate, pitcher HR-allowed tendency, park factor, wind/temperature; plus-money markets because power is clustered |
| **Runs / RBIs** | The most lineup-dependent: model the teammates as much as the player |

([Betting News](https://www.bettingnews.com/sports-betting-guides/mlb-hitter-props/), [Prediction Engine](https://predictionengine.app/learn/mlb-player-props-guide))

**Context stack:** handedness/pitch mix (unreliable in small samples as standalone predictors), park and weather (dimensions, walls, altitude, wind, temperature affect carry), bullpen exposure (hitter props cover the whole game), and removal risk in blowouts ([Betting News](https://www.bettingnews.com/sports-betting-guides/mlb-hitter-props/)).

### 4.2 The pitcher modeling chain (previously omitted — this matters)

```
CONFIRMED STARTER → EXPECTED BATTERS FACED → K-RATE PER MATCHUP → DISTRIBUTION → PRICE
```

- **Strikeouts** are the flagship pitcher prop: model expected batters faced (a function of pitch count, effectiveness, and manager hooks), then a per-batter strikeout probability from the matchup — the pitcher's K rate blended with each opposing hitter's strikeout tendency, shrunk toward league average. Pitch-count/removal uncertainty is the dominant variance source, not K-rate.
- **Outs recorded** is driven by batters faced, but batters faced must be converted into outs: model each batter's on-base/out outcome (including double plays and other multi-out events), then layer removal uncertainty on top.
- **Hits/earned runs allowed** need batted-ball distribution, defense, and sequencing (clustered big innings make earned runs overdispersed).
- **Removal risk**: a starter exiting early hands the rest of the game to a known bullpen — which changes the matchup profile for batter props too.

The same guide cited above treats PA-opportunity mispricing as the core MLB inefficiency; the symmetric pitcher question — whether books underweight batters-faced uncertainty — is the natural companion research target.

### 4.3 A worked probability example (illustrative)

With a projected hits mean of λ = 1.35, the Poisson distribution gives: P(0 hits) = 25.9%, P(1) = 35.0%, P(2) = 23.6%, P(3+) = 15.5% — so **over 0.5 hits = 74.1%**, over 1.5 = 39.1% ([Prediction Engine](https://predictionengine.app/learn/mlb-player-props-guide); exact values 74.08% and 39.08%). At a hypothetical -145 price on over 0.5 hits, implied probability is 59.2%; your 74% estimate makes that +EV if your λ is right. That is exactly why the λ input (PAs, lineup slot, matchup) is where the research effort belongs — and why a hits-in-N-PAs binomial model with PA uncertainty is a cleaner formulation than raw Poisson.

### 4.4 About your over-0.5 hits/runs/RBIs success

Your experience is a legitimate candidate hypothesis, with one important refinement: distinguish **over 0.5 hits** (needs 1 hit; typically -140 to -180) from **over 0.5 combined HRR** (needs 1 of anything; typically much shorter odds) from separate run/RBI markets. The combined version wins very often — but high hit rate is not value: at a hypothetical -250 you need to win 71.4% just to break even. Past wins are evidence to test, not proof of edge — survivorship bias guarantees someone always has a hot streak (Section 12). What the research does support as a research direction: **PA-based hitter models are a transparent, testable starting point** for mispricing research ([Baseball Bet System](https://baseballbetsystem.com/articles/mlb-hits-runs-rbis-props/)) — whether plate appearances are actually underweighted at current books is precisely what your own testing must establish.

---

## 5. NBA: The Minutes-First Sport

### 5.1 The modeling chain

```
AVAILABILITY/ROTATION → MINUTES → TEAM POSSESSIONS → USAGE SHARE → STAT DISTRIBUTION → PRICE
```

Minutes are the biggest single lever, because they scale every counting stat ([OddsShopper](https://www.oddsshopper.com/articles/betting-101/how-to-make-your-own-nba-projections)). A complete published architecture for this exists and is worth studying as a template ([Datafield case study](https://datafield.dev/sports-betting-textbook/part-07/chapter-34/case-study-01.html)):

1. **Ingest game logs** with minutes, box stats, game pace, usage rate, team/opponent scores.
2. **Recency-weighted per-minute rates** via EWMA, blended with a league-average prior (Bayesian shrinkage) so small samples don't run the model. That case study used a 0.95 decay, a prior weight of 5, the last ~20 games, and a 3-game minimum — illustrative tuning choices, not professional standards.
3. **Minutes projection**: recency-weighted average adjusted for rest and blowout risk. That study's rest multipliers (0 days: ×0.96 … 3+: ×1.02) and blowout floor (×0.90) are illustrative; note its hard cap around 42 minutes would exclude regulation 44-minute and overtime outcomes — a real limitation. Better: model minutes as a distribution that conserves the team's total regulation minutes across players, with an overtime scenario branch.
4. **Contextual adjustments**: opponent defensive profile by position, pace, home/away, Vegas total and spread, missing-teammate usage, minutes boosts for injuries.
5. **Uncertainty quantification**: minutes uncertainty propagates into stat uncertainty, producing a mean and spread per stat — which is what prices the prop.

### 5.2 Stat-specific mechanisms (beyond points)

- **Rebounds**: model available rebounds (teammate + opponent miss rates, pace) × the player's rebound share, not raw per-game averages.
- **Assists**: potential assists (passes leading to shots) × teammate conversion; a playmaker's assist line moves with who finishes his passes, not just his volume.
- **Threes**: three-point attempts are the volume input; conversion is the rate — separate them.
- **Combo props (PRA, etc.)**: do not assume the sign of the dependence. \(\operatorname{Var}(P+R+A) = \operatorname{Var}(P)+\operatorname{Var}(R)+\operatorname{Var}(A) + 2\operatorname{Cov}(P,R)+2\operatorname{Cov}(P,A)+2\operatorname{Cov}(R,A)\) — the conditional covariances can be either sign depending on role and game flow. Estimate them from data or generate them through shared simulations; never just sum marginal variances.

### 5.3 The context stack that moves NBA lines

- **Usage in the night's actual lineup**, not season average. One guide treats a bump of 3+ percentage points from baseline as a meaningful signal ([NBA Props Betting](https://nbapropsbetting.com/articles/nba-prop-betting-strategy/)) — a heuristic to validate.
- **Pace**: that same guide treats ~8 possessions as a meaningful gap and 12 as substantial — but only bet it if the line hasn't already absorbed it; blowouts functionally slow even a 105-pace game ([NBA Props Betting](https://nbapropsbetting.com/articles/nba-prop-betting-strategy/)).
- **Efficiency**: true shooting, three-point volume, free-throw trips; usage without efficiency doesn't score points ([OddsShopper](https://www.oddsshopper.com/articles/betting-101/how-to-bet-nba-points-props)).
- **Injury inheritance**: when a primary scorer sits, check what the replacement inherits — shot attempts point to points props, playmaking to assists props ([OddsShopper](https://www.oddsshopper.com/articles/betting-101/how-to-bet-nba-points-props)).
- **Timing (practitioner claim)**: a late scratch within 2 hours of tip moves the line, and that guide reports the market is slowest on which teammate inherits the possessions, especially second-unit ball-handlers ([NBA Props Betting](https://nbapropsbetting.com/articles/nba-prop-betting-strategy/)). Verify with your own timestamped logs.
- **Distributions**: NBA star props are higher-volume than NFL, so symmetric distributions are a reasonable starting candidate; low-count stats (threes, blocks, steals) need count distributions or simulation ([The Prop Bettor's Edge](https://thepropbettorsedge.com/modules/selecting-distribution/sport-specific-guide)).
- **Guard against your own model**: blending your projection with the market (e.g., 50/50) is a common guardrail ([OddsShopper](https://www.oddsshopper.com/articles/betting-101/how-to-make-your-own-nba-projections)) — but note that averaging a projected mean with a book's line does not automatically produce a calibrated distribution; blend central estimates if you must, and derive alternate-line probabilities from a coherent distribution.

---

## 6. NFL: The Game-Script Sport

### 6.1 The modeling chain

```
GAME SCRIPT (SPREAD/TOTAL) → TEAM PLAYS → DROPBACKS/RUSHES → ROUTES/TARGETS/CARRIES → YARDS/TDs → PRICE
```

The NFL chain has one more layer than the others because team play volume and the pass/run split depend on the expected game flow. Note the distinction: **dropbacks** (pass plays including sacks and scrambles) are not the same as pass attempts — a sack or scramble is a dropback without an attempt. Model game script probabilistically (a distribution of leads/deficits across game states), not deterministically — being a 14-point underdog raises the probability of trailing-script outcomes; it does not mechanically dictate any one player's workload.

Simulation — not closed-form math — is the standard approach, because the dependencies are too tangled for a single distribution ([ATS Wins](https://atswins.ai/articles/recent-articles/nfl-player-prop-simulation-model/)):

1. Simulate team environment per trial: expected plays, pace, pass rate, game state.
2. Draw player participation: snaps, routes, targets, carries per projected role.
3. Allocate opportunities from team volume × role shares.
4. Convert opportunities to outcomes: targets → catches and yards (via catch rate, aDOT, YAC), carries → yards (YPC), red-zone work → TD probability.
5. Store every trial's stat line; that source recommends **10,000+ trials**; use shrinkage priors so small samples don't dominate ([ATS Wins](https://atswins.ai/articles/recent-articles/nfl-player-prop-simulation-model/)).

This chain is a **proposed modeling specification** — the inputs are the right ones to model, but no source demonstrates that any particular one is a proven edge against current prices.

### 6.2 The context stack

- **Spread = script prior**: a 14-point underdog's RB tends to lose rushing work (team abandons run); the favorite's RB tends to gain it (clock-killing); passing volume tends to flow to the trailing team ([Sports Betting Dime](https://www.sportsbettingdime.com/guides/how-to/nfl-player-prop-bets/)).
- **Total = environment**: that guide suggests avoiding over-piles in games with totals below 40 and under-piles when totals approach 60 ([Sports Betting Dime](https://www.sportsbettingdime.com/guides/how-to/nfl-player-prop-bets/)).
- **Usage metrics**: routes, route participation, target share, rush share, red-zone involvement — not season averages; check whether one huge game is inflating a player's average ([Sports Betting Dime](https://www.sportsbettingdime.com/guides/how-to/nfl-player-prop-bets/), [ATS Wins](https://atswins.ai/articles/recent-articles/nfl-player-prop-simulation-model/)).
- **Coverage matchup**: vs man coverage, identify which corner shadows which receiver; vs zone, target distribution changes ([Sports Betting Dime](https://www.sportsbettingdime.com/guides/how-to/nfl-player-prop-bets/)).
- **Weather**: wind and rain suppress completions and yards — the line often already reflects it, so check whether the move is complete ([Sports Betting Dime](https://www.sportsbettingdime.com/guides/how-to/nfl-player-prop-bets/)).
- **TDs are sparse**: model them as low-count outcomes from red-zone shares, not as "averages" ([The Prop Bettor's Edge](https://thepropbettorsedge.com/modules/selecting-distribution/sport-specific-guide)).
- **For your receiving-yards work** (nfeloapp.com): target share, air yards, and aDOT are the core inputs; yards props are high-volume, so a simulated mean + spread prices every alternate directly — but validate the tails, because receiving-yards distributions are typically right-skewed even at high volume ([NFL Player Betting](https://nflplayerbetting.com/articles/nfl-receiving-yards-over-under-tips/)).

---

## 7. Which Props Are "Easiest to Beat"?

Honest answer: **no comparative evidence establishes that one prop type is universally easiest to beat**, and any guide claiming otherwise is selling certainty the data doesn't have. What the research supports is a framework for ranking prop families per sport:

| Criterion | What to check |
|---|---|
| **Modelability** | Is the stat generated by a clean opportunity chain you can simulate? (MLB hits-in-N-PAs, NFL receptions: strong. NFL TDs: sparse. NBA steals: noisy) |
| **Input quality** | Are the inputs public, timestamped, and granular? (Statcast, nflverse, nba_api: yes) |
| **Market attention** | Main lines on stars are commonly assumed to be the sharpest; secondary players, combos, and alternates may get less book attention — verify empirically |
| **Uncertainty** | Opportunity uncertainty (minutes, PAs, snaps) is where books are plausibly slowest |
| **Liquidity/limits** | Low-limit markets move on little money — good if you're early, bad if you need size |
| **Demonstrated out-of-sample value** | Evaluate calibration, achievable-price returns, uncertainty, and CLV together on untouched or prospective data — CLV alone does not establish profitability (Section 12) |

**Best-supported research candidates (hypotheses to test, not established edges):**

- **MLB**: PA-driven markets (hits, HRR) for road/top-of-order hitters in high-total games — PA-based hitter models are a transparent starting point for testing, not evidence that current prices underweight plate appearances ([Baseball Bet System](https://baseballbetsystem.com/articles/mlb-hits-runs-rbis-props/)). Your over-0.5 family lives here.
- **NBA**: teammate-inheritance props after injury news ([NBA Props Betting](https://nbapropsbetting.com/articles/nba-prop-betting-strategy/)).
- **NFL**: receiving-volume props (receptions, receiving yards) driven by routes/target share — the most data-rich, most simulatable NFL markets ([The Prop Bettor's Edge](https://thepropbettorsedge.com/modules/selecting-distribution/sport-specific-guide), [ATS Wins](https://atswins.ai/articles/recent-articles/nfl-player-prop-simulation-model/)).

Also examine **unders** with the same rigor as overs. A public bias toward overs is widely asserted in betting commentary, but whether it produces +EV unders at current prices is an empirical question for your own data — price both sides of every market you model.

---

## 8. Alternate Lines and Parlays

### 8.1 Alternate lines: one distribution, many prices

Alternates are the same prop at shifted thresholds with shifted prices. The correct method: derive probabilities for **every** threshold from your single fitted distribution, then compare each to its own price. A hypothetical points menu (line 24.5), illustrating the shape: Over 19.5 at -220, 22.5 at -145, 24.5 at -110, 27.5 at +140, 29.5 at +195, 34.5 at +350, 39.5 at +600 ([Shurzy](https://www.shurzy.com/content/post/alternate-line-player-props-explained/)).

- +200 implies 33.3%; if you project 30+ points at 42%, over 29.5 at +200 is +EV.
- **Fat-tail players** (boom/bust receivers, high-variance scorers) are the classic alternate-over candidates: the guide's example prices over 34.5 at +350 (implied 22.2%) against an estimated true ~30% ([Shurzy](https://www.shurzy.com/content/post/alternate-line-player-props-explained/)).
- **Lower alternates are traps at heavy juice**: 70% at -220 is roughly break-even; at a true 68% it loses money. The main line can be fairly priced while a specific alternate is mispriced — in either direction ([Shurzy](https://www.shurzy.com/content/post/alternate-line-player-props-explained/)).

### 8.2 Same-game parlays: correlation repricing plus margin

SGPs are priced by: pricing each leg independently, detecting correlated legs, adjusting the price for that correlation, and adding margin on top ([Land Your Bets](https://landyourbets.com/how-same-game-parlays-work)). Two things must be kept separate:

1. **The correlation adjustment is legitimate repricing, not a tax.** Positively correlated legs should pay less than an independent multiplication implies. Example from the guide: two 50% legs priced independently → 25% joint, fair +300; if the true joint probability is 35%, the fair price is \(1/0.35 = 2.857\), roughly **+186**. If the book offers only **+150** (break-even 40%), the bet has \(0.35 \times 2.5 - 1 = -12.5\%\) EV: the correlation adjustment was fair, the price was not. The question is never whether correlation was priced; it is whether the book's correlation estimate and margin leave a gap you can beat ([Land Your Bets](https://landyourbets.com/how-same-game-parlays-work)).
2. **The extra margin on top is the tax.** The guide calls SGP pricing a "double tax" — correlation adjustment plus additional juice ([Land Your Bets](https://landyourbets.com/how-same-game-parlays-work)). A real example: Kyler Murray TD (+140) + Cardinals team total over 29.5 (-120) would pay +340 if independent; DraftKings' SGP price was +300 ([The Lines](https://www.thelines.com/betting/guides/same-game-parlay/)). Note that the payout change alone cannot tell you how much of that gap is fair correlation repricing versus extra margin — separating them requires your own joint estimate.

For context on parlay economics generally: Nevada books held **30.95% of parlay dollars 1992–2020** (vs ~5% on straight football) and **56.3% in October 2021** ([The Lines](https://www.thelines.com/betting/guides/same-game-parlay/)) — parlay-wide realized holds, not SGP-specific margins, but a measure of how expensive the parlay product is.

**The only SGP test that matters** (assuming all legs have action and no void/repricing occurs — actual evaluation must follow the book's void-leg rules):

\[
EV_{\text{parlay}} = P(\text{all legs win}) \times D_{\text{quoted}} - 1
\]

Estimate the joint probability from a shared simulation of the game scenario (never by multiplying marginal probabilities unless independence is justified), and compare it to the quoted payout. SGP edges exist only where your joint estimate beats the book's price — an advanced, research-gated use case.

### 8.3 Multi-game parlays (your Friday slate use case)

(Section 16 expands all of this into a full parlay-engineering framework — when stacking compounds your edge, when it compounds your losses, and how to size it.)

Legs from different games are approximately independent, so a multi-game parlay's EV is approximately (again assuming all legs have action):

\[
EV_{\text{parlay}} = \prod_i (p_i D_i) - 1
\]

Because edges multiply, one strongly +EV leg can mathematically outweigh a slightly -EV leg — but "every leg must be +EV standalone" is the right screening policy, because it keeps you from rationalizing weak legs. The failure mode to internalize — high hit rates with negative EV: six legs each at -250 with a true 70% win probability hit \(0.7^6 = 11.76\%\) of the time; the multiplied payout is \(1.4^6 = 7.53\), so EV is \(0.1176 \times 7.53 - 1 = -11.4\%\). You will hit these parlays more often than you'd think and still lose money on them. Rule: **only parlay legs your model independently prices as +EV, and always evaluate the joint probability against the actual quoted payout.**

---

## 9. Settlement Rules (Read Before Betting)

From DraftKings' current official sport rules (rules vary by book and jurisdiction — check each book's house rules for your state):

| Sport | Official DraftKings rule (current) |
|---|---|
| **NBA** | "Participation in a Game shall mean the player entering the Game according to the Game's official box score." No minimum minutes. Additionally, pre-halftime NBA player-stat bets (excluding Unders and already-decided bets) are **voided if the player doesn't participate in the 2nd half due to injury or illness** (with source confirmation within 2 hours). |
| **NFL** | "Participation shall mean playing in at least one play in the applicable Event." Pre-halftime full-game player-stat bets (excluding Unders and decided bets) are voided if the player doesn't participate in the 2nd half due to injury/illness. |
| **MLB** | Participation = throwing at least one pitch (pitchers) or recording at least one plate appearance (position players). Crucially: **pre-game single-game player props are void if the player does not START the game** — a substitute appearance doesn't count. Starting-pitcher props settled on full-game statistics are voided (except Unders, X-or-Fewer markets, live bets, and already-decided bets) if the pitcher throws at least one pitch and leaves for any reason or no reason before recording five batters faced. |

([DraftKings basketball rules](https://sportsbook.draftkings.com/help/sport-rules/basketball), [DraftKings football rules](https://sportsbook.draftkings.com/help/sport-rules/football), [DraftKings baseball rules](https://sportsbook.draftkings.com/help/sport-rules/baseball); cross-reference summary: [Action Network](https://www.actionnetwork.com/education/prop-betting-rules-what-happens-if-player-doesnt-play))

Practical implications: the DK in-game-injury void for pre-halftime overs materially changes the tail risk of over bets; the MLB must-start rule means a "questionable" starter who appears only as a late substitute voids the bet (no loss) at DK — but a different book's rules may differ. **Settlement rules are part of EV**: a market with a void rule on bad outcomes is worth slightly more than one without.

---

## 10. Data Source Inventory

### 10.1 Official results and player data (free)

| Source | Provides | Timing / limits |
|---|---|---|
| [nflverse / nflreadr](https://nflreadr.nflverse.com/articles/nflverse_data_schedule.html) | NFL play-by-play, rosters, snap counts, weekly NGS, injuries | Per its update-schedule doc: PBP raw within ~15 min post-game, cleanest data Thursday, injuries daily 7AM UTC during the season. **Current-season availability of the injury table and other specific datasets is unverified here — confirm in the docs before relying on it** |
| [Baseball Savant / Statcast](https://baseballsavant.mlb.com/) | Pitch- and batted-ball-level data: xBA, xwOBA, exit velo, spin, sprint speed | Statcast back to 2015; no key required |
| [MLB Stats API](https://statsapi.mlb.com/api/v1/teams) | Schedules, rosters, live pitch-by-pitch game feeds | Undocumented endpoints; no key |
| pybaseball (Baseball-Reference, FanGraphs) | Deep historical batting/pitching stats | FanGraphs actively blocks scripts (HTTP 403), per the [MLB data inventory](https://mlbanalytic.com/articles/free-public-baseball-data-sources-ranked.html) |
| nba_api (stats.nba.com) | NBA box scores, play-by-play, tracking, hustle stats | Aggressive undocumented rate limits — cache everything, per the [NBA data inventory](https://nbaanalytic.com/articles/free-basketball-data-sources-ranked.html) |
| Basketball-Reference | Advanced metrics, pbp, transactions | No official API; rate-limited, per the same inventory |
| pbpstats | NBA lineup, on/off, possession data | Per the [NBA data inventory](https://nbaanalytic.com/articles/free-basketball-data-sources-ranked.html), narrower scope than nba_api |
| hoopR | NBA and college play-by-play via R packages | R-only ecosystem, per the same inventory |
| [FTN Network](https://ftnfantasy.com/) | Proprietary NFL charting, DVOA, betting tools | Paid |

### 10.2 Participation, injuries, lineups

NFL practice reports and game-status designations drive late line movement ([Prop Lab](https://proplabsports.com/learn/how-sportsbooks-set-prop-lines)); current-season nflverse injury availability is unverified here (check its docs); MLB confirmed lineups post day-of (check the day-of lineup, not yesterday's slot); NBA injury reports have their own cadence — the final report before tip is what moves numbers.

### 10.3 Odds services (the critical piece)

| Source | Provides | Notes |
|---|---|---|
| [The Odds API (the-odds-api.com)](https://the-odds-api.com/) | Live odds, 100+ sports, 100+ books; player props for selected US sports; historical snapshots dating back to 2020 (per its homepage; coverage varies by market — verify prop-market depth) | $30–$249/mo tiers include historical odds, per its site |
| [TheOddsAPI (theoddsapi.com)](https://theoddsapi.com/) | Live props across ~50 books for NBA/NHL/MLB/WNBA + NFL in season; historical archive | Props on Business plan ($99/mo); its guides are the source of the 10–30 min lag and 500-markets-per-night claims |
| [OpticOdds](https://opticodds.com/sports-betting-api) | Per the vendor's site: real-time odds from 200+ sportsbooks, player props, alternate markets, injury data, and [historical odds](https://opticodds.com/historical-odds) ([developer docs](https://developer.opticodds.com/docs/odds-api-getting-started-guide)) | You already have an OpticOdds connection — read its current prop/historical coverage for your sports directly in the docs before building |
| [OddsPapi](https://oddspapi.io/blog/backtest-betting-model-free-historical-odds/) | Historical timestamped odds snapshots (350+ books) | Free tier 250 req/month; verify prop-market (vs match-odds) coverage before relying on it |

**The honest limitation:** this report does not include an empirical backtest. Historical results alone cannot prove a betting strategy was profitable anyway — you need timestamped odds (what price was available when you would have bet) and as-of injury information. Whether you already possess usable historical data (archived lines, nfeloapp exports, etc.) is unknown to this report; if you do, a backtest becomes possible immediately; if not, prospective paper tracking starts today (Section 12).

---

## 11. The AI System: Researcher vs. Probability Engine

The single most important architectural decision: **separate the LLM's job from the model's job.**

### 11.1 The AI researcher (LLM) does:
- Retrieve and structure context: injury reports, confirmed lineups, beat-writer news, weather, coaching tendencies.
- Resolve player identities and extract structured facts **with provenance and timestamps** — every extracted fact links to its source URL.
- Flag what changed since the lines were posted (so you don't double-count news the books already priced).
- Explain model outputs in plain language.
- **Never invent an adjustment.** Missing information stays "unknown" — the model treats it as uncertainty, not as zero.

### 11.2 The probability engine (reproducible code) does:
- Distribution fitting, Monte Carlo simulation, devig, EV, Kelly sizing — all in auditable code, not LLM arithmetic.
- Maintains two model variants: an **independent model** (built purely from player/team data) and a **market-informed blend** (your central estimate averaged with the devigged market line, e.g., 50/50) — the blend is a guardrail against your own model's blind spots ([OddsShopper](https://www.oddsshopper.com/articles/betting-101/how-to-make-your-own-nba-projections)), with the caveat from Section 5.3 that blending means doesn't fix calibration.
- Benchmarks both against the market itself: the no-vig closing line is the comparison benchmark — persistent outperformance of it is the standard (though not conclusive) evidence that a model adds information.

### 11.2.1 The companion implementation

This guide ships with a working implementation of the probability engine (`prop-engine/`): odds conversions, all three devig methods, the distribution library (Poisson, binomial, normal, negative binomial), EV (standard, settlement-aware, boosted), parlay and pick'em pricing, fractional Kelly with a cap, and a bet log that settles picks by outcome and house rules, records closing prices separately as CLV diagnostics, and reports ROI, calibration bins, and Brier score. Its test suite asserts selected arithmetic examples and known mathematical cases (independent oracles where possible) — run it before trusting any output. It computes what happens if your probabilities are right; producing those probabilities remains your job and the AI researcher's.

### 11.3 Why this split matters

A systematic review of 219 studies (2010–July 2024) on machine learning in sports betting found prediction performance alone does not demonstrate profitability, and that data quality, real-time decision-making, and the inherent unpredictability of sports remain the core challenges ([Tajeuna et al., arXiv:2410.21484](https://arxiv.org/abs/2410.21484)). One experiment reported by the review (Walsh & Joshi, 2024) found that **optimizing a predictive model for calibration, rather than accuracy, led to significantly higher betting profits in that experiment** ([arXiv:2410.21484](https://arxiv.org/pdf/2410.21484)) — suggestive, not a general rule. Still, calibration of probabilities — not picks — is the core discipline.

### 11.4 The daily workflow

**Morning (or day before):**
1. Pull slate, odds across books, and all games' base context.
2. Run the probability engine on every market; devig a sharp book as benchmark.
3. Compute EV for every prop, main line and alternates; log candidates.

**Lineup/news watch (the active window):**
4. Monitor injury reports and confirmed lineups (MLB day-of; NFL practice reports; NBA final injury report).
5. On news: re-run the engine with updated availability; compare against prices that haven't moved yet.

**Final check:**
6. Re-devig; confirm the price still beats your probability after the move; line-shop for the best available number ([Betting News](https://www.bettingnews.com/sports-betting-guides/mlb-hitter-props/)).
7. Size with fractional Kelly; log the bet with timestamps and the closing line.

**Single game vs. multi-game slate — where they actually differ:**

- **Single game**: all your bets share one game's scenario distribution — a wrong game-script read loses them together. Model one shared simulation and read every bet from it; concentrate stakes only in the strongest 1–2 edges; cap total exposure to the single game.
- **Multi-game slate (your Friday case)**: legs are near-independent across games, so variance per dollar is lower — but execution complexity is higher: staggered start times mean lineup confirmations arrive on different schedules; re-run the model per game as its news lands; re-check stale prices before the later games; and never let the slate's "fun" framing justify parlays that fail the Section 8 EV test. A big slate lowers variance; it does not create edge by itself.

---

## 12. Validation: The Gatekeeper

### 12.1 Backtesting rules

- **Select bets using information and executable prices available at your actual decision time** (for most strategies, that's the price you could have bet at decision time — not opening odds unless you actually bet at the open).
- **Calculate returns using the price actually taken**, the outcome, and applicable settlement/void rules.
- **Use closing prices separately, as a CLV diagnostic** — not for settlement.
- **Chronological structure**: train and calibrate on earlier data, test on untouched later data, then paper-trade prospectively.
- **Evaluate the selected betting policy** (which bets your system actually places, at what size), not just predictions for all players.
- **No fixed sample size establishes significance** — it depends on effect size, prices, dependence, and selection bias. Note also that multiple props from one game are not independent observations. One odds-data vendor recommends 300–500 bets as a practical minimum for basic signal detection ([OddsPapi](https://oddspapi.io/blog/backtest-betting-model-free-historical-odds/)) — a rule of thumb, not a statistical guarantee.

### 12.2 ROI volatility and the biases that fake edges

- At 2.00 odds, ROI standard deviation is roughly 16 points over 40 bets, ~5 over 400, ~1.6 over 4,000 — a hot month proves nothing ([Clawarbs](https://clawarbs.com/blog/why-betting-backtests-lie/)).
- Beware: overfitting via many filters (removing past losers by chance), survivorship bias, cherry-picked windows, multiple-comparisons (test enough rules and some will look great), and prices you couldn't actually get ([Clawarbs](https://clawarbs.com/blog/why-betting-backtests-lie/)).

### 12.3 Calibration

- Group predictions into probability bins and check observed frequency vs predicted (reliability curve; ideal is y = x) ([Sports-AI.dev](https://www.sports-ai.dev/blog/ai-model-calibration-brier-score)).
- Track Brier score: average squared difference between predicted probability and outcome; a coin-flip model scores 0.25 on 50/50s ([Sports-AI.dev](https://www.sports-ai.dev/blog/ai-model-calibration-brier-score)).
- Recalibrate with Platt scaling (fast, may underfit) or isotonic regression (flexible, may overfit small samples) ([Sports-AI.dev](https://www.sports-ai.dev/blog/ai-model-calibration-brier-score)).

### 12.4 Closing line value (CLV)

CLV is the standard diagnostic for market-beating: record the price you took and the closing price for the same market; compare against the **no-vig** close. Track the pattern over a large logged sample — you can be 3-7 in a fortnight on well-priced bets and 7-3 on badly priced ones, so short runs of results prove nothing in either direction ([BestNFLPlayerPropBets](https://bestnflplayerpropbets.com/articles/nfl-prop-closing-line-value/)). Two cautions: CLV is a diagnostic, not proof (pair it with actual ROI over a large logged sample), and neither direction is logically conclusive — negative CLV on a sample doesn't rule out positive EV any more than positive CLV guarantees it.

### 12.5 Bankroll sizing

Full Kelly: stake fraction = \((bp - q)/b\). Example: +120 odds, break-even 45.45%, your estimate 50% → full Kelly 8.33% of bankroll. **Use fractional Kelly** (½ = 4.17%, ¼ = 2.08%) because your probability estimates are uncertain, and full Kelly assumes they're perfect ([Circa Sports](https://www.circasports.com/blog/kelly-criterion-for-sports-betting-explained)). Many prop bettors additionally cap individual props at 0.5–1% of bankroll regardless of Kelly output — label which rule wins when they conflict.

---

## 13. The Output Schema (What Every Projection Should Contain)

| Field | Example |
|---|---|
| Player / prop / line | Jalen Brunson, points, 26.5 |
| Book / price / **odds timestamp** | DraftKings, -118, 2026-10-23T18:32Z |
| Devigged market probability | 54.2% (reference-book quote available at decision time, 18:30Z) — an estimate, not truth; record the actual closing benchmark separately afterward for CLV |
| Model probability | 61.0% (independent) / 57.5% (market blend) |
| Uncertainty | SD of probability estimate; minutes/PA uncertainty flag |
| EV | At -118 (decimal 1.8475) with 57.5%: \(0.575 \times 1.8475 - 1 = +6.2\%\) |
| Kelly stake | Full Kelly \(= (0.8475 \times 0.575 - 0.425)/0.8475 = 7.4\%\); quarter Kelly **1.8%**, or the 1% bankroll cap if it applies — state which |
| Evidence | Injury report (URL, timestamp), confirmed lineup, pace/spread/total inputs |
| Invalidation conditions | "Bet void if Brunson inactive (DK: must appear in box score); re-run if a high-usage teammate's status changes" |
| Decision | BET / PASS |

Every logged bet then accumulates into the CLV, calibration, and ROI record from Section 12.

---

## 14. What This Research Could Not Verify

- **This report does not include an empirical backtest.** Whether you already hold usable historical data (archived odds with timestamps, as-of injury info) is unknown; if you do, a valid backtest is possible; if not, prospective paper tracking starts now.
- No source provides evidence that any specific prop type has a demonstrated, repeatable edge across bettors — including over-0.5 MLB combos. The mechanisms (opportunity inputs, news lag) are plausible and worth testing; the profitability claims require your own logged, as-of record.
- Book SGP correlation models are proprietary; any SGP edge claim rests on your own simulation being better, unverified until logged.
- Parlay-wide historical holds (30%+ in Nevada) are the best available proxy for SGP economics; SGP-specific margins aren't separately published ([The Lines](https://www.thelines.com/betting/guides/same-game-parlay/)).
- Distribution guidance (VMR thresholds, HRR variance ratios, Poisson floors) comes from practitioner guides, not peer-reviewed validation — treat as starting points to fit and test on held-out data.

---

## 15. The Complete System in One Paragraph

Model **opportunity before performance** in every sport — MLB plate appearances by lineup slot (and batters faced for pitchers), NBA minutes by rotation, NFL targets by a probabilistic game script. Fit the stat's distribution by held-out fit and calibration — symmetric distributions for high-volume stats, count distributions for low-volume ones, simulation for anything with dependent components, never a naive Poisson on correlated combos like HRR. Devig a sharp book to estimate the market's fair probability, and only bet where your calibrated probability beats the best executable price after vig — EV is \(p \times D - 1\) against the price you can actually get. Test the proposed mispricing hypotheses with logged CLV: slow teammate-prop updates after injury news, PA opportunity in MLB, alternates on fat-tail players. Treat alternates as one distribution tested against many prices, and parlays (multi-game or SGP) as EV-gated constructions evaluated jointly against the quoted payout. Size with fractional Kelly under an explicit per-bet cap, log every bet with its odds timestamp and closing line, and let calibration + CLV + a large logged ROI sample — not any hot streak, including past over-0.5 success — decide whether the system is real. When there's no edge, **pass** — on most nights, for most props, passing is the winning play.

---

## 16. Parlay Engineering: Stacking as a Tool, Not a Trap

This chapter repairs an imbalance in the first draft. Parlays are not automatically bad — and your instinct is mathematically correct in one important way: **when every leg is +EV and the ticket is priced multiplicatively across independent outcomes, a parlay has higher EV per dollar than the singles, because edges multiply.** The catch is that the same multiplication compounds losses, and variance explodes. The parlay format is an amplifier of leg quality — nothing more, nothing less.

### 16.1 The core math: edges multiply

Under independence, no voids, and a quoted payout equal to the product of the leg prices — a condition to verify per ticket, not assume — the parlay EV is:

\[
EV_{\text{parlay}} = \prod_i (p_i D_i) - 1
\]

**Hypothetical worked example (code-verified, illustrative only):** four legs, each with a true 55% win probability priced at -110 (implied 52.4% — a +5.0% edge per leg). Same $100 total budget:

| Construction | Hit profile | EV per $100 | Character |
|---|---|---:|---|
| Four $25 singles | 39.1% of nights profitable; 75.9% of nights finish at -$5 or better | +$5.00 | Grinds |
| Six 2-leg parlays (round robin, ~$16.70 each) | 30.25% per ticket | +$10.25 | Middle variance |
| One $100 four-leg parlay | 9.15% of nights | +$21.55 | Lottery-plus |

The four-leg parlay has **4.3x the EV** of the singles strategy on the same budget — purely from multiplying four +5% edges. That is the quantitative version of "parlays increase payout," and it is correct.

### 16.2 The two-sided blade

The same multiplication runs in reverse with no edge. Same four legs but true probability 52% (no edge at -110):

- Four singles: **-$0.73** per $100.
- One four-leg parlay: **-$2.88** per $100 — nearly 4x worse.

And a leg with negative EV reduces the ticket's expected-return multiplier (its \(p_iD_i\) is below 1), though it does not necessarily flip the whole ticket negative. Practitioner guidance is blunt on this: never add legs or alternate lines just to inflate payout; a heavy favorite adds losing risk while contributing little to the payout ([OddsShopper](https://www.oddsshopper.com/articles/betting-101/why-you-cant-win-parlays)). **Rule (screening policy): a leg may enter a parlay only if you would bet it as a single at that price.**

### 16.3 What theory actually says about optimal parlaying

Two results from the optimization literature are directly useful — both are mathematical results under stated assumptions (independent events, known-or-estimated probabilities, specific payout structures), not evidence that any real-world betting policy is optimal or profitable. The first is a theoretical preprint. Treat both as structure, not gospel:

- **The optimal ticket book is the outer product of single-event strategies.** Recent work on optimal parlay wagering under Kelly growth shows the optimal set of tickets factorizes into one-event solutions, and a leg is active in a parlay if and only if it is active on its own — an optimal parlay never contains a leg you would not bet singly ([arXiv:2603.26620](https://arxiv.org/pdf/2603.26620)).
- **For Kelly bettors, multibetting simultaneous games replicates sequential singles.** Research on simultaneous-game betting finds that for a Kelly (log-utility) bettor, betting parlays across simultaneous games produces the same monetary outcome as betting the games sequentially would; with multiplicative payouts books take a higher percentage on multibets, so the right choice depends on your objective, and you should hold off combining only if you expect prices to improve closer to game time ([Decision Analysis, INFORMS](https://pubsonline.informs.org/doi/10.1287/deca.1080.0106)).

Translated: **if your legs are +EV and priced multiplicatively, parlaying them is theoretically sound; the discipline is entirely in leg quality and stake size.**

### 16.4 The four objectives — compare constructions on all of them

\[
\operatorname{Var}(R) = D^2 q(1-q)
\]

where \(q\) is the ticket's joint win probability and \(D\) its decimal payout. **Exact enumeration of the same hypothetical night** (all figures code-verified in the companion script `parlay-math/parlay_comparison.py`):

| Winning legs | P | Four $25 singles | Six 2-leg parlays (~$16.70 each) | One $100 four-leg parlay |
|---:|---:|---:|---:|---:|
| 0 | 4.10% | -$100.00 | -$100.00 | -$100.00 |
| 1 | 20.05% | -$52.27 | -$100.00 | -$100.00 |
| 2 | 36.75% | -$4.55 | -$39.26 | -$100.00 |
| 3 | 29.95% | +$43.18 | +$82.23 | -$100.00 |
| 4 | 9.15% | +$90.91 | +$264.46 | +$1,228.33 |
| **Expected profit** | | **+$5.00** | **+$10.25** | **+$21.55** |
| **P(profitable night)** | | **39.1%** | **39.1%** | **9.15%** |

Read the last two rows together — this is the whole parlay trade-off in one table: **larger expected profit and larger payouts coexist with far fewer profitable nights.** And the variance does not average out quickly: repeating the four-leg ticket for 100 nights with this same +21.55% edge, the probability you are cumulatively **down money** after 100 tickets is about **29.5%** (you need 8+ wins; each win nets +$1,228 vs -$100 per miss). A parlay bettor with a genuine edge will routinely look and feel like a losing bettor for months at a time. That is not a reason to avoid parlays — it is the reason stake sizing (Section 16.5) is non-negotiable.

### 16.5 Sizing and overlapping exposure

- **Size parlays by fractional Kelly on the joint probability, under your per-bet cap.** The Kelly fraction for a 9% probability, 13.3x payout ticket is far smaller than for any single leg. If the cap says 0.5–1% of bankroll, it applies to the ticket, not to each leg's notional.
- **Watch shared legs across tickets.** A round robin of six 2-leg combos from four selections means each player appears in three tickets — one bad read on one player loses three tickets at once. Round robins redistribute exposure; they do not fix mispriced selections, and an "anchor" player repeated in every combination is a single point of failure.
- **Assess the portfolio, not tickets.** Independently applying standalone Kelly stakes to overlapping tickets can overallocate bankroll — evaluate their shared outcomes jointly rather than simply adding individual allocations. Simulate the slate's shared outcomes and cap total exposure to any one game, one team, or one night. Treat the per-ticket fractional-Kelly rule above as a sizing heuristic subject to this portfolio check.

### 16.6 Sport-specific stacking mechanisms

How legs connect differs by sport — these are modeling relationships to estimate, not proven edges:

**MLB — same-team hitters are genuinely correlated, through opportunity.** Team plate appearances create chances for the whole stack; runners on base multiply RBI opportunities for hitters behind them; traffic chases the starter and exposes weaker relievers; a big inning bats around and clusters opportunities in adjacent lineup spots ([Stokastic MLB stacking guide](https://www.stokastic.com/articles/mlb-dfs/mlb-dfs-stacking)). A stack of 1-2-3 hitters in a high-total game shares a favorable scenario. The dependencies run through base-state transitions and lineup sequencing: runners on base create RBI chances for the next hitters, and a big inning can bat around and extend itself — there is no fixed pool of outcomes to divide. Note that this stacking logic comes from DFS, where top-heavy prize structures reward correlated upside; a sportsbook may already charge for that same dependence in an SGP price. A successful DFS stacking mechanism is not evidence of an underpriced parlay.

**NFL — QB-WR stacking changes the shape, not the mean.** A secondary analysis of fantasy-point outcomes over ten seasons (2016-2025): stacked QB+WR pairs produced the same average combined fantasy output as unstacked pairs, but with weekly scoring correlations of **0.265-0.345** (effectively zero when unstacked), standard deviations **12-18% higher**, 50+ point boom weeks **59-90% more frequent**, and double-bust weeks **30-50% more frequent** ([Edgeline FF](https://edgelineff.com/insights/mythbusters-qb-pass-catcher-stacking)). Important caveat: fantasy-point correlation is not the joint probability that two specific sportsbook thresholds clear, so these figures cannot directly price an SGP — they establish the direction and rough magnitude of the dependence. Whether stacking helps depends entirely on whether the SGP price already charges for that correlation (Section 8.2).

**NBA — teammate correlation runs through possessions and is partially zero-sum.** Teammates share team possessions (positive: more team possessions helps everyone), but shot distribution within a possession is zero-sum (negative: one player's volume is taken from another), assists require a teammate's made shot (positive), and injury reallocation moves usage in chunks. Estimate the sign per pair and per game script; do not assume (Section 5.2).

**Cross-game vs same-game — the pricing difference that matters most.** Cross-game parlays are typically priced multiplicatively, so the compounding of 16.1 applies most cleanly there — but verify the quote: a book can still shade a cross-game parlay price, and different games do not guarantee product pricing or true independence. Outcomes across games may be approximately independent while your **model errors remain shared** — one flawed assumption (e.g., a mis-set pace or usage baseline) can run through every leg of a multi-game ticket. SGPs carry correlation penalties plus extra margin (Section 8.2). Practical hierarchy: cross-game stacks of individually +EV legs are the theoretically cleanest construction; same-game stacking is a separate, harder problem requiring your own joint simulation.

### 16.7 Boosts, insurance, and cash-out — the promo layer

- **Profit boosts.** A fractional profit boost \(b\) changes decimal odds to \(D_{\text{boosted}} = 1 + (1+b)(D-1)\). DraftKings' example: a 25% boost on a -115 bet moves the break-even probability from 53.5% to 47.9% ([DraftKings support](https://support.draftkings.com/dk/en/how-do-i-apply-a-boost?id=kb_article_view&sysparm_article=KB0010436)). A boost is +EV only if the boosted break-even is below your true probability — it does not make the bet more likely to win ([OddsShopper](https://www.oddsshopper.com/articles/betting-101/odds-boosts-strategy)). Illustration: a three-leg parlay at +1,400 breaks even at 6.7%; a 30% boost to +1,820 lowers break-even to 5.2% — if your true rate is 6%, the boost flips the ticket from -EV to +EV ([OddsShopper](https://www.oddsshopper.com/articles/betting-101/odds-boosts-strategy)). Boost terms to check: caps, minimum legs, eligible markets, expiration, one boost per slip, boost not returned on cash-out but returned on void ([DraftKings](https://support.draftkings.com/dk/en/how-do-i-apply-a-boost?id=kb_article_view&sysparm_article=KB0010436)).
- **Cash-out.** Cash-out offers are priced with a bookmaker margin and are linked to the already-margined in-play price, so routinely accepting them reduces expected returns; a fair cash-out offer is EV-neutral by construction, and offers are typically below fair value ([Whelan, Economics of Betting Markets lecture notes](https://www.karlwhelan.com/Teaching/BettingMarkets/15.InplayandCashout.pdf)). Evaluate each offer as a new bet: if the offered price beats your updated probability's fair value, take it; otherwise hold. Hedging is the same math done manually.
- **Parlay insurance / bonus refunds.** Verify the actual promotion terms before valuing them: whether refunds come as cash or bonus bets (bonus bets return only the profit, not the stake, on a win — a materially worse refund), the qualifying conditions, and the void-leg rules that apply (Section 9). The official boost page fetched for this report did not establish insurance conditions, so treat any refund value as unverified until read from the specific promotion's terms.

### 16.8 The parlay decision tree

```
1. Select players by conditions (Section 17)          → candidates
2. Price each single vs the best available line      → keep only +EV legs
3. Estimate joint probabilities:
   - cross-game: independence (or near it)           → multiply
   - same-game: shared simulation                    → never multiply marginals
4. Compare candidate tickets: EV, P(profit), drawdown — same total stake
5. Apply fractional Kelly per ticket under the cap; cap slate-wide exposure
6. Log everything (odds timestamp, closing line)      → Section 12
```

### 16.9 Pick'em apps: Pick6, PrizePicks, Underdog

Pick'em apps are parlays with fixed payout structures: you pick more/less against a posted projection line, and the payout schedule depends on the entry type and size — there are no odds to devig, so the analysis flips from "remove the vig" to "compare your joint probability to the payout." Three distinct entry types need separate math: **fixed all-correct entries** (e.g., PrizePicks Power Play) pay multiplier \(M\) for every leg correct; **flex entries** pay reduced amounts for partial misses (price by enumerating the full outcome distribution); and **peer-to-peer entries** (e.g., DraftKings Pick6) guarantee a Base Payout with uncertain Extra Winnings on top — model the base as the floor and treat extras as unpriced upside, never as expected value you can count on ([DraftKings Pick6](https://pick6.draftkings.com/pick6-prizes)).

**The math.** If the multiplier \(M\) is the total payout (including stake — verify per app; the official pages do not state this), the entry EV is:

\[
EV = P(\text{all correct}) \times M - 1, \qquad \text{per-leg break-even} = M^{-1/n}
\]

**PrizePicks Power Play** (every pick must hit; multipliers from the official site): 2 picks = 3x, 3 = 6x, 4 = 10x, 5 = 20x, 6 = 37.5x ([PrizePicks](https://www.prizepicks.com/ways-to-pick)). That implies equal-probability per-leg break-evens of **57.7%, 55.0%, 56.2%, 54.9%, 54.7%** respectively ([OddsPapi](https://oddspapi.io/blog/prizepicks-api-odds-access/)) — equivalent to roughly **-121 to -137** per leg depending on entry size. Note this \(M^{-1/n}\) is the break-even for legs of *equal* probability; it is not a separate requirement that every unequal-probability leg must clear. The comparison that matters: **the app's structure demands a larger per-leg edge than a -110 sportsbook prop (52.4% break-even)**. **DraftKings Pick6** is peer-to-peer: a 3-pick entry has a minimum Base Payout of 6x, with Extra Winnings on top depending on how other entries fare (a 4/4 example paid 18x total on the entry) ([DraftKings Pick6](https://pick6.draftkings.com/pick6-prizes)). **Flex Play** variants pay reduced amounts for partial misses (e.g., 2 of 3 returns 1x; 3 of 5 returns 0.4x) ([PrizePicks](https://www.prizepicks.com/ways-to-pick)) — priced by the same enumeration logic as the round robin in 16.4, so evaluate them with the full outcome distribution, not the headline multiplier.

**What this changes strategically.**

1. **Your required edge per leg is bigger, but the lines may be softer.** A PrizePicks leg needs ~55-58% to break even versus ~52.4% at -110 — but the app's pricing structure does not move with betting money the way a sportsbook price does: per OddsPapi's analysis, the effective per-leg price for a two-pick 3x entry stays fixed at 1.73 (= √3) while the projection line itself can move — equivalent pricing varies by entry size, per the break-even table above ([OddsPapi](https://oddspapi.io/blog/prizepicks-api-odds-access/)). Whether softer lines, promotions, payout variants, or peer-to-peer extras outweigh the higher break-even is an empirical question for your own logs — do not assume any single factor decides it.
2. **The six-leg example from 8.3 is literally a pick'em entry.** Six legs each at a true 55%: the app pays 37.5x for 6/6, so EV = \(0.55^6 \times 37.5 - 1 = +3.8\%\). For comparison, the same six legs at -110 sportsbook odds pay \(1.909^6 = 48.4\)x total — EV \(= 0.0277 \times 48.4 - 1 = +34\%\) at the same true probabilities. so when -110 pricing is actually available, **the sportsbook parlay pricing beats the fixed multiplier**; the pick'em app's candidate advantages are its less market-responsive lines, promotions, and payout variants — each of which changes this comparison and must be checked, not assumed. Same rule as 16.2: never include a leg you would not take at the implied per-leg price.
3. **Correlation still applies.** Same-game legs in one entry share the game scenario (Section 16.6) — estimate the joint probability from shared simulation, never by multiplying marginals, and check the app's rules on same-game entries.
4. **Void and settlement rules differ from sportsbooks** (e.g., how a postponed game or "no action" line is handled) — read the app's specific rules before evaluating EV, just as in Section 9.

The tool that accompanies this guide (Section 11's probability engine) computes pick'em EV, per-leg break-evens, and flex-play enumerations alongside standard sportsbook pricing.

---

## 17. Form, Streaks, and Judgment: The Human Layer

You are right that real-world mechanisms matter — and the resolution is not to abandon probability, but to use it properly: **conditional probability is how real-world understanding becomes an auditable forecast.** It does not claim to eliminate uncertainty; it expresses uncertainty about mechanisms' effects. "Picking a player when he hits" is a claim about observable pregame conditions; this chapter makes that claim testable.

### 17.1 Three different things hiding inside "form"

Do not collapse these — they have different evidence and different modeling treatments:

1. **Observable state changes** — role, workload, lineup slot, health, matchup, coverage, environment, rest. These are the bread and butter of Sections 4-6: model them directly as inputs.
2. **Latent form** — changes in shooting stroke, bat speed, velocity, mechanics, or fatigue that box scores do not fully capture. Candidate features: treat as inputs to test, never as vibes.
3. **Outcome streaks** — recent hits and misses. Contains some information, some randomness, and a well-documented bias risk. Requires the most care.

### 17.2 What the science actually says about streaks

The story is genuinely two-sided, and both sides matter:

- **The original finding (1985):** Gilovich, Vallone, and Tversky's canonical study concluded the hot hand was an illusion — people saw patterns in randomness.
- **The correction (2018):** Miller and Sanjurjo discovered a subtle selection bias in the standard test — when you select observations by streaks, the expected continuation rate is mathematically lower than the unconditional rate even for a fair coin. Correcting for this bias **reverses the canonical study's conclusions**: the data are consistent with a real, modest hot hand ([Miller & Sanjurjo, Econometrica 2018](https://arxiv.org/abs/1902.01265)). So "the hot hand is a myth" is simply not a settled fact.
- **Experts can exploit it (in some settings):** re-analyzing the data from the original hot-hand field study, researchers found that experienced practitioners' bets predicted future outcomes — the first evidence that people can profitably exploit hot-hand beliefs in that setting ([A Visible (Hot) Hand?, OSF preprint](https://ideas.repec.org/p/osf/osfxxx/sd32u.html)). Caveat: this reanalysis provides evidence from one field-study betting setting; it does not demonstrate profitability on sportsbook player props.

### 17.3 But the market layer changes everything

A real performance effect is not a betting edge if the price already reflects it — and the market evidence is sobering:

- **MLB (2010-2021, 25,000+ games):** three-game streaks strongly shaped which teams the market favored (56.9% vs 48.3% favorite rates for streak vs non-streak teams), but the pricing itself was remarkably accurate: streak teams' implied win probabilities aligned closely with realized win rates (51.8% implied vs 51.7% actual at open — a +0.1-point overvaluation, far smaller than the vig), and the authors conclude the market is "quite accurate at pricing momentum effects, even in opening lines" ([Harvard working paper](https://dash.harvard.edu/server/api/core/bitstreams/81e73570-084b-4e39-84d3-ccb4649c61ab/content)). The paper separately documents favorite-longshot bias in opening moneylines that largely closes by game time — a different finding from streak pricing.
- **Soccer betting stakes (612 Bundesliga matches):** bettors' relative stakes on a team rose in the minute after it scored an equalizer (47.0% vs 37.2% of stakes — a 9.8-percentage-point raw difference, about 26% relative; the authors' regression estimate is significant at the 1% level), while the authors detected **no predictive momentum effect on outcomes** — they conclude bettors clearly believe in momentum ([Gambling on Momentum, arXiv:2211.06052](https://arxiv.org/pdf/2211.06052)). The public bets streaks; in this sample no predictive momentum value was detected at those prices.

Net: the hot-hand correction says the effect can be real; the market studies above (team-level MLB and soccer samples — not player props specifically) found prices that were already accurate or stakes that outran value. These do not prove player-prop markets price form perfectly — they mean the burden of proof is on your measurement. Your edge cannot be "he is hot, bet him." Your edge must be in **measuring the effect better than the price**: distinguishing which streaks come with an observable cause (role change, lineup move, matchup) and which are noise.

### 17.4 Encoding judgment as testable features

Every "eye test" call becomes a structured, timestamped feature with provenance:

| Vague intuition | Testable feature |
|---|---|
| "He's hot right now" | Last-7 and last-15 game rates vs season baseline, with rest/role context flags |
| "He's due for a bigger role" | Lineup slot change, snap/route share trend, teammate absence (with dates) |
| "Great matchup tonight" | Opponent allowed-rate by position, handedness/pitch-mix flags, coverage type |
| "He always shows up here" | Situational dummy (primetime, division, revenge) — tested, kept only if it survives |

The model then answers the only question that matters: **which pregame conditions change this player's outcome distribution, and does the offered price reflect the change?** Features that improve out-of-sample calibration stay; features that do not are dropped. This is how your judgment gets stronger every week instead of just more confident.

### 17.5 The prospective A/B/C test for human judgment

Run three versions of your system forward and let the logs decide:

- **A — Baseline model** (Sections 4-6).
- **B — Baseline + structured context features** (17.4).
- **C — Baseline + timestamped overrides**: before lines are checked, record your (or the AI's) call to move a player up or down — with the reason, direction, magnitude, and the information you had at that moment.

Log every override including the passes and the misses — memorable correct calls are exactly how survivorship bias fakes expertise. Evaluate all three versions on the full set: calibration, achievable-price returns, uncertainty, and drawdown, with CLV as a diagnostic (Section 12). If C beats A and B on that full set over a large sample, your judgment has measurable value and deserves a larger role. If it does not, you will have found that out for the price of paper bets instead of real ones. **Either result is a win for the method.**

### 17.6 What not to do

- Do not bet a player purely because he performed yesterday — the market knows, and recency-driven pricing is documented ([Harvard MLB study](https://dash.harvard.edu/server/api/core/bitstreams/81e73570-084b-4e39-84d3-ccb4649c61ab/content)).
- Do not avoid a player purely because he missed yesterday — the same math runs in reverse.
- Do not let a hot streak of your own bets raise your stakes — raise them only when calibration and CLV say your probabilities are genuinely better than the market's.

---

## Sources

**Odds providers & market mechanics**
- [The Odds API (the-odds-api.com)](https://the-odds-api.com/) — pricing, historical snapshots to 2020, market coverage
- [TheOddsAPI — Player Props & Edge Detection](https://theoddsapi.com/guides/player-props)
- [TheOddsAPI — Betting Markets List](https://the-odds-api.com/sports-odds-data/betting-markets.html)
- [OpticOdds — Sports Betting API](https://opticodds.com/sports-betting-api), [Historical Odds](https://opticodds.com/historical-odds), [Developer docs](https://developer.opticodds.com/docs/odds-api-getting-started-guide)
- [Prop Lab — How Sportsbooks Set Prop Lines](https://proplabsports.com/learn/how-sportsbooks-set-prop-lines)
- [OddsPapi — No-Vig Odds Methods](https://oddspapi.io/blog/no-vig-odds-api/)
- [OddsPapi — Backtesting With Historical Odds](https://oddspapi.io/blog/backtest-betting-model-free-historical-odds/)

**Methodology & modeling**
- [OddsShopper — Make Your Own NBA Projections](https://www.oddsshopper.com/articles/betting-101/how-to-make-your-own-nba-projections)
- [OddsShopper — NBA Points Props](https://www.oddsshopper.com/articles/betting-101/how-to-bet-nba-points-props)
- [Datafield — NBA Player Prop Projection System Case Study](https://datafield.dev/sports-betting-textbook/part-07/chapter-34/case-study-01.html)
- [Datafield — Probability Distributions in Betting](https://datafield.dev/sports-betting-textbook/part-02/chapter-07/)
- [Baseball Bet System — MLB HRR Props Modeling](https://baseballbetsystem.com/articles/mlb-hits-runs-rbis-props/)
- [Prediction Engine — MLB Player Props Guide](https://predictionengine.app/learn/mlb-player-props-guide)
- [The Prop Bettor's Edge — Sport-Specific Distribution Guide](https://thepropbettorsedge.com/modules/selecting-distribution/sport-specific-guide)
- [NBA Props Betting — Pace, Usage, Line Movement](https://nbapropsbetting.com/articles/nba-prop-betting-strategy/)
- [ATS Wins — NFL Player Prop Simulation Model](https://atswins.ai/articles/recent-articles/nfl-player-prop-simulation-model/)
- [Sports Betting Dime — NFL Player Prop Strategy](https://www.sportsbettingdime.com/guides/how-to/nfl-player-prop-bets/)
- [NFL Player Betting — Receiving Yards Props](https://nflplayerbetting.com/articles/nfl-receiving-yards-over-under-tips/)

**Parlays, alternates, settlement**
- [Land Your Bets — How Same-Game Parlays Work](https://landyourbets.com/how-same-game-parlays-work)
- [The Lines — Same Game Parlay Guide](https://www.thelines.com/betting/guides/same-game-parlay/)
- [Shurzy — Alternate Line Player Props](https://www.shurzy.com/content/post/alternate-line-player-props-explained/)
- [DraftKings — Basketball Rules](https://sportsbook.draftkings.com/help/sport-rules/basketball)
- [DraftKings — Football Rules](https://sportsbook.draftkings.com/help/sport-rules/football)
- [DraftKings — Baseball Rules](https://sportsbook.draftkings.com/help/sport-rules/baseball)
- [Action Network — Prop Settlement Rules](https://www.actionnetwork.com/education/prop-betting-rules-what-happens-if-player-doesnt-play)

**Validation & bankroll**
- [Clawarbs — Why Betting Backtests Lie](https://clawarbs.com/blog/why-betting-backtests-lie/)
- [Sports-AI.dev — Model Calibration & Brier Score](https://www.sports-ai.dev/blog/ai-model-calibration-brier-score)
- [Circa Sports — Kelly Criterion](https://www.circasports.com/blog/kelly-criterion-for-sports-betting-explained)
- [BestNFLPlayerPropBets — Closing Line Value on NFL Props](https://bestnflplayerpropbets.com/articles/nfl-prop-closing-line-value/)
- [Tajeuna et al. — A Systematic Review of Machine Learning in Sports Betting, arXiv:2410.21484](https://arxiv.org/abs/2410.21484)

**Data sources**
- [nflreadr — nflverse Data Schedule](https://nflreadr.nflverse.com/articles/nflverse_data_schedule.html)
- [MLBAnalytic — Free Baseball Data Sources](https://mlbanalytic.com/articles/free-public-baseball-data-sources-ranked.html)
- [NBAAnalytic — Free Basketball Data Sources](https://nbaanalytic.com/articles/free-basketball-data-sources-ranked.html)
- [FTN Fantasy](https://ftnfantasy.com/)
- [Betting News — MLB Hitter Props](https://www.bettingnews.com/sports-betting-guides/mlb-hitter-props/)

**Parlays, stacking, form & judgment (Part 2)**
- [Miller & Sanjurjo — Surprised by the Hot Hand Fallacy? A Truth in the Law of Small Numbers, Econometrica 2018 / arXiv:1902.01265](https://arxiv.org/abs/1902.01265)
- [A Visible (Hot) Hand? Expert Players Bet on the Hot Hand and Win — OSF preprint](https://ideas.repec.org/p/osf/osfxxx/sd32u.html)
- [Gambling on Momentum — arXiv:2211.06052](https://arxiv.org/pdf/2211.06052)
- [Uncovering Behavioral Biases in MLB Betting Markets — Harvard working paper](https://dash.harvard.edu/server/api/core/bitstreams/81e73570-084b-4e39-84d3-ccb4649c61ab/content)
- [Optimal Parlay Wagering and Whitrow Asymptotics — arXiv:2603.26620](https://arxiv.org/pdf/2603.26620)
- [Optimal Betting Strategies for Simultaneous Games — Decision Analysis (INFORMS)](https://pubsonline.informs.org/doi/10.1287/deca.1080.0106)
- [OddsShopper — Why You Can't Win Parlays (And How To Win Them)](https://www.oddsshopper.com/articles/betting-101/why-you-cant-win-parlays)
- [OddsShopper — Odds Boosts Strategy](https://www.oddsshopper.com/articles/betting-101/odds-boosts-strategy)
- [DraftKings — How do I apply a boost?](https://support.draftkings.com/dk/en/how-do-i-apply-a-boost?id=kb_article_view&sysparm_article=KB0010436)
- [Whelan — In-Play and Cash-Out economics (lecture notes)](https://www.karlwhelan.com/Teaching/BettingMarkets/15.InplayandCashout.pdf)
- [Edgeline FF — QB/Pass-Catcher Stacking: 10 Years of Data](https://edgelineff.com/insights/mythbusters-qb-pass-catcher-stacking)
- [Stokastic — MLB DFS Stacking](https://www.stokastic.com/articles/mlb-dfs/mlb-dfs-stacking)
- [PrizePicks — Ways to Pick (payout tables)](https://www.prizepicks.com/ways-to-pick)
- [DraftKings Pick6 — Prizes](https://pick6.draftkings.com/pick6-prizes)
- [OddsPapi — PrizePicks API & leg pricing](https://oddspapi.io/blog/prizepicks-api-odds-access/)
