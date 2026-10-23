---
tags: [record, betlog]
---

# Bet Log

The single source of truth. No bet is real until it's logged with its odds timestamp. **Log passes too** — no-bet discipline is part of the record.

## How it works (cloud side)
- Live log: `prop-engine/bets.csv` (this vault holds a snapshot — the cloud file is authoritative)
- Add: `python3 bet_log.py add --date ... --player ... --line ... --selection over --book ... --odds ... --odds-ts ... --model-prob ... --decision bet|paper|pass`
- Settle: `python3 bet_log.py settle <id> win|loss|void --close-odds ... --close-odds-opp ... --close-line ... --close-ts ...`
- Report: `python3 bet_log.py report` → ROI (paper/live separately), raw same-line CLV, fair-close EV, calibration bins, Brier

## Current state (snapshot 2026-10-22, all pending)
| # | Sport | Entry | Price |
|---|---|---|---:|
| 1 | NFL | Swift OVER 14.5 rush att | -111 |
| 2 | NFL | Douglas OVER 3.5 rec | +105 |
| 3 | NFL | Stevenson UNDER 42.5 rush yds | -112 |
| 4 | NFL | 3-leg SGP (1+2+3) | 7.38x |
| 5 | NBA | Gordon OVER 6 reb | PM 54.18¢ |
| 6 | NBA | SGA OVER 30.5 pts | +102 |
| 7 | NBA | J. Williams OVER 18.5 pts | -106 |
| 8 | NBA | Jokic OVER 24.5 pts | -110 |
| 9 | NBA | Jokic OVER 9.5 ast | +108 |

## Settlement rules (DraftKings official)
- **NFL**: player must play at least one snap; pre-halftime full-game props void if the player misses the entire 2nd half to injury (except unders/decided bets).
- **NBA**: check the specific book's scratch rules; settlement-aware EV accounts for voids.

## Reading the report (what good looks like)
- **CLV**: beat the no-vig close on 55%+ of bets over a large sample — diagnostic, not proof.
- **Calibration**: predicted 55% events hit ~55% across 100+ bets; Brier < 0.25 on coin-flip markets.
- **No fixed sample size proves anything** — multiple props from one game are not independent.
