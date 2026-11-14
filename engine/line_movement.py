"""Line movement: does the side a line moves toward win more than the opening price said?
Game lines (moneyline, all sports with scores) and NBA player props (data/market_bt.csv, same line both snapshots).
For each market: consensus no-vig prob at the FIRST snapshot and the LAST snapshot before start.
Reports: (1) open vs close accuracy (Brier), (2) when the price moved 2+ pts, how often the side it moved toward won,
vs what the open and the close said. Writes Record/Line Movement.md.   python engine/line_movement.py"""
import pandas as pd,numpy as np,glob
def imp(o): return 100/(o+100) if o>0 else -o/(-o+100)
W={'pinnacle':2,'fanduel':1.5}
out=["# Line Movement","","Opening = first saved snapshot, closing = last saved snapshot before start (no-vig consensus, Pinnacle 2x, FanDuel 1.5x).",""]
def report(df,title,unit):
    df=df.dropna(subset=['po','pc','y']); df=df[(df.po>0.02)&(df.po<0.98)]
    bo=((df.po-df.y)**2).mean(); bc=((df.pc-df.y)**2).mean()
    out.append(f"## {title}"); out.append(f"{len(df)} {unit}. Brier (lower = more accurate): open {bo:.4f}, close {bc:.4f} -> {'close more accurate' if bc<bo else 'open more accurate'}."); out.append("")
    out.append("| moved toward a side by | n | open said | close said | that side won | won - open | noise ± |"); out.append("|---|---|---|---|---|---|---|")
    d=df.pc-df.po
    for lo,hi in [(0.01,0.02),(0.02,0.04),(0.04,0.08),(0.08,1)]:
        m=(d.abs()>=lo)&(d.abs()<hi); x=df[m]
        if len(x)<5: continue
        s=np.sign(d[m]); po=np.where(s>0,x.po,1-x.po); pc=np.where(s>0,x.pc,1-x.pc); w=np.where(s>0,x.y,1-x.y)
        se=np.sqrt((po*(1-po)).sum())/len(x)
        out.append(f"| {lo*100:.0f}-{hi*100:.0f} pts | {len(x)} | {po.mean()*100:.1f}% | {pc.mean()*100:.1f}% | {w.mean()*100:.1f}% | {(w.mean()-po.mean())*100:+.1f} | {se*100:.1f} |")
    out.append("")
# game lines
S=pd.concat([pd.read_csv(f).assign(sp=f.split('/')[2]) for f in glob.glob('data/scores/*/*.csv')]).drop_duplicates('event_id',keep='last')
G=[]
for f in glob.glob('data/odds/*/*/games_*.csv'):
    try:
        g=pd.read_csv(f)
        if 'event_id' in g: G.append(g)
    except Exception: pass
G=pd.concat(G); G=G[(G.market=='h2h')&G.event_id.isin(S.event_id)]
G['snap']=pd.to_datetime(G.snap_et,utc=True); G=G[G.snap<pd.to_datetime(G.start,utc=True)]
def cons(x,home):
    ps=[]
    for b,y in x.groupby('book'):
        h=y[y.name==home].price; a=y[y.name!=home].price
        if len(h) and len(a): p,q=imp(h.iloc[-1]),imp(a.iloc[-1]); ps.append((p/(p+q),W.get(b,1)))
    return sum(a*w for a,w in ps)/sum(w for a,w in ps) if len(ps)>=2 else np.nan
rows=[]
for ev,g in G.groupby('event_id'):
    snaps=sorted(g.snap.unique())
    if len(snaps)<2: continue
    s=S[S.event_id==ev].iloc[0]; home=g.home.iloc[0]
    if s.home_score==s.away_score: continue
    rows.append(dict(sp=s.sp,po=cons(g[g.snap==snaps[0]],home),pc=cons(g[g.snap==snaps[-1]],home),y=int(s.home_score>s.away_score),hrs=(snaps[-1]-snaps[0]).total_seconds()/3600))
R=pd.DataFrame(rows); report(R,f"Game moneylines ({', '.join(f'{k} {v}' for k,v in R.sp.value_counts().items())})","games with 2+ snapshots")
# NBA props
try:
    d=pd.read_csv('data/market_bt.csv'); d=d[d.actual!=d.line]
    d['snap']=pd.to_datetime(d.snap_et,utc=True)
    k=['date','market','player','line']
    def cp(x):
        x=x.copy(); x['w']=x.book.map(lambda b:W.get(b,1)); return (x.fair_over*x.w).sum()/x.w.sum() if x.book.nunique()>=2 else np.nan
    P=[]
    for key,g in d.groupby(k):
        sn=sorted(g.snap.unique())
        if len(sn)<2: continue
        P.append(dict(po=cp(g[g.snap==sn[0]]),pc=cp(g[g.snap==sn[-1]]),y=g.over_hit.iloc[0]))
    report(pd.DataFrame(P),"NBA player props (over side, same line at open and close)","props with 2+ snapshots")
except Exception as e: out.append(f"props skipped: {e}")
out.append("Read: if 'that side won' beats 'open said' by more than ~2x noise, line moves carry information -> bet early with the move / avoid betting against it. If close is more accurate than open, our prices should always come from the latest snapshot.")
open('Record/Line Movement.md','w').write("\n".join(out)); print("\n".join(out))
