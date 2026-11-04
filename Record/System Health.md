---
tags: [system, health]
---

# System health (2026-11-04 08:19 ET)

Written by `engine/health.py` each morning. Fix STALE rows before trusting a card.

| feed | age | limit | status |
|---|---:|---:|---|
| results (box scores) | 0.0 d | 1.5 d | ok |
| odds board | 0.6 d | 1.5 d | ok |
| odds pregame | 1.6 d | 1.5 d | **STALE** |
| NBA game logs (cloud: API-NBA + morning gap fill) | 2.0 d | 2.5 d | ok |
| NBA matchup context (laptop, optional) | 2.8 d | 14 d | ok |
| NFL data (nflverse) | 0.8 d | 8 d | ok |

## Odds API credits

Lowest key seen today: 69 left of 500 (about 108/day on that key). 27 days until the 1st reset. Three keys x 500 = 1,500 a month, about 50/day sustainable.

## Problems

- odds pregame: check odds.yml pregame tag
- Odds credits: current pace runs out before the 1st. Cut extra tags (nbaalt, mlb) before the board/pregame/close core.
