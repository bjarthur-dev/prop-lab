"""NBA matchup breakdown: the WHY behind a stat, then a context projection, then (last) the line.
Uses the laptop's stats.nba.com context pull (engine/data/context/<season>/, see fetch_context.py) + game logs.

    python engine/nba/matchup.py DATE "Player Name" ["Player Name" ...]      (opponent/lines found from data/odds/nba/DATE/)
    python engine/nba/matchup.py DATE "Player Name@OPP"                      (force the opponent, e.g. "Jalen Brunson@DET")

For each player:
  1. Role: minutes, usage, touches, time of possession, how he creates (drives / pull-ups / catch-and-shoot / post).
  2. Shot diet vs this defense: his attempts by zone x what this opponent allows in each zone vs league.
  3. Play types: his top Synergy play types x this defense's points per possession allowed in them.
  4. Pace, free-throw rate allowed, defensive rating, rim / three-point defense (defended FG% vs expected).
  5. Rebounding pool (both teams' misses, opponent crash rate) and assist conversion (opponent FG% allowed).
  6. Defenders: who on this roster has guarded him (matchup minutes, pts, FG) and their defended FG% vs expected.
  7. Context projection for PTS / REB / AST / 3PM = his blended per-minute rate x minutes x the matchup factors,
     with P(over) at the sharp main line next to the market's fair %. A gap is a QUESTION to answer, not a bet.
Early-season numbers are shrunk toward last season (player k=8 games, team k=10 games)."""
import sys, os, glob, math
import numpy as np, pandas as pd
from scipy.stats import norm
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import norm_name

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
CUR, PRI = "2026-27", "2025-26"
KP, KT = 8.0, 10.0
FULL = {"Atlanta Hawks": "ATL", "Boston Celtics": "BOS", "Brooklyn Nets": "BKN", "Charlotte Hornets": "CHA", "Chicago Bulls": "CHI",
    "Cleveland Cavaliers": "CLE", "Dallas Mavericks": "DAL", "Denver Nuggets": "DEN", "Detroit Pistons": "DET", "Golden State Warriors": "GSW",
    "Houston Rockets": "HOU", "Indiana Pacers": "IND", "LA Clippers": "LAC", "Los Angeles Clippers": "LAC", "Los Angeles Lakers": "LAL",
    "Memphis Grizzlies": "MEM", "Miami Heat": "MIA", "Milwaukee Bucks": "MIL", "Minnesota Timberwolves": "MIN", "New Orleans Pelicans": "NOP",
    "New York Knicks": "NYK", "Oklahoma City Thunder": "OKC", "Orlando Magic": "ORL", "Philadelphia 76ers": "PHI", "Phoenix Suns": "PHX",
    "Portland Trail Blazers": "POR", "Sacramento Kings": "SAC", "San Antonio Spurs": "SAS", "Toronto Raptors": "TOR", "Utah Jazz": "UTA",
    "Washington Wizards": "WAS"}
ZONES = [("Restricted Area", "rim", 2), ("In The Paint (Non-RA)", "paint", 2), ("Mid-Range", "mid", 2),
         ("Corner 3", "corner3", 3), ("Above the Break 3", "atb3", 3)]
PLAYTYPES = ["prballhandler", "prrollman", "isolation", "spotup", "transition", "postup", "handoff", "cut", "offscreen", "offrebound"]
PT_NAME = {"prballhandler": "P&R ball-handler", "prrollman": "P&R roll man", "isolation": "isolation", "spotup": "spot-up",
           "transition": "transition", "postup": "post-up", "handoff": "handoff", "cut": "cut", "offscreen": "off-screen",
           "offrebound": "putback"}

_cache = {}
def ctx(name, season=CUR):
    k = (name, season)
    if k not in _cache:
        p = os.path.join(ROOT, "engine", "data", "context", season, f"{name}.csv")
        _cache[k] = pd.read_csv(p) if os.path.exists(p) else None
    return _cache[k]

def w(gp, k): return float(gp) / (float(gp) + k) if gp == gp and gp else 0.0
def blend(c, p, wc):
    if c is None or (isinstance(c, float) and math.isnan(c)): return p
    if p is None or (isinstance(p, float) and math.isnan(p)): return c
    return wc * c + (1 - wc) * p

def team_map():
    t = ctx("team_defend_overall")
    m = dict(zip(t.TEAM_NAME, t.TEAM_ABBREVIATION)); m.update(FULL); return m

