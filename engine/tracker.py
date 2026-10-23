"""Grade the zero-stake mechanism tracker.  python engine/tracker.py
Reads Record/mechanism_tracker.csv. For each hypothesis: n, hit rate, mean market p, edge = hit - p_market,
the matched CONTROL arm's edge for the same hypothesis, net = edge - control edge, and a game-clustered SE.
Until a hypothesis has controls, it is graded against the documented side bias (unders ~+1.5 pts, overs ~-1.5 pts,
SickFade 396k NBA props at close) so an under theory doesn't get credit for 'unders lose less'."""
import numpy as np, pandas as pd
SIDE_BIAS = {"under": 0.015, "over": -0.015}

def clustered_se(df):
    g = df.groupby("game")["resid"].sum()
    n = len(df)
    return float(np.sqrt((g ** 2).sum()) / n) if n > 1 else float("nan")

def main(path="Record/mechanism_tracker.csv"):
    d = pd.read_csv(path)
    d = d[d["hit"].astype(str).isin(["0", "1", "0.0", "1.0"])].copy()
    if d.empty:
        print("no graded rows yet"); return
    d["hit"] = d["hit"].astype(float); d["arm"] = d.get("arm", "hyp").fillna("hyp")
    d["hyp_id"] = d.get("hyp_id", d["hypothesis"].str.split().str[0]).fillna(d["hypothesis"].str.split().str[0])
    d["resid"] = d["hit"] - d["p_market_side"]
    rows = []
    for h, g in d.groupby("hyp_id"):
        hyp, ctl = g[g["arm"] == "hyp"], g[g["arm"] == "control"]
        edge = hyp["resid"].mean() if len(hyp) else np.nan
        base = ctl["resid"].mean() if len(ctl) else hyp["side"].map(SIDE_BIAS).mean()
        rows.append(dict(hyp=h, n=len(hyp), n_control=len(ctl), hit=round(hyp["hit"].mean(), 3), p_mkt=round(hyp["p_market_side"].mean(), 3),
                         edge_pts=round(100 * edge, 1), baseline_pts=round(100 * base, 1), net_pts=round(100 * (edge - base), 1),
                         se_pts=round(100 * clustered_se(hyp), 1), baseline="control arm" if len(ctl) else "side-bias prior"))
    out = pd.DataFrame(rows)
    print(out.to_string(index=False))
    print("\nRead: |net| < 2*se is noise. ~150 entries -> +/-4 pts; a real 5-pt edge needs ~400, 3-pt ~1,100.")
    return out

if __name__ == "__main__":
    main()
