"""NBA engine v1 — every tunable in one place. Values marked (H) are heuristics to refit from the record."""
SEASON_CUR = "2026-27"
SEASON_PRIOR = "2025-26"

# recency weighting (games ago -> weight 0.5 ** (g / half_life))
HL_RATES = 40            # (H) per-minute rates (stable; long memory)
HL_MINUTES = 6           # (H) minutes react faster to role changes
PRIOR_SEASON_DISCOUNT = 0.7   # (H) extra weight multiplier on last season's games

# Bayesian shrinkage toward league per-minute rate, in "minutes of prior" (H)
SHRINK_MIN = {"pts": 120, "reb": 100, "ast": 100, "fg3m": 300, "fg3a": 100}
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
LIVE = True              # Rules §9 live pilot (2026-10-24): qualifying sides are BET (real money) at pilot stakes
UNIT_PCT = 0.5           # §9: 0.5% per straight bet during the pilot (§1 says 1% after graduation)
PER_GAME_CAP = 1.0       # §9
PER_PLAYER_CAP = 0.5     # §9
SLATE_CAP = {"micro": 2.0, "small": 2.0, "medium": 2.0, "large": 2.0}  # §9: 2% per day during the pilot

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

# v1.2 threes (sourced paddings: Medvedovsky ~240 3PA in-season; Blackport ~750 3PA reliability point)
P3_PAD = 240        # current-season 3P% padded with this many attempts of the player's prior
P3_PRIOR_PAD = 750  # the player's prior (earlier seasons) padded toward league 3P% with this many attempts
P3_BETA_N = 400     # (H) remaining uncertainty in true 3P% for the simulation

# v1.3 (2026-10-23) — tuned on the real 2025-26 walk-forward backtest (5,856 player-games, 18 dates).
# Fitted VMR around each player's own season rate understates real game-to-game spread (reb 1.04, ast 1.05 -> overconfident
# by ~5 pts at p>=0.55). Floors + rate uncertainty below cut that to ~+1 (reb) / ~-1 (ast) with the best log-loss.
VMR_FLOOR = {"pts": 2.0, "reb": 1.5, "ast": 1.35, "fg3m": 1.0, "fg3a": 1.2}
RATE_CV = 0.10            # lognormal uncertainty on each player's true per-minute rate, per simulation
