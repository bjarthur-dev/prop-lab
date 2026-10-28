@echo off
REM Silent NBA log refresh for Windows Task Scheduler (no pause). Logs to engine\out\update_nba_data.log
cd /d "%~dp0\.."
set PY=python
py -3.14 --version >nul 2>nul && set PY=py -3.14
%PY% engine\nba\fetch.py > engine\out\update_nba_data.log 2>&1
%PY% engine\nba\fetch_context.py >> engine\out\update_nba_data.log 2>&1
git add -f engine/data/players_2026-27.csv engine/data/teams_2026-27.csv engine/data/positions.csv engine/data/context
git commit -m "laptop: auto refresh NBA game logs" >> engine\out\update_nba_data.log 2>&1
git pull --rebase --autostash >> engine\out\update_nba_data.log 2>&1
git push >> engine\out\update_nba_data.log 2>&1
