"""Build engine/out/DATE/nfl_shares.csv for a slate from nflverse pbp (v1.1 fitted weights).
    python engine/nfl/build_shares.py 2026-10-25 --season 2026 --week 7
Optional engine/out/DATE/nfl_out.csv (column: player, using pbp names like "J.Chase" or full names) = OUT players:
they are dropped and their target/carry shares are handed to teammates in proportion to existing shares (v1.1 simple rule).
Run fetch_nfl.py first each week so the latest games are in."""
import os, sys, argparse, re
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shares as S

def key(n):  # "Ja'Marr Chase" / "J.Chase" -> "jchase"
    n = re.sub(r"[^a-z. ]", "", str(n).lower()).replace(" jr", "").replace(" sr", "").strip()
    parts = re.split(r"[. ]+", n); parts = [p for p in parts if p]
    return (parts[0][0] + "".join(parts[1:])) if len(parts) > 1 else n

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("date"); ap.add_argument("--season", type=int, required=True)
    ap.add_argument("--week", type=int, required=True); A = ap.parse_args()
    out = f"engine/out/{A.date}"; os.makedirs(out, exist_ok=True)
    S.build(); f = S.features(A.season, A.week)
    last = S.pg[S.pg.season == A.season].groupby("pid").week.max()
    f["last_week"] = last.reindex(f.index)
    f = f[(f.n_cur >= 1) & ((f.tgt_share >= 0.05) | (f.carry_share >= 0.15))].copy()
    team_last = S.pg[(S.pg.season == A.season) & (S.pg.week < A.week)].groupby("posteam").week.max()
    f["missed_last"] = f.last_week < f.team.map(team_last)   # flag: absent from his team's last game (injury/benched), byes excluded
    f["key"] = f["name"].map(key)
    outp = f"{out}/nfl_out.csv"
    if os.path.exists(outp):
        outs = set(pd.read_csv(outp)["player"].map(key))
        hit = f[f.key.isin(outs)]
        print("OUT applied:", ", ".join(hit["name"]) or "none matched")
        for team, grp in hit.groupby("team"):
            keep = (f.team == team) & ~f.key.isin(outs)
            for col in ("tgt_share", "carry_share", "rz_carry_share", "ez_tgt_share"):
                lost, have = grp[col].sum(), f.loc[keep, col].sum()
                if have > 0: f.loc[keep, col] = (f.loc[keep, col] * (1 + lost / have)).clip(upper=0.45)
        f = f[~f.key.isin(outs)]
    cols = ["name", "team", "pos", "tgt_share", "catch_rate", "ypc", "carry_share", "ypc_rush", "rz_carry_share", "ez_tgt_share", "n_cur", "last_week", "missed_last"]
    r = f.reset_index()[["pid"] + cols].rename(columns={"name": "player"})
    r.loc[r.carry_share < 0.05, "carry_share"] = 0
    r.to_csv(f"{out}/nfl_shares.csv", index=False, float_format="%.4f")
    print(f"wrote {out}/nfl_shares.csv: {len(r)} players, {r.team.nunique()} teams; {int(r.missed_last.sum())} flagged missed_last (check injury report)")

if __name__ == "__main__": main()
