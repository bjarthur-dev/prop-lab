@echo off
REM Daily NBA run. Needs today's Scout files in Inbox\Perplexity: "<date> B slate.md" and "<date> C board.md".
cd /d "%~dp0\.."
set /p D=Slate date (YYYY-MM-DD):
set /p CLS=Slate class (micro/small/medium/large) [large]:
if "%CLS%"=="" set CLS=large
python engine\nba\fetch.py
python engine\nba\scout_to_csv.py %D%
python engine\nba\run_slate.py %D% --class %CLS% --caps engine\out\%D%\min_caps.csv
echo.
echo Results: engine\out\%D%\summary.md  (candidates.csv has every side)
pause
