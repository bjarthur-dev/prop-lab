"""Today's NBA prop movers: implied mean (consensus, no-vig, normal approx) at the first vs latest snapshot.
Lists props whose mean moved 0.25+ (lead from Record/Line Movement.md: small moves under-react).
Saves data/movers/<date>.csv for forward grading.   python engine/movers.py [date]"""
import pandas as pd,numpy as np,glob,re,sys,os,json
from scipy.stats import norm
D=sys.argv[1] if len(sys.argv)>1 else pd.Timestamp.now(tz="America/New_York").strftime("%Y-%m-%d")
def imp(o): return 100/(o+100) if o>0 else -o/(-o+100)
PHI=json.load(open('data/dispersion.json')).get('nba',{})
MK={'player_points':'pts','player_rebounds':'reb','player_assists':'ast','player_threes':'3pm','player_points_rebounds_assists':'pra'}
F=[f for f in glob.glob(f'data/odds/nba/{D}/*.csv') if re.search(r'/(board|close|pregame|open|pick6)_\d+\.csv$',f)]
d=pd.concat([pd.read_csv(f) for f in F]); d=d[d.market.isin(MK)&(d.book!='pick6')].dropna(subset=['over','under'])
d['snap']=pd.to_datetime(d.snap_et,utc=True); d=d[d.snap<pd.to_datetime(d.start_et,utc=True)]
po=d.over.map(imp); pu=d.under.map(imp); d['p']=po/(po+pu); d=d[d.p.between(0.05,0.95)]
d['mu']=[r.line+np.sqrt(max(r.line,0.5)*PHI.get(MK[r.market],1.5))*norm.ppf(r.p) for r in d.itertuples()]
rows=[]
for (pl,m),g in d.groupby(['player','market']):
    sn=sorted(g.snap.unique())
    if len(sn)<2: continue
    o=g[g.snap==sn[0]]; c=g[g.snap==sn[-1]]
    if o.book.nunique()<2 or c.book.nunique()<2: continue
    mv=c.mu.median()-o.mu.median()
    dk=c[c.book=='draftkings']
    rows.append(dict(player=pl,stat=MK[m],game=g.game.iloc[0],start=g.start_et.iloc[0][11:16],open_mu=round(o.mu.median(),2),now_mu=round(c.mu.median(),2),move=round(mv,2),
                     side='over' if mv>0 else 'under',dk_line=dk.line.iloc[0] if len(dk) else np.nan,dk_over=dk.over.iloc[0] if len(dk) else np.nan,dk_under=dk.under.iloc[0] if len(dk) else np.nan,first=str(sn[0])[11:16],last=str(sn[-1])[11:16]))
R=pd.DataFrame(rows)
if len(R):
    R=R[R.move.abs()>=0.25].sort_values('move',key=abs,ascending=False)
    os.makedirs('data/movers',exist_ok=True); R.to_csv(f'data/movers/{D}.csv',index=False)
    print(R[(R.move.abs()<0.75)].head(30).to_string(index=False)); print(len(R),"movers (0.25+);",(R.move.abs()<0.75).sum(),"in the 0.25-0.75 band")
else: print("need 2+ snapshots today")
