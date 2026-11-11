"""College basketball: price every DraftKings moneyline / alt spread / alt total against the other books.
    python engine/cbb_alt.py data/odds/ncaab/<date>/cbbalt_<HHMM>.csv out.csv   (pull with odds.yml tag=cbbalt)
Fits a normal margin and total per game to the other books' two-sided main + alternate lines (Pinnacle 2x, FanDuel 1.5x).
Checked 11-11 against exact-line consensus: within about 1 point. Used for DK stepped-up parlay boosts."""
import pandas as pd,numpy as np,sys
from scipy.stats import norm
from scipy.optimize import least_squares
d=pd.read_csv(sys.argv[1])
now=pd.Timestamp.now(tz="UTC"); d=d[pd.to_datetime(d.start_et,utc=True)>now+pd.Timedelta(minutes=15)]
d["mk"]=d.market.str.replace("alternate_","")
def imp(o): return 100/(o+100) if o>0 else -o/(-o+100)
def dec(o): return 1+(o/100 if o>0 else 100/-o)
W={"pinnacle":2.0,"fanduel":1.5,"betrivers":1.0,"betmgm":1.0}
rows=[];fits=[]
for ev,e in d.groupby("event_id"):
    home,away=e.home.iloc[0],e.away.iloc[0]; st=e.start_et.iloc[0]
    ot=e[e.book!="draftkings"]
    # spreads: home cover prob at home point h  -> P(M > -h)
    S=[];T=[]
    for (b,mk),g in ot.groupby(["book","mk"]):
        idx={(r.name,r.point):r.price for r in g.itertuples()}
        for (nm,pt),pr in idx.items():
            if mk=="spreads" and nm==home and (away,-pt) in idx:
                a,c=imp(pr),imp(idx[(away,-pt)]); S.append((pt,a/(a+c),W.get(b,1)))
            if mk=="totals" and nm=="Over" and ("Under",pt) in idx:
                a,c=imp(pr),imp(idx[("Under",pt)]); T.append((pt,a/(a+c),W.get(b,1)))
        if mk=="h2h":
            h=g[g.name==home]; a=g[g.name==away]
            if len(h) and len(a): x,y=imp(h.price.iloc[0]),imp(a.price.iloc[0]); S.append((-0.0001,x/(x+y),W.get(b,1)*0.5))
    if len(S)<4: continue
    S=np.array(S); 
    fm=least_squares(lambda v: np.sqrt(S[:,2])*(norm.sf(-S[:,0],v[0],v[1])-S[:,1]),[0,11],bounds=([-80,5],[80,25]))
    mu,sdm=fm.x
    TT=None
    if len(T)>=4:
        T=np.array(T); ft=least_squares(lambda v: np.sqrt(T[:,2])*(norm.sf(T[:,0],v[0],v[1])-T[:,1]),[T[:,0].mean(),12],bounds=([80,5],[220,25])); TT=ft.x
    fits.append((home,len(S),round(mu,1),round(sdm,1),None if TT is None else (round(TT[0],1),round(TT[1],1))))
    for r in e[e.book=="draftkings"].itertuples():
        if not (-400<=r.price<=-150): continue
        if r.mk=="h2h": p=norm.sf(0,mu if r.name==home else -mu,sdm); lab=f"{r.name} moneyline"
        elif r.mk=="spreads":
            m=mu if r.name==home else -mu; p=norm.sf(-r.point,m,sdm); lab=f"{r.name} {r.point:+g}"
        elif r.mk=="totals" and TT is not None:
            p=norm.sf(r.point,*TT) if r.name=="Over" else norm.cdf(r.point,*TT); lab=f"{r.name} {r.point:g}"
        else: continue
        rows.append(dict(eid=ev,game=f"{away} @ {home}",start=st[11:16],leg=lab,mk=r.mk,dk=int(r.price),p=p,ev=(p*dec(r.price)-1)*100,pts=len(S),sd=round(sdm,1)))
o=pd.DataFrame(rows); o.to_csv(sys.argv[2],index=False)
f=pd.DataFrame(fits,columns=["home","pts","mu","sd","tot"]); print(f.sd.describe().round(1).to_dict())
print(o.groupby("mk").ev.describe().round(1))
