---
tags: [system, health]
---

# System health (2026-11-01 23:51 ET)

Written by `engine/health.py` each morning. Fix STALE rows before trusting a card.

| feed | age | limit | status |
|---|---:|---:|---|
| results (box scores) | 0.5 d | 1.5 d | ok |
| odds board | 0.4 d | 1.5 d | ok |
| odds pregame | 0.2 d | 1.5 d | ok |
| NBA game logs | 1.0 d | 2.5 d | ok |
| NBA matchup context (laptop) | 0.5 d | 4 d | ok |
| NFL data (nflverse) | 0.5 d | 8 d | ok |

## Odds API credits

Lowest key seen today: 305 left of 500 (about 195/day on that key). 30 days until the 1st reset. Three keys x 500 = 1,500 a month, about 50/day sustainable.

## Problems

- Odds credits: current pace runs out before the 1st. Cut extra tags (nbaalt, mlb) before the board/pregame/close core.
