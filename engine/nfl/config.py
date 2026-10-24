"""NFL engine v1 tunables. (H) = heuristic to refit on 2023-25 nflverse data; [S] = sourced (see Research - Advanced NFL and MLB mechanisms)."""
N_SIMS = 20000
PLAYS_BASE = 61.3          # [F] fitted 2023-26 REG (1,820 team-games): plays per team-game at a 44 total
PLAYS_PER_TOTAL_PT = 0.08  # [F] was 0.25 (H)
PLAYS_SD = 8.0             # [F] resid sd 8.4 (some of it is script, modeled separately)
MARGIN_SD = 12.6           # [F] final margin ~ Normal(-spread, 12.6); bias 0.0
BASE_PASS_RATE = 0.606     # [F] dropback rate incl. sacks/scrambles at pick'em
PROE_WEIGHT_CUR = 0.5      # [I] 50/50 current-season vs prior PROE at weeks 6-8
SPREAD_PASS_SLOPE = 0.0024 # [F] +0.24 pp per point of spread (was 0.005 from research)
SCRIPT_K = 0.055           # [F] pass rate shift per 14 pts of margin surprise
PASS_RATE_CLIP = (0.40, 0.78)
SACK_RATE = 0.066          # [F] league sacks per dropback; per-QB override
SCRAMBLE_RATE = 0.056      # [F] per non-sack dropback; per-QB override
SHARE_CONC = 80.0          # [F] target-share Beta concentration (backtest: 10/90 bands 8.5%/9.7%)
CARRY_CONC = 8.0           # [F] carry-share Beta concentration (carry splits swing a lot game to game)
TD_CAL = (0.80, 0.75)      # [F] ATD recalibration: lambda' = a * lambda^b (fit 2024-25, Brier .1996 -> .1989)
TD_RZ_W_RUSH = 0.77        # [F] share of rushing TDs from inside the 10 (rest allocated by overall carry share)
TD_RZ_W_PASS = 0.49        # [F] share of passing TDs from inside the 10 (rest allocated by overall target share)
TD_PTS_SHARE = 0.736       # [F] 7 x offensive TDs / points
RUSH_TD_SHARE = 0.385      # [F] share of offensive TDs that are rushing
# per-catch yards (gamma) by position: mean, sd  (H; refit from pbp)
CATCH_YDS = {"WR": (12.5, 10.5), "TE": (10.5, 8.5), "RB": (7.5, 7.5)}
CARRY_YDS_BIG = (0.043, 24.4)  # [F] 4.3% of carries go 15+, averaging 24.4 (15 + exponential 9.4); rest ~ Normal(core, CARRY_SD)
CARRY_SD = 3.6             # [F] sd of non-explosive carries
WEATHER_PASS_YDS = {"calm": 1.0, "wind12": 0.916, "wind15": 0.93, "wind20": 0.907, "rain": 0.85}  # [S]/[C] Sharp
