"""DraftKings Football Moonshot backtest on real play-by-play (nflverse 2026 pbp).
Rules (DK Network 11/01/2026): round starts on first run/pass snapped outside opp 20. +0.2 completion/run with positive yards,
+0.5 per full 10 yds, +0.5 first down, +2.0 offensive TD (bonus doubling ignored = conservative). Ends on incompletion/INT/
lost fumble/turnover on downs/safety (spike = incompletion). Punts/FGs/kicks don't end it. Halftime/game end -> settle at current.
For every drive start of team T: replay the game forward and record the max multiplier before the round ends.
    python engine/nfl/moonshot.py <pbp.csv.gz> [teams...]"""
import pandas as pd,numpy as np,sys
p=pd.read_csv(sys.argv[1],low_memory=False,usecols=lambda c:c in['game_id','play_id','posteam','defteam','game_half','drive','play_type','yards_gained','complete_pass','incomplete_pass','interception','fumble_lost','fourth_down_failed','safety','first_down','touchdown','td_team','qb_spike','qb_kneel','sack','yardline_100','penalty','season_type','week','home_team','away_team'])
p=p[p.play_type.isin(['pass','run','punt','field_goal','kickoff','extra_point','qb_kneel','qb_spike','no_play'])].sort_values(['game_id','play_id'])
T=[1.2,1.5,2.0,3.0,5.0,8.0,12.0,20.0]
rows=[]
for gid,g in p.groupby('game_id',sort=False):
    g=g.reset_index(drop=True); pt=g.play_type.values
    starts=g.index[(g.play_type.isin(['pass','run']))&(g.yardline_100>20)&(g.drive!=g.drive.shift(1).where(g.play_type.shift(1).isin(['pass','run','qb_kneel','qb_spike'])))]
    for s in starts:
        half=g.game_half[s]; m=0.0; mx=0.0; ended=False; n=0; c=0; tds=0
        for i in range(s,len(g)):
            r=g.loc[i]
            if r.game_half!=half: break
            if r.play_type in('pass','run','qb_spike','qb_kneel'):
                n+=1; y=r.yards_gained if pd.notna(r.yards_gained) else 0
                if r.play_type=='qb_spike' or r.incomplete_pass==1 or r.interception==1 or r.fumble_lost==1 or r.fourth_down_failed==1 or r.safety==1:
                    ended=True; break
                if r.play_type=='qb_kneel': continue
                act=(r.play_type=='run' or r.complete_pass==1)
                if act: c+=1
                istd=(r.touchdown==1 and r.td_team==r.posteam)
                if istd: tds+=1
                f=(2**max(0,tds-1)) * (2**(1+(c-10)//5) if c>=10 else 1)   # bonus doubling (DK rules, interpreted)
                v=0.0
                if act and y>0: v+=0.2+0.5*int(y//10)
                if r.first_down==1: v+=0.5
                if istd: v+=2.0
                m+=v*f
                mx=max(mx,m)
        rows.append(dict(game=gid,week=g.week[s],team=g.posteam[s],opp=g.defteam[s],max_mult=mx,plays=n,**{f"hit_{t}":mx>=t for t in T}))
R=pd.DataFrame(rows)
R.to_csv('data/moonshot_bt.csv',index=False)
print(f"{len(R)} drive starts, {R.game.nunique()} games. League hit rates: "+", ".join(f"{t}x {R[f'hit_{t}'].mean()*100:.0f}%" for t in T))
tm=R.groupby('team')[[f'hit_{t}' for t in T]].mean().mul(100).round(0); tm['n']=R.groupby('team').size()
op=R.groupby('opp')[[f'hit_{t}' for t in T]].mean().mul(100).round(0)
want=sys.argv[2:]
if want:
    print(tm.loc[[t for t in want if t in tm.index]].sort_values('hit_1.5',ascending=False).to_string())
    print("as defense (opponent starts with ball):"); print(op.loc[[t for t in want if t in op.index]].to_string())
else: print(tm.sort_values('hit_1.5',ascending=False).to_string())
