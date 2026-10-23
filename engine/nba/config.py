"""NBA engine v1 — every tunable in one place. Values marked (H) are heuristics to refit from the record."""
SEASON_CUR = "2026-27"
SEASON_PRIOR = "2025-26"

# recency weighting (games ago -> weight 0.5 ** (g / half_life))
HL_RATES = 40            # (H) per-minute rates (stable; long memory)
HL_MINUTES = 6           # (H) minutes react faster to role changes
PRIOR_SEASON_DISCOUNT = 0.7   # (H) extra weight multiplier on last season's games

# Bayesian shrinkage toward league per-minute rate, in "minutes of prior" (H)
SHRINK_MIN = {"pts": 120, "reb": 100, "ast": 100, "fg3m": 300}
MIN_PRIOR_GAMES = 4      # (H) last season's avg minutes counts as this many games
NO_CUR_GAMES_MIN_FACTOR = 0.9  # (H) role uncertainty for players with no current-season game

# team constraints
TEAM_MINUTES = 241.0     # 240 + expected OT minutes
ROTATION_MIN = 8.0       # projected minutes to count as rotation
ROTATION_SIZE = 10
MAX_MIN = 38.0
SD_MIN_DEFAULT = 5.5     # (H) minutes SD floor
BLOWOUT_START = 6.0      # (H) spread points before starters lose minutes
BLOWOUT_MIN_PER_PT = 0.25  # (H) starter minutes lost per spread point beyond BLOWOUT_START
STARTER_MIN = 28.0

# market anchoring: scale team points to the implied team total
TEAM_PTS_CLIP = (0.80, 1.25)
AST_EXP = 0.8            # (H) assists scale with points factor ** AST_EXP
REB_EXP = 0.5            # (H) rebounds scale with (game total / league avg total) ** REB_EXP

# dispersion (variance / mean given minutes). Refit from logs by model.fit_vmr()
VMR_DEFAULT = {"pts": 2.2, "reb": 1.3, "ast": 1.4, "fg3m": 1.2}

N_SIMS = 20000

# pricing / rules (mirror System/Rules.md)
MARKET_WEIGHT = 0.75
SHRINK_EDGE = 0.4
MIN_SHRUNK_EDGE_PTS = 3.0
MIN_MODEL_VS_MARKET_PTS = 3.0
PAPER_SHRUNK_EDGE_PTS = 1.5
LIVE = False             # paper-only until the graduation gate in Rules §8
UNIT_PCT = 1.0
PER_GAME_CAP = 3.0
PER_PLAYER_CAP = 2.0
SLATE_CAP = {"micro": 5.0, "small": 8.0, "medium": 12.0, "large": 10.0}  # large capped at 10 while paper/v1

SEASON_ID_CUR = "22026"   # nba_api LeagueGameLog SEASON_ID for 2026-27 regular season
LEAGUE_AVG_TOTAL = 230.0  # (H) refreshed by run_slate from the logs when available
DATA_DIR = "engine/data"
OUT_DIR = "engine/out"
MIN_BLEND_OVER_BE_PTS = 2.0   # (H) blended p must beat break-even by this much (synthetic test: stops fake edges)
MAX_MODEL_VS_MARKET_PTS = 10.0  # (H) bigger disagreement with a sharp market = likely missing info -> PAPER + investigate
MIN_STALE_EDGE_PTS = 2.5     # (H) path B: sharp consensus (excl. the book we bet) beats break-even by this much
MIN_REF_BOOKS = 2            # path B needs at least this many other books at the same line
MODEL_VETO_PTS = 3.0         # (H) path B is vetoed only if the model says the side is >3 pts below break-even

# v1.1 minutes allocation (fixes: blowout rule undone by normalization; vacated minutes flowing to stars)
BENCH_ABSORB = 1.0        # (H) bench players' weight when absorbing vacated minutes
STARTER_ABSORB = 0.2      # (H) starters absorb some, much less
STARTER_HEADROOM = 2.0    # (H) a starter can rise at most this many minutes above his baseline
BENCH_HEADROOM = 12.0     # (H) a bench player can rise up to baseline + this ...
BENCH_CEILING_FLOOR = 28.0  # (H) ... or to at least this (a backup center stepping into a starting role)
SAME_POS_SHARE = 0.7      # (H) share of an OUT player's minutes pre-routed to same-position bench players (needs data/positions.csv)
