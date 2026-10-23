"""Walk-forward backtest on real logs (run on your PC after fetch.py):  python engine/nba/backtest.py
For every 7th game date from Dec 1 on, project each player's points/rebounds/assists from games BEFORE that date only,
then compare to what happened. Reports MAE vs a naive season-average baseline and calibration of P(over) at the naive line.
Use it to tune HL_RATES / SHRINK_MIN / HL_MINUTES in config.py: lower MAE and calibration gaps near 0 win."""
import os, sys, glob
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
import config as C
from model import load_logs, player_baselines, fit_vmr
from common import nb_draw

def main(season_file=f"{C.DATA_DIR}/players_{C.SEASON_PRIOR}.csv", season_id=None):
    logs = load_logs([season_file]); season_id = season_id or str(logs["season_id"].iloc[0])
    vmr = fit_vmr(logs); rng = np.random.default_rng(1)
    dates = sorted(d for d in logs["game_date"].unique() if pd.Timestamp(d) >= pd.Timestamp(logs["game_date"].min()) + pd.Timedelta(days=40))[::7]
    rows = []
    for d in dates:
        base, _ = player_baselines(logs, d, season_id)
        day = logs[logs["game_date"] == d].merge(base, on="player_id", suffixes=("", "_b"))
        hist = logs[logs["game_date"] < d].groupby("player_id")[["pts", "reb", "ast", "min"]].mean().add_suffix("_naive")
        day = day.join(hist, on="player_id").dropna(subset=["pts_naive"])
        day = day[day["min_base"] >= 15]
        for s in ("pts", "reb", "ast"):
            mu = day[f"{s}_pm"] * day["min_base"]
            line = np.floor(day[f"{s}_naive"]) + 0.5
            mins = np.clip(rng.normal(day["min_base"].values[:, None], day["sd_min"].values[:, None], (len(day), 4000)), 0, 48)
            sims = nb_draw(rng, (day[f"{s}_pm"].values[:, None] * mins), vmr[s])
            p = (sims > line.values[:, None]).mean(axis=1)
            rows.append(pd.DataFrame({"stat": s, "date": d, "actual": day[s].values, "proj": mu.values, "naive": day[f"{s}_naive"].values,
                                      "p_over": p, "hit": (day[s].values > line.values).astype(int)}))
    r = pd.concat(rows)
    print(f"backtest rows: {len(r)} over {len(dates)} dates | VMR {vmr}")
    for s, g in r.groupby("stat"):
        mae_m, mae_n = (g.actual - g.proj).abs().mean(), (g.actual - g.naive).abs().mean()
        brier = ((g.p_over - g.hit) ** 2).mean(); brier_flat = ((g.hit.mean() - g.hit) ** 2).mean()
        print(f"\n{s}: MAE model {mae_m:.2f} vs naive {mae_n:.2f} ({(1-mae_m/mae_n)*100:+.1f}%) | Brier {brier:.4f} vs flat {brier_flat:.4f}")
        g = g.assign(bin=pd.cut(g.p_over, [0, .35, .45, .55, .65, 1]))
        print(g.groupby("bin", observed=True).agg(pred=("p_over", "mean"), actual=("hit", "mean"), n=("hit", "size")).round(3).to_string())
    os.makedirs(C.OUT_DIR, exist_ok=True); r.to_csv(f"{C.OUT_DIR}/backtest_{C.SEASON_PRIOR}.csv", index=False)

if __name__ == "__main__":
    main()
