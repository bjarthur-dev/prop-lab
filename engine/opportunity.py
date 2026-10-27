"""Opportunity report: WHY a stat should happen, per leg, for every sport. Stats come from opportunity:
minutes x role (usage / shares / plate appearances) x pace x game script x who's missing x conditions.
    python engine/opportunity.py nba DATE "Player Name" [...]     (reads engine/out/DATE/outs.csv, data/odds/nba/DATE/games_*.csv)
    python engine/opportunity.py nfl DATE "Player Name" [...]     (reads engine/out/DATE/nfl_shares.csv, nfl_out.csv, nfl_games.csv)
    python engine/opportunity.py mlb DATE "Player Name" [...]     (reads data/results/mlb/*.csv history, data/odds/mlb/DATE/games_*.csv)
Prints a markdown block per player for the card. Pure box-score/odds data: no tracking, on/off or play-by-play yet (stated as gaps)."""
import sys, os, glob
import numpy as np, pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "nba"))
from common import norm_name

# ---------------------------------------------------------------- NBA
def _nba_logs():
    fs = ["engine/data/players_2025-26.csv", "engine/data/players_2026-27.csv"]
    d = pd.concat([pd.read_csv(f).assign(S=("25-26" if "2025" in f else "26-27")) for f in fs if os.path.exists(f)])
    d = d[d.MIN > 0].copy(); d["used"] = d.FGA + 0.44 * d.FTA + d.TOV
    tm = d.groupby(["GAME_ID", "TEAM_ABBREVIATION"]).agg(t_used=("used", "sum"), t_min=("MIN", "sum")).reset_index()
    d = d.merge(tm, on=["GAME_ID", "TEAM_ABBREVIATION"])
    d["usg"] = 100 * (d.used / d.MIN) / (d.t_used / d.t_min) / 5
    d["key"] = d.PLAYER_NAME.map(norm_name); d["date"] = pd.to_datetime(d.GAME_DATE)
    return d

def _nba_game_lines(date):
    fs = sorted(glob.glob(f"data/odds/nba/{date}/games_*.csv"))
    if not fs: return {}
    g = pd.read_csv(fs[-1]); g = g[g.book == "draftkings"]; out = {}
    for (h, a), x in g.groupby(["home", "away"]):
        sp = x[(x.market == "spreads") & (x.name == h)].point; tot = x[x.market == "totals"].point
        out[(h, a)] = (float(sp.iloc[0]) if len(sp) else None, float(tot.iloc[0]) if len(tot) else None)
    return out

NBA_FULL = {"Atlanta Hawks": "ATL", "Boston Celtics": "BOS", "Brooklyn Nets": "BKN", "Charlotte Hornets": "CHA", "Chicago Bulls": "CHI",
    "Cleveland Cavaliers": "CLE", "Dallas Mavericks": "DAL", "Denver Nuggets": "DEN", "Detroit Pistons": "DET", "Golden State Warriors": "GSW",
    "Houston Rockets": "HOU", "Indiana Pacers": "IND", "Los Angeles Clippers": "LAC", "Los Angeles Lakers": "LAL", "Memphis Grizzlies": "MEM",
    "Miami Heat": "MIA", "Milwaukee Bucks": "MIL", "Minnesota Timberwolves": "MIN", "New Orleans Pelicans": "NOP", "New York Knicks": "NYK",
    "Oklahoma City Thunder": "OKC", "Orlando Magic": "ORL", "Philadelphia 76ers": "PHI", "Phoenix Suns": "PHX", "Portland Trail Blazers": "POR",
    "Sacramento Kings": "SAC", "San Antonio Spurs": "SAS", "Toronto Raptors": "TOR", "Utah Jazz": "UTA", "Washington Wizards": "WAS"}

