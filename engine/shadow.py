"""Shadow grading: score EVERY priced prop (not just bets) against the result and the market.
    python engine/shadow.py            -> grades all data/shadow/<sport>/*.csv it can, writes Record/Shadow report
NBA results come from engine/data/players_2026-27.csv (refresh with engine/update_nba_data.bat on the laptop).
NFL results come from engine/data/nfl/pbp_2026_slim.csv.gz (refreshed by the cloud results Action).
Questions it answers: does the model beat the market (Brier skill vs devigged market)? Is it calibrated? Where is the lean?
This is the evidence that decides when the model-health gate can relax and when NFL/MLB can go live (Rules §9)."""
import os, sys, glob
import numpy as np, pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "nba"))
from common import norm_name

COL = {"pts": "PTS", "reb": "REB", "ast": "AST", "fg3m": "FG3M"}

def nba_actuals():
    f = "engine/data/players_2026-27.csv"
    if not os.path.exists(f): return None
    d = pd.read_csv(f); d["key"] = d["PLAYER_NAME"].map(norm_name); d["date"] = d["GAME_DATE"].astype(str).str[:10]
    return d

def grade_nba():
    acts = nba_actuals(); rows = []
    for f in sorted(glob.glob("data/shadow/nba/*.csv")):
        s = pd.read_csv(f)
        s = s[(s["side"] == "over") & s["p_model"].notna() & s["p_market"].notna()].copy()
        if "book" in s.columns: s = s[s["book"].astype(str).str.lower().isin(["draftkings", "dk", "fanduel"])].drop_duplicates(["player", "market", "line"])
        s["key"] = s["player"].map(norm_name); date = str(s["date"].iloc[0]) if len(s) else None
        if acts is None or date is None or date > acts["date"].max(): continue      # results not in yet
        a = acts[acts["date"] == date].set_index("key")
        for _, r in s.iterrows():
            col = COL.get(r["market"])
            if col is None: continue
            if r["key"] not in a.index: rows.append(dict(r, actual=np.nan, hit=np.nan, status="DNP/void")); continue
            v = float(a.loc[r["key"], col] if not isinstance(a.loc[r["key"], col], pd.Series) else a.loc[r["key"], col].iloc[0])
            rows.append(dict(r, actual=v, hit=float(v > r["line"]), status="graded"))
    return pd.DataFrame(rows)

def nfl_actuals(season=2026):
    f = f"engine/data/nfl/pbp_{season}_slim.csv.gz"
    if not os.path.exists(f): return None
    d = pd.read_csv(f, low_memory=False)
    d = d[d.play_type.isin(["pass", "run"]) & (d.two_point_attempt != 1)]
    rec = d[d.receiver_player_name.notna()].groupby(["game_date", "posteam", "receiver_player_name"]).agg(
        rec_yds=("receiving_yards", "sum"), receptions=("complete_pass", "sum")).reset_index().rename(columns={"receiver_player_name": "short"})
    ru = d[(d.play_type == "run") & (d.qb_scramble != 1) & d.rusher_player_name.notna()].groupby(["game_date", "posteam", "rusher_player_name"]).agg(
        rush_yds=("rushing_yards", "sum"), carries=("rush_attempt", "size")).reset_index().rename(columns={"rusher_player_name": "short"})
    a = rec.merge(ru, on=["game_date", "posteam", "short"], how="outer").fillna(0)
    a["key"] = a["short"] + "|" + a["posteam"]
    return a, set(d["game_date"].astype(str).unique())

def grade_nfl():
    got = nfl_actuals(); rows = []
    if got is None: return pd.DataFrame()
    acts, dates = got
    for f in sorted(glob.glob("data/shadow/nfl/*.csv")):
        s = pd.read_csv(f)
        s = s[(s["side"] == "over") & s["p_model"].notna() & s["p_market"].notna()].copy()
        if s.empty: continue
        date = str(s["date"].iloc[0])
        if date not in dates: continue                     # game not in pbp yet (refreshed Mon/Tue/Fri)
        if "key" not in s.columns:
            s["key"] = s["player"].astype(str) + "|" + s.get("team", pd.Series("", index=s.index)).astype(str)
        a = acts[acts["game_date"].astype(str) == date].set_index("key")
        played = set(a.index)
        for _, r in s.drop_duplicates(["key", "market", "line"]).iterrows():
            if r["market"] not in ("rec_yds", "rush_yds", "receptions", "carries"): continue
            if r["key"] not in played:
                rows.append(dict(r, actual=np.nan, hit=np.nan, status="DNP/void")); continue
            v = float(a.loc[r["key"], r["market"]]); rows.append(dict(r, actual=v, hit=float(v > r["line"]), status="graded"))
    return pd.DataFrame(rows)

