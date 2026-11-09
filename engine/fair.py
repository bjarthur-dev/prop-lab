"""One pricer for every slip (sportsbook parlay, Pick6, Betr). Replaces the ad-hoc Poisson scripts.

    python engine/fair.py --payout 2.9 --bankroll 32 nfl:Cook:rush_yds:over:74.5 nba:Lendeborg:ast:over:3.5
    python engine/fair.py --american +267 nba:Sengun:pr:under:29.5 nfl:Cook:rush_yds:under:88.5
    leg = sport:player:market:side:line        (optional --date YYYY-MM-DD, default today ET)

How a leg is priced (engine/market_backtest.py is the evidence, Record/Market Backtest.md the report):
  1. Same line quoted two-way by 2+ books -> weighted no-vig consensus (Pinnacle 2, FanDuel 1.5, others 1).
     15 dates / 5,480 lines: the consensus is calibrated to about 1-2 points. Nothing beats it.
  2. Different line -> fit a negative binomial through each book's main line (mean solved per book, weighted
     median), spread from data/dispersion.json (variance / mean, fitted on box scores). Poisson was wrong here:
     it called points lowered two steps 81% when they hit 67%.
  3. One-sided alternate prices at the exact line (if snapshotted) are blended in 50/50 after a vig haircut.
  4. Overs get OVER_HAIRCUT taken off: overs hit ~1.5 points under their no-vig price. Unders get no credit for it.
Legs in the same game are flagged (the product assumes independence)."""
import argparse, datetime as dt, glob, json, math, os, re, sys, unicodedata
from zoneinfo import ZoneInfo
import numpy as np, pandas as pd
from scipy.optimize import brentq
from scipy.stats import nbinom, poisson

MK = {"pts": "player_points", "reb": "player_rebounds", "ast": "player_assists", "3pm": "player_threes",
      "pra": "player_points_rebounds_assists", "pr": "player_points_rebounds", "pa": "player_points_assists",
      "ra": "player_rebounds_assists", "rush_yds": "player_rush_yds", "rec_yds": "player_reception_yds",
      "rec": "player_receptions", "rush_att": "player_rush_attempts", "pass_yds": "player_pass_yds",
      "sog": "player_shots_on_goal", "saves": "player_total_saves", "nhl_pts": "player_points", "nhl_ast": "player_assists",
      "goals": "player_goals", "blocks": "player_blocked_shots"}
COMBO = {"player_points_rebounds_assists": ["player_points", "player_rebounds", "player_assists"],
         "player_points_rebounds": ["player_points", "player_rebounds"], "player_points_assists": ["player_points", "player_assists"],
         "player_rebounds_assists": ["player_rebounds", "player_assists"]}
# variance / mean. NBA values are fitted (market_backtest.py rewrites data/dispersion.json); the rest are priors.
PHI = {"nba": {"player_points": 3.3, "player_rebounds": 1.28, "player_assists": 1.2, "player_threes": 1.22,
               "player_points_rebounds_assists": 2.95, "player_points_rebounds": 3.0, "player_points_assists": 3.0, "player_rebounds_assists": 1.5},
       "nfl": {"player_rush_yds": 14.0, "player_reception_yds": 17.0, "player_receptions": 1.6, "player_rush_attempts": 2.0, "player_pass_yds": 18.0},
       "nhl": {"player_shots_on_goal": 1.15, "player_total_saves": 1.5, "player_points": 1.05, "player_assists": 1.05, "player_goals": 1.05, "player_blocked_shots": 1.2}}
W = {"pinnacle": 2.0, "fanduel": 1.5}
OVER_HAIRCUT = 0.015
ALT_VIG = 1.07
PAYOUT = {"pick6": {2: 3, 3: 6, 4: 10, 5: 20, 6: 25}, "betr": {2: 3}}

def norm(n): return re.sub(r"[^a-z]", "", unicodedata.normalize("NFKD", str(n)).encode("ascii", "ignore").decode().lower())
def imp(o): o = float(o); return 100 / (o + 100) if o > 0 else -o / (-o + 100)
def sf(k, m, phi): return float(poisson.sf(k, m)) if phi <= 1.001 else float(nbinom.sf(k, m / (phi - 1), 1 / phi))
def solve_mean(line, p_over, phi):
    try: return brentq(lambda m: sf(math.floor(line), m, phi) - p_over, 0.01, 600)
    except ValueError: return None

def phi_for(sport, market):
    d = dict(PHI.get(sport, {}))
    try: d.update(json.load(open("data/dispersion.json")).get(sport, {}))
    except Exception: pass
    return d.get(market, 1.3)

def load(sport, date):
    fr = []
    for f in glob.glob(f"data/odds/{sport}/{date}/*.csv"):
        if os.path.basename(f).startswith("games"): continue
        d = pd.read_csv(f, low_memory=False)
        if "player" in d.columns: fr.append(d)
    if not fr: raise SystemExit(f"no odds files for {sport} {date}")
    o = pd.concat(fr, ignore_index=True).sort_values("snap_et")
    o = o.drop_duplicates(["book", "market", "player", "line"], keep="last")
    o["k"] = o.player.map(norm)
    return o

def _fit_mean(x, market, sport):
    """weighted median of the mean implied by each book's own two-way main line"""
    phi = phi_for(sport, market); pts = []
    t = x[(x.market == market) & x.over.notna() & x.under.notna() & (x.book != "pick6")]
    for r in t.itertuples():
        io, iu = imp(r.over), imp(r.under); m = solve_mean(r.line, io / (io + iu), phi)
        if m: pts.append((m, W.get(r.book, 1.0)))
    if not pts: return None, 0, phi
    pts.sort(); tot = sum(w for _, w in pts); acc = 0
    for m, w in pts:
        acc += w
        if acc >= tot / 2: return m, len(pts), phi

