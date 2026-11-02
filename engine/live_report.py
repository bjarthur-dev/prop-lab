"""Real-money results by method, after tool costs, plus the next-upgrade gate.
    python engine/live_report.py  -> Record/Live Report.md
Reads Record/bets.csv (decision == live, settled) and Record/expenses.csv (date,item,amount,notes).
Tiers by payout multiple: safe (<= 3x or singles), mid (3-8x), long shot (>= 8x), hedge (type live_hedge)."""
import os
import pandas as pd

def tier(r):
    if str(r.type) == "live_hedge": return "hedge"
    m = r.payout_mult if pd.notna(r.payout_mult) else 0
    if r.type == "single" or m <= 3: return "safe"
    return "long shot" if m >= 8 else "mid"

def main():
    b = pd.read_csv("Record/bets.csv")
    b = b[(b.decision == "live") & b.result.isin(["win", "loss", "push", "refund"])].copy()
    b["profit"] = b.profit.fillna(0); b["tier"] = b.apply(tier, axis=1)
    b["boosted"] = b.notes.fillna("").str.contains("boost", case=False)
    ex = pd.read_csv("Record/expenses.csv") if os.path.exists("Record/expenses.csv") else pd.DataFrame(columns=["date", "item", "amount"])
    bk = open("Record/Bankroll.md").read()
    cur = float(bk.split("current_bankroll:")[1].split()[0])
    gross, staked, cost = b.profit.sum(), b.stake.sum(), ex.amount.sum()
    L = ["---", "tags: [record, live]", "---", "", "# Live results by method (real money)", "",
         "Written by `engine/live_report.py` each morning. Tool costs come from `Record/expenses.csv`.", "",
         f"**{len(b)} settled bets, staked ${staked:.2f}, profit ${gross:+.2f} (ROI {100*gross/max(staked,1):+.1f}%). "
         f"Tool costs ${cost:.2f}. Net after tools ${gross-cost:+.2f}.** Bankroll now ${cur:.2f}.", "",
         "| method | bets | won | staked | profit | ROI |", "|---|---:|---:|---:|---:|---:|"]
    for t, x in b.groupby("tier"):
        L.append(f"| {t} | {len(x)} | {int((x.result=='win').sum())} | ${x.stake.sum():.2f} | ${x.profit.sum():+.2f} | {100*x.profit.sum()/max(x.stake.sum(),.01):+.0f}% |")
    for flag, x in b.groupby("boosted"):
        L.append(f"| {'boosted' if flag else 'no boost'} (all tiers) | {len(x)} | {int((x.result=='win').sum())} | ${x.stake.sum():.2f} | ${x.profit.sum():+.2f} | {100*x.profit.sum()/max(x.stake.sum(),.01):+.0f}% |")
    L += ["", "| date | bets | profit | running |", "|---|---:|---:|---:|"]
    run = 0
    for d, x in b.groupby("date"):
        run += x.profit.sum(); L.append(f"| {d} | {len(x)} | ${x.profit.sum():+.2f} | ${run:+.2f} |")
    big = b.sort_values("profit", ascending=False).head(1)
    if len(big) and gross > 0:
        L += ["", f"Without the single biggest win ({big.date.iloc[0]}, ${big.profit.iloc[0]:+.2f}) profit would be "
              f"${gross-big.profit.iloc[0]:+.2f}: one long shot is carrying the record until the sample grows."]
    # upgrade gate (Bankroll.md funding rule)
    month = pd.Timestamp.now(tz="America/New_York").strftime("%Y-%m")
    last30 = b[pd.to_datetime(b.date) >= pd.Timestamp.now() - pd.Timedelta(days=30)]
    mprofit = last30.profit.sum(); mcost = ex[ex.date.astype(str).str[:7] == month].amount.sum() if len(ex) else 0
    L += ["", "## Next upgrade gate", "",
          f"- Profit last 30 days ${mprofit:+.2f} vs tool costs this month ${mcost:.2f}.",
          "- Odds API paid tier (~$30/mo, confirm price): buy only when the price-edge report shows mean CLV > 0 over 50+ legs, "
          "30-day profit excluding the biggest win >= $60, and bankroll >= $150 (cost <= 15%, bankroll stays >= $60)."]
    ok = mprofit - (b.sort_values('profit').profit.iloc[-1] if len(b) else 0) >= 60 and cur >= 150
    L.append(f"- Status: **{'PASSES: check CLV, then buy' if ok else 'not yet'}**")
    open("Record/Live Report.md", "w").write("\n".join(L) + "\n"); print("\n".join(L[8:]))

if __name__ == "__main__":
    main()
