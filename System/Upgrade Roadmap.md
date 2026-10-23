---
tags: [system, roadmap]
updated: 2026-10-23
---

# Upgrade Roadmap

Order: fix the record → then risk → then the model. Reasoning is in [[Research - Upgrade Report]].

- [x] 0. Create [[Rules]], [[Slate Playbook]], [[Researcher Prompt]], [[2026-10-22 Audit]], Bases views
- [ ] 1. **Record integrity**: add the [[Rules]] §6 columns to `bets.csv` / `bet_log.py`; timestamp validation; flag tonight's rows; Gordon → 5.5 *(hours)*
- [ ] 2. **Caps in code**: per bet 1%, per game 3%, per player 1.5–2%, slate cap by class, no singles + SGP of the same legs, book whitelist *(hours)*
- [ ] 3. **Pass rule in code**: auto-PASS unless shrunk edge ≥ 3 pts and model vs sharp devig ≥ 3 pts; no unquoted SGPs *(hours)*
- [ ] 4. **Odds snapshot pipeline**: The Odds API ($30–59/mo tier to start; historical props from May 2023) → append-only DuckDB at open / bet time / T−10 *(1–2 days)*
- [ ] 5. **Evaluation layer**: CLV vs devigged close, Brier/log-loss skill vs close, quantile calibration bins, test martingale, segment report by slate_class / reason_code *(1–2 days)*
- [ ] 6. **Prediction-market + pick'em chapter** in The Guide: ask + live fee, depth, DNP = No, displayed-multiplier break-evens *(hours)*
- [ ] 7. **Researcher + reviewer** workflow live ([[Researcher Prompt]]) *(1 day)*
- [x] 8. **NBA engine v1 built 2026-10-23** ([[NBA Engine]]; synthetic tests pass; real-data backtest pending on your PC). Original spec:: minutes distribution (spread / back-to-back / OT) × time-decayed shrunk per-possession rates × pace × opponent → NB/Poisson simulation; pre-computed "if X sits" scenarios *(1–3 weeks)*
- [ ] 9. **NFL engine**: script-simulated volume → route/carry shares → regressed efficiency → skewed yards, Poisson TDs, wind *(1–3 weeks)*
- [ ] 10. **Blend redesign**: blend means, market weight 0.7–0.8, refit at ~200 bets
- [ ] 11. **Automation** (below)
- [ ] 12. Tune the slate classes and graduation gate from data

## Automation design (Windows)
| Local time | Runner | Job |
|---|---|---|
| 06:30 | Task Scheduler → `ingest.py` | Box scores (nba_api / nflreadpy) → DuckDB; auto-settle; CLV |
| open, bet time, T−10 | Task Scheduler → `odds_snapshot.py` | Append-only odds snapshots |
| ~11:00–13:30 + 30 min pre-tip | Claude local scheduled task "research" | [[Researcher Prompt]] → slate note facts JSON |
| after research | `price.py` | Projections + devig → p_model, shrunk edge, [[Rules]] caps → candidates |
| before logging | Claude task "reviewer" (separate) | Falsify every number; block unverified |
| next morning | Python + Claude | Settlement, report, review note |

Notes: Claude Desktop local tasks run only while the PC is awake and the app is open, and catch up only once after a missed run. Put a time guard in every prompt ("if after tip, create no bets"). DuckDB is the source of truth and the vault mirrors it; this replaces "the cloud sandbox is the live version". For live edits while Obsidian is open, the Local REST API plugin has a built-in MCP server (port 27124).
