---
date: 2026-10-23
sport: MLB
game_id: "TB@MIL 2026-10-23 WS G1"
start_et: "20:00"
slate_class: large
player: Jacob Misiorowski
market: pitcher_strikeouts
line: 6.5
selection: under
book: FanDuel
executable: true
quoted: true
odds: 104
odds_ts: "2026-10-23T13:37:53-04:00"
logged_at: "2026-10-23T15:20:00-04:00"
minutes_to_start: 280
decision: watch
stake_pct: 0
p_model: 0.561
p_market: 0.470
p_market_method: "Pinnacle 6.5 o-125/u+103 multiplicative devig (13:38 feed, 10:58 quote)"
market_source: Pinnacle
p_blend: 0.493
break_even: 0.490
shrunk_edge_pts: 2.8
dist: "sim: BF ~ N(20.5, 3.5) x Binomial(BF, Beta(p=0.306, n=300))"
mu: 6.27
sd_or_vmr: ""
corr_group: "WS-G1"
reason_code: postseason_leash
dnp_rule: void
model_version: k_model_v0
run_id: "2026-10-23-claude-1520"
verified: true
close_odds: 104
close_odds_opp: -132
close_line: 6.5
close_ts: "2026-10-23T19:57:32-04:00"
clv_pct: -4.6
result: win
pnl_units: 0
actual: 3
settled_at: "2026-10-24T08:32:00-04:00"
settle_sources: "MLB statsapi (data/results/mlb/2026-10-23.csv: 3 K, 15 outs, 78 pitches); Fox Sports/AP recap (5 IP, 4 H, 1 R, season-low 3 K)"
---

# Misiorowski under 6.5 K (WATCH, reclassified from PAPER at 17:40 ET)

**Mechanism (sourced):** K% 37.9 over 665 BF in the regular season, but 29.7% over 37 BF in the postseason, at 91 pitches a start (94, 88) and 19/18 BF (MLB Stats API, ESPN game logs, via [[2026-10-23 B slate]] and [[2026-10-23 C board]]). The Rays strike out only 19.1% vs RHP (MLB Stats API). Roof closed. Model: talent K% shrunk to 34.8%, log5 vs the Rays → 30.6% per BF, BF 20.5 ± 3.5 (between the postseason leash and the market's 16.5-outs line) → mean 6.27 K.

**Why PAPER, not BET:**
- **[[Rules]] §3:** model beats sharp devig by +9.1 pts ✅, but shrunk edge is **2.8 < 3** ❌.
- **The edge depends on modeling choices.** With no talent shrinkage (37.9%), the mean rises to ~6.8 and the edge mostly disappears. A long leash (22 BF) does the same. This is a test of the leash + shrink hypothesis, not a confident edge.

**Also blended:** p_blend 0.493 at market weight 0.75 is only +0.3 pts over break-even (0.490). The [[Rules]] §7 blend also says no real bet, which agrees with PAPER.

**Reviewer issues:** price is from 13:37 ET; re-check at Job D. Lineups not posted.

**Reclassified 17:40 ET → WATCH (stake 0).** Rules v2 (added 15:40, after this was logged) requires the blend to beat break-even by ≥ 2 pts: 0.75×47.0 + 0.25×56.1 = 49.3% vs 49.0% is **+0.3**, and the shrunk edge is **2.8 < 3**. It fails twice. It's still tracked at the logged price and close for CLV.

**Sensitivity found by research ([[Research - Advanced NFL and MLB mechanisms]]):**
- v0 omitted American Family Field's K factor (~+12%, secondary source). At half weight, P(under) drops to ~49.6%, close to Pinnacle's 47.0%.
- A pitch-budget hook (88±10 pitches at his postseason 4.8 P/PA) pushes it back up to 61–67%.
- So the whole disagreement is **one assumption: does the short postseason leash persist?** He has also had a playoff whiff collapse (37.3% → 22.3%; four-seamer 40% → 16%), which supports the hook and the under, but on 2 starts.
- The model input "Rays K% vs RHP 19.1%" came from the Scout (MLB Stats API split). The research couldn't find it independently, so verify it on Savant.

**Close (Scout Job E, 19:57 ET):** FanDuel 6.5 o−132 / **u+104** (unchanged from our entry; it touched −138/+108 at 19:53). Pinnacle o−126 / u+104 → fair under **46.8%**. **CLV vs the Pinnacle close: -4.6%.** The market never moved toward the under, so by the system's main yardstick this entry was a small loser before the result. The WATCH call was right.

**Settled 2026-10-24 (morning, cloud):** 3 K in 15 outs (5.0 IP), 78 pitches, 18 BF. Two sources agree: MLB statsapi box score and the AP recap on Fox Sports ("season-low three strikeouts"). Under 6.5 **wins**, but it's WATCH at stake 0, so P&L is 0. BF 18 and 78 pitches came in at the short end of our 20.5 ± 3.5 leash assumption, which supports the hook thesis. One result can't undo the −4.6% CLV verdict, though: the market price was fair and we got the coin flip.