def prow(name, df):
    if df is None: return None
    k = norm_name(name); x = df[df.PLAYER_NAME.map(norm_name) == k]
    return x.iloc[0] if len(x) else None

def trow(abbr, df, season=CUR):
    if df is None: return None
    if "TEAM_ABBREVIATION" in df.columns:
        x = df[df.TEAM_ABBREVIATION == abbr]
    else:
        tm = team_map(); x = df[df.TEAM_NAME.map(lambda n: tm.get(n)) == abbr]
    return x.iloc[0] if len(x) else None

def pgp(player, season):
    r = prow(player, ctx("player_usage", season)); return float(r["GP"]) if r is not None else 0.0

def tgp(abbr, season):
    r = trow(abbr, ctx("team_advanced", season)); return float(r["GP"]) if r is not None else 0.0

def tval(name, abbr, col):
    """team stat blended current/prior season with league means for both; returns (value, league_mean)."""
    c, p = ctx(name, CUR), ctx(name, PRI)
    rc, rp = trow(abbr, c), trow(abbr, p) if p is not None else None
    wc = w(tgp(abbr, CUR), KT)
    v = blend(float(rc[col]) if rc is not None and col in rc else None, float(rp[col]) if rp is not None and col in rp else None, wc)
    lg = blend(float(c[col].mean()) if c is not None and col in c else None, float(p[col].mean()) if p is not None and col in p else None, wc)
    return v, lg

def trel(name, abbr, col):
    """team volume stat relative to league, computed within each season, then blended."""
    out = []
    for se in (CUR, PRI):
        d = ctx(name, se); r = trow(abbr, d) if d is not None else None
        out.append(float(r[col]) / float(d[col].mean()) if r is not None and col in r and d[col].mean() else None)
    return blend(out[0], out[1], w(tgp(abbr, CUR), KT))

def pzone(player, z):
    """per-game FGA and FG% in a zone (shot-location data are season totals)."""
    vals = []
    for se in (CUR, PRI):
        r = prow(player, ctx("player_shot_zones", se)); gp = pgp(player, se)
        if r is None or not gp or r[f"{z}_FGA"] != r[f"{z}_FGA"]: vals.append((None, None)); continue
        vals.append((float(r[f"{z}_FGA"]) / gp, float(r[f"{z}_FG_PCT"]) if r[f"{z}_FG_PCT"] == r[f"{z}_FG_PCT"] else None))
    wc = w(pgp(player, CUR), KP)
    return blend(vals[0][0], vals[1][0], wc), blend(vals[0][1], vals[1][1], wc)

def pval(name, player, col, k=KP):
    c, p = ctx(name, CUR), ctx(name, PRI)
    rc, rp = prow(player, c), prow(player, p)
    gp = pgp(player, CUR)
    vc = float(rc[col]) if rc is not None and col in rc and rc[col] == rc[col] else None
    vp = float(rp[col]) if rp is not None and col in rp and rp[col] == rp[col] else None
    return blend(vc, vp, w(gp, k))

# --------------------------------------------------------------- game logs (per-minute base rates, minutes, sd)
def logs():
    if "logs" not in _cache:
        fs = [os.path.join(ROOT, "engine", "data", f"players_{s}.csv") for s in (PRI, CUR)]
        d = pd.concat([pd.read_csv(f).assign(S=s) for f, s in zip(fs, (PRI, CUR)) if os.path.exists(f)])
        d = d[d.MIN > 0].copy(); d["key"] = d.PLAYER_NAME.map(norm_name); d["date"] = pd.to_datetime(d.GAME_DATE)
        _cache["logs"] = d
    return _cache["logs"]

def base(player, date):
    d = logs(); g = d[(d.key == norm_name(player)) & (d.date < pd.Timestamp(date))].sort_values("date")
    if g.empty: return None
    cur, pri = g[g.S == CUR], g[g.S == PRI]
    wc = w(len(cur), KP); out = {"team": g.TEAM_ABBREVIATION.iloc[-1], "gp_cur": len(cur)}
    for s in ["PTS", "REB", "AST", "FG3M", "OREB", "DREB", "FGA", "FTA", "FG3A"]:
        rc = cur[s].sum() / cur.MIN.sum() if len(cur) else None
        rp = pri[pri.MIN >= 10][s].sum() / pri[pri.MIN >= 10].MIN.sum() if len(pri[pri.MIN >= 10]) else None
        out[s] = blend(rc, rp, wc)
    last = g.tail(5).MIN.mean(); mc = cur.MIN.mean() if len(cur) else None; mp = pri.MIN.mean() if len(pri) else None
    last3 = g.tail(3).MIN.mean()
    out["MIN"] = 0.5 * last3 + 0.5 * (blend(mc, mp, w(len(cur), 3.0)) if mc is not None else mp)
    big = g[g.MIN >= 20].tail(60)
    out["sd"] = {s: float((big[s] / big.MIN * out["MIN"]).std()) if len(big) >= 8 else None for s in ["PTS", "REB", "AST", "FG3M"]}
    return out

