"""How NBA stats move together across players in the same game (teammates and opponents).
For each team-game: the team's top scorer (by season PPG) as the anchor; correlations of his stats with each teammate's
and each opponent's stats, by teammate role (2nd option, starter big, etc. approximated by season averages).
Writes Record/Combo Correlations.md.   python engine/teammate_corr.py"""
import pandas as pd,numpy as np,glob
from scipy.stats import spearmanr
b=pd.concat([pd.read_csv(f,low_memory=False) for f in glob.glob('engine/data/players_20*.csv')])
b['MIN']=pd.to_numeric(b.MIN,errors='coerce').fillna(0); b=b[b.MIN>=10].copy()
b['season']=b.SEASON_ID.astype(str)
avg=b.groupby(['season','TEAM_ID','PLAYER_ID']).agg(ppg=('PTS','mean'),rpg=('REB','mean'),apg=('AST','mean'),gp=('GAME_ID','size')).reset_index()
avg=avg[avg.gp>=15]; avg['rank']=avg.groupby(['season','TEAM_ID']).ppg.rank(ascending=False,method='first')
b=b.merge(avg,on=['season','TEAM_ID','PLAYER_ID']).reset_index(drop=True)
# rank within team-season by ppg
star=b[b['rank']==1][['GAME_ID','TEAM_ID','PLAYER_ID','PTS','REB','AST','FG3M']].rename(columns=lambda c:c if c in('GAME_ID','TEAM_ID') else 's_'+c)
oth=b[b['rank']>1].copy()
oth['role']=np.select([oth['rank']==2,(oth.rpg>=7),(oth.apg>=5)],['2nd scorer','big (7+ rpg)','playmaker (5+ apg)'],'other rotation')
tm=oth.merge(star,on=['GAME_ID','TEAM_ID'])
op=oth.merge(star,on='GAME_ID',suffixes=('','_s')); op=op[op.TEAM_ID!=op.TEAM_ID_s]
def summarize(df,title):
    out=[f"## {title}","| anchor stat | other player stat | role | pairs | median corr | 25-75% |","|---|---|---|---|---|---|"]
    for a,c in [('PTS','PTS'),('AST','PTS'),('PTS','REB'),('PTS','AST'),('REB','REB'),('AST','AST')]:
        for role,g in df.groupby('role'):
            rs=[]
            for (sp,p),x in g.groupby(['s_PLAYER_ID','PLAYER_ID']):
                if len(x)>=20 and x['s_'+a].std()>0 and x[c].std()>0: rs.append(spearmanr(x['s_'+a],x[c]).statistic)
            if len(rs)>=15: out.append(f"| star {a.lower()} | {c.lower()} | {role} | {len(rs)} | {np.median(rs):+.2f} | {np.percentile(rs,25):+.2f} to {np.percentile(rs,75):+.2f} |")
    return out
out=["# Combo Correlations (NBA, 2025-26 + 2026-27)","Anchor = each team's top scorer. Pairs need 20+ shared games. Spearman correlation per pair, then the median across pairs.",""]
out+=summarize(tm,"Teammates")+[""]
# opponents meet too rarely for per-pair stats: pool z-scores (each player's stat minus his season mean, over his season sd)
b=b.copy()
for c in ['PTS','REB','AST']:
    m=b.groupby(['season','PLAYER_ID'])[c].transform('mean').to_numpy(); sdv=b.groupby(['season','PLAYER_ID'])[c].transform('std').to_numpy()
    b['z_'+c]=(b[c].to_numpy()-m)/sdv
zs=b[b['rank']==1][['GAME_ID','TEAM_ID','z_PTS','z_REB','z_AST']].rename(columns={'TEAM_ID':'ANCH_TEAM','z_PTS':'sz_PTS','z_REB':'sz_REB','z_AST':'sz_AST'})
K=['GAME_ID','TEAM_ID','rank','z_PTS','z_REB','z_AST']
o2=b[b['rank']<=8][K].reset_index(drop=True).merge(zs.reset_index(drop=True),on='GAME_ID'); o2=o2[o2.TEAM_ID!=o2.ANCH_TEAM]
t2=b[(b['rank']>1)&(b['rank']<=8)][K].reset_index(drop=True).merge(zs.reset_index(drop=True),on='GAME_ID'); t2=t2[t2.TEAM_ID==t2.ANCH_TEAM]
out+=["## Pooled (z-scores, all rotation players vs the top scorer)","| anchor | other | teammates corr (n) | opponents corr (n) |","|---|---|---|---|"]
for a,c in [('PTS','PTS'),('PTS','REB'),('PTS','AST'),('AST','PTS'),('REB','REB')]:
    ct=t2[['sz_'+a,'z_'+c]].dropna(); co=o2[['sz_'+a,'z_'+c]].dropna()
    out.append(f"| star {a.lower()} | {c.lower()} | {ct.corr().iloc[0,1]:+.3f} ({len(ct)}) | {co.corr().iloc[0,1]:+.3f} ({len(co)}) |")
out+=["","Read: positive = they go up together (stack overs, or unders); negative = one up, the other down (pair over with under). DK's SGP prices bake in its own guesses; edges come where its guess differs."]
open('Record/Combo Correlations.md','w').write("\n".join(out)); print("\n".join(out))
