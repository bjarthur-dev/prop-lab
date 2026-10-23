---
tags: [system, roles, automation]
updated: 2026-10-23
---

# Roles & Automation — who does what

**One sentence:** Perplexity finds and sources facts. Claude verifies them, does all the math, enforces [[Rules]], and keeps the record. Python scripts eventually own every number that can be fetched by code. You make the final call and place the bets.

## The four roles
| Role | Who | Owns | Never does |
|---|---|---|---|
| **Scout** | Perplexity | Live web facts with URLs: slate, start times, injury/lineup status, spreads/totals, prop prices at named books (both sides + timestamp), weather, role-change mechanisms, box scores, closing prices | Probabilities, projections, picks, sizing; editing anything outside `Inbox/` |
| **Engine + Auditor** | Claude | Verifying Scout files (falsify, second source), projections, devig, EV, shrunk edge, [[Rules]] caps, slate class, bet notes, settlement, CLV/calibration reports, all `System/`, `Slates/`, `Record/` notes | Inventing stats; treating an unverified Scout fact as true |
| **Data layer** (to build) | Python on your PC via Task Scheduler | Odds snapshots (The Odds API → DuckDB), box scores (nba_api / nflreadpy), auto-settle | Judgment |
| **Decider** | You | Approving the card, placing bets, changing [[Rules]] | Overriding the pass rule without logging the reason |

Why this split: Perplexity's strength is fast, cited, current web search. Claude's is reasoning, code and keeping a consistent record. The failure we're designing out is the 2026-10-22 one, where research ("angles", small samples, media prices) flowed straight into bets with nothing checking it.

## Folder ownership (no two agents edit the same file)
```
Prop-Lab/
├─ Inbox/Perplexity/     ← Perplexity writes ONLY here (one new file per job run)
├─ Inbox/Requests/       ← Claude writes requests for Perplexity here
├─ Slates/  Record/  System/  Players/  Markets/   ← Claude writes; Perplexity reads only
```
A Scout file moves through `status: new → verified | rejected` (set by Claude in its own review, never by editing Perplexity's file in place). Facts reach a slate note only after verification.

## The daily clock (ET)
| Time | Who | Job | Output |
|---|---|---|---|
| 07:30 | Perplexity | **A. Results**: box scores for every open bet, 2 sources each | `Inbox/Perplexity/{date} A results.md` |
| 08:30 | Claude | Settle, CLV where closes exist, update review + Market Intel | `Record/{date} Review.md` |
| 11:00 | Perplexity | **B. Slate sheet**: games, times, TV, spreads/totals open→current, injury report #1, rest/b2b, travel, weather | `… B slate.md` |
| 11:30 | Claude | Classify slate, run projections, build the candidate list, write **requests** (exact props and books to price, statuses to confirm) | `Inbox/Requests/{date} requests.md` |
| ~13:30 (after the NBA game-day report) / Sun 10:00 NFL | Perplexity | **C. News + board**: answer the requests; prices for candidates at named books, both sides, timestamps; new statuses | `… C board.md` |
| per window, T−90 → T−45 | Perplexity → Claude | **D. Late news** (NFL inactives at T−90) → Claude reprices, applies [[Rules]], writes the card, logs paper/bets **before start** | slate note + `Record/Bets/` |
| T−10 → T−5 | Perplexity (until Python exists) | **E. Close capture**: both sides of every logged market at the book logged + one sharp book | `… E close.md` |

Staggered start windows (7:00 / 7:30 / 10:00 NBA; 1:00 / 4:05 / 4:25 / 8:20 NFL): run D and E **per window**. After early games settle, Claude re-sizes the late window on the updated bankroll.

**Automation reality check.** Claude scheduled tasks on your PC run only while the Claude desktop app is open and the PC is awake (one catch-up run after a missed time). Perplexity's scheduled Tasks may not be able to write into this folder; if not, you trigger Jobs A–E with the prompt at those times. The Python data layer (Odds API + nba_api/nflreadpy) is the step that makes jobs A and E fully hands-off, and it's [[Upgrade Roadmap]] #4.

## How a projection gets formed (v0 → v1)
1. **Market prior:** devig a real two-way price from a sharp-ish book (FanDuel, Caesars, Pinnacle, Circa) → p_market → back out the market's implied mean through the stat's distribution.
2. **Model mean (Claude):**
   - NBA: minutes distribution (role, spread/blowout, b2b, OT) × per-minute rates (season blended with prior, shrunk; 3P% shrunk hard) × pace × opponent (shrunk).
   - NFL: team plays × pass rate (spread/total script, wind) → dropbacks/carries × player share (routes, targets, carries, red-zone) × efficiency regressed hard → skewed yards, Poisson TDs.
   - **v0 (now):** built from Scout-sourced season stats in the files. **v1:** built from nba_api/nflreadpy on your PC.
3. **Adjustments only via sourced deltas:** vacated usage/targets, status changes, wind ≥ 12 mph. Never head-to-head, last-3 streaks or affiliate angles.
4. **Blend means**, market weight 0.75 → convert to p with the right distribution (NB for counts, skewed for yards).
5. **Decide** with [[Rules]] §3: executable price, shrunk edge ≥ 3 pts, caps by slate class ([[Slate Playbook]]), log before start.

## Handoff contract (what Claude needs from every Scout file)
Every fact = value + `source_url` + exact quote + `retrieved_at` (ET). Prices = book + both sides + line + timestamp. Unknowns written as `UNKNOWN`. Picks and "angles" go only in a `quarantine:` list. The full contract is in [[Perplexity Prompt]].
