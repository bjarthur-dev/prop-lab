---
tags: [system, health]
---

# System health (2026-11-02 08:55 ET)

Written by `engine/health.py` each morning. Fix STALE rows before trusting a card.

| feed | age | limit | status |
|---|---:|---:|---|
| results (box scores) | 0.0 d | 1.5 d | ok |
| odds board | 0.8 d | 1.5 d | ok |
| odds pregame | 0.6 d | 1.5 d | ok |
| NBA game logs (cloud: API-NBA + morning gap fill) | 1.0 d | 2.5 d | ok |
| NBA matchup context (laptop, optional) | 0.0 d | 14 d | ok |
| NFL data (nflverse) | 0.0 d | 8 d | ok |

## Odds API credits

Lowest key seen today: 302 left of 500 (about 99/day on that key). 29 days until the 1st reset. Three keys x 500 = 1,500 a month, about 50/day sustainable.

## Problems

- Odds credits: current pace runs out before the 1st. Cut extra tags (nbaalt, mlb) before the board/pregame/close core.
