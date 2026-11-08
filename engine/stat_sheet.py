"""Our own stat sheet: every real-money bet since the system started (2026-10-26), by venue, sport, type, boost and month,
plus withdrawals/tool costs and the bankroll path.  python engine/stat_sheet.py  -> Record/Stat Sheet.md"""
import os
import pandas as pd

def venue(r):
    b = str(r.book).lower(); m = str(r.market).lower()
    return "Pick6" if "pick6" in b or m == "pick6" else "Sportsbook"

def main():
    b = pd.read_csv("Record/bets.csv")
    b = b[(b.decision == "live") & b.result.isin(["win", "loss", "push", "refund"])].copy()
    b["profit"] = b.profit.fillna(0); b["venue"] = b.apply(venue, axis=1)
    b["boosted"] = b.notes.fillna("").str.contains("boost", case=False) | b.player.fillna("").str.contains("boost", case=False)
    b["kind"] = b.type.fillna("single").replace({"pick6": "Pick6 entry", "single": "single", "parlay": "parlay", "live_hedge": "live hedge"})
    b["month"] = b.date.astype(str).str[:7]
    ex = pd.read_csv("Record/expenses.csv") if os.path.exists("Record/expenses.csv") else pd.DataFrame(columns=["date", "item", "amount"])
    bk = open("Record/Bankroll.md").read(); cur = float(bk.split("current_bankroll:")[1].split()[0])
    won = b[b.result == "win"]; staked = b.stake.sum(); prof = b.profit.sum()
    big = b.sort_values("profit", ascending=False).head(5)

    def tbl(col, title):
        out = [f"### By {title}", "", "| | bets | won | staked | profit | ROI |", "|---|---:|---:|---:|---:|---:|"]
        for k, x in b.groupby(col):
            out.append(f"| {k} | {len(x)} | {int((x.result=='win').sum())} | ${x.stake.sum():.2f} | ${x.profit.sum():+.2f} | {100*x.profit.sum()/max(x.stake.sum(),.01):+.0f}% |")
        return out + [""]
    L = ["---", "tags: [record, stat-sheet]", "---", "", "# Our stat sheet (real money, since 2026-10-26)", "",
         "Written by `engine/stat_sheet.py` every morning from Record/bets.csv and Record/expenses.csv. DraftKings' own 'Stat Sheet' also counts older play and Predictions; this one is only what we've bet together.", "",
         f"- **Bets:** {len(b)} settled, {len(won)} won ({100*len(won)/max(len(b),1):.0f}%).",
         f"- **Staked:** ${staked:.2f}. **Profit:** ${prof:+.2f} (ROI {100*prof/max(staked,1):+.1f}%).",
         f"- **Tools paid from winnings:** ${ex.amount.sum():.2f}. **Net after tools:** ${prof-ex.amount.sum():+.2f}.",
         f"- **Bankroll now:** ${cur:.2f} (DraftKings).", ""]
    L += tbl("venue", "venue") + tbl("sport", "sport") + tbl("kind", "bet type") + tbl("boosted", "boosted (True = a profit boost or promo was applied)") + tbl("month", "month")
    L += ["### Biggest wins", "", "| date | bet | stake | profit |", "|---|---|---:|---:|"]
    for _, r in big.iterrows():
        L.append(f"| {r.date} | {str(r.player)[:90]} | ${r.stake:.2f} | ${r.profit:+.2f} |")
    L += ["", "### Withdrawals and tool costs", "", "| date | item | amount |", "|---|---|---:|"]
    for _, r in ex.iterrows():
        L.append(f"| {r.date} | {r['item']} | ${float(r.amount):.2f} |")
    open("Record/Stat Sheet.md", "w").write("\n".join(L) + "\n"); print("\n".join(L[7:12]))

if __name__ == "__main__":
    main()
