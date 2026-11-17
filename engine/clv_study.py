import pandas as pd, glob, os, numpy as np
def imp(o): return np.where(o>0,100/(o+100),-o/(-o+100))
W={'pinnacle':2,'fanduel':1.5}
out=[]
for d in sorted(glob.glob('data/odds/nba/2026-1*')):
    fs=[f for f in glob.glob(d+'/*.csv') if os.path.basename(f).split('_')[0] in ('open','board','pregame','close')]
    if len(fs)<2: continue
    df=pd.concat([pd.read_csv(f) for f in fs],ignore_index=True)
    df=df[df.book!='pick6'].dropna(subset=['over','under'])
    df['snap']=pd.to_datetime(df.snap_et,utc=True); df['start']=pd.to_datetime(df.start_et,utc=True)
    df=df[df.snap<df.start]
    df['po']=imp(df.over)/(imp(df.over)+imp(df.under))
    k=['game','market','player','line']
    snaps=sorted(df.snap.unique())
    if len(snaps)<2: continue
    for key,x in df.groupby(k):
        ss=sorted(x.snap.unique())
        if len(ss)<2: continue
        e,l=ss[0],ss[-1]
        if (l-e)<pd.Timedelta(hours=2): continue
        def stat(s):
            y=x[x.snap==s]; dk=y[y.book=='draftkings']; o=y[y.book!='draftkings']
            if len(dk)!=1 or len(o)<3: return None
            w=o.book.map(lambda b:W.get(b,1)); fair=(o.po*w).sum()/w.sum()
            return dk.iloc[0], fair
        A=stat(e); B=stat(l)
        if A is None or B is None: continue
        (dke,fe),(dkl,fl)=A,B
        for side in ('over','under'):
            pe=fe if side=='over' else 1-fe; pl=fl if side=='over' else 1-fl
            oe,ol=dke[side],dkl[side]
            dec=1+(oe/100 if oe>0 else 100/-oe)
            ev=pe*dec-1
            out.append(dict(date=os.path.basename(d),key=key,side=side,ev_early=ev,dk_imp_early=float(imp(oe)),dk_imp_late=float(imp(ol)),fair_early=pe,fair_late=pl,hrs=(l-e).total_seconds()/3600))
R=pd.DataFrame(out)
R['dk_move']=R.dk_imp_late-R.dk_imp_early      # + = DK price for this side got worse (moved our way if we bet early)
R['fair_move']=R.fair_late-R.fair_early
R['clv_vs_late_fair']=R.fair_late*(1/R.dk_imp_early)-1   # EV of the early DK price, judged by late consensus (approx, uses DK implied incl vig)
def summ(m,lab):
    print(f"{lab}: n={len(m)}  days={m.date.nunique()}  DK price moved toward side: {(m.dk_move>0.005).mean()*100:.0f}%  away: {(m.dk_move<-0.005).mean()*100:.0f}%  mean DK move {m.dk_move.mean()*100:+.2f} pts  mean fair move {m.fair_move.mean()*100:+.2f} pts")
summ(R,'ALL DK sides (same line both snaps)')
for t in (0.0,0.02,0.04):
    summ(R[R.ev_early>=t],f'early EV >= {t*100:.0f}%')
print(R.groupby('date').size().to_string())
