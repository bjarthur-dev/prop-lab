"""Alt-ladder scan: price every DraftKings alternate rung (points/rebounds/assists/threes) from the sharp main line +
the player's own game-to-game SD; keep rungs where DK is cheaper than the other books. Run after an nbaalt odds snapshot.
    python engine/alt_scan.py   (date set below as D; edit or extend to argv)"""
import pandas as pd, numpy as np, glob, sys
from scipy.stats import norm
sys.path.insert(0,"engine/nba"); from common import norm_name
def imp(a): a=float(a); return 100/(a+100) if a>0 else -a/(-a+100)
def dec(a): a=float(a); return 1+a/100 if a>0 else 1+100/-a
D=sys.argv[1] if len(sys.argv)>1 else "2026-10-26"
main=pd.read_csv(sorted(glob.glob(f"data/odds/nba/{D}/board_*.csv"))[-1]).dropna(subset=["over","under"])
alt=pd.read_csv(sorted(glob.glob(f"data/odds/nba/{D}/nbaalt_*.csv"))[-1])
MK={"player_points":"PTS","player_rebounds":"REB","player_assists":"AST","player_threes":"FG3M"}
logs=pd.concat([pd.read_csv(f) for f in ["engine/data/players_2025-26.csv","engine/data/players_2026-27.csv"]])
logs=logs[logs.MIN>=20]; logs["key"]=logs.PLAYER_NAME.map(norm_name)
sd={}
for (k),g in logs.groupby("key"):
    g=g.sort_values("GAME_DATE").tail(60)
    if len(g)>=10: sd[k]={c:float(g[c].std()) for c in MK.values()}
# sharp main line -> mu per player/market
mus={}
for (pl,mk,ln),g in main.groupby(["player","market","line"]):
    if mk not in MK: continue
    sh=g[g.book.isin(["pinnacle","fanduel"])]; ref=sh if len(sh) else g[g.book!="draftkings"]
    if ref.empty: continue
    p=np.mean([imp(o)/(imp(o)+imp(u)) for o,u in zip(ref.over,ref.under)])
    k=norm_name(pl); s=sd.get(k,{}).get(MK[mk])
    if not s or s<=0: continue
    s=max(s, 1.0 if MK[mk]!="FG3M" else 0.9)
    mu=ln - s*norm.ppf(1-p)   # P(Y > line) = p (over x.5 <=> X >= x+1 <=> Y > x+0.5 with continuity)
    mus[(pl,mk)]=(mu,s,ln,p,len(ref))
rows=[]
alt["base"]=alt.market.str.replace("_alternate","")
for (pl,mk,ln),g in alt.groupby(["player","base","line"]):
    if (pl,mk) not in mus: continue
    dk=g[(g.book=="draftkings")&g.over.notna()]
    if dk.empty: continue
    mu,s,L,pm,nref=mus[(pl,mk)]
    p=1-norm.cdf((ln-mu)/s)
    oth=g[(g.book!="draftkings")&g.over.notna()]
    price=float(dk.over.iloc[0]); med_oth=float(np.median(oth.over.map(imp))) if len(oth) else np.nan
    rows.append(dict(player=pl,market=MK[mk],line=ln,dk=int(price),p_fair=round(p,3),ev=round(100*(p*dec(price)-1),1),
                     dk_imp=round(imp(price),3),others_imp=round(med_oth,3) if med_oth==med_oth else None,n_oth=len(oth),
                     main_line=L,mu=round(mu,1),sd=round(s,1),game=dk.game.iloc[0],start=dk.start_et.iloc[0]))
r=pd.DataFrame(rows)
r["dk_ge_oth"]=r.dk_imp<=r.others_imp.fillna(1)
r.to_csv(f"data/edges/{D}_alts.csv",index=False)
good=r[(r.ev>=3)&r.dk_ge_oth&(r.n_oth>=2)&(r.p_fair>=0.35)].sort_values("ev",ascending=False)
print(len(r),"DK alt rungs priced;",len(good),"qualify (EV>=3%, DK pays >= other books, >=2 books, p>=35%)")
print(good.head(30)[["player","market","line","dk","p_fair","ev","others_imp","n_oth","main_line","mu","sd","game"]].to_string(index=False))
