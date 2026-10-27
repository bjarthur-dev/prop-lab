@echo off
REM Pull NBA matchup context (shot zones, play types, tracking, defense, matchups, on/off) from stats.nba.com and send to GitHub.
REM Run once a day (takes ~5-8 min). First run also pulls last season for baselines.
cd /d "%~dp0\.."
set PY=python
py -3.14 --version >nul 2>nul && set PY=py -3.14
if not exist engine\data\context\2025-26\_log.txt %PY% engine\nba\fetch_context.py 2025-26
%PY% engine\nba\fetch_context.py 2026-27
if errorlevel 1 (echo. & echo FETCH FAILED - send Claude a screenshot. & pause & exit /b 1)
git add -f engine/data/context
git commit -m "laptop: NBA matchup context"
git pull --rebase --autostash
git push
if errorlevel 1 (echo. & echo PUSH FAILED - send Claude a screenshot. & pause & exit /b 1)
echo.
echo Done. Matchup context sent to GitHub.
pause
