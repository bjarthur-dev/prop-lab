"""NFL prop calibration: are the books' no-vig prices right for NFL player props?
Joins every saved NFL odds snapshot (last pregame quote per book/player/market/line) to play-by-play stat lines
(engine/data/nfl/pbp_2026_slim.csv.gz). Name match = first initial + last name (pbp style) + game date.
Writes Record/NFL Prop Calibration.md.   python engine/nfl/prop_calibration.py"""
import pandas as pd,numpy as np,glob,re
def imp(o): return 100/(o+100) if o>0 else -o/(-o+100)
def key(n):
    n=re.sub(r"\b(Jr|Sr|II|III|IV)\.?$","",str(n)).strip(); p=n.replace("'","").split()
    return (p[0][0]+"."+"".join(p[1:])).lower().replace(".","").replace("-","") if len(p)>1 else n.lower()
pbp=pd.read_csv('engine/data/nfl/pbp_2026_slim.csv.gz',low_memory=False)
pbp=pbp[pbp.season_type.eq('REG')|pbp.season_type.isna()] if 'season_type' in pbp else pbp
rec=pbp[pbp.receiver_player_name.notna()&(pbp.pass_attempt==1)].groupby(['game_date','receiver_player_name']).agg(rec=('complete_pass','sum'),rec_yds=('receiving_yards','sum')).reset_index().rename(columns={'receiver_player_name':'nm'})
ru=pbp[pbp.rusher_player_name.notna()&(pbp.rush_attempt==1)&(pbp.qb_kneel!=1)].groupby(['game_date','rusher_player_name']).agg(rush_att=('rush_attempt','sum'),rush_yds=('rushing_yards','sum')).reset_index().rename(columns={'rusher_player_name':'nm'})
pa=pbp[pbp.passer_player_name.notna()&(pbp.pass_attempt==1)&(pbp.sack!=1)].groupby(['game_date','passer_player_name']).agg(pass_yds=('receiving_yards','sum'),pass_att=('pass_attempt','sum')).reset_index().rename(columns={'passer_player_name':'nm'})
st=rec.merge(ru,on=['game_date','nm'],how='outer').merge(pa,on=['game_date','nm'],how='outer').fillna(0)
st['k']=st.nm.str.lower().str.replace(".","",regex=False).str.replace("-","",regex=False).str.replace("'","",regex=False)
MK={'player_reception_yds':'rec_yds','player_receptions':'rec','player_rush_yds':'rush_yds','player_rush_attempts':'rush_att','player_pass_yds':'pass_yds','player_pass_attempts':'pass_att'}
F=[f for f in glob.glob('data/odds/nfl/*/*.csv') if re.search(r'/(open|board|close|pregame|nflx|nfltmr)_\d+\.csv$',f)]
o=[]
for f in F:
    try: x=pd.read_csv(f)
    except Exception: continue
    if 'over' not in x and 'side' in x:   # long format (nflx)
        x=x.pivot_table(index=['snap_et','game','start_et','book','market','player','line'],columns='side',values='price',aggfunc='first').reset_index().rename(columns={'Over':'over','Under':'under'})
    if not {'over','under','start_et'}<=set(x.columns): continue
    o.append(x[['snap_et','start_et','book','market','player','line','over','under']])
o=pd.concat(o); o=o[o.market.isin(MK)&o.over.notna()&o.under.notna()&(o.book!='pick6')]
o['t']=pd.to_datetime(o.snap_et,utc=True); o=o[o.t<pd.to_datetime(o.start_et,utc=True)]
o=o.sort_values('t').drop_duplicates(['start_et','book','market','player','line'],keep='last')
po=o.over.map(imp); pu=o.under.map(imp); o['p']=po/(po+pu)
o['game_date']=pd.to_datetime(o.start_et.str[:10]).dt.strftime('%Y-%m-%d'); o['k']=o.player.map(key); o['stat']=o.market.map(MK)
W={'pinnacle':2,'fanduel':1.5}; o['w']=o.book.map(lambda b:W.get(b,1))
c=o.groupby(['game_date','k','stat','line']).apply(lambda g: pd.Series({'p':np.average(g.p,weights=g.w),'n':g.book.nunique()}),include_groups=False).reset_index()
known=set(st.k); days=set(st.game_date)
c=c.merge(st[['game_date','k','rec','rec_yds','rush_yds','rush_att','pass_yds','pass_att']],on=['game_date','k'],how='left')
c['matched']=c.rec.notna()
c=c[c.matched|(c.k.isin(known)&c.game_date.isin(days))]   # unmatched known player on a played date = 0 (or inactive -> void)
c=c.fillna(0)
c['act']=[r[r.stat] for _,r in c.iterrows()]; c=c[c.act!=c.line]; c['y']=(c.act>c.line).astype(int)
c=c[c.n>=2]
out=["# NFL Prop Calibration",f"{len(c)} player-lines (2+ books, last pregame quote) joined to play-by-play, {c.game_date.min()} to {c.game_date.max()}.","Over side. 'Books said' = no-vig consensus chance of the over.","",
     "| stat | n | books said (over) | over hit | gap | noise ± |","|---|---|---|---|---|---|"]
for s,g in list(c.groupby('stat'))+[('ALL',c)]:
    se=np.sqrt((g.p*(1-g.p)).sum())/len(g)
    out.append(f"| {s} | {len(g)} | {g.p.mean()*100:.1f}% | {g.y.mean()*100:.1f}% | {(g.y.mean()-g.p.mean())*100:+.1f} | {se*100:.1f} |")
c['b']=pd.cut(c.p,[0,.3,.4,.45,.55,.6,.7,1])
out+=["","| priced (over) | n | books said | over hit | gap |","|---|---|---|---|---|"]
for b,g in c.groupby('b',observed=True): out.append(f"| {b} | {len(g)} | {g.p.mean()*100:.1f}% | {g.y.mean()*100:.1f}% | {(g.y.mean()-g.p.mean())*100:+.1f} |")
# low lines (x.5 receptions <=2.5, yards < 15)
lo=c[((c.stat=='rec')&(c.line<=2.5))|((c.stat.isin(['rec_yds','rush_yds']))&(c.line<20))]
z=c[~c.matched]
out+=["",f"Zero-stat games assumed (player known, no touch/target that day; true inactives would have voided): {len(z)} of {len(c)}. Results below with them counted as 0; 'matched only' excludes them (upper bound for overs)."]
m=c[c.matched]
for s,g in m.groupby('stat'): out.append(f"- matched only {s}: n={len(g)}, said {g.p.mean()*100:.1f}%, over hit {g.y.mean()*100:.1f}%")
if len(lo): out+=["",f"Low lines (rec <=2.5, yards <20): n={len(lo)}, books said over {lo.p.mean()*100:.1f}%, over hit {lo.y.mean()*100:.1f}% ({(lo.y.mean()-lo.p.mean())*100:+.1f})."]
open('Record/NFL Prop Calibration.md','w').write("\n".join(out)); print("\n".join(out))
