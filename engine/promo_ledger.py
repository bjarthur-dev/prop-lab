"""Promo ledger: boosted/promo bets vs plain bets, expected profit (stake x EV) vs actual, predicted vs actual hit rate.
Writes Record/Promo Ledger.md.   python engine/promo_ledger.py"""
import pandas as pd,numpy as np
b=pd.read_csv('Record/bets.csv',dtype=str,keep_default_na=False)
for c in ['stake','model_prob','ev_pct','profit']: b[c]=pd.to_numeric(b[c],errors='coerce')
s=b[b.profit.notna()&(b.stake>0)].copy()
s['kind']=np.where(s.notes.str.contains('boost|Boost|promo|Promo|Bet & Earn|CageBreaker|discount|Bucks|Super Boost',regex=True),'promo / boost','plain')
s['exp']=s.stake*s.ev_pct/100
out=["# Promo Ledger","Every settled real-money bet, split into promo/boosted vs plain. Expected = stake x our EV at bet time.","","| kind | bets | staked | expected profit | actual profit | predicted hit | actual hit |","|---|---|---|---|---|---|---|"]
for k,g in s.groupby('kind'):
    out.append(f"| {k} | {len(g)} | ${g.stake.sum():.2f} | ${g.exp.sum():+.2f} | ${g.profit.sum():+.2f} | {g.model_prob.mean()*100:.1f}% | {(g.profit>0).mean()*100:.1f}% |")
p=s[s.kind!='plain']; big=p.profit.max()
out+=["",f"Promo profit without the single biggest win (${big:.2f}): ${p.profit.sum()-big:+.2f}.","From 2026-11-09 (calibrated pricer) on:"]
q=s[s.date>='2026-11-09']
for k,g in q.groupby('kind'): out.append(f"- {k}: {len(g)} bets, expected ${g.exp.sum():+.2f}, actual ${g.profit.sum():+.2f}, predicted hit {g.model_prob.mean()*100:.1f}% vs actual {(g.profit>0).mean()*100:.1f}%")
open('Record/Promo Ledger.md','w').write("\n".join(out)); print("\n".join(out))
