---
tags: [slate, template]
date: 
sports: []
games: 
slate_class: 
first_start_et: 
last_start_et: 
bankroll: 100
slate_cap_pct: 
bets: 0
paper: 0
passes: 0
exposure_pct: 0
reviewer_incidents: 0
status: pending
---

# {{date}} — {{slate name}}

## 0. Classify ([[Slate Playbook]])
- Games: __ → class **micro / small / medium / large** → slate cap __%, per-game cap 3%
- Start windows: __ (separate slips per window; re-size after early settles)
- Day type: early season / back-to-back night / national TV / weather game / holiday

## 1. Facts ([[Researcher Prompt]] → reviewer)
- Researcher JSON pasted / linked:
- Reviewer incidents: __ (any > 0 → fix before pricing)
- Mechanisms to price (vacated minutes/usage/targets, script):

## 2. Market read
- Spread/total open → current per game (snapshot timestamps)
- Sharp reference available? (FanDuel / Caesars / Pinnacle / Circa / exchange): yes/no per market

## 3. Pricing (code, not vibes)
| # | Pick | Book (executable?) | Price | p_model | p_market (method) | Shrunk edge | Stake % | corr_group | Decision |
|---|---|---|---:|---:|---:|---:|---:|---|---|
|  |  |  |  |  |  |  |  |  |  |

## 4. Exposure check ([[Rules]] §2)
- Per game ≤ 3% · per player ≤ 1.5–2% · slate ≤ cap · ≤ 2 straights per game · no singles + SGP of the same legs

## 5. Pick'em / exchange
- Break-even from the **displayed** multiplier; exchange = ask + live fee; DNP rule noted
- 1-game slate: deliberate script stack or skip

## 6. Log before start (`odds_ts ≤ logged_at ≤ start`)
- One note per bet in `Record/Bets/` from [[_Bet Template]]; passes logged too

## Post-game
- [ ] Settle with both closing sides + timestamps
- [ ] CLV vs devigged close, skill vs close
- [ ] Review → [[Review Template]]; market lessons → [[Market Intel]]
