---
tags: [system, workflow]
---

# Daily Workflow

The chain, every slate, no shortcuts: **classify → facts → mechanism → price → pass**. All numbers (caps, thresholds, blend) live in [[Rules]] — that file wins any conflict.

## 0. Classify the slate — [[Slate Playbook]]
- Count games and start windows → micro / small / medium / large → slate cap. Decide *when* each edge type gets bet (projection vs opener = early; pick'em vs sharp = late; news = immediately).

## 1. Morning — context sweep (AI researcher's job, via [[Researcher Prompt]] + reviewer)
- Pull the slate, injuries, lineups (30-45 min before tip/kick for NBA/NFL finals).
- Check the market: open → current line moves, ticket splits. Reverse line movement is a **hypothesis to test** against your CLV record, not a proven signal — see [[Market Intel]].
- Weather for outdoor games (zero adjustment if it's clean — don't weather-hedge).
- Read news for *mechanisms*, not takes: who inherits vacated volume, which backup draws the mismatch.

## 2. Model — price every market from one distribution
- Game script is probabilistic, never one scenario.
- Opportunity before performance: plays → dropbacks/routes/carries → player volume.
- Distribution per stat: normal for yards/volume stats, count distributions (Poisson/NB) for receptions/TDs, **never Poisson on correlated combos** (HRR: negative binomial, VMR ~2).
- Run the [[Math Engine]]: devig a sharp two-way price → market fair; your model → your fair; blend **means, not probabilities**, at market weight 0.7–0.8 ([[Rules]] §7).

## 3. Decide — the pass discipline
- EV = p × D − 1 at the best executable price. **Line-shop across books** (the 2026-10-22 slate: SGA +102 → -111 within an hour).
- Apply the [[Rules]] §3 pass rule: executable price, shrunk edge ≥ 3 pts, beats the sharp devig, no small-sample/affiliate thesis, no unquoted parlays.
- Sizing and caps per [[Rules]] §1–2: 1% unit, 3% per game, slate cap by class. (Replaces the old "2% cap / 5-10% nightly".)

## 4. Log — before the games start
- Every decision: `bet_log.py add ... --decision bet|paper|pass` with odds timestamp.
- No bet is real until it's logged.

## 5. Settle — after the games end
- Settle with closing prices (`--close-odds`, `--close-odds-opp`, `--close-line`, `--close-ts`).
- Run `bet_log.py report`: ROI (paper and live separately), both CLV diagnostics, calibration bins, Brier.
- Fill the [[Review Template]] for the slate note. Update [[Market Intel]] with what the line moves taught you.

## Pass
The default output. A 16-game NFL week: hundreds of markets, expect **0-2 clear +EV spots per slate**. Forcing picks is manufacturing -EV bets.
