"""Pick6 scan: price every DraftKings Pick6 standard (x1) line against the sharp sportsbook market.
Pick6 lines are often a half to two points off the books' main line; the edge is taking the side the sharp market
says hits >= ~58-60% (a 2-pick at 3x needs 57.7% per pick, 3-pick at 6x needs 55%; use the app's real payout).

    python engine/pick6_scan.py D [sport ...]      (reads data/odds/<sport>/D/*.csv, newest file containing pick6 rows)

Fair probability at the Pick6 line:
  * same line at the sharp books -> devig (Pinnacle/FanDuel, else consensus of non-DK books)
  * different line -> normal fit: mu = L - s*Phi^-1(1-p) from the sharp main line, s = player's game SD (NBA logs,
    last 60 games with >=20 min) or a market SD ratio for NFL/MLB. Integer-ish stats get a continuity margin.
Writes data/edges/D_pick6.csv and prints the best picks and the best 2- and 3-pick entries (one pick per game)."""
import pandas as pd, numpy as np, glob, sys, itertools, os
from scipy.stats import norm
sys.path.insert(0, "engine/nba")
try:
    from common import norm_name
except Exception:
    def norm_name(s): return str(s).lower().replace(".", "").replace("'", "").strip()

def imp(a): a = float(a); return 100/(a+100) if a > 0 else -a/(-a+100)

D = sys.argv[1] if len(sys.argv) > 1 else pd.Timestamp.now(tz="America/New_York").strftime("%Y-%m-%d")
SPORTS = sys.argv[2:] or ["nba", "nfl", "mlb"]
SHARP = ["pinnacle", "fanduel"]
NBA_MK = {"player_points": "PTS", "player_rebounds": "REB", "player_assists": "AST", "player_threes": "FG3M",
          "player_points_rebounds_assists": None}
SD_RATIO = {"player_reception_yds": 0.62, "player_rush_yds": 0.55, "player_receptions": 0.42, "player_pass_yds": 0.24,
            "player_pass_attempts": 0.18, "player_pass_completions": 0.2, "player_rush_attempts": 0.3,
            "pitcher_strikeouts": 0.4, "pitcher_outs": 0.2, "batter_total_bases": 0.9, "batter_hits": 0.9,
            "player_points": 0.3, "player_rebounds": 0.38, "player_assists": 0.45, "player_threes": 0.6}

nba_sd = {}
if "nba" in SPORTS:
    try:
        logs = pd.concat([pd.read_csv(f) for f in ["engine/data/players_2025-26.csv", "engine/data/players_2026-27.csv"]
                          if os.path.exists(f)])
        logs = logs[logs.MIN >= 20]; logs["key"] = logs.PLAYER_NAME.map(norm_name)
        for k, g in logs.groupby("key"):
            g = g.sort_values("GAME_DATE").tail(60)
            if len(g) >= 10: nba_sd[k] = {c: float(g[c].std()) for c in ["PTS", "REB", "AST", "FG3M"]}
    except Exception as e:
        print("NBA logs unavailable:", e)

def load(sport):
    fs = sorted(glob.glob(f"data/odds/{sport}/{D}/*.csv"))
    fs = [f for f in fs if not os.path.basename(f).startswith("games_")]
    frames = []
    for f in fs:
        try:
            x = pd.read_csv(f); x["file"] = os.path.basename(f); frames.append(x)
        except Exception:
            pass
    if not frames: return None
    a = pd.concat(frames)
    if "book" not in a or not (a.book == "pick6").any(): return None
    # newest snapshot per book/player/market/line
    a = a.sort_values("file").drop_duplicates(["book", "player", "market", "line"], keep="last")
    return a

def sd_for(sport, player, market, line):
    if sport == "nba":
        s = nba_sd.get(norm_name(player), {}).get(NBA_MK.get(market) or "", None)
        if s: return max(s, 0.9 if market == "player_threes" else 1.0)
    r = SD_RATIO.get(market)
    return max(r * max(line, 1.0), 0.8) if r else None

