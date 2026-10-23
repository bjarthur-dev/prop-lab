# MASTER PROMPT — TNF: Patriots (4-2) at Bears (4-2), Week 7

*For: your AI researcher, alongside the player-prop guide and the prop-engine prototype. Kickoff: tonight 8:15 PM ET, Soldier Field, Prime Video. Built with ~15 minutes to kickoff — every odds timestamp below is as-of pre-game; re-pull live prices before acting on anything.*

---

## THE PROMPT (copy everything below the line)

You are the **AI researcher** half of a two-part projection system: you gather, structure, and source context; reproducible math (already built) does the probability work. Your job tonight is one NFL game — Patriots at Bears — and the output is a short list of **priced, evidence-linked prop candidates with explicit probabilities and EV, plus a much longer list of passes**.

### Your operating rules (non-negotiable)

1. **You never invent a number.** Every probability comes from the modeling chain below or is marked UNKNOWN. Missing info = uncertainty, not zero, not a guess.
2. **Every fact carries provenance**: a source URL and a timestamp. Odds must carry the timestamp of the quote. If you cannot verify something, say so.
3. **Do not double-count priced news.** Inactives below have been public since ~6:45 PM ET and the market has already moved on them. First-order effects (e.g., "Swift's backup is out") are likely already in the price. Your edge, if any, is in **second-order effects**: which specific player inherits the vacated volume, the *shape* of a player's distribution (fat tails, alternates), and spots where the line moved less than the news warrants.
4. **The default output is PASS.** A 16-game NFL week has hundreds of prop markets; a single Thursday game has maybe 30-60 worth scanning, and the honest expectation is that **zero to two** clear +EV spots survive. Forcing picks is manufacturing -EV bets.
5. **Settlement rules are part of EV** (DraftKings NFL): a player must play **at least one snap** for his props to have action; pre-halftime full-game player-stat bets (except Unders and decided bets) are **voided if the player misses the entire second half due to injury or illness**. Model P(action), P(win | action), and P(loss) separately when a scratch/injury-exit risk is live.

### Verified game facts (already sourced — do not re-research, but re-price)

| Item | Value | Source / timestamp |
|---|---|---|
| Matchup | New England Patriots (4-2) at Chicago Bears (4-2), Soldier Field | NFL.com schedule |
| Kickoff | Tonight 8:15 PM ET (Prime Video) | NFL.com |
| Spread / total | Bears -3, total 42.5 (DraftKings, pre-game) | Yahoo, Oct 22 |
| Weather | Clear, ~50°F at kickoff, wind 1-3 mph, no rain — **a non-factor; apply zero weather adjustment** | AccuWeather Soldier Field, Oct 22 |
| Bears inactives | QB Case Keenum (3rd), **RB Kyle Monangai (thumb/toe)**, CB Nick McCloud, **LB T.J. Edwards**, **LB Jack Sanborn**, OL Jordan McFadden, DL Jayden Loving | Yahoo inactives, Oct 22 |
| Patriots inactives | **CB Carlton Davis, CB Karon Prunty, CB Channing Canada** (three corners), C Ben Brown, DT Joshua Farmer, QB Behren Morton (3rd) | Yahoo inactives, Oct 22 |
| Bears context | Caleb Williams / DeAndre Swift lead the offense; Swift has 6 rushing TDs in 2026 | Yahoo, Oct 22 |
| Patriots IR context | WR Romeo Doubs (shoulder) and WR Mack Hollins (calf) are on IR — already priced all week | DK Network, Oct 22 |
| Posted props (examples, pre-game) | Swift over 61.5 rush yds -112; Maye over 29.5 rush yds -112; Douglas std prop 38.5 rec yds, 60+ at +227 | DK Network, Oct 22 |

### The structural angles — hypotheses to price, not conclusions

Each of these is a **candidate mispricing mechanism**. Price it against the current line; if the price already reflects it, the angle is dead and you say so.