def nba(date, players):
    d = _nba_logs(); lines = _nba_game_lines(date); D = pd.Timestamp(date)
    outs = set(pd.read_csv(f"engine/out/{date}/outs.csv")["player"].map(norm_name)) if os.path.exists(f"engine/out/{date}/outs.csv") else set()
    lg_tot = 2 * pd.read_csv("engine/data/teams_2025-26.csv").PTS.mean() if os.path.exists("engine/data/teams_2025-26.csv") else 230
    blocks = []
    for name in players:
        k = norm_name(name); x = d[(d.key == k) & (d.date < D)].sort_values("date")
        if x.empty: blocks.append(f"### {name}\n- no game logs (rookie/new): opportunity unknown, PASS unless confirmed role"); continue
        team = x.TEAM_ABBREVIATION.iloc[-1]; cur = x[x.S == "26-27"]; pri = x[x.S == "25-26"]
        last5 = x.tail(5)
        b2b = (D - x.date.iloc[-1]).days == 1 if x.S.iloc[-1] == "26-27" else False
        # vacated usage: teammates OUT tonight who played for this team recently
        tmates = d[(d.TEAM_ABBREVIATION == team) & (d.date < D)]
        vac = []
        for kk, g in tmates.groupby("key"):
            if kk in outs and kk != k:
                g = g.sort_values("date").tail(15)
                vac.append((g.PLAYER_NAME.iloc[-1], g.MIN.mean(), g.usg.mean(), g.PTS.mean(), g.AST.mean(), g.REB.mean()))
        vac = sorted(vac, key=lambda v: -v[1] * v[2])[:4]
        vac_usage_min = sum(v[1] * v[2] / 100 for v in vac)
        # with/without: this player's usage/minutes in games where the top vacated teammate did NOT play
        ww = ""
        if vac:
            top = norm_name(vac[0][0])
            tg = set(tmates[tmates.key == top].GAME_ID)
            mine = x[x.TEAM_ABBREVIATION == team]
            wo = mine[~mine.GAME_ID.isin(tg)]; wi = mine[mine.GAME_ID.isin(tg)]
            if len(wo) >= 2 and len(wi) >= 2:
                ww = (f"- **Without {vac[0][0]}** ({len(wo)} g): {wo.MIN.mean():.1f} min, usg {wo.usg.mean():.0f}%, {wo.PTS.mean():.1f} pts / {wo.REB.mean():.1f} reb / {wo.AST.mean():.1f} ast "
                      f"vs with him ({len(wi)} g): {wi.MIN.mean():.1f} min, usg {wi.usg.mean():.0f}%, {wi.PTS.mean():.1f} / {wi.REB.mean():.1f} / {wi.AST.mean():.1f}")
        # game script
        gl = None; opp = None
        for (h, a), v in lines.items():
            if NBA_FULL.get(h) == team or NBA_FULL.get(a) == team:
                home = NBA_FULL.get(h) == team; opp = NBA_FULL.get(a) if home else NBA_FULL.get(h)
                sp = v[0] if home else (-v[0] if v[0] is not None else None); gl = (sp, v[1], home)
        script = ""
        if gl:
            sp, tot, home = gl
            blow = "blowout risk: starters may sit the 4th" if sp is not None and abs(sp) >= 10 else ("close game: full minutes" if sp is not None and abs(sp) <= 4 else "normal")
            pace = "fast/high-scoring" if tot and tot >= lg_tot + 5 else ("slow/low-scoring" if tot and tot <= lg_tot - 5 else "average pace")
            script = f"- **Game script:** {'home' if home else 'away'} vs {opp}, spread {sp:+.1f}, total {tot} → {pace}; {blow}"
        def s(g, lab):
            if g.empty: return f"{lab}: none"
            return (f"{lab}: {len(g)} g, {g.MIN.mean():.1f} min, usg {g.usg.mean():.0f}%, FGA {g.FGA.mean():.1f}, FTA {g.FTA.mean():.1f}, 3PA {g.FG3A.mean():.1f}, "
                    f"{g.PTS.mean():.1f} pts / {g.REB.mean():.1f} reb ({g.OREB.mean():.1f} off) / {g.AST.mean():.1f} ast")
        blk = [f"### {name} ({team})", f"- {s(cur, 'This season')}", f"- {s(pri, 'Last season')}",
               "- Last 5: " + " | ".join(f"{r.date:%m-%d} {r.MIN:.0f}m usg{r.usg:.0f} {int(r.FGA)}fga {int(r.FTA)}fta {int(r.PTS)}p {int(r.REB)}r {int(r.AST)}a" for _, r in last5.fillna(0).iterrows())]
        blk.append(f"- **Out tonight (vacated):** " + ("; ".join(f"{v[0]} {v[1]:.0f} min, usg {v[2]:.0f}%, {v[3]:.1f} pts/{v[4]:.1f} ast/{v[5]:.1f} reb" for v in vac) + f" → ~{vac_usage_min:.1f} usage-minutes freed" if vac else "nobody with recent minutes"))
        if ww: blk.append(ww)
        if b2b: blk.append("- **Back-to-back (2nd night):** minutes/efficiency risk; check for rest")
        if script: blk.append(script)
        blk.append("- Gaps: no on/off lineup data, tracking (touches, potential assists) or coach rotation notes; official starters ~30 min before tip.")
        blocks.append("\n".join(blk))
    return "\n\n".join(blocks)

