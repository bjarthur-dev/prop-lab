"""Price a props board against the projections and apply System/Rules.md (pass rule, blend, caps)."""
import numpy as np
import pandas as pd
import config as C
from common import american_to_dec, implied, devig, norm_name
from model import simulate

MARKETS = {"pts": "pts", "points": "pts", "reb": "reb", "rebounds": "reb", "ast": "ast", "assists": "ast",
           "fg3m": "fg3m", "threes": "fg3m", "pra": "pra", "pr": "pr", "pa": "pa", "ra": "ra"}


def p_over(sim, market, line):
    return float((sim[market] > line).mean())


def market_mult(row, vmr, market, line, p_target):
    """Find the mean multiplier that makes the model's P(over) equal the market's (for blending means)."""
    lo, hi = 0.5, 1.6
    for _ in range(18):
        mid = (lo + hi) / 2
        if p_over(simulate(row, vmr, n=6000, mult=mid), market, line) < p_target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def shadow_offset(path="data/shadow/nba_graded.csv"):
    """v1.5 level correction learned from shadow grading: how far the model's P(over) has run below/above the actual
    over hit rate, shrunk by n/(n+SHADOW_PRIOR_N). Pooled across markets (per-market estimates are too noisy yet).
    Returns (offset, n). The model's ranking is kept; only its level is corrected."""
    import os
    if not os.path.exists(path):
        return 0.0, 0
    g = pd.read_csv(path)
    g = g[(g.get("status") == "graded") & g["hit"].notna() & g["p_model"].notna()]
    n = len(g)
    if n < C.SHADOW_MIN_ROWS:
        return 0.0, n
    raw = float(g["hit"].mean() - g["p_model"].mean())
    return raw * n / (n + C.SHADOW_PRIOR_N), n


def price_board(proj, board, vmr, slate_class="large"):
    """board columns: player, market, line, book, over, under, executable (bool), ts"""
    off, n_shadow = shadow_offset()
    board = board.copy()
    board["key"] = board["player"].map(norm_name)
    board["mk"] = board["market"].str.lower().map(MARKETS)
    proj = proj.set_index("key")
    out, cache = [], {}
    for (key, mk, line), grp in board.dropna(subset=["mk"]).groupby(["key", "mk", "line"]):
        if key not in proj.index:
            out.append({"player": grp["player"].iloc[0], "market": mk, "line": line, "decision": "PASS", "why": "no projection (not in rotation / name mismatch)"})
            continue
        row = proj.loc[key]
        if key not in cache:
            cache[key] = simulate(row, vmr, seed=abs(hash(key)) % 2**31)
        po_raw = p_over(cache[key], mk, line)
        po = float(np.clip(po_raw + off, 0.02, 0.98))
        two = grp.dropna(subset=["over", "under"])
        if two.empty:
            continue
        ex = grp[grp["executable"].astype(str).str.lower().isin(["true", "1", "yes"])]
        for side in ("over", "under"):
            best = ex.dropna(subset=[side])
            if best.empty:
                continue
            b = best.loc[best[side].map(american_to_dec).idxmax()]
            refs = two[two["book"] != b["book"]]
            refs = refs if len(refs) else two          # sharp consensus excludes the book we'd bet into
            p_mkt = float(np.median([devig(o, u) for o, u in zip(refs["over"], refs["under"])]))
            pm = po if side == "over" else 1 - po
            pk = p_mkt if side == "over" else 1 - p_mkt
            be = implied(b[side])
            shrunk = C.SHRINK_EDGE * (pm - be) * 100
            gap = (pm - pk) * 100
            mkt_edge = (pk - be) * 100
            rec = {"player": row["player"], "team": row["team"], "opp": row["opp"], "market": mk, "line": line, "side": side,
                   "book": b["book"], "price": b[side], "ts": b.get("ts", ""), "min_proj": round(row["min_proj"], 1),
                   "mu": round(float(np.mean(cache[key][mk])), 2), "p_model": round(pm, 3), "p_model_raw": round(po_raw if side == "over" else 1 - po_raw, 3), "shadow_offset": round(off, 3), "p_market": round(pk, 3),
                   "n_ref_books": int(len(refs)), "break_even": round(be, 3),
                   "ev_model_pct": round((pm * american_to_dec(b[side]) - 1) * 100, 1),
                   "shrunk_edge_pts": round(shrunk, 2), "model_vs_market_pts": round(gap, 1), "market_edge_pts": round(mkt_edge, 1)}
            model_path = shrunk >= C.PAPER_SHRUNK_EDGE_PTS and gap > 0
            market_path = mkt_edge >= 1.0 and (pm - be) * 100 >= -C.MODEL_VETO_PTS
            if model_path or market_path:
                c_m = market_mult(row, vmr, mk, line, p_mkt)
                c_b = C.MARKET_WEIGHT * c_m + (1 - C.MARKET_WEIGHT) * 1.0
                pb = p_over(simulate(row, vmr, n=8000, mult=c_b), mk, line)
                pb = pb if side == "over" else 1 - pb
                rec["p_blend"] = round(pb, 3)
                blend_ok = (pb - be) * 100 >= C.MIN_BLEND_OVER_BE_PTS
                too_big = gap > C.MAX_MODEL_VS_MARKET_PTS
                full_model = (shrunk >= C.MIN_SHRUNK_EDGE_PTS and gap >= C.MIN_MODEL_VS_MARKET_PTS and not too_big and blend_ok)
                full_market = (mkt_edge >= C.MIN_STALE_EDGE_PTS and len(refs) >= C.MIN_REF_BOOKS and blend_ok)
                full = full_model or full_market
                rec["decision"] = ("BET" if C.LIVE else "PAPER") if full else "WATCH"
                rec["blend_edge_pts"] = round((pb - be) * 100, 2)
                rec["path"] = "model" if full_model else "stale price" if full_market else ""
                rec["why"] = ("clears Rules §3 (model edge)" if full_model else
                              "clears Rules §3 (stale price vs sharp consensus)" if full_market else
                              "model-market gap >10 pts: likely missing info, investigate" if too_big else
                              "edge below the Rules §3 bar")
            else:
                rec["decision"], rec["why"] = "PASS", "no edge"
            out.append(rec)
    res = pd.DataFrame(out)
    return apply_caps(res, slate_class)


def apply_caps(res, slate_class):
    if res.empty or "decision" not in res:
        return res
    res["stake_pct"] = 0.0
    take = res[res["decision"].isin(["BET", "PAPER"])].sort_values("blend_edge_pts", ascending=False)
    used_game, used_player, total = {}, {}, 0.0
    cap = C.SLATE_CAP.get(slate_class, 5.0)
    for i, r in take.iterrows():
        game = "-".join(sorted([str(r["team"]), str(r["opp"])]))
        if (used_game.get(game, 0) + C.UNIT_PCT > C.PER_GAME_CAP or used_player.get(r["player"], 0) + C.UNIT_PCT > C.PER_PLAYER_CAP
                or total + C.UNIT_PCT > cap or ((res["player"] == r["player"]) & (res["market"] == r["market"]) & (res["stake_pct"] > 0)).any()):
            res.loc[i, ["decision", "why"]] = ["PASS", "cap reached (game/player/slate) or opposite side held"]
            continue
        res.loc[i, "stake_pct"] = C.UNIT_PCT
        used_game[game] = used_game.get(game, 0) + C.UNIT_PCT
        used_player[r["player"]] = used_player.get(r["player"], 0) + C.UNIT_PCT
        total += C.UNIT_PCT
    return res
