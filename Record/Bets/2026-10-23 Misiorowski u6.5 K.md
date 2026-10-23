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
decision: paper
stake_pct: 1
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
close_odds: 
close_odds_opp: 
close_line: 
close_ts: 
clv_pct: 
result: pending
pnl_units: 
---

# Misiorowski under 6.5 K (PAPER)

**Mechanism (sourced):** K% 37.9 over 665 BF in the regular season, but 29.7% over 37 BF in the postseason, at 91 pitches a start (94, 88) and 19/18 BF (MLB Stats API, ESPN game logs, via [[2026-10-23 B slate]] and [[2026-10-23 C board]]). The Rays strike out only 19.1% vs RHP (MLB Stats API). Roof closed. Model: talent K% shrunk to 34.8%, log5 vs the Rays → 30.6% per BF, BF 20.5 ± 3.5 (between the postseason leash and the market's 16.5-outs line) → mean 6.27 K.

**Why PAPER, not BET:**
- **[[Rules]] §3:** model beats sharp devig by +9.1 pts ✅, but shrunk edge is **2.8 < 3** ❌.
- **The edge depends on modeling choices.** With no talent shrinkage (37.9%), the mean rises to ~6.8 and the edge mostly disappears. A long leash (22 BF) does the same. This is a test of the leash + shrink hypothesis, not a confident edge.

**Also blended:** p_blend 0.493 at market weight 0.75 is only +0.3 pts over break-even (0.490). The [[Rules]] §7 blend also says no real bet, which agrees with PAPER.

**Reviewer issues:** price is from 13:37 ET; re-check at Job D. Lineups not posted.
