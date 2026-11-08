"""Simulate DraftKings Football Moonshot on nflverse play-by-play.
Rules (DK help page): start 0.00x; completed pass +yds>0 +0.2; rush yds>0 +0.2; each full 10 yds +0.5; first down +0.5 (incl. penalty 1st downs);
offensive TD +2.0. Values double from the 2nd scoring event (FG / ST TD count) and again each extra; and double on the 10th rush/pass and every 5th after.
Round k of a half = plays between enders k-1 and k (incompletion incl. spike/grounding, INT, lost fumble, turnover on downs, safety).
Round starts on the first rush/pass snapped outside the opp 20; ender before start -> void. Half ends without ender -> settles at current multiplier."""
import sys, os, numpy as np, pandas as pd
LAG=int(os.environ.get("LAG","0")); TDFD=os.environ.get("TDFD","1")=="1"; SC=os.environ.get("SC","1")=="1"
cols = ["half_seconds_remaining","down","ydstogo","score_differential","xpass","game_id","play_id","game_half","play_type","complete_pass","incomplete_pass","interception","fumble_lost","safety","fourth_down_failed",
        "qb_spike","qb_kneel","yards_gained","first_down","first_down_penalty","pass_touchdown","rush_touchdown","field_goal_result","return_touchdown",
        "yardline_100","rush_attempt","pass_attempt","sack","season_type","td_team","posteam"]
frames = [pd.read_csv(f, usecols=lambda c: c in cols, low_memory=False) for f in sys.argv[1:]]
d = pd.concat(frames); d = d[d.season_type == "REG"].sort_values(["game_id", "play_id"])
for c in ["complete_pass","incomplete_pass","interception","fumble_lost","safety","fourth_down_failed","qb_spike","qb_kneel","first_down","first_down_penalty","pass_touchdown","rush_touchdown","return_touchdown","rush_attempt","pass_attempt","sack"]:
    d[c] = d[c].fillna(0)
rounds = []; feats = {}   # (game, half, k, M, busted, started_on_ender)
for (g, h), x in d.groupby(["game_id", "game_half"], sort=False):
    if h not in ("Half1", "Half2"): continue
    k, started, M, nplays, nscore = 1, False, 0.0, 0, 0
    for r in x.itertuples(index=False):
        pt = r.play_type
        scrim = pt in ("pass", "run")
        ender = (r.incomplete_pass == 1 or r.qb_spike == 1 or r.interception == 1 or r.fumble_lost == 1 or r.fourth_down_failed == 1 or r.safety == 1) and pt != "no_play"
        if not started:
            if scrim and r.yardline_100 > 20 and not ender:
                started, M, nplays, nscore = True, 0.0, 0, 0; feats[(g,h,k)] = (r.half_seconds_remaining, r.yardline_100, r.down, r.ydstogo, r.score_differential, r.xpass)
            elif ender:
                rounds.append((g, h, k, np.nan, True, True)); k += 1; continue   # void (or loss if the ender itself starts the round)
        if not started:
            continue
        # scoring events (FG made, ST TD) that are not scrimmage plays still count toward the scoring bonus
        is_fg = r.field_goal_result == "made"
        if pt in ("pass", "run") or r.first_down_penalty == 1:
            if scrim: nplays += 1
            n2 = nplays - LAG; fac = 2 ** max(0, (n2 - 5) // 5) if n2 >= 10 else 1
            if scrim and not ender:
                y = r.yards_gained if pd.notna(r.yards_gained) else 0
                gain = 0.0
                if (r.complete_pass == 1 or (pt == "run" and r.qb_kneel != 1)) and y > 0 and r.sack != 1: gain += 0.2 + 0.5 * int(y // 10)
                if r.first_down == 1 and (TDFD or not (r.pass_touchdown == 1 or r.rush_touchdown == 1)): gain += 0.5
                otd = r.pass_touchdown == 1 or r.rush_touchdown == 1
                if otd: nscore += 1; gain += 2.0
                sfac = 2 ** max(0, nscore - 1) if SC else 1
                M += gain * fac * sfac
            elif pt == "no_play" and r.first_down_penalty == 1:
                M += 0.5 * fac * 2 ** max(0, nscore - 1)
        if is_fg or r.return_touchdown == 1: nscore += 1
        if ender:
            rounds.append((g, h, k, M, True, False)); k += 1; started = False; M = 0.0
    if started: rounds.append((g, h, k, M, False, False))
R = pd.DataFrame(rounds, columns=["game","half","k","M","busted","void"])
F = pd.DataFrame([(a,b,c,*v) for (a,b,c),v in feats.items()], columns=["game","half","k","secs","yl","down","togo","sd","xpass"]); R = R.merge(F, on=["game","half","k"], how="left"); R.to_csv("data/moonshot_rounds.csv", index=False)
v = R[~R.void]
print(f"games {R.game.nunique()}, rounds {len(R)}, void {int(R.void.sum())} ({100*R.void.mean():.1f}%), live rounds {len(v)}, survive-to-half-end {int((~v.busted).sum())}")
print("multiplier at bust: median %.2f, mean %.2f" % (v.M.median(), v.M.mean()))
out = []
for T in [1.1,1.2,1.3,1.4,1.5,1.75,2,2.5,3,4,5,7.5,10,15,20,30,50]:
    pay = np.where(v.M >= T, T, np.where(~v.busted, v.M, 0.0))
    out.append((T, (v.M >= T).mean(), pay.mean() - 1))
print("\ntarget  hit%   EV per $1")
for T, p, ev in out: print(f"{T:6.2f}  {100*p:5.1f}  {100*ev:+6.1f}%")
# void treated as loss (if the ender play itself counts as the round's first play)
w = R.copy(); w.loc[w.void, "M"] = 0.0
print("\nIf an ender as the first play counts as a LOSS instead of void:")
for T in [1.2,1.5,2,3,5,10]:
    pay = np.where(w.M >= T, T, np.where(~w.busted, w.M, 0.0)); print(f"{T:6.2f}  hit {100*(w.M>=T).mean():5.1f}%  EV {100*(pay.mean()-1):+6.1f}%")
