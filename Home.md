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
- [[NBA Engine]] — v1 projection engine (minutes → rates → market-anchored sim), how it decides, how to run it on Windows
- [[MLB Module]] — MLB chains (pitcher Ks, batter H/TB/HRR), World Series micro-slate plan, Scout MLB fields
- [[Researcher Prompt]] — reusable facts-only researcher + separate falsifying reviewer
- [[Upgrade Roadmap]] — what to build next, in order
- [[Research - Advanced NBA mechanisms]] — shot zones, schemes, rotations, reb/ast tracking, market patterns; engine v1.5 plan + tracker v2 (H4–H8)
- [[Research - Upgrade Report]] — the full audit + research behind all of this
- [[The Guide]] — the full methodology (17 chapters: math, per-sport modeling, parlays, pick'em, form/streaks)
- [[Math Engine]] — the prop-engine code: devig, distributions, EV, Kelly
- [[Master Prompt - NFL]] / [[Master Prompt - NBA]] — archived one-game dossiers (superseded by [[Researcher Prompt]])

## Tonight / recent slates
- [[2026-10-23 NBA + WS G1]] — 12 NBA + World Series G1: 124 NBA props scanned → all PASS; 1 paper bet (Misiorowski u6.5 K)
- [[2026-10-22 TNF + NBA]] — Patriots-Bears + Nuggets-Thunder: the first full two-sport slate

## The record
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