def report(g, sport):
    out = [f"## {sport}"]
    g = g[g["status"] == "graded"].copy()
    if g.empty: return out + ["No graded props yet."]
    g["p_blend"] = g.get("p_blend", 0.75 * g["p_market"] + 0.25 * g["p_model"])
    b = lambda p: float(((g[p] - g["hit"]) ** 2).mean())
    bm, bk, bb = b("p_model"), b("p_market"), b("p_blend")
    out += [f"Graded props: **{len(g)}** over {g['date'].nunique()} day(s). Over hit rate {g['hit'].mean():.3f} vs market's average {g['p_market'].mean():.3f} vs model's {g['p_model'].mean():.3f}.",
            f"Brier: model {bm:.4f} · market {bk:.4f} · blend {bb:.4f} → **model skill vs market {100*(1-bm/bk):+.1f}%**, blend skill {100*(1-bb/bk):+.1f}% (positive = better than the market).",
            "", "| market | n | over hit | market p | model p | model skill vs mkt |", "|---|---:|---:|---:|---:|---:|"]
    for m, x in g.groupby("market"):
        sk = 1 - ((x.p_model - x.hit) ** 2).mean() / ((x.p_market - x.hit) ** 2).mean()
        out.append(f"| {m} | {len(x)} | {x.hit.mean():.3f} | {x.p_market.mean():.3f} | {x.p_model.mean():.3f} | {100*sk:+.1f}% |")
    g["bin"] = pd.cut(g["p_model"], [0, .3, .4, .5, .6, .7, 1])
    out += ["", "Model calibration (P(over)):", "", "| model p bin | n | predicted | actual | market p |", "|---|---:|---:|---:|---:|"]
    for k, x in g.groupby("bin", observed=True):
        out.append(f"| {k} | {len(x)} | {x.p_model.mean():.3f} | {x.hit.mean():.3f} | {x.p_market.mean():.3f} |")
    g["gap"] = g["p_model"] - g["p_market"]
    g["gbin"] = pd.cut(g["gap"], [-1, -.10, -.05, 0, .05, .10, 1])
    out += ["", "Does disagreeing with the market pay? (over hit vs market p, by model−market gap)", "", "| gap bin | n | over hit | market p | hit − market |", "|---|---:|---:|---:|---:|"]
    for k, x in g.groupby("gbin", observed=True):
        out.append(f"| {k} | {len(x)} | {x.hit.mean():.3f} | {x.p_market.mean():.3f} | {100*(x.hit.mean()-x.p_market.mean()):+.1f} pts |")
    se = np.sqrt(0.25 / len(g)) * 100
    out += ["", f"Noise check: with {len(g)} props one standard error on a hit rate is about ±{se:.1f} pts (game clustering makes it larger). Need ~1,500+ graded props before trusting a 2-pt difference."]
    return out

def main():
    os.makedirs("Record/Shadow", exist_ok=True)
    lines = ["---", "tags: [record, shadow]", "---", "", "# Shadow grading: every priced prop vs result and market", "",
             "Written by `engine/shadow.py` (morning settlement runs it). Rules §9 uses this to decide when the model-health gate relaxes and when NFL/MLB go live.", ""]
    g = grade_nba()
    if len(g): g.to_csv("data/shadow/nba_graded.csv", index=False)
    lines += report(g, "NBA") if len(g) else ["## NBA", "No graded props yet (results for the logged dates aren't in engine/data yet)."]
    n = grade_nfl()
    if len(n): n.to_csv("data/shadow/nfl_graded.csv", index=False)
    lines += [""] + (report(n, "NFL") if len(n) else ["## NFL", "No graded props yet (play-by-play for the logged dates isn't in yet; the results Action refreshes it Mon/Tue/Fri)."])
    open("Record/Shadow/Shadow Report.md", "w").write("\n".join(lines) + "\n")
    print("\n".join(lines[8:]))

if __name__ == "__main__": main()