# ---------------------------------------------------------------- NFL
def nfl(date, players):
    out = f"engine/out/{date}"; blocks = []
    sh = pd.read_csv(f"{out}/nfl_shares.csv") if os.path.exists(f"{out}/nfl_shares.csv") else pd.DataFrame()
    gm = pd.read_csv(f"{out}/nfl_games.csv") if os.path.exists(f"{out}/nfl_games.csv") else pd.DataFrame()
    outs = pd.read_csv(f"{out}/nfl_out.csv") if os.path.exists(f"{out}/nfl_out.csv") else pd.DataFrame(columns=["player", "team"])
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "nfl"))
    for name in players:
        last = name.split()[-1].lower(); r = sh[sh.player.astype(str).str.lower().str.contains(last)] if len(sh) else sh
        if r.empty: blocks.append(f"### {name}\n- not in shares (inactive/IR or name mismatch)"); continue
        r = r.iloc[0]; team = r.team
        g = gm[(gm.home == team) | (gm.away == team)] if len(gm) else gm
        line = ""
        if len(g):
            g = g.iloc[0]; home = g.home == team; sp = g.spread_home if home else -g.spread_home
            imp_pts = (g.total - sp) / 2
            line = (f"- **Game script:** {'home' if home else 'away'}, spread {sp:+.1f}, total {g.total} → implied team points {imp_pts:.1f}; "
                    + ("trailing script → more passing volume" if sp >= 6 else ("leading script → more rushing, fewer late passes" if sp <= -6 else "neutral script"))
                    + f"; weather {g.get('weather', 'calm')}")
        tm_out = outs[outs.get("team", pd.Series(dtype=str)).astype(str) == team]["player"].tolist() if "team" in outs.columns else []
        blocks.append("\n".join([f"### {name} ({team}, {r.pos})",
            f"- **Role:** target share {r.tgt_share:.0%} of throws, catch rate {r.catch_rate:.0%}, {r.ypc:.1f} yds/catch; carry share {r.carry_share:.0%} at {r.ypc_rush:.1f} ypc; "
            f"red-zone carries {r.rz_carry_share:.0%}, end-zone/RZ targets {r.ez_tgt_share:.0%} (recency-weighted, 2026 + 10% of 2025)",
            f"- Games this season {int(r.n_cur)}; missed last team game: {bool(r.missed_last)}" + (f"; games missed {int(r.games_missed)}" if "games_missed" in r else ""),
            f"- **Teammates out:** {', '.join(tm_out) if tm_out else 'none listed'} (fresh absences' shares were redistributed)", line,
            "- Gaps: no route participation / snap counts / coverage data yet."]))
    return "\n\n".join(blocks)

# ---------------------------------------------------------------- MLB
PA_BY_SLOT = {1: 4.65, 2: 4.55, 3: 4.45, 4: 4.35, 5: 4.25, 6: 4.15, 7: 4.05, 8: 3.9, 9: 3.77}
def mlb(date, players, slots=None):
    files = sorted(glob.glob("data/results/mlb/*.csv")); hist = pd.concat([pd.read_csv(f) for f in files]) if files else pd.DataFrame()
    fs = sorted(glob.glob(f"data/odds/mlb/{date}/games_*.csv")); tot = None
    if fs:
        g = pd.read_csv(fs[-1]); t = g[(g.book == "draftkings") & (g.market == "totals")].point
        tot = float(t.iloc[0]) if len(t) else None
    blocks = []
    for i, name in enumerate(players):
        h = hist[hist.player.astype(str).str.contains(name.split()[-1], case=False)] if len(hist) else hist
        slot = (slots or {}).get(name)
        pa = PA_BY_SLOT.get(slot) if slot else None
        recent = " | ".join(f"{r.date[5:]} {int(r.pa) if r.pa == r.pa else '?'}PA {int(r.hits)}H {int(r.runs)}R {int(r.rbi)}RBI" for _, r in h.tail(6).iterrows()) if len(h) and "hits" in h else "no postseason box scores in data/results"
        blocks.append("\n".join([f"### {name}" + (f" (bats {slot})" if slot else ""),
            f"- **Opportunity:** expected PA ≈ {pa:.2f} from lineup slot" if pa else "- Lineup slot unknown (projected lineups only until ~4 h before first pitch)",
            f"- Game total {tot} (DraftKings) → {'low-scoring: fewer runs/RBI chances' if tot and tot <= 7.5 else 'normal scoring'}" if tot else "- Game total unknown",
            f"- Recent box scores: {recent}",
            "- Gaps: no Statcast (exit velocity, whiff%), platoon splits or bullpen-usage feed from the cloud yet."]))
    return "\n\n".join(blocks)

if __name__ == "__main__":
    sport, date, *names = sys.argv[1:]
    print({"nba": nba, "nfl": nfl, "mlb": mlb}[sport](date, names))
