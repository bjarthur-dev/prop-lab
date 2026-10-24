"""Player shares from nflverse pbp (shared by backtest.py and build_shares.py). Defaults fitted in the v1.1 backtest:
recency half-life 3 games, prior season weight 0.1 per game."""
import numpy as np, pandas as pd
from calibrate import load, team_games
HL, PRIOR_W = 3.0, 0.1

def build(years=(2023, 2024, 2025, 2026)):
    global pg, TGT_PER_ATT
    d = load(years); tg = team_games(d)
    p = d[(d.two_point_attempt != 1) & (d.qb_kneel != 1) & (d.qb_spike != 1) & d.play_type.isin(["pass", "run"])].copy()
    p["rz"] = p.yardline_100 <= 10
    des_run = p[(p.play_type == "run") & (p.qb_scramble != 1) & p.rusher_player_id.notna()]
    tgts = p[(p.play_type == "pass") & p.receiver_player_id.notna()]
    team_rz_car = des_run[des_run.rz].groupby(["game_id", "posteam"]).size().rename("t_rz_car")
    team_rz_tgt = tgts[tgts.rz].groupby(["game_id", "posteam"]).size().rename("t_rz_tgt")
    rec = tgts.groupby(["game_id", "posteam", "receiver_player_id"]).agg(name=("receiver_player_name", "first"),
          targets=("pass_attempt", "size"), receptions=("complete_pass", "sum"), rec_yds=("receiving_yards", "sum"),
          rz_tgt=("rz", "sum")).reset_index().rename(columns={"receiver_player_id": "pid"})
    ru = des_run.groupby(["game_id", "posteam", "rusher_player_id"]).agg(rname=("rusher_player_name", "first"),
          carries=("rush_attempt", "size"), rush_yds=("rushing_yards", "sum"), rz_car=("rz", "sum")).reset_index().rename(columns={"rusher_player_id": "pid"})
    pg = rec.merge(ru, on=["game_id", "posteam", "pid"], how="outer")
    pg["name"] = pg.name.fillna(pg.rname); pg = pg.drop(columns="rname").fillna({c: 0 for c in ["targets", "receptions", "rec_yds", "rz_tgt", "carries", "rush_yds", "rz_car"]})
    td = d[d.td_player_id.notna() & (d.touchdown == 1) & ((d.rush_touchdown == 1) | (d.pass_touchdown == 1))]
    tdc = td.groupby(["game_id", "td_player_id"]).size().rename("tds").reset_index().rename(columns={"td_player_id": "pid"})
    pg = pg.merge(tdc, on=["game_id", "pid"], how="left").fillna({"tds": 0})
    pg = pg.merge(tg[["game_id", "posteam", "season", "week", "att", "rushes", "team_spread", "total", "home", "away", "spread_line"]], on=["game_id", "posteam"])
    pg = pg.merge(team_rz_car, on=["game_id", "posteam"], how="left").merge(team_rz_tgt, on=["game_id", "posteam"], how="left").fillna({"t_rz_car": 0, "t_rz_tgt": 0})
    # a pass target counts against aimed attempts; use team targets as the share denominator (throwaways excluded)
    team_tgt = tgts.groupby(["game_id", "posteam"]).size().rename("t_tgt")
    pg = pg.merge(team_tgt, on=["game_id", "posteam"], how="left")
    TGT_PER_ATT = (tgts.groupby(["game_id", "posteam"]).size().sum() / tg.att.sum())

    return pg

def features(s, w, hl=HL, prior_w=PRIOR_W):
    h = pg[((pg.season == s) & (pg.week < w)) | (pg.season == s - 1)].copy()
    cur = h.season == s
    h["wt"] = np.where(cur, 0.5 ** ((w - h.week) / hl), prior_w)
    agg = lambda c: (h[c] * h.wt)
    h["w_tg"], h["w_ttg"], h["w_car"], h["w_tr"] = agg("targets"), agg("t_tgt"), agg("carries"), agg("rushes")
    h["w_rzc"], h["w_trzc"], h["w_rzt"], h["w_trzt"] = agg("rz_car"), agg("t_rz_car"), agg("rz_tgt"), agg("t_rz_tgt")
    f = h.groupby("pid").agg(name=("name", "last"), team=("posteam", "last"), n_cur=("season", lambda x: (x == s).sum()),
        w_tg=("w_tg", "sum"), w_ttg=("w_ttg", "sum"), w_car=("w_car", "sum"), w_tr=("w_tr", "sum"),
        w_rzc=("w_rzc", "sum"), w_trzc=("w_trzc", "sum"), w_rzt=("w_rzt", "sum"), w_trzt=("w_trzt", "sum"),
        tg=("targets", "sum"), rc=("receptions", "sum"), ry=("rec_yds", "sum"), car=("carries", "sum"), rsy=("rush_yds", "sum"),
        cur_rec_yds=("rec_yds", lambda x: x[h.loc[x.index, "season"] == s].mean()),
        cur_rush_yds=("rush_yds", lambda x: x[h.loc[x.index, "season"] == s].mean()),
        cur_rec=("receptions", lambda x: x[h.loc[x.index, "season"] == s].mean()),
        cur_car=("carries", lambda x: x[h.loc[x.index, "season"] == s].mean()))
    f["tgt_share"] = f.w_tg / f.w_ttg.clip(lower=1e-9) * TGT_PER_ATT       # targets per aimed attempt
    f["carry_share"] = f.w_car / f.w_tr.clip(lower=1e-9)
    f["catch_rate"] = (f.rc + 0.65 * 40) / (f.tg + 40)
    f["ypc"] = (f.ry + 10.9 * 30) / (f.rc + 30)
    f["ypc_rush"] = (f.rsy + 4.2 * 60) / (f.car + 60)
    f["rz_carry_share"] = (f.w_rzc + 0.5 * f.carry_share) / (f.w_trzc + 0.5)
    f["ez_tgt_share"] = (f.w_rzt + 0.5 * f.tgt_share) / (f.w_trzt + 0.5)
    f["pos"] = np.where(f.carry_share > 0.25, "RB", "WR")
    return f

