import numpy as np
rng=np.random.default_rng(7)
def odds(p): return p/(1-p)
def log5(pk,bk,lg=0.222):
    o=odds(pk)*odds(bk)/odds(lg); return o/(1+o)
def dec(a): a=float(a); return 1+a/100 if a>0 else 1+100/-a
def imp(a): return 1/dec(a)
def devig(o,u): po,pu=imp(o),imp(u); return po/(po+pu)
def shrink(k,bf,prior=0.222,n0=150): return (k+prior*n0)/(bf+n0)
N=200000
def sim(name,k_rs,bf_rs,k_ps,bf_ps,opp,bf_mu,bf_sd):
    pk=shrink(k_rs+k_ps,bf_rs+bf_ps)            # talent K%, shrunk lightly toward league
    p=log5(pk,opp)
    # parameter uncertainty on p (beta) + BF uncertainty (normal, truncated)
    ps=rng.beta(p*300,(1-p)*300,N)
    bf=np.clip(np.round(rng.normal(bf_mu,bf_sd,N)),8,30).astype(int)
    k=rng.binomial(bf,ps)
    print(f"{name}: talent K% {pk:.3f} | vs-lineup p {p:.3f} | BF mean {bf.mean():.1f} | K mean {k.mean():.2f}")
    return k
# Misiorowski: RS 252/665, PS 11/37; Rays K% vs RHP 19.1
# BF: RS 22.2/start, PS 19,18; market outs line 16.5 (~5.5 IP) implies ~21 BF -> use 20.5 +- 3.5
kM=sim("Misiorowski",252,665,11,37,0.191,20.5,3.5)
# Martinez: RS 109/722, PS 6/34; Brewers K% vs RHP 22.3; BF: RS 23.3, PS 18,16; market outs 12.5-13.5 -> ~17.5 BF +- 3.5
kN=sim("Martinez",109,722,6,34,0.223,17.5,3.5)
def show(name,k,fd,pin,alts):
    print(f"\n{name}")
    for ln,(o,u) in fd.items():
        po=(k>ln).mean(); 
        fair=devig(*pin[ln]) if ln in pin else None
        for side,price,p in (("over",o,po),("under",u,1-po)):
            ev=p*dec(price)-1; be=imp(price)
            mk=f" | Pinnacle fair {fair if side=='over' else 1-fair:.3f}" if fair else ""
            print(f"  {side} {ln}: model p {p:.3f} | FD {price} BE {be:.3f} | EV {ev*100:+.1f}% | raw edge {100*(p-be):+.1f} pts | shrunk(0.4) {40*(p-be):+.1f}{mk}")
    for ln,price in alts.items():
        po=(k>=ln).mean(); ev=po*dec(price)-1
        print(f"  alt {ln}+ at FD {price}: model p {po:.3f} BE {imp(price):.3f} EV {ev*100:+.1f}%")
show("Misiorowski",kM,{6.5:(-132,104)},{6.5:(-125,103)},{5:-900,6:-350,8:136,9:280,10:540})
show("Martinez",kN,{3.5:(144,-186)},{3.5:(135,-173)},{3:-225,5:310,6:680})
# sensitivity: Martinez with RS-like leash 21 BF
k2=sim("Martinez (long-leash scenario)",109,722,6,34,0.223,21,3.5); print("  P(>=4)",(k2>=4).mean().round(3))
k3=sim("Misiorowski (short-leash 19 BF)",252,665,11,37,0.191,19,3.0); print("  P(>=7)",(k3>=7).mean().round(3))
