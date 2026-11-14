"""NBA prop line movement using implied means, so line changes count too.
Each snapshot's consensus implied mean = line + sd * z(p_over) (normal approx, sd from NB dispersion), averaged over books/lines.
Tests: is the closing mean closer to the result than the opening mean, and when the mean moved, did the result go that way?
Appends to Record/Line Movement.md.   python engine/prop_movement.py"""
import pandas as pd,numpy as np,json
from scipy.stats import norm
import glob,re
def nrm(x): return re.sub(r"[^a-z]","",str(x).lower().replace(" jr","").replace(" iii","").replace(" ii",""))
def imp(o): return 100/(o+100) if o>0 else -o/(-o+100)
F=[f for f in glob.glob('data/odds/nba/*/*.csv') if re.search(r'/(board|close|pregame|open)_\d+\.csv$',f)]
d=pd.concat([pd.read_csv(f,usecols=lambda c:c in('snap_et','start_et','book','market','player','line','over','under')).assign(date=f.split('/')[3]) for f in F])
d=d.dropna(subset=['over','under']); d=d[d.book!='pick6']; d['snap']=pd.to_datetime(d.snap_et,utc=True); d=d[d.snap<pd.to_datetime(d.start_et,utc=True)]
po=d.over.map(imp); pu=d.under.map(imp); d['fair_over']=po/(po+pu)
box=pd.read_csv('engine/data/players_2026-27.csv',low_memory=False); box=box[pd.to_numeric(box.MIN,errors='coerce').fillna(0)>0].copy()
box['PRA']=box.PTS+box.REB+box.AST; box['k']=box.PLAYER_NAME.map(nrm); d['k']=d.player.map(nrm)
COL={'player_points':'PTS','player_rebounds':'REB','player_assists':'AST','player_threes':'FG3M','player_points_rebounds_assists':'PRA'}
d=d[d.market.isin(COL)]
d=d.merge(box[['k','GAME_DATE','PTS','REB','AST','FG3M','PRA']],left_on=['k','date'],right_on=['k','GAME_DATE'])
d['actual']=[getattr(r,COL[r.market]) for r in d.itertuples()]
PHI=json.load(open('data/dispersion.json')).get('nba',{}) if True else {}
MK={'player_points':'pts','player_rebounds':'reb','player_assists':'ast','player_threes':'3pm','player_points_rebounds_assists':'pra'}
d=d[d.fair_over.between(0.05,0.95)]
def sd(m,mu):
    phi=PHI.get(MK[m],1.5) if isinstance(PHI,dict) else 1.5
    return np.sqrt(max(mu,0.5)*phi)
d['mu']=[r.line+sd(r.market,r.line)*norm.ppf(r.fair_over) for r in d.itertuples()]
rows=[]
for (dt,pl,m),g in d.groupby(['date','player','market']):
    sn=sorted(g.snap.unique())
    if len(sn)<2: continue
    o=g[g.snap==sn[0]]; c=g[g.snap==sn[-1]]
    if o.book.nunique()<2 or c.book.nunique()<2: continue
    rows.append(dict(date=dt,m=MK[m],mo=o.mu.median(),mc=c.mu.median(),y=g.actual.iloc[0],hrs=(sn[-1]-sn[0]).total_seconds()/3600))
R=pd.DataFrame(rows); R['mv']=R.mc-R.mo; R['res']=R.y-R.mo
out=["","## NBA props by implied mean (line changes included)",f"{len(R)} player-stat-days with an open and a close snapshot (median gap {R.hrs.median():.1f} h).",
     f"Average miss: open mean {np.abs(R.y-R.mo).mean():.2f}, close mean {np.abs(R.y-R.mc).mean():.2f} ({'close' if np.abs(R.y-R.mc).mean()<np.abs(R.y-R.mo).mean() else 'open'} more accurate)."]
def table(R,title):
    out.extend(["",f"### {title}","| stat | mean moved by | n | avg move | result vs open, in move direction | share of move realised |","|---|---|---|---|---|---|"])
    for m,g in list(R.groupby('m'))+[('ALL',R)]:
        for lo,hi in [(0.25,0.75),(0.75,1.5),(1.5,99)]:
            x=g[(g.mv.abs()>=lo)&(g.mv.abs()<hi)]
            if len(x)<15: continue
            s=np.sign(x.mv); dirres=(x.res*s).mean(); avgmv=x.mv.abs().mean(); se=(x.res*s).std()/np.sqrt(len(x))
            out.append(f"| {m} | {lo}-{hi} | {len(x)} | {avgmv:.2f} | {dirres:+.2f} ± {se:.2f} | {dirres/avgmv*100:.0f}% |")
table(R[R.date<'2026-11-15'],"Found on (Oct 24 - Nov 14)")
F=R[R.date>='2026-11-15']
table(F,f"Forward test (from Nov 15, {len(F)} so far)") if len(F) else out.append("\nForward test starts Nov 15.")
out.append("")
out.append("Share realised ~100% = the move was right and the close is fair; >100% = moves under-react (bet with moves early); <0% = moves are noise/overreaction.")
open('Record/Line Movement.md','a').write("\n".join(out)); print("\n".join(out))
