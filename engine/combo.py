"""NBA same-game combos: true joint chance of 2+ legs vs DK's SGP price, using real correlations.
Each leg's chance comes from engine/fair.py (market consensus). Correlation between legs = Spearman correlation of the
two stats in the players' shared games (2025-26 + 2026-27 box scores; same player or teammates/opponents in the same game).
Gaussian copula sim with negative-binomial marginals matched to each leg's market chance.
    python engine/combo.py --date 2026-11-13 --dk +420 nba:Jalen Johnson:pts:over:22.5 nba:Jalen Johnson:ast:over:6.5
    python engine/combo.py --table      -> league-wide average correlations (which combos DK should shade)"""
import sys,argparse,numpy as np,pandas as pd,glob
sys.path.insert(0,'engine'); import fair
from scipy.stats import norm as N, nbinom, spearmanr
COL={'pts':'PTS','reb':'REB','ast':'AST','3pm':'FG3M','pra':'PRA','pr':'PR','pa':'PA','ra':'RA','stl':'STL','blk':'BLK'}
def box():
    b=pd.concat([pd.read_csv(f,low_memory=False) for f in glob.glob('engine/data/players_20*.csv')])
    b=b[pd.to_numeric(b.MIN,errors='coerce').fillna(0)>=10].copy()
    b['PRA']=b.PTS+b.REB+b.AST; b['PR']=b.PTS+b.REB; b['PA']=b.PTS+b.AST; b['RA']=b.REB+b.AST; b['k']=b.PLAYER_NAME.map(fair.norm)
    return b
def pair_corr(b,p1,s1,p2,s2):
    a=b[b.k==fair.norm(p1)][['GAME_ID',COL[s1]]]; c=b[b.k==fair.norm(p2)][['GAME_ID',COL[s2]]]
    if fair.norm(p1)==fair.norm(p2): m=b[b.k==fair.norm(p1)]; x,y=m[COL[s1]],m[COL[s2]]
    else: m=a.merge(c,on='GAME_ID',suffixes=('_a','_b')); x,y=m.iloc[:,1],m.iloc[:,2]
    if len(x)<12: return None,len(x)
    r=spearmanr(x,y).statistic; return float(r)*(len(x)/(len(x)+10)),len(x)  # shrink toward 0 on small samples
def sim(legs,R,n=300000,seed=3):
    rng=np.random.default_rng(seed); L=np.linalg.cholesky(R+1e-9*np.eye(len(R))); z=rng.standard_normal((n,len(legs)))@L.T; u=N.cdf(z)
    hit=np.ones(n,bool)
    for i,l in enumerate(legs):
        phi=fair.phi_for('nba',fair.MK[l['stat']]); mu=fair.solve_mean(l['line'],l['p_over'],phi)
        v=nbinom.ppf(u[:,i],mu/(phi-1),1/phi) if phi>1.001 else __import__('scipy.stats',fromlist=['poisson']).poisson.ppf(u[:,i],mu)
        hit&=(v>l['line']) if l['side']=='over' else (v<l['line'])
    return hit.mean()
if __name__=="__main__":
    a=argparse.ArgumentParser(); a.add_argument('legs',nargs='*'); a.add_argument('--date'); a.add_argument('--dk'); a.add_argument('--table',action='store_true'); a=a.parse_args()
    b=box()
    if a.table:
        pairs=[('pts','reb'),('pts','ast'),('reb','ast'),('pts','3pm'),('ast','3pm'),('reb','3pm')]
        print("same player, Spearman correlation across players with 20+ games (median, 25-75%):")
        for s1,s2 in pairs:
            rs=[spearmanr(g[COL[s1]],g[COL[s2]]).statistic for _,g in b.groupby('k') if len(g)>=20]
            print(f"  {s1}-{s2}: {np.nanmedian(rs):+.2f} ({np.nanpercentile(rs,25):+.2f} to {np.nanpercentile(rs,75):+.2f}), {len(rs)} players")
        sys.exit()
    o=fair.load('nba',a.date); legs=[]
    for s in a.legs:
        _,pl,st,sd,ln=s.split(':'); r=fair.leg_prob(o,'nba',pl,fair.MK[st],sd,float(ln))
        if 'err' in r: sys.exit(f"{s}: {r['err']}")
        po=r['p'] if sd=='over' else 1-r['p']; legs.append(dict(player=r['player'],stat=st,side=sd,line=float(ln),p=r['p'],p_over=po)); print(f"  {r['player']} {sd} {ln} {st}: {r['p']*100:.1f}%")
    k=len(legs); R=np.eye(k); info=[]
    for i in range(k):
        for j in range(i+1,k):
            r,n=pair_corr(b,legs[i]['player'],legs[i]['stat'],legs[j]['player'],legs[j]['stat']); R[i,j]=R[j,i]=r or 0; info.append(f"{legs[i]['player'].split()[-1]} {legs[i]['stat']} x {legs[j]['player'].split()[-1]} {legs[j]['stat']}: r={0 if r is None else r:+.2f} ({n} games)")
    w,V=np.linalg.eigh(R); R=V@np.diag(np.clip(w,1e-4,None))@V.T
    J=sim(legs,R); ind=np.prod([l['p'] for l in legs])
    print("  "+"; ".join(info)); print(f"joint {J*100:.1f}% (independent {ind*100:.1f}%)",end='')
    if a.dk: o_=float(a.dk); dec=1+(o_/100 if o_>0 else 100/-o_); print(f" | DK {a.dk} = {100/dec:.1f}% -> EV {(J*dec-1)*100:+.1f}%")
    else: print()
