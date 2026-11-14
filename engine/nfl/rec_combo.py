"""Receptions x receiving-yards combos (e.g. UNDER receptions + OVER yards): true joint chance vs DK's SGP price.
Sim: receptions ~ negative binomial with mean set so P(rec <= R) matches the market; yards = sum of that many catches
bootstrapped from the player's own catches (2025-26), scaled so P(yds > Y) matches the market. Joint = share of sims with both.
    python engine/nfl/rec_combo.py "P.Washington" JAX --rec 4.5 --rec_under 0.58 --yds 61.5 --yds_over 0.50 --dk 475
Also: --backtest  -> checks the sim's joint against what actually happened for every receiver-game (calibration)."""
import pandas as pd,numpy as np,argparse
from scipy.optimize import brentq
from scipy.stats import nbinom
rng=np.random.default_rng(7)
def catches(name=None,team=None,seasons=(2025,2026)):
    d=pd.concat([pd.read_csv(f'engine/data/nfl/pbp_{s}_slim.csv.gz',usecols=['game_id','season','week','posteam','pass_attempt','complete_pass','receiving_yards','receiver_player_name']) for s in seasons])
    d=d[(d.pass_attempt==1)&d.receiver_player_name.notna()]
    if name: d=d[d.receiver_player_name==name]
    if team: d=d[d.posteam==team]
    return d
def nb(mu,k=8):  # k = size; receptions are slightly over-dispersed vs Poisson
    p=k/(k+mu); return k,p
def joint(cy,R,pu,Y,po,n=200000,k=8):
    mu=brentq(lambda m: nbinom.cdf(np.floor(R),*nb(m,k))-pu,0.05,20)
    rec=nbinom.rvs(*nb(mu,k),size=n,random_state=rng)
    tot=np.zeros(n); mx=rec.max()
    draws=rng.choice(cy,size=(n,max(mx,1)))
    mask=np.arange(max(mx,1))[None,:]<rec[:,None]; base=(draws*mask).sum(1)
    s=brentq(lambda s: (base*s>Y).mean()-po,0.3,3)
    yds=base*s
    return dict(mu_rec=mu,scale=s,joint=((rec<=R)&(yds>Y)).mean(),indep=pu*po)
if __name__=="__main__":
    a=argparse.ArgumentParser(); a.add_argument('name'); a.add_argument('team')
    for x in ['rec','rec_under','yds','yds_over']: a.add_argument('--'+x,type=float)
    a.add_argument('--dk',type=float,help='DK SGP american odds')
    a=a.parse_args()
    c=catches(a.name,a.team); cy=c[c.complete_pass==1].receiving_yards.fillna(0).values
    g=c.groupby('game_id').agg(rec=('complete_pass','sum'),yds=('receiving_yards','sum'))
    print(f"{a.name}: {len(g)} games, {len(cy)} catches, {np.mean(cy):.1f} yds/catch; past games with rec<={a.rec:g} & yds>{a.yds:g}: {((g.rec<=a.rec)&(g.yds>a.yds)).mean()*100:.0f}% ({((g.rec<=a.rec)&(g.yds>a.yds)).sum()}/{len(g)})")
    r=joint(cy,a.rec,a.rec_under,a.yds,a.yds_over)
    dec=1+(a.dk/100 if a.dk>0 else 100/-a.dk) if a.dk else None
    print(f"sim: joint {r['joint']*100:.1f}% (if independent {r['indep']*100:.1f}%); DK pays {a.dk:+.0f} = {100/dec:.1f}% -> EV {(r['joint']*dec-1)*100:+.1f}%" if dec else r)
