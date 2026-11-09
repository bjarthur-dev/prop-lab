"""Honest scoreboard of the real money. Writes Record/Audit.md (runs every morning in results.yml).
    python engine/audit.py
Shows profit with and without the single biggest win, results by bet type, whether stated hit chances came true,
and closing-line value. These are the numbers that decide stake size, not how a slip feels."""
import numpy as np, pandas as pd
def imp(o): o = np.asarray(o, float); return np.where(o < 0, -o / (-o + 100), 100 / (o + 100))

def main():
    b = pd.read_csv("Record/bets.csv"); b["profit"] = pd.to_numeric(b.profit, errors="coerce")
    L = b[(b.decision == "live") & b.profit.notna() & (b.stake > 0)].copy()
    out = ["# Audit (real money)\n", f"Updated {pd.Timestamp.now(tz='America/New_York'):%Y-%m-%d %H:%M} ET. Built by engine/audit.py.\n"]
    if L.empty: open("Record/Audit.md", "w").write("\n".join(out)); return
    top = L.profit.max()
    out.append(f"- Settled bets: **{len(L)}**, staked **${L.stake.sum():.2f}**, profit **${L.profit.sum():+.2f}** ({L.profit.sum()/L.stake.sum()*100:+.0f}%).")
    out.append(f"- Without the single biggest win (${top:.2f}): **${L.profit.sum()-top:+.2f}**. That is the number to judge the method by.")
    out.append(f"- Open bets: {int(((b.decision=='live') & b.profit.isna()).sum())}.\n")
    L["kind"] = L.type.fillna("?")
    g = L.groupby("kind").agg(bets=("stake", "size"), staked=("stake", "sum"), profit=("profit", "sum"), wins=("profit", lambda x: int((x > 0).sum()))).round(2)
    g["roi_pct"] = (g.profit / g.staked * 100).round(0)
    out.append("## By bet type\n\n" + g.sort_values("staked", ascending=False).to_markdown() + "\n")
    g = L.groupby("date").agg(bets=("stake", "size"), staked=("stake", "sum"), profit=("profit", "sum")).round(2)
    out.append("## By day\n\n" + g.to_markdown() + "\n")
    C = L[L.model_prob.notna() & ~L.result.astype(str).str.contains("void|refund|cashout")].copy()
    if len(C):
        C["won"] = (C.profit > 0).astype(int); exp, act = C.model_prob.sum(), int(C.won.sum())
        rng = np.random.default_rng(0); sim = (rng.random((100000, len(C))) < C.model_prob.values).sum(1)
        out.append("## Did our stated hit chances come true?\n")
        out.append(f"- {len(C)} bets carried a stated chance. They added up to **{exp:.1f} expected wins**; **{act} won**.")
        out.append(f"- Chance of doing this badly by luck alone if the numbers were right: **{(sim <= act).mean()*100:.0f}%**.")
        out.append("- Under ~10% means the stated chances were too high, not that we were unlucky.\n")
    P = b[b.decision.isin(["paper", "live"]) & b.close_odds.notna() & b.close_odds_opp.notna()].copy()
    P = P[pd.to_numeric(P.line, errors="coerce") == P.close_line]
    if len(P):
        a, o = imp(P.close_odds), imp(P.close_odds_opp); P["cf"] = a / (a + o); P["clv"] = P.cf / imp(P.odds) - 1
        out.append("## Closing-line value (singles with a recorded close)\n")
        out.append(f"- {len(P)} bets. Average CLV **{P.clv.mean()*100:+.1f}%**; beat the close **{(P.clv>0).mean()*100:.0f}%** of the time.")
        out.append(f"- Our stated chance averaged {P.model_prob.mean()*100:.1f}%, the closing no-vig price {P.cf.mean()*100:.1f}%, and {((P.result=='win').mean())*100:.1f}% won.")
        out.append("- Positive average CLV over 50+ bets is the proof of an edge. Negative means the picks are not beating the market.\n")
    open("Record/Audit.md", "w").write("\n".join(out)); print("\n".join(out))

if __name__ == "__main__": main()
