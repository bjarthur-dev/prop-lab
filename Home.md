---
tags: [moc, home]
---

# Prop Lab — Home

The player-prop projection system: **AI does the research, code does the math, the record decides what's real.**

## The three rules
1. **A projection above the line is not a good over** — only +EV bets count, and the default output is [[Daily Workflow#Pass|PASS]].
2. **Log every decision** — bets, paper bets, and passes — in the [[Bet Log]]. The record is the product.
3. **Never trust a number you can't source** — every probability comes from the [[Math Engine]] or is marked UNKNOWN.

## Start here
- [[Rules]] — **the single source of every number** (sizing, caps, pass rule, books, graduation). Wins any conflict.
- [[Slate Playbook]] — how 1 game vs 10+ games, start times and day types change bet count, slips and exposure
- [[Daily Workflow]] — the checklist for every slate
- [[Roles & Automation]] — who does what: Perplexity = Scout (sourced facts → `Inbox/`), Claude = Engine + Auditor, Python = data layer, you = Decider; the daily ET clock
- [[Perplexity Prompt]] — standing instructions for Perplexity (Jobs A–E)
- [[NFL Engine]] — v1: line → plays → script-aware pass rate → shares → simulated yards/TDs (PAPER/WATCH only)
- [[NBA Engine]] — v1 projection engine (minutes → rates → market-anchored sim), how it decides, how to run it on Windows
- [[Mechanism Tracker]] — v2: zero-stake theory tests with matched controls, H1a–H8 + DvP placebo, grader `engine/tracker.py`
- [[MLB Module]] — MLB chains (pitcher Ks, batter H/TB/HRR), World Series micro-slate plan, Scout MLB fields
- [[Cloud Pipeline]] — **what runs with the laptop off**: GitHub Actions (results, Scout ingest, watchdog, tests), Claude cloud morning settlement 08:17, Perplexity delivery by GitHub issue
- [[Afternoon Card Task]] — the daily 14:52 bet card (live pilot, [[Rules]] §9) — create it in the Claude app
- [[Bankroll Growth Plan]] — the ranked, research-backed plan: tokens/boosts first, price-edge singles, what to avoid
- [[Bankroll]] — live-pilot bankroll and limits
- [[Laptop Refresh Task]] — keep NBA data current from the laptop (Windows startup/daily, or a Claude task)
- [[Morning Settlement Task]] — the morning settlement prompt (now a cloud scheduled task)
- [[Researcher Prompt]] — reusable facts-only researcher + separate falsifying reviewer
- [[Upgrade Roadmap]] — what to build next, in order
- [[Research - Advanced NFL and MLB mechanisms]] — NFL engine v1 design (volume → shares → simulated tails), K model v1 (PA-by-PA, hook, park), N1–N10 + M1–M8 theories
- [[Research - Advanced NBA mechanisms]] — shot zones, schemes, rotations, reb/ast tracking, market patterns; engine v1.5 plan + tracker v2 (H4–H8)
- [[Research - Upgrade Report]] — the full audit + research behind all of this
- [[The Guide]] — the full methodology (17 chapters: math, per-sport modeling, parlays, pick'em, form/streaks)
- [[Math Engine]] — the prop-engine code: devig, distributions, EV, Kelly
- [[Master Prompt - NFL]] / [[Master Prompt - NBA]] — archived one-game dossiers (superseded by [[Researcher Prompt]])

## Tonight / recent slates
- [[2026-10-23 NBA + WS G1]] — 12 NBA + World Series G1: 124 NBA props scanned → all PASS; 1 paper bet (Misiorowski u6.5 K)
- [[2026-10-22 TNF + NBA]] — Patriots-Bears + Nuggets-Thunder: the first full two-sport slate

## The record
- [[2026-10-28 Review]]: **LIVE none placed, $0.** Paper 1–3 legs, both slips lost (Trae 8 ast, 2 short). CLV: price_edge 4/4 positive (+2.8 / +3.8 / +2.9 / +7.4%); segment 8/8, mean +5.7%; running 19 entries, **+0.7%**. Tracker H1a hyp 0/3 vs control 1/2. Shadow 1,506 graded (NBA model −4.0%, blend +1.0%; matchup v1 −6.2% on 795). **NBA gate review due (1,346 props), under-lean unexplained.** Bankroll $39.00
- [[2026-10-27 Review]]: **LIVE 0–1, −$5.00** (off-card Pick6 Tatum < 25.5 ✗ 40 in OT / Harper > 16.5 ✗ 13). Paper 0–1 (Thybulle 3PM). PASSed Cade 8+/Reaves 7+ slip would have won. CLV: price_edge 4/4 positive, mean +7.2% (none placed); running 15 entries, −0.2%. Shadow 1,069 graded (NBA model −4.9%, blend +2.0%; matchup v1 −1.1% on 201). **Bankroll $39.00** (DK 27 + Betr 12). Kill-switch question for the user
- [[2026-10-26 Review]]: **LIVE 0–1, −$5.00** (Pick6 Miller 20+ ✓ / JJJ 15+ ✗, he left hurt; a discounted line). Paper 3–5. CLV: price_edge legs **+6.8% / +4.9%**, model WATCH legs −4.2% / −3.7%; running 13 entries, −1.5%. Shadow 942 graded (NBA model −4.1%, blend +2.6%; NFL model −2.8%). 10-25 NFL flags settled from pbp (20–15 final). **Bankroll $25.00**
- [[2026-10-25 Review]]: 0 staked bets; paper-track **18–13, 4 open** (NFL WATCH 16–12, NBA 2–1; +3.35 notional u). CLV only on SNF: 5 entries, all negative, mean **−4.0%**; running CLV 9 entries, −2.6%. Tracker N1 hyp 20/36 vs controls 16/35 (noise). 11 NFL players flagged single-source. Bankroll $30.00
- [[2026-10-24 Review]]: 0 staked bets; paper-track 1–3 (Mitchell u AST and Harden u REB lost at **+2.5% / +2.0% CLV**, Rasmussen o5.5 K lost at −3.7%; Pick6 HRR slip won, $0). Tracker hyp 4/6 vs controls 4/7. Running CLV 4 entries, −0.95%. Bankroll $30.00
- [[2026-10-23 Review]] — 0 staked bets; WATCH Misiorowski u6.5 K won (3 K) at **−4.6% CLV**; tracker 4/15 vs market p 0.50 (H1 0/7, H2 1/3, H3-legacy 3/5; noise). Live pilot bankroll $30.00
- [[Bet Log]] — 2026-10-22 settled **4–5, −$14.17** at $10 stakes (−$1.42 at 1%), 0/9 closes captured — see [[2026-10-22 Review]] and [[2026-10-22 Audit]]
- `Record/Bets.base` — Bases views: open bets, exposure by game, CLV by market, reason-code ledger, calibration bins (one note per bet from [[_Bet Template]])
- [[Review Template]] — run after every slate settles

## Libraries
- [[Market Intel]] — line moves, RLM, books vs pick'em apps, CLV lessons
- [[_Player Template]] — one note per player you track (form/streak protocol)
- [[_Slate Template]] — copy for each new slate

## Where things live
- **Source of truth: GitHub** https://github.com/bjarthur-dev/prop-lab — Claude commits here; Perplexity reads it; Obsidian (PC + phone) pulls it via the Obsidian Git plugin.

## Older cloud-side notes
- Guide: `player-prop-projection-guide.md` · Engine: `prop-engine/` · Log: `prop-engine/bets.csv`
- Target state ([[Upgrade Roadmap]] #4, #11): a local DuckDB is the source of truth, and the vault mirrors it. Until then, treat `bets.csv` as canonical and note any changes made on the cloud side here.