# --------------------------------------------------------------- odds: opponent + sharp main lines
def game_info(date, player, team):
    fs = sorted(glob.glob(os.path.join(ROOT, "data", "odds", "nba", date, "*.csv")))
    fs = [f for f in fs if not os.path.basename(f).startswith("games_")]
    tm = team_map(); opp = home = None; lines = {}
    for f in reversed(fs):
        o = pd.read_csv(f); x = o[o.player.map(lambda s: norm_name(str(s))) == norm_name(player)]
        if x.empty: continue
        a, h = x.game.iloc[0].split("@"); ta, th = tm.get(a), tm.get(h)
        opp, home = (th, False) if ta == team else (ta, True)
        main = x[~x.market.str.endswith("_alternate") & x.over.notna() & x.under.notna() & (x.book != "pick6")]
        for mk, g in main.groupby("market"):
            sh = g[g.book.isin(["pinnacle", "fanduel"])]; ref = sh if len(sh) else g
            L = ref.line.mode().iloc[0]; r = ref[ref.line == L]
            imp = lambda a: 100 / (a + 100) if a > 0 else -a / (-a + 100)
            p = float(np.mean([imp(o_) / (imp(o_) + imp(u)) for o_, u in zip(r.over, r.under)]))
            lines[mk] = (float(L), p)
        break
    gl = sorted(glob.glob(os.path.join(ROOT, "data", "odds", "nba", date, "games_*.csv")))
    spread = total = None
    if gl and opp:
        g = pd.read_csv(gl[-1]); g = g[g.book == "draftkings"]
        for _, r in g.iterrows():
            if {tm.get(r.home), tm.get(r.away)} == {team, opp}:
                if r.market == "totals": total = float(r.point)
                if r.market == "spreads" and tm.get(r.name) == team: spread = float(r.point)
    return opp, home, lines, spread, total