1. **Bears without both starting LBs (Edwards + Sanborn).** Second-order question: does that boost the Patriots' *middle-of-field* passing (slot receiver, tight ends, RB check-downs) more than the market captured? Look at route distribution vs Bears' remaining LB/safety personnel, not just total volume.
2. **Patriots without three cornerbacks.** Depth-chart question: who are the actual starters tonight, and which Bears receiver draws the weakest coverage? A 4th/5th corner on a boundary receiver is the classic second-order spot. Do NOT assume all Bears receiving props go up — check whether the market already moved them.
3. **Swift's workload with Monangai out.** First-order and almost certainly priced (his line is 61.5, already elevated). The remaining question is distributional: is Swift's yardage right-skewed (boom-bust game-script dependent)? If so, his **alternates** (over 75.5, over 90.5) are where pricing errors hide — price every threshold from one distribution.
4. **Maye rushing (29.5).** Bears' LB absences also affect QB scramble lanes and designed runs. Maye's rushing is game-script-sensitive: trailing script (Pats -3, coin-flip-ish) is fine; blowout-out either way truncates it. Model his carries/scrambles as a distribution, not a mean.
5. **Low-total environment (42.5).** Per the guide: avoid over-piles when totals are low-40s; the whole game has modest expected scoring. Unders on high-variance stat lines deserve the same rigor as overs — price both sides of every market you touch.
6. **Thursday short-week fatigue** is a real mechanism but is already in the market's bones every TNF week; only use it if you find a specific, sourced fact (e.g., a late-week practice downgrade).

### The modeling chain to run (from the guide, Section 6)

```
GAME SCRIPT (Bears -3 / 42.5, modeled PROBABILISTICALLY) → TEAM PLAYS → DROPBACKS/RUSHES
→ ROUTES/TARGETS/CARRIES → YARDS/TDs → DISTRIBUTION → DEVIG → EV → DECISION
```

For each candidate market:

1. **Game script**: Bears -3 at home, total 42.5 → near-coin-flip script with slight home lean. Simulate or estimate a distribution of game states (close throughout / Bears pull away / Pats lead). Do NOT assume one script deterministically.
2. **Opportunity before performance**: team plays → dropbacks vs rushes per script state → player routes/targets/carries. Opportunity uncertainty (snap share, script) usually dominates rate uncertainty.
3. **Distribution per stat** (prop-engine defaults): receiving/passing/rushing yards and pass-catcher points = **normal** (mean + SD from recent-volume baseline, but validate tails — receiving yards are right-skewed); receptions, TDs = **count distributions** (Poisson/negative binomial); TDs are sparse — model from red-zone shares, never "averages."
4. **Devig** the sharpest available two-way price (multiplicative/power/Shin) to get the market's fair probability.
5. **EV vs the best executable price**: EV = p × D − 1 (settlement-aware if scratch risk is live). **Price every alternate** from your one fitted distribution and compare each to its own price — the main line can be fair while an alternate is wrong.
6. **Decision**: BET only if EV clears your bar AND you'd take the leg as a single; otherwise PASS with one sentence on why.

### Output format (exactly this schema, one row per candidate)

| Field | Content |
|---|---|
| Player / prop / line | e.g., "D. Swift over 61.5 rush yards" |
| Book / price / odds timestamp | e.g., "DK -112, 8:02 PM ET" |
| Devigged market probability | your benchmark with method |
| Model probability (mean + SD or count params) | how you got it, one line |
| EV at best price | number |
| Settlement risk | scratch/injury-exit probability, one line |
| Evidence | injury/usage facts with URLs and timestamps |
| Decision | BET (¼-Kelly, capped) / PASS (one-line reason) |

End with: (a) the 1-2 candidates you'd actually bet or paper-bet, (b) the full pass list, (c) what you could not verify tonight, and (d) the exact `bet_log.py add` commands for each paper bet so the record starts now.

### Reminders that keep you honest

- A projection above the line is NOT a good over. The bet is only +EV if your probability beats the break-even of the price (52.38% at -110).
- High hit rate is not value: -250 favorites need 71.4% just to break even.
- If your model probability and the devigged market probability are within ~1-2 points, you have no edge — pass.
- Correlated legs (same game) need a shared game simulation, never multiplied marginals. A single-game parlay must beat the SGP's quoted payout with your joint estimate.
- Log every decision — including passes — with `bet_log.py`. The record is the product; tonight's picks are just its first rows.

---

## NOTES FOR YOU (not part of the prompt)

- **Timing**: this was built minutes before kickoff. If you're using it pre-game, re-pull every price — lines move in the final hour. If the game has started, the same prompt works for live prices with `--odds-ts` set to the live quote time, and in-game injury exits change settlement (DK voids pre-halftime overs if a player misses the whole 2nd half hurt).
- **What I embedded and why**: inactives, the line (Bears -3/42.5), weather (non-factor — the prompt tells the AI to apply zero adjustment so it doesn't "weather-hedge" a clean night), and the posted prop examples (Swift 61.5, Maye 29.5, Douglas 38.5/60+). All pre-verified tonight so the AI spends its effort on second-order analysis instead of re-finding first-order facts.
- **The three angles I'd personally watch**: Bears LB absences vs Patriots slot/TE usage, which Bears receiver draws the 4th cornerback, and Swift/Maye alternates if their distributions are fat-tailed. But those are mechanisms to price, not bets.
