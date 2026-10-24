"""NFL engine v1 tunables. (H) = heuristic to refit on 2023-25 nflverse data; [S] = sourced (see Research - Advanced NFL and MLB mechanisms)."""
N_SIMS = 20000
PLAYS_BASE = 63.0          # (H) offensive plays per team-game at a 44 total
PLAYS_PER_TOTAL_PT = 0.25  # (H) extra plays per point of total above 44
PLAYS_SD = 6.0             # (H)
MARGIN_SD = 13.5           # (H) final margin ~ Normal(-spread, 13-14)
BASE_PASS_RATE = 0.585     # (H) league dropback rate incl. sacks/scrambles
PROE_WEIGHT_CUR = 0.5      # [I] 50/50 current-season vs prior PROE at weeks 6-8
SPREAD_PASS_SLOPE = 0.005  # [S] ~+0.5 pp pass rate per point of spread (underdog throws more)
SCRIPT_K = 0.07            # (H) in-game script: pass rate shift per 14 pts of realized margin vs expectation
PASS_RATE_CLIP = (0.40, 0.78)
SACK_RATE = 0.065          # (H) league sacks per dropback; per-QB override
SCRAMBLE_RATE = 0.04       # (H) per-QB override
SHARE_CONC = 40.0          # (H) Beta concentration for game-to-game share variation (lower = noisier)
TD_PTS_SHARE = 0.70        # (H) share of points from offensive TDs (rest FG/XP/def)
RUSH_TD_SHARE = 0.42       # (H) league share of offensive TDs that are rushing
# per-catch yards (gamma) by position: mean, sd  (H; refit from pbp)
CATCH_YDS = {"WR": (12.5, 10.5), "TE": (10.5, 8.5), "RB": (7.5, 7.5)}
CARRY_YDS_BIG = (0.07, 18.0)  # (H) 7% of carries are explosive, exponential mean 18 yds; rest ~ Normal(ypc_core, 3)
WEATHER_PASS_YDS = {"calm": 1.0, "wind12": 0.916, "wind15": 0.93, "wind20": 0.907, "rain": 0.85}  # [S]/[C] Sharp