rows = []
for sport in SPORTS:
    a = load(sport)
    if a is None:
        print(f"{sport}: no pick6 lines in data/odds/{sport}/{D}/ (dispatch odds.yml tag pick6)"); continue
    p6 = a[(a.book == "pick6") & ~a.market.str.endswith("_alternate")]
    # one-way Pick6 lines that sit beside a two-way line for the same player/market are DISCOUNTED picks (reduced payout): drop them
    two = p6[p6.over.notna() & p6.under.notna()][["player", "market"]].drop_duplicates()
    oneway = p6.over.isna() | p6.under.isna()
    p6 = p6[~(oneway & p6.set_index(["player", "market"]).index.isin(two.set_index(["player", "market"]).index))]
    books = a[(a.book != "pick6") & ~a.market.str.endswith("_alternate") & a.over.notna() & a.under.notna()]
    for _, r in p6.iterrows():
        g = books[(books.player == r.player) & (books.market == r.market)]
        if g.empty: continue
        sh = g[g.book.isin(SHARP)]; ref = sh if len(sh) else g[g.book != "draftkings"]
        if ref.empty: ref = g
        # main = the line most books post
        L = ref.line.mode().iloc[0]; rl = ref[ref.line == L]
        pL = float(np.mean([imp(o)/(imp(o)+imp(u)) for o, u in zip(rl.over, rl.under)]))
        if abs(r.line - L) < 1e-9:
            p_over, how = pL, "same line"
        else:
            s = sd_for(sport, r.player, r.market, L)
            if not s: continue
            mu = L - s*norm.ppf(1-pL)
            p_over, how = float(1-norm.cdf((r.line-mu)/s)), f"fit from {L} (sd {s:.1f})"
        offered = [("MORE", p_over, r.over), ("LESS", 1-p_over, r.under)]
        for side, p, px in offered:
            if pd.isna(px): continue   # Pick6 doesn't offer this side (one-way pick)
            mult = round(1/imp(px)/1.732, 2) if px == px else None   # -137 = standard x1; other prices = boosted/discounted pick
            rows.append(dict(sport=sport, game=r.game, start=r.get("start_et", ""), player=r.player, market=r.market,
                             pick6_line=r.line, side=side, p=round(p, 3), sharp_line=L, sharp_p_over=round(pL, 3),
                             n_books=int(len(rl)), how=how, pick6_price=px, pick_mult=mult))
if not rows:
    print("no Pick6 picks priced"); sys.exit(0)
r = pd.DataFrame(rows).sort_values("p", ascending=False)
os.makedirs("data/edges", exist_ok=True); r.to_csv(f"data/edges/{D}_pick6.csv", index=False)
good = r[(r.p >= 0.58) & (r.n_books >= 2) & (r.pick_mult.between(0.95, 1.05))]   # standard picks only
print(f"{len(r)} Pick6 picks priced; {len(good)} standard picks at >= 58% (2+ books)")
print(good.head(25)[["sport", "player", "market", "pick6_line", "side", "p", "sharp_line", "sharp_p_over", "n_books", "game", "start"]].to_string(index=False))
# best entries, one pick per game, by joint probability (independent legs)
top = good.drop_duplicates(["game"]).head(8)
for n, mult in [(2, 3.0), (3, 6.0)]:
    best = None
    for c in itertools.combinations(top.itertuples(), n):
        pj = float(np.prod([x.p for x in c]))
        if best is None or pj > best[0]: best = (pj, c)
    if best:
        pj, c = best
        print(f"\nBest {n}-pick: " + " + ".join(f"{x.player} {x.side} {x.pick6_line} {x.market.replace('player_','')} ({x.p:.0%})" for x in c)
              + f"  -> all hit {pj:.0%}; break-even at {mult:.0f}x = {1/mult:.0%}; EV at {mult:.0f}x {100*(pj*mult-1):+.0f}%  (use the app's real payout)")
