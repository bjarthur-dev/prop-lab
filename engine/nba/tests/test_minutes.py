"""Regression tests for the two v1 minutes bugs. Run: python engine/nba/tests/test_minutes.py"""
import os, sys
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import config as C
from model import project_game

POS = ["G", "G-F", "F", "C", "F-C", "G", "F", "C", "G", "F"]
def team(name, mins, keys):
    return pd.DataFrame({"player_id": range(len(mins)), "player": keys, "key": keys, "team": name, "min_base": mins, "pos": POS,
                         "sd_min": 5.5, "pts_pm": 0.5, "reb_pm": 0.2, "ast_pm": 0.1, "fg3m_pm": 0.05})

mins = [34, 33, 31, 30, 28, 22, 20, 18, 14, 11]
keys = ["star1", "star2", "wing", "c_start", "pf", "g6", "w7", "c_backup", "g9", "f10"]
base = pd.concat([team("HOM", mins, keys), team("AWY", mins, [k + "_a" for k in keys])], ignore_index=True)

def get(df, k): return float(df.loc[df["key"] == k, "min_proj"].iloc[0])

# 1) blowout: at -9.5 each starter should lose the full rule amount (0.875), not ~0.26
pk = project_game(base, "HOM", "AWY", 0.0, 230.0, league_total=230)
bl = project_game(base, "HOM", "AWY", -9.5, 230.0, league_total=230)
loss = get(pk, "star1") - get(bl, "star1")
want = (9.5 - C.BLOWOUT_START) * C.BLOWOUT_MIN_PER_PT
print(f"blowout -9.5: star1 loses {loss:.2f} min (rule says {want:.3f})"); assert abs(loss - want) < 0.05
tot = bl[bl.team == "HOM"]["min_proj"].sum(); print(f"team minutes {tot:.1f}"); assert abs(tot - C.TEAM_MINUTES) < 0.2

# 2) starting C out: backup C should absorb most of the 30 minutes; stars rise little
out = project_game(base, "HOM", "AWY", 0.0, 230.0, out_keys={"c_start"}, league_total=230)
d_back, d_star = get(out, "c_backup") - get(pk, "c_backup"), get(out, "star1") - get(pk, "star1")
print(f"C out: c_backup {get(pk,'c_backup'):.1f} -> {get(out,'c_backup'):.1f} (+{d_back:.1f}); star1 +{d_star:.2f}")
assert d_back >= 12 and d_star <= C.STARTER_HEADROOM + 0.01

# 3) min_set: confirmed replacement starter at 28
ms = project_game(base, "HOM", "AWY", 0.0, 230.0, out_keys={"c_start"}, min_set={"c_backup": 28.0}, league_total=230)
print(f"min_set: c_backup {get(ms,'c_backup'):.1f}, star1 {get(ms,'star1'):.1f}"); assert abs(get(ms, "c_backup") - 28) < 0.01
print("ALL MINUTES TESTS PASSED")
