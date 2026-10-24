@echo off
REM Refresh NBA game logs from nba_api and send them to GitHub (cloud jobs use them). Double-click it, about once a day/week.
cd /d "%~dp0\.."
set PY=python
py -3.14 --version >nul 2>nul && set PY=py -3.14
%PY% engine\nba\fetch.py
if errorlevel 1 (echo. & echo FETCH FAILED - send Claude a screenshot. & pause & exit /b 1)
git pull --rebase
git add -f engine/data/players_2026-27.csv engine/data/teams_2026-27.csv engine/data/positions.csv
git commit -m "laptop: refresh NBA game logs"
git push
echo.
echo Done. NBA data refreshed and sent to GitHub.
pause
