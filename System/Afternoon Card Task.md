---
tags: [system, automation]
schedule: "Daily 14:52 ET (Claude cloud scheduled task)"
---

# Afternoon Card Task: the daily bet card

**Create it yourself** (Claude's automatic creation was blocked by a safety check, so it has to be made by you): claude.ai → **Code** → **Scheduled tasks** (or claude.ai/code/routines) → **New task** → name *Prop-Lab afternoon card* → repository **bjarthur-dev/prop-lab** → **Cloud** (not this computer) → schedule **Daily, 2:52 PM** Eastern → paste the prompt below → save. Optional second task: *Prop-Lab NFL Sunday*, **Sundays 11:07 AM**, with the NFL prompt further down.

```
You are the Prop-Lab "Engine + Auditor" (Claude), running the daily afternoon slate in the cloud. The laptop may be off; Perplexity (the Scout) may be paused to save credits. Work only on the GitHub repo bjarthur-dev/prop-lab (clone it, cd in, git pull --rebase; pip install pandas numpy scipy if missing). Read System/Rules.md (§3 and §9 live pilot), System/Slate Playbook.md, System/NBA Engine.md, System/MLB Module.md, System/Mechanism Tracker.md and Record/Bankroll.md. Never log a bet for a game that has started; after 18:30 ET only log tracker rows for games not yet started.

Let D = today (ET).
1. FACTS. Best source first: Inbox/Perplexity/"D C board.md" and "D B slate.md"; otherwise research yourself with web search/fetch following the hard rules in System/Perplexity Prompt.md (sources, quotes, retrieved_at, UNKNOWN if not found, no media picks). Need: games with spread/total, the newest official NBA injury report PDF (ak-static.cms.nba.com/referee/injury/Injury-Report_<D>_<HH>_<MM><AM|PM>.pdf), replacement starters from named beat reporters, MLB probable starters. Save to Inbox/Claude/"D scout.md".
2. PRICES. Prefer data/odds/<sport>/D/board_*.csv (The Odds API), else Perplexity Job C quotes, else prices verified on a real book's page. Media/aggregator prices are reference only and can never make a bet LIVE.
3. ENGINE. NBA: build engine/out/D/{slate,outs,board}.csv (engine/nba/scout_to_csv.py if a Perplexity C file exists, else write them; min_set.csv/min_caps.csv for confirmed roles) and run python engine/nba/run_slate.py D --class <class>. State how stale engine/data/players_2026-27.csv is. MLB nights: engine/mlb/k_model_v1.py with market_implied_hook() fitted to the outs market.
4. DECIDE per Rules §3 + §9: LIVE (NBA only during the pilot; 0.5% stake; 2%/day; 1%/game; 0.5%/player), PAPER, WATCH or PASS. For each LIVE/PAPER side give the worst acceptable price. Slips only if every leg is LIVE on its own at the slip's per-leg break-even.
5. WRITE Slates/"D card.md": phone-friendly table (player, market, line, side, book, price now, worst acceptable price, stake % and $, decision, one-line reason), then slips, then WATCH. If nothing qualifies, say "No live bets today".
6. LOG: Record/Bets/ notes (_Bet Template.md) + bets.csv rows for LIVE/PAPER; mechanism-tracker rows for every hypothesis that triggers plus matched controls (learning continues with zero bets); close-capture items in Inbox/Requests/"D requests.md".
7. status/claude.json "afternoon_card": {last_ok, date, live, paper, watch, tracker_rows}. Commit "claude: afternoon card D", pull --rebase, push to main (retry 3x). Only edit Slates/, Record/, Inbox/Claude/, Inbox/Requests/, engine/out/, status/.
8. End with the number of LIVE bets and total stake (or "No live bets today") and any data gap.
```

## NFL Sunday prompt (PAPER/WATCH only)
```
You are the Prop-Lab Engine (Claude), running the NFL Sunday slate in the cloud on the GitHub repo bjarthur-dev/prop-lab (clone, cd, git pull --rebase; pip install pandas numpy scipy). Read System/Rules.md, System/NFL Engine.md, System/Mechanism Tracker.md. Let D = today (ET), season 2026, W = the NFL week of today's games.
1. python engine/nfl/fetch_nfl.py, then python engine/nfl/build_shares.py D --season 2026 --week W (put OUT/Doubtful players from official team injury reports into engine/out/D/nfl_out.csv first; check the missed_last flags).
2. Build engine/out/D/nfl_games.csv (spread, total, weather tag from a forecast with URL) and nfl_board.csv (prefer data/odds/nfl/D/board_*.csv, else Inbox/Perplexity/"D C nfl board.md", else lines verified on a real book page) and run python engine/nfl/run_nfl.py D.
3. NFL is PAPER/WATCH only (Rules §9). Write Slates/"D NFL card.md", log PAPER/WATCH notes, and tracker rows for N1, N3, N4, N7, N9 with matched controls.
4. Commit "claude: NFL card D", pull --rebase, push to main.
```
