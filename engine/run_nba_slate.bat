@echo off
REM Daily NBA run. Needs today's Scout files in Inbox\Perplexity: "<date> B slate.md" and "<date> C board.md".
cd /d "%~dp0\.."
set PY=python
py -3.14 --version >nul 2>nul && set PY=py -3.14
set /p D=Slate date (YYYY-MM-DD):
set /p CLS=Slate class (micro/small/medium/large) [large]:
if "%CLS%"=="" set CLS=large
%PY% engine\nba\fetch.py
%PY% engine\nba\scout_to_csv.py %D%
%PY% engine\nba\run_slate.py %D% --class %CLS% --caps engine\out\%D%\min_caps.csv
echo.
echo Results: engine\out\%D%\summary.md  (candidates.csv has every side)
pause
