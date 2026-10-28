---
tags: [system, engine, nfl, matchup]
version: v1
updated: 2026-10-27
code: engine/nfl/matchup.py, engine/nfl/fetch_context.py
---

# NFL matchup layer v1

The cloud pulls the free nflverse data with `engine/nfl/fetch_context.py`. The results Action runs it Mon/Tue/Fri after the play-by-play refresh, so the laptop isn't needed. Sources:
- snap counts
- Next Gen Stats: receiving separation, cushion, aDOT and air-yard share; rushing yards over expected and 8+ man box rate; passing
- PFR advanced stats: defensive targets and yards allowed, pressures, blitzes, missed tackles; drops; broken tackles
- FTN charting: box counts, blitzers, play action, motion, screens

`python engine/nfl/matchup.py DATE "Full Name" ...` prints, for each player:
- **Role:** snap share trend, targets per game and target share, share of team air yards, aDOT, separation, YAC over expected; carries share and rushing yards over expected.
- **The opponent vs his position (WR/TE/RB):** targets, yards and yards per target allowed per game vs league.
- **The opponent's front:** pressure %, blitz %, 8+ man box %.
- **Pace and PROE (pass rate over expected) for both teams.**
- **Context multipliers to apply to the NFL engine's mean.** They're shrunk: a 2026 sample of k = 4 games is blended with 2025, and half the defense's deviation is treated as real.
- **The market line, shown last.**

Use it for every NFL leg on Sunday cards. A leg needs role stability (snap and target share holding or rising) plus a matchup that agrees with the side.