# --------------------------------------------------------------- the breakdown
def breakdown(date, player, opp=None):
    b = base(player, date)
    if b is None: return f"### {player}\n- no game logs found\n", None
    team = b["team"]; opp2, home, lines, spread, total = game_info(date, player, team)
    opp = opp or opp2
    if not opp: return f"### {player} ({team})\n- no game found in today's odds (pass \"{player}@OPP\")\n", None
    L = [f"### {player} ({team}) {'vs' if home else '@'} {opp}" + (f" · spread {spread:+.1f}, total {total}" if spread is not None else "")]
    proj = {}

    # 1. role
    usg = pval("player_usage", player, "USG_PCT"); touches = pval("player_track_possessions", player, "TOUCHES")
    top = pval("player_track_possessions", player, "TIME_OF_POSS")
    drv = pval("player_track_drives", player, "DRIVES"); pu = pval("player_track_pullupshot", player, "PULL_UP_FGA")
    cs = pval("player_track_catchshoot", player, "CATCH_SHOOT_FGA"); post = pval("player_track_possessions", player, "POST_TOUCHES")
    L.append(f"- **Role:** {b['MIN']:.1f} min proj · usage {100*usg:.0f}% · {touches or 0:.0f} touches, {top or 0:.1f} min of possession/g · "
             f"creates: {drv or 0:.1f} drives, {pu or 0:.1f} pull-up FGA, {cs or 0:.1f} catch-and-shoot FGA, {post or 0:.1f} post touches"
             if usg is not None else f"- **Role:** {b['MIN']:.1f} min proj (no tracking row)")

    # 2. shot diet vs defense allowed
    zone_pts = 0.0; zl = []
    for z, short, val in ZONES:
        fga, pct = pzone(player, z)
        if not fga or fga < 0.3: continue
        v, lg = tval("team_shot_zones_allowed", opp, f"{z}_OPP_FG_PCT")
        rel = trel("team_shot_zones_allowed", opp, f"{z}_OPP_FGA")
        if v is None or lg is None: continue
        d = 0.5 * (v - lg)                       # half the defense's deviation is real (rest is opponent shot luck)
        zone_pts += fga * d * val
        zl.append(f"{short} {fga:.1f} FGA ({100*(pct or 0):.0f}%) vs {opp} allows {100*v:.0f}% (lg {100*lg:.0f}%"
                  + (f", {rel*100-100:+.0f}% attempts" if rel else "") + ")")
    if zl: L.append("- **Shot diet vs this defense:** " + "; ".join(zl) + f" → **{zone_pts:+.1f} pts** from shot quality allowed")

    # 3. play types
    pt_pts = 0.0; pl = []
    rows = []
    for pt in PLAYTYPES:
        poss = pval(f"player_playtype_{pt}", player, "POSS", k=KP)
        if poss is None: continue
        rows.append((poss, pt))
    for per_g, pt in sorted(rows, reverse=True)[:3]:
        v, lg = tval(f"team_playtype_def_{pt}", opp, "PPP"); pctl, _ = tval(f"team_playtype_def_{pt}", opp, "PERCENTILE")
        if v is None: continue
        d = 0.5 * (v - lg); pt_pts += per_g * d
        pl.append(f"{PT_NAME[pt]} {per_g:.1f} poss/g → {opp} allows {v:.2f} PPP (lg {lg:.2f}, def pctile {100*(pctl or 0):.0f})")
    if pl: L.append("- **Play types:** " + "; ".join(pl) + f" → **{pt_pts:+.1f} pts**")

    # 4. pace / FT / rating / rim + 3PT defense
    pace_o, lgp = tval("team_advanced", opp, "PACE"); pace_t, _ = tval("team_advanced", team, "PACE")
    pace_f = ((pace_o + pace_t) / 2) / lgp if pace_o and pace_t and lgp else 1.0
    if total: pace_f = 0.5 * pace_f + 0.5 * (total / 228.0)   # market total folds in both offenses
    drt, lgd = tval("team_advanced", opp, "DEF_RATING"); fta, lgf = tval("team_opponent", opp, "OPP_FTA")   # per game
    rim, _ = tval("team_defend_less_than_6ft", opp, "PLUSMINUS"); three, _ = tval("team_defend_3_pointers", opp, "PCT_PLUSMINUS")
    ft_pts = (b["FTA"] * b["MIN"]) * 0.78 * 0.5 * ((fta / lgf) - 1) if fta and lgf else 0.0
    L.append(f"- **Environment:** pace factor {pace_f:.3f} (opp pace {pace_o:.1f}, own {pace_t:.1f}, lg {lgp:.1f}{', total ' + str(total) if total else ''}) · "
             f"{opp} def rating {drt:.1f} (lg {lgd:.1f}) · FTA allowed {fta:.1f} (lg {lgf:.1f}) → {ft_pts:+.1f} pts · "
             f"rim D_FG {100*(rim or 0):+.1f} pts vs expected, 3PT D_FG {100*(three or 0):+.1f}")

    # 5. rebounding pool + assist conversion
    oc_o, lgoc = tval("team_track_rebounding", opp, "OREB_CHANCES"); oc_t, _ = tval("team_track_rebounding", team, "OREB_CHANCES")
    orb_o, lgorb = tval("team_advanced", opp, "OREB_PCT")
    pool_f = ((oc_o + oc_t) / (2 * lgoc)) if oc_o and oc_t and lgoc else 1.0
    crash = 1 - 0.3 * ((orb_o - lgorb) / lgorb) if orb_o and lgorb else 1.0
    rc = pval("player_track_rebounding", player, "REB_CHANCES"); rcp = pval("player_track_rebounding", player, "REB_CHANCE_PCT")
    ofg, lgofg = tval("team_opponent", opp, "OPP_FG_PCT"); conv = (ofg / lgofg) if ofg and lgofg else 1.0
    pa = pval("player_track_passing", player, "POTENTIAL_AST"); a = pval("player_track_passing", player, "AST")
    L.append(f"- **Boards/assists:** reb chances {rc or 0:.1f}/g, grabs {100*(rcp or 0):.0f}% · rebound pool x{pool_f:.2f} "
             f"({opp} {oc_o:.1f} own-miss chances, crash OREB% {100*(orb_o or 0):.1f} vs lg {100*(lgorb or 0):.1f} → x{crash:.2f}) · "
             f"potential ast {pa or 0:.1f}/g ({a or 0:.1f} ast) · {opp} opp FG% {100*(ofg or 0):.1f} (lg {100*(lgofg or 0):.1f}) → conversion x{conv:.2f}")

    # 6. defenders
    dl = []
    roster = set()
    for s in (CUR,):
        u = ctx("player_usage", s)
        if u is not None: roster |= set(u[u.TEAM_ABBREVIATION == opp].PLAYER_NAME)
    for s in (CUR, PRI):
        m = ctx("matchups", s)
        if m is None: continue
        x = m[(m.OFF_PLAYER_NAME.map(norm_name) == norm_name(player)) & m.DEF_PLAYER_NAME.isin(roster)]
        for _, r in x.sort_values("MATCHUP_TIME_SEC", ascending=False).head(3).iterrows():
            dfg = pval("player_defend_overall", r.DEF_PLAYER_NAME, "PCT_PLUSMINUS")
            dl.append(f"{r.DEF_PLAYER_NAME} ({s}: {r.MATCHUP_TIME_SEC/60:.0f} min, {r.PLAYER_PTS:.0f} pts on {r.MATCHUP_FGM:.0f}/{r.MATCHUP_FGA:.0f}"
                      + (f"; his D_FG {100*dfg:+.1f} vs exp" if dfg is not None else "") + ")")
    if dl: L.append("- **Defenders who've guarded him (this roster):** " + "; ".join(dl[:4]))

    # 7. context projection
    m = b["MIN"]; ppace = pace_f
    proj["player_points"] = max(0.0, b["PTS"] * m * ppace + 0.5 * zone_pts + 0.5 * pt_pts + ft_pts)
    proj["player_rebounds"] = b["REB"] * m * pool_f * crash
    proj["player_assists"] = b["AST"] * m * ppace * conv
    tf = (1 + 0.5 * (three or 0) / 0.36) if three is not None else 1.0
    proj["player_threes"] = b["FG3M"] * m * ppace * tf
    sdmap = {"player_points": "PTS", "player_rebounds": "REB", "player_assists": "AST", "player_threes": "FG3M"}
    out = []
    for mk, mu in proj.items():
        s = b["sd"].get(sdmap[mk]) or max(1.0, 0.45 * mu)
        s = max(s, 0.9 if mk == "player_threes" else 1.2)
        if mk in lines:
            Lm, pm = lines[mk]; pc = 1 - norm.cdf((Lm + 0.5 - 0.5 - mu) / s) if False else 1 - norm.cdf((Lm - mu) / s)
            out.append(f"{mk.replace('player_', '')} **{mu:.1f}** (line {Lm}: context {100*pc:.0f}% over vs market {100*pm:.0f}%"
                       + (" ← gap, explain it" if abs(pc - pm) >= 0.08 else "") + ")")
            proj[mk] = (mu, s, Lm, pc, pm)
        else:
            out.append(f"{mk.replace('player_', '')} {mu:.1f}")
    L.append("- **Context projection:** " + " · ".join(out))
    L.append(f"- *Sample:* {b['gp_cur']} games this season (shrunk toward last season); team defense numbers are partly noise this early.")
    return "\n".join(L) + "\n", proj

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--save"]; save = "--save" in sys.argv
    D = args[0]; rows = []
    for arg in args[1:]:
        name, _, opp = arg.partition("@")
        txt, proj = breakdown(D, name.strip(), opp.strip() or None)
        print(txt)
        for mk, v in (proj or {}).items():
            if isinstance(v, tuple):
                rows.append(dict(date=D, player=name.strip(), market=mk, ctx_mean=round(v[0], 2), sd=round(v[1], 2), line=v[2],
                                 p_ctx=round(v[3], 3), p_mkt=round(v[4], 3), model_version="matchup v1"))
    if save and rows:   # shadow log: graded later vs results, like the NBA engine (proves or disproves the "why")
        out = os.path.join(ROOT, "data", "shadow", "matchup"); os.makedirs(out, exist_ok=True)
        f = os.path.join(out, f"{D}.csv"); old = pd.read_csv(f) if os.path.exists(f) else pd.DataFrame()
        pd.concat([old, pd.DataFrame(rows)]).drop_duplicates(["player", "market", "line"], keep="last").to_csv(f, index=False)
        print(f"saved {len(rows)} rows -> {f}")
