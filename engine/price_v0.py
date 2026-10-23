import re, sys, json, statistics as st
import numpy as np
def dec(a): a=float(a); return 1+a/100 if a>0 else 1+100/-a
def imp(a): return 1/dec(a)
def devig(o,u):
    po,pu=imp(o),imp(u); return po/(po+pu)
txt=open(sys.argv[1]).read()
rows=[]
# compact format: {player: X, ... pts: '...', reb: '...', ast: '...'}
for m in re.finditer(r"\{player: ([^,]+), role: ([^,]+(?:\([^)]*\))?)[^{]*?status_1315: ([^,]+),.*?(?=\n    - \{player|\nR9_|\nR10|\n```)", txt, re.S):
    player, role, status = m.group(1).strip(), m.group(2).strip(), m.group(3).strip()
    blk=m.group(0).replace('\n',' ')
    blk=re.sub(r"\s+"," ",blk)
    for mk in ('pts','reb','ast'):
        mm=re.search(mk+r": '([^']*)'", blk)
        if not mm: continue
        seg=mm.group(1)
        fd=re.search(r"FD\(exec\): (\d+\.?\d*) o([+-]\d+)/u([+-]\d+)", seg)
        refs=re.findall(r"(DK|MGM|CZR)\(ref\): (\d+\.?\d*) o([+-]\d+)@([\d:]+)/u([+-]\d+)@([\d:]+)", seg)
        rows.append(dict(player=player,role=role,status=status,market=mk,fd=fd.groups() if fd else None,refs=[(b,l,o,u,t1) for b,l,o,t1,u,t2 in refs]))
# CHI format
chi=txt[txt.find('R9_CHI_board'):txt.find('R9_WAS')]
for m in re.finditer(r"- player: (.+?)\n(.*?)(?=\n  - player:|\Z)", chi, re.S):
    player=m.group(1).strip(); blk=m.group(2)
    for mk in ('pts','reb','ast'):
        mm=re.search(r"\n\s+"+mk+r": \{(.*)", blk)
        if not mm: continue
        seg=mm.group(1)
        fd=re.search(r"FanDuel: 'line (\d+\.?\d*) \| over ([+-]\d+) \| under ([+-]\d+)", seg)
        refs=[]
        for b,s in re.findall(r"(DraftKings|BetMGM|Caesars) \(reference\): '([^']*)'", seg):
            o=re.search(r"over (\d+\.?\d*) ([+-]\d+)",s); u=re.search(r"under (\d+\.?\d*) ([+-]\d+)",s)
            if o and u and o.group(1)==u.group(1): refs.append((b,o.group(1),o.group(2),u.group(2),''))
        rows.append(dict(player=player,role='CHI',status='',market=mk,fd=fd.groups() if fd else None,refs=refs))
out=[]
for r in rows:
    if not r['fd']: continue
    line,o,u=r['fd']
    same=[devig(ro,ru) for b,l,ro,ru,t in r['refs'] if l==line]
    if not same: continue
    p_cons=st.median(same+[devig(o,u)])  # consensus incl FD
    p_ref=st.median(same)
    for side,price,p in (('over',o,p_ref),('under',u,1-p_ref)):
        ev=p*dec(price)-1; be=imp(price)
        out.append((ev,r['player'],r['market'],line,side,price,round(p,3),round(be,3),len(same)))
out.sort(reverse=True)
print(f"{len(rows)} player-markets parsed")
for x in out[:25]: print(f"EV {x[0]*100:+.1f}% | {x[1]} {x[2]} {x[4]} {x[3]} FD {x[5]} | p_ref {x[6]} BE {x[7]} | n_ref {x[8]}")
json.dump(out,open('/home/claude/engine/nba_board.json','w'))
