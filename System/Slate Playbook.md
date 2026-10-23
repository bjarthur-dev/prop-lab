---
tags: [system, slates, playbook]
updated: 2026-10-23
---

# Slate Playbook — how the day changes the plan

**Core idea:** slate size changes **how many** bets you place and **how much** you risk. It never changes the edge threshold ([[Rules]] §3). More games means more legs clear the bar. It does *not* mean you should force more parlays.

## 1. Classify the slate first
| Class | Games | Expect qualifying legs | Straight bets | Pick'em slips | Max slate exposure | Per-game cap |
|---|---|---|---|---|---|---|
| **Micro** (TNF/MNF/SNF, lone national NBA game, playoffs) | 1–2 | 0–4 | 0–4 | 0–2 · 3–5 legs · Flex · deliberate script stack | 3–5% | = slate cap |
| **Small** | 3–5 | 2–8 | 2–8 | 1–3 · 4–6 legs · ≤ 2 legs/game | 5–8% | 3% |
| **Medium** | 6–9 | 5–15 | 5–15 | 2–4 *disjoint* 5–6-leg slips, 1 leg/game | 8–12% | 3% |
| **Large** (NBA 10–15, NFL Sunday main) | 10+ | 10–30 | 10–30 | 3–6 disjoint 5–6-leg slips | 10–20% | 3% |

*(Heuristic. Tune it from the record by logging `slate_class` on every row.)*

## 2. One game vs ten games
- **One game:** about 40–80 props, all eyes on them, every leg tied to one game script. Closes are sharp and correlation is total. Picking "the best 3 tonight" out of 20 is mostly selecting noise: in the simulation the top-5 *looked* like 3.4% edges and were really 0.3%. **Expect PASS to be the right answer most nights.** If you play, play 1–3 legs, or one deliberate script stack, and that's all.
- **Ten+ games:** 1,000+ props, thin attention per prop, and lines go stale after news. The best picks are genuinely better (true edge ~6× higher in the simulation), *but only after shrinking*. This is where the system makes money: broad coverage, speed after news, disjoint slips with one leg per game so the independence math holds.
- **Two sports on one night** (tonight): still a micro slate. 3–5% total, not 90%.

## 3. Timing: bet when your edge is freshest
| Edge source | When to bet |
|---|---|
| Your projection vs the opener | **Early.** Openers are softest; limits are low but enough for you |
| Pick'em line vs sharp book | **Late**, 60–15 min before lock, when the books are most efficient |
| Injury/lineup news | **Within minutes.** Pre-compute "if X sits" scenarios so you just fire |

**NBA news clock** (local time of the team): the day-before injury report is due 5 pm (1 pm game day for the 2nd leg of a back-to-back), plus a mandatory game-day update 11 am–1 pm (8–10 am for tips ≤ 5 pm) since the Dec 19 2025 memo. Confirm whether 2026-27 changed this.
**NFL:** inactives come ~90 min before kick. The 1 pm window's results and injuries inform 4:05/4:25 and SNF prices.
**Staggered tips:** separate slips per start window (Pick6 entries can't be edited). Recompute sizing once early games settle.

## 4. Day types
| Day | What changes | Play |
|---|---|---|
| Early season (now) | Stale priors, books also unsure | Edges are bigger *and* you know less, so shrink more |
| NBA back-to-back-heavy night | Wider minutes distributions, later news | Wait for the news, then hit stale props |
| National TV / holidays / playoffs | Micro slate, peak attention | Micro rules; playoffs: tighter rotations → minutes edges |
| Late season | Tanking and rest volatility | React to news; fade stale starter lines |
| Wind ≥ 12 mph (NFL) | Passing −8%, unders 59% at 12–14 mph | Adjust passing volume and efficiency; at 15+ mph the line already has it |
| Thursday NFL | No meaningful under effect (46.8% overs vs 48.7%) | Don't add a TNF adjustment |

## 5. 2026-27 market changes
At NBA partner books: no same-player under parlays, no opening-tip bets, no "miss shots" props, and **no unders on players projected under 12 minutes**. The deep-bench under is gone there. Prediction markets aren't covered by these bans.

## 6. Where to look first
- **NFL:** unders on skewed, low-volume markets (RB receiving yards, 10–19-yard receiving lines, sub-10 rushing lines). These are 2020–22 results that may have decayed, so test them. Shop anytime-TD prices (books differ by 30+ cents).
- **NBA:** role players, rebounds and assists, 0.5/1.5 low-count markets, alt-line tails, and anything stale in the hour after news.
