"""Turn the Scout's Job B (slate) and Job C (board) markdown files into CSVs the engine reads."""
import re, sys, os
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from common import TEAMS

def parse_board(text):
    rows = []
    def add(player, mk, book, line, o, u, ex, ts):
        rows.append(dict(player=player, market=mk, line=float(line), book=book, over=float(o), under=float(u), executable=ex, ts=ts))
    # compact format
    for m in re.finditer(r"\{player: ([^,]+), role:.*?(?=\n    - \{player|\nR9_|\nR10|\n```)", text, re.S):
        player = m.group(1).strip(); blk = re.sub(r"\s+", " ", m.group(0))
        for mk in ("pts", "reb", "ast"):
            mm = re.search(mk + r": '([^']*)'", blk)
            if not mm: continue
            seg = mm.group(1)
            f = re.search(r"FD\(exec\): (\d+\.?\d*) o([+-]\d+)/u([+-]\d+) \[([\d:]+)\]", seg)
            if f: add(player, mk, "FanDuel", f.group(1), f.group(2), f.group(3), True, f.group(4))
            for b, l, o, t1, u, t2 in re.findall(r"(DK|MGM|CZR)\(ref\): (\d+\.?\d*) o([+-]\d+)@([\d:]+)/u([+-]\d+)@([\d:]+)", seg):
                add(player, mk, b, l, o, u, False, t1)
    # long format (CHI block)
    for m in re.finditer(r"- player: (.+?)\n(.*?)(?=\n  - player:|\nR9_|\n```|\Z)", text, re.S):
        player = m.group(1).strip(); blk = m.group(2)
        for mk in ("pts", "reb", "ast"):
            mm = re.search(r"\n\s+" + mk + r": \{(.*)", blk)
            if not mm: continue
            seg = mm.group(1)
            f = re.search(r"FanDuel: 'line (\d+\.?\d*) \| over ([+-]\d+) \| under ([+-]\d+) \| EXECUTABLE \| retrieved ([\d:]+)", seg)
            if f: add(player, mk, "FanDuel", f.group(1), f.group(2), f.group(3), True, f.group(4))
            for b, s in re.findall(r"(DraftKings|BetMGM|Caesars) \(reference\): '([^']*)'", seg):
                o = re.search(r"over (\d+\.?\d*) ([+-]\d+) @([\d:]+)", s); u = re.search(r"under (\d+\.?\d*) ([+-]\d+)", s)
                if o and u and o.group(1) == u.group(1): add(player, mk, b, o.group(1), o.group(2), u.group(2), False, o.group(3))
    return pd.DataFrame(rows).drop_duplicates()

def _name(last_first):
    p = [x.strip() for x in last_first.split(",")]
    return f"{p[1]} {p[0]}" if len(p) == 2 else last_first

def parse_slate(text):
    games, outs = [], []
    for m in re.finditer(r"- game_id: ([A-Z]{3})@([A-Z]{3}) \d{4}-\d{2}-\d{2}\n(.*?)(?=\n- game_id|\n```|\Z)", text, re.S):
        away, home, blk = m.group(1), m.group(2), re.sub(r"\s+", " ", m.group(3))
        spread = total = None
        sp = re.search(r"spread:.*?FanDuel: '([^']*)'", blk)
        if sp:
            for name, ab in TEAMS.items():
                mm = re.search(re.escape(name) + r" ([+-]\d+\.?\d*)", sp.group(1))
                if mm and ab == home: spread = float(mm.group(1))
                elif mm and ab == away and spread is None: spread = -float(mm.group(1))
        tt = re.search(r"total:.*?FanDuel: '[^']*?(?:Over|Under) (\d+\.?\d*)", blk)
        if tt: total = float(tt.group(1))
        games.append(dict(away=away, home=home, spread_home=spread, total=total))
        for team, last_first in re.findall(r"'([A-Z]{3}): ([^|']+?) \| (?:Out|Doubtful) \|", blk):
            outs.append(dict(team=team, player=_name(last_first)))
    return pd.DataFrame(games), pd.DataFrame(outs)

def parse_status_changes(text):
    """Job C R6: players whose status changed to Out (added) or away from Out (removed)."""
    add, rem = [], []
    pairs = re.findall(r'player: "([^"]+)", team: [A-Z]{3}, was: "[^"]*", now: "([^"]+)"', text)
    pairs += re.findall(r"'[A-Z]{3}: ([^|']+?) \| [^'>]*?-> ([A-Za-z]+)", text)
    for name, now in pairs:
        (add if now.lower().startswith(("out", "doubtful")) else rem).append(_name(name.strip()))
    return add, rem

if __name__ == "__main__":
    date = sys.argv[1]
    inbox = "Inbox/Perplexity"
    out = f"engine/out/{date}"; os.makedirs(out, exist_ok=True)
    b = open(f"{inbox}/{date} B slate.md", encoding="utf-8").read()
    games, outs = parse_slate(b)
    cpath = f"{inbox}/{date} C board.md"
    if os.path.exists(cpath):
        c = open(cpath, encoding="utf-8").read()
        board = parse_board(c); board.to_csv(f"{out}/board.csv", index=False)
        add, rem = parse_status_changes(c)
        outs = pd.concat([outs[~outs["player"].isin(rem)], pd.DataFrame({"team": "", "player": add})], ignore_index=True)
        print(f"board rows: {len(board)}")
    games.to_csv(f"{out}/slate.csv", index=False); outs.to_csv(f"{out}/outs.csv", index=False)
    print(f"games: {len(games)}  outs: {len(outs)}  -> {out}")
