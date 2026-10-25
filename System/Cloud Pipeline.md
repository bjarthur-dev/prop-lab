---
tags: [system, automation, cloud]
updated: 2026-10-24
---

# Cloud Pipeline: what runs with the laptop off

**GitHub is the hub.** Everything below runs on GitHub's or Anthropic's or Perplexity's servers and writes into the repo `bjarthur-dev/prop-lab`. The laptop (Obsidian) only reads and edits; it pulls changes when it's on.

| Time (ET) | Who | Job | Writes |
|---|---|---|---|
| 07:07 daily | **GitHub Action** `results.yml` | MLB box scores (statsapi.mlb.com) → `data/results/mlb/DATE.csv`; auto-fills MLB tracker rows; refreshes NFL play-by-play Mon/Tue/Fri | `data/`, `Record/mechanism_tracker.csv`, `status/actions.json` |
| 07:30 | **Perplexity** Job A (scheduled in Perplexity Computer) | NBA/NFL results (2 sources), closes, MLB second check | GitHub issue `scout: DATE A results` → Action `ingest-scout.yml` saves `Inbox/Perplexity/DATE A results.md` |
| 08:17 daily | **Claude cloud scheduled task** "Prop-Lab morning settlement (cloud)" | Verify, settle bets + tracker, write the review, push to main | `Record/`, `Markets/`, `Home.md`, `status/claude.json` |
| 11:00 / 13:30 / hourly evening | Perplexity Jobs B, C, D, E | Slate, board, late news, closes | issues → `Inbox/Perplexity/` |
| Hourly :17 | **GitHub Action** `watchdog.yml` | Checks heartbeats + due Scout files | opens/updates a `pipeline-alert` issue (GitHub emails you); closes it when healthy |
| 10:37 / 13:37 / every 15 min 12:00–23:59 | **GitHub Action** `odds.yml` | Prop odds + game spreads/totals (`games_*.csv`) from The Odds API: board, and closes for logged bets (looks 75 min ahead because GitHub runs the 15-min schedule ~hourly) (idle until the `ODDS_API_KEY` secret exists) | `data/odds/<sport>/DATE/` |
| 14:52 daily (create it: [[Afternoon Card Task]]) | **Claude cloud scheduled task** | Facts (Perplexity files or its own research) → engine → **bet card** `Slates/DATE card.md` + tracker rows | `Slates/`, `Record/`, `Inbox/Claude/` |
| Every push to `engine/` | **GitHub Action** `tests.yml` | NBA, NFL, MLB test suites | red X on the commit if anything broke |

## Tested 2026-10-24
- `results.yml` ran on GitHub for 2026-10-23: World Series G1 final pulled (32 player rows; Misiorowski 3 K / 15 outs / 78 pitches). ✅
- `ingest-scout.yml`: a test issue was saved to `Inbox/Perplexity/` and closed within a minute (test file then removed). ✅
- `watchdog.yml` ran clean (no alert). `tests.yml` passed on GitHub. ✅

## Learning loop (shadow grading, added 2026-10-24)
- The afternoon card saves **every** priced prop (model p, market p, decision) to `data/shadow/<sport>/DATE.csv`.
- The morning settlement runs `python engine/shadow.py`, which grades them against results and writes Record/Shadow/Shadow Report.md: Brier skill vs the market, calibration bins, and whether disagreeing with the market pays.
- NBA results come from the laptop's `engine/update_nba_data_auto.bat` (Windows Task Scheduler, at logon) or the manual `update_nba_data.bat`.
- ~200–400 graded NBA props a day → ~1,000 in under a week → enough to retune the model-health gate (Rules §9).

## What can't run in the cloud (yet)
- **NBA box scores and logs.** ESPN returns 403 to GitHub's servers and stats.nba.com / cdn.nba.com block cloud IPs. We don't disguise requests to get past that. NBA results come from Perplexity's Job A; NBA game logs for the engine come from `nba_api` on the laptop (`engine/setup_windows.bat`) when it's on. Options to close the gap: a paid NBA data API, or a small always-on home machine.
- **Odds snapshots / close capture.** Built (`odds.yml`); waits for your The Odds API key as the GitHub secret `ODDS_API_KEY` (the-odds-api.com, $30/mo for 20K credits ≈ NBA + NFL open/board/close). Note: committing raw odds to a public repo may be against the provider's terms; making the repo private is cleaner but Actions minutes then count (2,000/mo free).
- **Claude pricing runs** (NBA slate, NFL Sunday) are still done in conversation; they can become cloud scheduled tasks once Job C arrives reliably by issue.

## Odds API budget (2 free keys, 500 credits each; key 1 had 429 left on 2026-10-24)
Key 1 is used first; the job switches to key 2 only when key 1 is out. Free mode (`ODDS_TIER` unset): NBA points/rebounds/assists board at 13:37 daily (~24 credits on an 8-game night), MLB K + outs (2 per game), NFL receiving/rushing yards board on Sundays (~28), and T-10 closes only for games with a logged bet. ≈ 30–35 credits a day → about 26 days on ~930 credits. Remaining credits are logged in status/actions.json; the job warns when a key drops under 60 (paid tier: 1,500). Health check that costs 0: run the `odds` workflow with tag `check`.

## Credit budget (2026-10-24)
Perplexity Computer runs cost credits ($1 per 100; ~100-900 per run). Weekly included usage ran out 2026-10-24; resets Thu 09:00. Until then only the Sunday NFL Job C runs; A, B, C and D are paused, Claude covers slate/results itself, and the watchdog Scout check is off (SCOUT_CHECKS in .github/scripts/watchdog.py). After the reset: resume A and C only, measure credits per run, keep B/D off while everything is paper.

## Your one-time setup (Perplexity)
1. Paste the updated [[Perplexity Prompt]] (DELIVERY section is new).
2. In Perplexity Computer: Plugins → GitHub → connect `bjarthur-dev/prop-lab` → Tools → set **create issue** to **Always allow**.
3. Re-create Jobs A–E as **Scheduled Tasks/Automations in Computer** (cloud), not tied to the DESKTOP device. Delete the old device-based ones so nothing writes twice.

## Phone
Obsidian Git on mobile is unstable (its author says so; a 2026 bug can revert pulled changes). On the phone, read the vault on GitHub or use GitSync (Android/iOS) / Working Copy (iOS) pull-only. Don't edit the same note from the phone and the PC at once.