def leg_prob(o, sport, player, market, side, line):
    market = MK.get(market, market); side = side.lower().replace("more", "over").replace("less", "under")
    x = o[o.k.str.contains(norm(player))]
    names = sorted(x.player.unique())
    if len(names) > 1:
        ex = [n for n in names if norm(n) == norm(player)]
        if ex: x = x[x.player == ex[0]]; names = ex
        else: return {"err": f"ambiguous player: {names[:5]}"}
    if x.empty: return {"err": "player not in today's odds files"}
    game = x.game.iloc[0]; info = []
    t = x[(x.market == market) & (x.line == line) & x.over.notna() & x.under.notna() & (x.book != "pick6")]
    p = None
    if len(t) >= 2:
        f = [imp(a) / (imp(a) + imp(b)) for a, b in zip(t.over, t.under)]; w = [W.get(b, 1.0) for b in t.book]
        p = float(np.average(f, weights=w)); info.append(f"exact line, {len(t)} books")
    else:
        if market in COMBO and x[(x.market == market) & x.under.notna()].empty:
            ms = [_fit_mean(x, c, sport)[0] for c in COMBO[market]]
            m, n, phi = (sum(ms), 1, phi_for(sport, market)) if all(ms) else (None, 0, None)
            if m: info.append("mean = sum of the parts")
        else: m, n, phi = _fit_mean(x, market, sport)
        if m:
            p = sf(math.floor(line), m, phi); info.append(f"fitted: mean {m:.1f}, spread {phi:.2f}, {n} book lines")
        a = x[(x.market == market + "_alternate") & (x.line == line) & x.over.notna() & (x.book != "pick6")]
        if len(a) >= 2:
            pa = float(np.median([imp(v) for v in a.over])) / ALT_VIG
            info.append(f"alt ladder {pa:.3f} ({len(a)} books)")
            p = pa if p is None else (p + pa) / 2
            if m and abs(pa - sf(math.floor(line), m, phi)) > 0.06: info.append("FIT AND LADDER DISAGREE >6 pts")
    if p is None: return {"err": f"no usable {market} line for {names[0]}"}
    if side == "over": p = p - OVER_HAIRCUT
    else: p = 1 - p
    return {"player": names[0], "market": market, "side": side, "line": line, "p": min(max(p, 0.01), 0.99), "game": game, "how": "; ".join(info)}

def stake(bank, p, dec_odds, minimum=5.0):
    """half Kelly, capped by hit chance (System/Lessons.md), with the user's $5 floor reported honestly"""
    b = dec_odds - 1; k = (b * p - (1 - p)) / b
    cap = 0.06 if p >= 0.55 else 0.04 if p >= 0.30 else 0.02 if p >= 0.15 else 0.01
    s = bank * max(0.0, min(k / 2, cap))
    return k, s, (s if s >= minimum else (minimum if k > 0 else 0.0))

def price(legs, dec_odds, bank, date=None):
    date = date or dt.datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d")
    cache = {}; out = []; P = 1.0
    for leg in legs:
        sport, player, market, side, line = leg.split(":")[:5]
        if sport not in cache: cache[sport] = load(sport, date)
        r = leg_prob(cache[sport], sport, player, market, side, float(line)); r["leg"] = leg; out.append(r)
        if "p" in r: P *= r["p"]
    ok = all("p" in r for r in out)
    games = [r.get("game") for r in out if "p" in r]
    res = {"legs": out, "ok": ok, "same_game": len(set(games)) < len(games)}
    if ok:
        k, s, s5 = stake(bank, P, dec_odds)
        res.update(hit=P, ev=P * dec_odds - 1, breakeven_leg=dec_odds ** (-1 / len(legs)), kelly=k, stake=s, stake_floor5=s5)
    return res

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("legs", nargs="+")
    ap.add_argument("--payout", type=float); ap.add_argument("--american", type=str); ap.add_argument("--date"); ap.add_argument("--bankroll", type=float)
    a = ap.parse_args()
    d = a.payout if a.payout else (1 + (float(a.american) / 100 if float(a.american) > 0 else 100 / -float(a.american)))
    bank = a.bankroll
    if bank is None:
        m = re.search(r"current_bankroll:\s*([\d.]+)", open("Record/Bankroll.md").read()); bank = float(m.group(1)) if m else 30.0
    r = price(a.legs, d, bank, a.date)
    for l in r["legs"]:
        print(f"  {l['leg']}: " + (f"{l['p']*100:.1f}%  [{l['how']}]" if "p" in l else "ERROR " + l["err"]))
    if not r["ok"]: print("cannot price the slip: fix the legs above"); return
    if r["same_game"]: print("  WARNING: legs share a game; the hit chance below assumes they are independent")
    print(f"pays {d:.2f}x | hit {r['hit']*100:.1f}% | EV {r['ev']*100:+.1f}% | each leg must average {r['breakeven_leg']*100:.1f}%")
    if r["ev"] <= 0: print("VERDICT: pass (negative EV at fair prices)")
    else: print(f"VERDICT: +EV. Kelly {r['kelly']*100:.1f}% of bankroll; system stake ${r['stake']:.2f} on ${bank:.2f}" + (f"; under the $5 floor, so $5 is {5/bank*100:.0f}% of bankroll" if r['stake'] < 5 else ""))

if __name__ == "__main__": main()
