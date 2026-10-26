---
tags: [system, automation, laptop]
---

# Laptop NBA refresh: keep NBA data current without thinking about it

NBA stat sites block cloud servers, so the NBA game logs have to come from the laptop. Pick one (or both):

## Option A: Windows does it (no Claude needed)
In Command Prompt:
```
echo call "%USERPROFILE%\Documents\Prop-Lab\engine\update_nba_data_auto.bat" > "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\PropLab NBA refresh.bat"
schtasks /Create /TN "PropLab NBA refresh" /TR "\"%USERPROFILE%\Documents\Prop-Lab\engine\update_nba_data_auto.bat\"" /SC DAILY /ST 08:00 /F
```
Line 1 runs it every time you sign in. Line 2 runs it at 8 AM whenever the laptop is on. The log is in `engine\out\update_nba_data.log`.

## Option B: a Claude scheduled task on this laptop (can also fix git problems)
Claude app → **Scheduled tasks** → **New task** → name *Prop-Lab laptop NBA refresh* → **Daily 7:50 AM** → turn on **Require this computer** and select the Prop-Lab folder → paste:
```
Prop-Lab laptop NBA data refresh. On this computer, in the folder C:\Users\bray bray\Documents\Prop-Lab (a git clone of github.com/bjarthur-dev/prop-lab), refresh the NBA game logs and push them to GitHub so the cloud jobs can use them.
1. Run engine\update_nba_data_auto.bat in that folder (fetches nba_api logs, commits engine/data/players_2026-27.csv, teams_2026-27.csv, positions.csv, then git pull --rebase --autostash and git push; log in engine\out\update_nba_data.log).
2. Read the log. If the push was rejected or the pull failed, run git pull --rebase --autostash then git push. On a merge conflict keep GitHub's version of every file except those three data files (keep the laptop's fresh copies), finish the rebase and push.
3. Confirm main is in sync with origin/main and report the latest GAME_DATE in engine/data/players_2026-27.csv. Edit nothing else. If nba_api times out, retry once after 2 minutes, then report and stop.
```
(Claude couldn't create this one itself; the safety check requires you to set up tasks that run commands on your computer.)
