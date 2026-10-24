---
tags: [system, mlb]
updated: 2026-10-23
season_state: "World Series: Rays vs Brewers, G1 Fri Oct 23, 8 pm ET; every game 8 pm ET; then offseason until spring 2027"
---

# MLB Module

The method lives in [[The Guide]] §4 (hitter + pitcher chains). Sizing, caps and the pass rule are in [[Rules]]; slate logic is in [[Slate Playbook]]. This note covers what's MLB-specific.

## Right now: the World Series is a micro slate
- **Schedule (all 8 pm ET):** G1–G2 Fri 10/23 and Sat 10/24 at MIL · G3–G5 Mon 10/26 to Wed 10/28 at TB · G6–G7 Fri 10/30 and Sat 10/31 at MIL (if needed). Source: [MLB.com](https://www.mlb.com/news/2026-mlb-world-series-faq-schedule-times-teams-and-more).
- One game a night, with maximum attention on it. That's the least favorable setup for this system ([[Slate Playbook]] §2). **Default to PAPER.** Treat the Series as a live test of the MLB pipeline (the Scout's fields, the K model, logging, close capture) before the 2027 season, when 15-game slates are where the edge is.
- Micro-slate caps apply: ≤ 3–5% total, every leg correlated through the same game. Pick'em needs two teams, which the Series gives you, but legs are still one game.

## The projection chains (v0)
**Pitcher strikeouts**, the most model-friendly MLB prop:
1. **Expected batters faced** = projected pitch count ÷ pitches per PA, capped by the times-through-order hook. **Postseason:** starters are pulled earlier (qualitative report: ~2 innings), so cut BF ~10–20% vs regular season except for aces with a long leash *(heuristic)*. The Scout reports each starter's last 3 postseason pitch counts and BF as facts.
2. **K% per PA** = log5 / odds-ratio of pitcher K% vs the opposing lineup's K% *against that handedness*, both shrunk toward league (2025 league K% 22.2%).
3. **2026 ABS challenge system:** 2 challenges per team, a slightly smaller zone, slightly fewer Ks expected, less umpire influence. **Down-weight pre-2026 umpire K data** heavily ([MLB.com](https://www.mlb.com/news/abs-challenge-system-2026-mlb-season-overview?p=0)).
4. Distribution: simulate BF (distribution, not a point) × binomial(K%). Price every alt line from the same simulation.

**Batter hits / total bases / HRR:**
1. PA from lineup slot (leadoff ~4.6–4.8, 9th ~3.8–4.0 *(unsourced, general knowledge)*). The confirmed lineup is required; no lineup means no bet.
2. Per-PA rates: season + prior, shrunk; platoon split regressed hard.
3. Pitcher quality *plus* bullpen exposure. In the postseason the starter goes fewer innings, so more PAs come against high-leverage relievers, which lowers hit and TB expectations.
4. Park + weather: American Family Field (MIL) has a **retractable roof**, so the Scout records roof status. Tropicana Field (TB) is a fixed dome, unless the Rays are playing elsewhere in 2026 — **confirm the TB venue** (the Scout checks).
5. Distribution: binomial(PA, p_hit) for hits; **never Poisson for HRR** (negative binomial, VMR ~2; [[Math Engine]]).

## What the Scout adds for MLB (Job B)
Probable starters (official), handedness, each starter's last 3 starts (pitch count, BF, Ks: facts only), confirmed lineups and batting order (when posted, usually ~2–4 h pre-game), home-plate umpire, roof status / weather, bullpen usage the previous 2 days (pitchers and pitch counts), injuries/IL. **Banned:** batter-vs-pitcher history (tiny samples), "hot streak" narratives.

## Markets to start with
1. **Pitcher K over/under:** most structure, most two-way prices.
2. Batter hits 0.5 / TB 1.5 at a sharp two-way book.
3. Skip HR and RBI props in the Series (high hold, mostly variance).

## K model v1 (2026-10-23): `engine/mlb/k_model_v1.py`
- **PA-by-PA simulation:** each PA draws K / BB / ball in play (log5 per lineup slot × half-weight park K factor × smooth decay per batter, no third-time-through cliff) and a pitch count. The starter is pulled when pitches exceed a **hook** drawn per sim. **K and outs come from the same draw**, so they're priced consistently.
- Talent K% = own regular season blended with the postseason sample at n/(n+70) (K% reliability ~70 BF).
- **`market_implied_hook()` — standing rule:** before pricing Ks, fit the hook so the model reproduces the **devigged outs-recorded market**. Then any K edge left is about strikeout *rate*, not a leash guess. If our K edge only exists with our own hook, it's a leash bet, and the outs market is where to test it.
- **Game 1 lesson:** with the leash fitted to the outs market (~106 pitches), v1 says Misiorowski K under 6.5 = **42.5%** vs Pinnacle's 46.8%. The v0 under (56%) was entirely a short-leash assumption that the outs market contradicted. The WATCH call and the −4.6% CLV agree. Martinez under 3.5 = 64.7% vs Pinnacle 59.8% (+4.9 pts, but FanDuel's −186/−192 needs 65.0%): pass.
- Inputs per pitcher in a JSON (see `example_inputs.json`): RS/PS K and BF, BB%, team or per-slot lineup K% vs hand, park factor, P/PA, hook. The Scout supplies outs lines both sides (Job C).
