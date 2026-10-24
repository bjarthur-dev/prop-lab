"""MLB strikeout + outs model v1: plate-appearance-by-plate-appearance simulation with a pitch-count hook.
Replaces v0's Normal(batters faced) with a pitch budget, adds a park K factor and smooth times-through-order decay,
and prices K and outs props from ONE simulation (so they stay consistent).

Usage:  python engine/mlb/k_model_v1.py inputs.json        (see example_inputs.json)
Evidence: [[Research - Advanced NFL and MLB mechanisms]] — K% reliability ~70 BF (Carleton), no sharp TTO cliff
(Brill/Deshpande/Wyner), AmFam K factor ~+12% (secondary), ABS net ~+0.05 K/team-game (ignored)."""
import json, sys
import numpy as np

LG_K = 0.222        # 2025 league K% (2026 final not sourced)
LG_BB = 0.084
P_PER_PA = {"K": 4.9, "BB": 5.8, "BIP": 3.4}   # (H) typical pitches by PA outcome; scaled by pitcher P/PA factor
BIP_OUT = 0.70      # (H) share of balls in play that become outs (incl. DP/CS noise ignored)

def odds(p): return p / (1 - p)
def log5(p_pit, p_bat, p_lg):
    o = odds(p_pit) * odds(p_bat) / odds(p_lg); return o / (1 + o)

def talent_k(rs_k, rs_bf, ps_k=0, ps_bf=0, rel_bf=70):
    """Blend postseason sample into the pitcher's own regular-season rate with weight n/(n+70)."""
    rs = rs_k / rs_bf
    if ps_bf <= 0: return rs
    w = ps_bf / (ps_bf + rel_bf)
    return (1 - w) * rs + w * (ps_k / ps_bf)

def simulate(inp, n=100000, seed=7):
    rng = np.random.default_rng(seed)
    pk = talent_k(inp["rs_k"], inp["rs_bf"], inp.get("ps_k", 0), inp.get("ps_bf", 0)) * inp.get("talent_adj", 1.0)
    pbb = inp.get("bb_pct", LG_BB)
    park = 1 + inp.get("park_k_factor", 0.0) * inp.get("park_weight", 0.5)
    lineup = inp.get("lineup_k", [inp.get("team_k", LG_K)] * 9)          # per-slot K% vs this hand (or team K%)
    ppa_scale = inp.get("p_per_pa", 3.9) / 3.9
    hook_mu, hook_sd = inp.get("hook_pitches", 90), inp.get("hook_sd", 10)
    max_bf = inp.get("max_bf", 30)
    p_k_by_slot = np.array([min(0.6, log5(pk, b, LG_K) * park) for b in lineup])
    hook = rng.normal(hook_mu, hook_sd, n)
    pitches = np.zeros(n); ks = np.zeros(n, int); outs = np.zeros(n, int); bf = np.zeros(n, int)
    alive = np.ones(n, bool)
    for i in range(max_bf):
        decay = 1 - inp.get("tto_decay_per_bf", 0.004) * i          # smooth decline, no 3rd-time cliff
        pk_i = p_k_by_slot[i % 9] * decay
        u = rng.random(n)
        is_k = (u < pk_i) & alive
        is_bb = (u >= pk_i) & (u < pk_i + pbb) & alive
        is_bip = alive & ~is_k & ~is_bb
        bip_out = is_bip & (rng.random(n) < BIP_OUT)
        p = np.where(is_k, P_PER_PA["K"], np.where(is_bb, P_PER_PA["BB"], P_PER_PA["BIP"])) * ppa_scale
        p = p + rng.normal(0, 1.2, n)
        pitches += np.where(alive, p, 0)
        ks += is_k; outs += is_k | bip_out; bf += alive
        if inp.get("max_outs"): alive &= outs < inp["max_outs"]
        alive &= pitches < hook
    return {"k": ks, "outs": outs, "bf": bf, "pitches": pitches, "talent_k": pk}

def american(p): return round(-100 * p / (1 - p)) if p >= 0.5 else round(100 * (1 - p) / p)

def report(name, inp, lines):
    s = simulate(inp)
    print(f"\n{name}: talent K% {s['talent_k']:.3f} | BF {s['bf'].mean():.1f} | pitches {s['pitches'].mean():.0f} | "
          f"K mean {s['k'].mean():.2f} | outs mean {s['outs'].mean():.1f}")
    for mk, ln in lines:
        p = (s[mk] > ln).mean()
        print(f"  {mk} {ln}: P(over) {p:.3f} (fair {american(p):+d}) | P(under) {1-p:.3f} (fair {american(1-p):+d})")
    return s

if __name__ == "__main__":
    cfg = json.load(open(sys.argv[1]))
    for name, block in cfg.items():
        report(name, block["inputs"], [tuple(x) for x in block["lines"]])


def devig(o, u):
    def imp(a): a = float(a); return 100 / (a + 100) if a > 0 else -a / (-a + 100)
    po, pu = imp(o), imp(u); return po / (po + pu)

def market_implied_hook(inp, outs_line, outs_over, outs_under, lo=55, hi=125):
    """Find the hook (mean pitch budget) that makes the model's P(outs > line) match the devigged outs market.
    Strikeouts priced with this hook carry no leash disagreement: any K edge left is pure K-rate."""
    target = devig(outs_over, outs_under)
    for _ in range(16):
        mid = (lo + hi) / 2
        p = (simulate({**inp, "hook_pitches": mid}, n=20000)["outs"] > outs_line).mean()
        lo, hi = (mid, hi) if p < target else (lo, mid)
    return (lo + hi) / 2, target
