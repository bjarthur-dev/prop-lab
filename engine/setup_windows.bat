@echo off
REM One-time setup for the Prop-Lab engine. Double-click from the vault's engine folder.
cd /d "%~dp0\.."
set PY=python
py -3.14 --version >nul 2>nul && set PY=py -3.14
%PY% --version >nul 2>nul || (echo Python not found. Install Python from https://www.python.org/downloads/ and tick "Add python.exe to PATH". & pause & exit /b 1)
echo Using:
%PY% --version
if not exist engine\out mkdir engine\out
%PY% -m pip install --upgrade pip
%PY% -m pip install nba_api pandas numpy tabulate
if errorlevel 1 (echo. & echo PACKAGE INSTALL FAILED - send Claude a screenshot of the lines above. & pause & exit /b 1)
%PY% engine\nba\tests\test_synthetic.py
%PY% engine\nba\tests\test_minutes.py
%PY% engine\nfl\tests\test_nfl.py
%PY% engine\nba\fetch.py
%PY% engine\nba\backtest.py > engine\out\backtest_report.txt 2>&1
echo.
echo Setup done. Backtest report: engine\out\backtest_report.txt
pause
