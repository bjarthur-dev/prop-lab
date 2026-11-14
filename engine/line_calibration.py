"""Are the books' prices right? Joins every saved game-line snapshot (latest before kickoff) to final scores.
Moneyline: no-vig consensus win chance (Pinnacle 2x, FanDuel 1.5x) vs actual win rate, by bucket and sport.
Spreads/totals: how often the consensus side covered. Writes Record/Line Calibration.md.
    python engine/line_calibration.py"""
import pandas as pd,numpy as np,glob,os
def imp(o): return 100/(o+100) if o>0 else -o/(-o+100)
W={'pinnacle':2,'fanduel':1.5}
S=pd.concat([pd.read_csv(f).assign(sp=f.split('/')[2]) for f in glob.glob('data/scores/*/*.csv')]).drop_duplicates('event_id',keep='last')
G=[]
for f in glob.glob('data/odds/*/*/games_*.csv'):
    try: g=pd.read_csv(f)
    except Exception: continue
    if 'event_id' in g: G.append(g)
G=pd.concat(G); G=G[G.event_id.isin(S.event_id)]
G['snap']=pd.to_datetime(G.snap_et,utc=True); G['st']=pd.to_datetime(G.start,utc=True); G=G[G.snap<G.st]
G=G.sort_values('snap').groupby(['event_id','book','market','name','point'],dropna=False).tail(1)
rows=[]
for ev,g in G[G.market=='h2h'].groupby('event_id'):
    s=S[S.event_id==ev].iloc[0]; home=g.home.iloc[0]
    ps=[]
    for b,x in g.groupby('book'):
        h=x[x.name==home].price; a=x[x.name!=home].price
        if len(h) and len(a): p,q=imp(h.iloc[0]),imp(a.iloc[0]); ps.append((p/(p+q),W.get(b,1)))
    if len(ps)<2 or s.home_score==s.away_score: continue
    p=sum(a*w for a,w in ps)/sum(w for a,w in ps); hw=int(s.home_score>s.away_score)
    fav_p=max(p,1-p); fav_won=hw if p>=0.5 else 1-hw
    rows.append(dict(sp=s.sp,p=fav_p,won=fav_won,hours=(g.st.iloc[0]-g.snap.max()).total_seconds()/3600))
M=pd.DataFrame(rows)
bins=[0.5,0.6,0.7,0.8,0.9,1.0]; M['bucket']=pd.cut(M.p,bins)
out=["# Line Calibration","","Do the books' prices match what happens? Favourite's no-vig win chance (consensus of all books, Pinnacle 2x, FanDuel 1.5x) from the last saved snapshot before kickoff, vs. how often the favourite actually won.",f"Games: {len(M)} ({', '.join(f'{k} {v}' for k,v in M.sp.value_counts().items())}). Data window: {S.date.min()} to {S.date.max()}.",""]
def tab(d,title):
    t=d.groupby('bucket',observed=True).agg(games=('won','size'),priced=('p','mean'),won=('won','mean')).reset_index()
    t['gap']=(t.won-t.priced)*100; t['se']=np.sqrt(t.priced*(1-t.priced)/t.games)*100
    out.append(f"## {title}"); out.append("| favourite priced | games | books said | actually won | gap (pts) | noise ± |"); out.append("|---|---|---|---|---|---|")
    for r in t.itertuples(): out.append(f"| {r.bucket} | {r.games} | {r.priced*100:.1f}% | {r.won*100:.1f}% | {r.gap:+.1f} | {r.se:.1f} |")
    out.append(f"| **all** | {len(d)} | {d.p.mean()*100:.1f}% | {d.won.mean()*100:.1f}% | {(d.won.mean()-d.p.mean())*100:+.1f} | {np.sqrt((d.p*(1-d.p)).sum())/len(d)*100:.1f} |"); out.append("")
tab(M,"All sports")
for sp,d in M.groupby('sp'): tab(d,sp.upper())
out.append("Gap within about 2x the noise column = the prices were right. Small samples: re-run as data grows (results.yml).")
open('Record/Line Calibration.md','w').write("\n".join(out)); print("\n".join(out))
