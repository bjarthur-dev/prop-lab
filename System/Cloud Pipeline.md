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
| Every push to `engine/` | **GitHub Action** `tests.yml` | NBA, NFL, MLB test suites | red X on the commit if anything broke |

## Tested 2026-10-24
- `results.yml` ran on GitHub for 2026-10-23: World Series G1 final pulled (32 player rows; Misiorowski 3 K / 15 outs / 78 pitches). ✅
- `ingest-scout.yml`: a test issue was saved to `Inbox/Perplexity/` and closed within a minute (test file then removed). ✅
- `watchdog.yml` ran clean (no alert). `tests.yml` passed on GitHub. ✅

## What can't run in the cloud (yet)
- **NBA box scores and logs.** ESPN returns 403 to GitHub's servers and stats.nba.com / cdn.nba.com block cloud IPs. We don't disguise requests to get past that. NBA results come from Perplexity's Job A; NBA game logs for the engine come from `nba_api` on the laptop (`engine/setup_windows.bat`) when it's on. Options to close the gap: a paid NBA data API, or a small always-on home machine.
- **Odds snapshots / close capture.** Planned with The Odds API ($30/mo tier, ~20K credits; the-odds-api.com, not theoddsapi.com). Needs your API key as a GitHub secret `ODDS_API_KEY`; until then Perplexity's Job E does it.
- **Claude pricing runs** (NBA slate, NFL Sunday) are still done in conversation; they can become cloud scheduled tasks once Job C arrives reliably by issue.

## Your one-time setup (Perplexity)
1. Paste the updated [[Perplexity Prompt]] (DELIVERY section is new).
2. In Perplexity Computer: Plugins → GitHub → connect `bjarthur-dev/prop-lab` → Tools → set **create issue** to **Always allow**.
3. Re-create Jobs A–E as **Scheduled Tasks/Automations in Computer** (cloud), not tied to the DESKTOP device. Delete the old device-based ones so nothing writes twice.

## Phone
Obsidian Git on mobile is unstable (its author says so; a 2026 bug can revert pulled changes). On the phone, read the vault on GitHub or use GitSync (Android/iOS) / Working Copy (iOS) pull-only. Don't edit the same note from the phone and the PC at once.
