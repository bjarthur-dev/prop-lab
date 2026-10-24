"""Sanity tests for NFL engine v1.  python engine/nfl/tests/test_nfl.py"""
import os, sys
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model import team_volume, simulate_game

rng = np.random.default_rng(0)
fav, dog = team_volume(rng, -7.0, 44), team_volume(rng, +7.0, 44)
d = dog["attempts"].mean() - fav["attempts"].mean()
print(f"pass attempts: 7-pt dog {dog['attempts'].mean():.1f} vs 7-pt fav {fav['attempts'].mean():.1f} (diff {d:.1f}; real 2023-26: +0.9)"); assert 0 < d < 4
print(f"rushes: fav {fav['rushes'].mean():.1f} vs dog {dog['rushes'].mean():.1f}"); assert fav["rushes"].mean() > dog["rushes"].mean()
shares = pd.DataFrame([
    dict(player="WR1", team="HOU", pos="WR", tgt_share=0.27, catch_rate=0.66, ez_tgt_share=0.25),
    dict(player="RB1", team="HOU", pos="RB", tgt_share=0.10, catch_rate=0.78, carry_share=0.62, ypc_rush=4.3, rz_carry_share=0.60, ez_tgt_share=0.08),
    dict(player="TE1", team="NYG", pos="TE", tgt_share=0.18, catch_rate=0.70, ez_tgt_share=0.15)])
r = simulate_game(dict(home="HOU", away="NYG", spread_home=-9.5, total=42.5), shares)
wr = r["WR1"]["rec_yds"]; print(f"WR1 rec yds mean {wr.mean():.1f} median {np.median(wr):.1f}"); assert wr.mean() > np.median(wr)
rb = r["RB1"]; p_td = (rb["td"] > 0).mean(); print(f"RB1 carries {rb['carries'].mean():.1f}, rush yds {rb['rush_yds'].mean():.1f}, P(ATD) {p_td:.3f} (lambda {rb['td_lambda']:.2f})")
assert 0.40 < p_td < 0.70
lr = r["WR1"]["longest_rec"]; print(f"WR1 longest rec median {np.median(lr):.1f}")
print("ALL NFL TESTS PASSED")
