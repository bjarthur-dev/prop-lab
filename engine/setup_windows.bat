@echo off
REM One-time setup for the Prop-Lab engine. Double-click from the vault's engine folder.
cd /d "%~dp0\.."
where python >nul 2>nul || (echo Python not found. Install Python 3.11+ from https://www.python.org/downloads/ and tick "Add python.exe to PATH". & pause & exit /b 1)
python -m pip install --upgrade pip
python -m pip install nba_api pandas numpy tabulate
python engine\nba\tests\test_synthetic.py
python engine\nba\fetch.py
python engine\nba\backtest.py > engine\out\backtest_report.txt 2>&1
echo.
echo Setup done. Backtest report: engine\out\backtest_report.txt
pause
