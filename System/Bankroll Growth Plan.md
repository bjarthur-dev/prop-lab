---
tags: [system, bankroll, plan]
updated: 2026-10-26
source: "Deep research 2026-10-26 (promos, alt lines, SGPs, Pick6, Kelly) — see chat report"
---

# Bankroll Growth Plan ($30, DraftKings + Pick6)

Goal: grow as fast as the math allows without likely going broke. Realistic month: median ~$38–45 from $30; doubling needs luck, not a method.

## Ranked methods (best first)
1. **No-sweat tokens / profit boosts.** Each $5 token is worth ~$2.20–2.75 in expected cash when placed on a single at **+200 to +400** that is fair or better vs other books (EV = S·[(p·D − 1) + (1 − p)·0.70]). Four tokens ≈ **+$9–11**. One token per independent event; never two on correlated outcomes. Check each token's eligible market and max refund first.
2. **Bonus-bet refunds:** use within 7 days, **unhedged**, on fair-or-better singles at **+300 to +500** (~70–75% conversion). Bonus stake isn't returned on a win.
3. **Price-edge singles** (`engine/edge_scan.py`): DK beats the sharp books' fair odds by ≥ 2% and the all-book consensus by ≥ 0. $1 each (cap $1.50), max 3/day, open exposure ≤ 25% of bankroll.
4. **Pick6 2–3 pick entries** only when every leg's sharp-implied chance at the Pick6 line is ≥ 59–60% (≥ 0.58/m for a leg with multiplier m). Discounted 0.5–0.8x legs almost never qualify.
5. **Alt-line rungs** only with ≥ 8–10% modeled EV from a per-player distribution fitted to the sharp main line; $0.25–0.50.
6. **2-leg parlays of qualifying legs** in different games, $1, or to meet a boost's leg requirement. Never unboosted same-game parlays; never 4+ legs.

## Avoid
Discounted Pick6 H+R+RBI stacks, unboosted SGPs, 4+ leg parlays, hedging bonus bets, chasing losses, betting above ~2x Kelly.

## Daily automation
- Afternoon card runs `edge_scan.py`: **price-edge legs**, a best 2-leg slip, and **no-sweat token candidates** (+150..+450, fair or better, with token EV).
- MLB days: an on-demand `mlbprops` odds snapshot (~6 credits per game) adds batter RBI / runs / TB / HR / H+R+RBI markets for token hunting.
- Late update re-checks prices before first pitch/tip.

## Track (proof it works)
CLV vs the closing sharp price on every bet (primary), realized vs expected ROI by method, token/bonus conversion, drawdown, any DraftKings limit or promo change (winning scan bettors can get limited).
