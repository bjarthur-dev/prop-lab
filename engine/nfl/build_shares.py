"""Build engine/out/DATE/nfl_shares.csv for a slate from nflverse pbp (v1.1 fitted weights).
    python engine/nfl/build_shares.py 2026-10-25 --season 2026 --week 7
Optional engine/out/DATE/nfl_out.csv (columns: player[, team], using pbp names like "J.Chase" or full names) = OUT players:
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
    ap.add_argument("--week", type=int, required=True)
    ap.add_argument("--board", default=None, help="today's prop board CSV(s) (glob) with a player column; default data/odds/nfl/DATE/board_*.csv")
    A = ap.parse_args()
    out = f"engine/out/{A.date}"; os.makedirs(out, exist_ok=True)
    S.build(); f = S.features(A.season, A.week)
    cur = S.pg[(S.pg.season == A.season) & (S.pg.week < A.week)]
    last = cur.groupby("pid").week.max()
    f["last_week"] = last.reindex(f.index)
    team_weeks = cur.groupby("posteam").week.apply(lambda w: sorted(set(w)))
    f["games_missed"] = [sum(1 for w in team_weeks.get(t, []) if pd.isna(lw) or w > lw) for t, lw in zip(f.team, f.last_week)]
    f["missed_last"] = f["games_missed"] > 0          # absent from his team's most recent game(s); byes don't count
    # v1.2 availability: sportsbooks only post props for players expected to play, so today's board is an availability signal
    import glob as _g
    bfiles = _g.glob(A.board) if A.board else _g.glob(f"data/odds/nfl/{A.date}/board_*.csv") + _g.glob(f"{out}/nfl_board.csv")
    def parts(n):
        n = re.sub(r"[^a-z. ]", "", str(n).lower()).replace(" jr", "").replace(" sr", "").replace(" iii", "").replace(" ii", "").strip()
        p = [x for x in re.split(r"[. ]+", n) if x]; return (p[0], "".join(p[1:])) if len(p) > 1 else (n, n)
    board_names = set()
    for bf in bfiles:
        try: board_names |= set(pd.read_csv(bf)["player"].dropna().astype(str).str.split("|").str[0])
        except Exception: pass
    bparts = [parts(n) for n in board_names]
    fp = f["name"].map(parts)
    f["on_board"] = [any(b[1] == t[1] and b[0].startswith(t[0]) for b in bparts) for t in fp] if bparts else False
    stale = (f.games_missed >= 2) & ~f.on_board              # e.g. IR: missed 2+ team games and no props today
    returning = (f.n_cur == 0) & f.on_board                  # e.g. back from injury: props today, no game yet this season
    print(f"availability: board names {len(board_names)}; dropped stale {int(stale.sum())}: " + ", ".join(f[stale & ((f.tgt_share >= .08) | (f.carry_share >= .2))]["name"] + "(" + f[stale & ((f.tgt_share >= .08) | (f.carry_share >= .2))]["team"] + ")"))
    print("returning (board, no 2026 game): " + ", ".join(f[returning & ((f.tgt_share >= .05) | (f.carry_share >= .15))]["name"] + "(" + f[returning & ((f.tgt_share >= .05) | (f.carry_share >= .15))]["team"] + ")"))
    for col in ("tgt_share", "carry_share", "rz_carry_share", "ez_tgt_share"):
        f.loc[returning, col] = f.loc[returning, col] * 0.8      # ramp-up haircut for a returning player
    f = f[~stale & ((f.n_cur >= 1) | returning) & ((f.tgt_share >= 0.05) | (f.carry_share >= 0.15))].copy()
    # returning players take their share from teammates (whose recent shares were built without them)
    for team in f[f.n_cur == 0]["team"].unique():
        ret = (f.team == team) & (f.n_cur == 0); oth = (f.team == team) & (f.n_cur > 0)
        for col in ("tgt_share", "carry_share", "rz_carry_share", "ez_tgt_share"):
            S_, r = f.loc[oth, col].sum(), f.loc[ret, col].sum()
            if S_ > 0: f.loc[oth, col] *= max(0.5, (S_ - r) / S_)
    f["key"] = f["name"].map(key)
    outp = f"{out}/nfl_out.csv"
    if os.path.exists(outp):
        o = pd.read_csv(outp)
        # match last name (+ team when given) and require the full first name to start with the pbp initials:
        # key() alone collides ("Brian Robinson" and "Bi.Robinson" both -> "brobinson")
        def parts(n):
            n = re.sub(r"[^a-z. ]", "", str(n).lower()).replace(" jr", "").replace(" sr", "").strip()
            p = [x for x in re.split(r"[. ]+", n) if x]; return (p[0], "".join(p[1:])) if len(p) > 1 else (n, n)
        fp = f["name"].map(parts); f["_m"] = False
        for _, row in o.iterrows():
            first, last = parts(row["player"])
            m = fp.map(lambda t: t[1] == last and first.startswith(t[0]))
            if "team" in o.columns and isinstance(row.get("team"), str): m &= f["team"].astype(str) == row["team"]
            f.loc[m, "_m"] = True
        outs = {True}
        hit = f[f._m]
        print("OUT applied:", ", ".join(hit["name"] + " (" + hit["team"] + ")") or "none matched")
        # v1.2: only a FRESH absence frees targets/carries; if he already missed games, teammates' recent shares reflect it
        for team, grp in hit[hit.games_missed == 0].groupby("team"):
            keep = (f.team == team) & ~f._m
            for col in ("tgt_share", "carry_share", "rz_carry_share", "ez_tgt_share"):
                lost, have = grp[col].sum(), f.loc[keep, col].sum()
                cap = 0.45 if "tgt" in col else 0.75   # targets cap at 45%; carry shares (of all team rushes) top out near 75%
                if have > 0:   # never cut an existing share (the old flat 0.45 clip cut RB1 carry shares, e.g. 0.65 -> 0.45)
                    cur = f.loc[keep, col]; f.loc[keep, col] = np.maximum(cur, (cur * (1 + lost / have)).clip(upper=cap))
        f = f[~f._m]
    cols = ["name", "team", "pos", "tgt_share", "catch_rate", "ypc", "carry_share", "ypc_rush", "rz_carry_share", "ez_tgt_share", "n_cur", "last_week", "missed_last", "games_missed", "on_board"]
    r = f.reset_index()[["pid"] + cols].rename(columns={"name": "player"})
    r.loc[r.carry_share < 0.05, "carry_share"] = 0
    r.to_csv(f"{out}/nfl_shares.csv", index=False, float_format="%.4f")
    print(f"wrote {out}/nfl_shares.csv: {len(r)} players, {r.team.nunique()} teams; {int(r.missed_last.sum())} flagged missed_last (check injury report)")

if __name__ == "__main__": main()
