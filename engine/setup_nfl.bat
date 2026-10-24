@echo off
REM One-time NFL data download for the Prop-Lab engine. Double-click from the vault's engine folder.
cd /d "%~dp0\.."
set PY=python
py -3.14 --version >nul 2>nul && set PY=py -3.14
echo Using:
%PY% --version
%PY% engine\nfl\fetch_nfl.py
%PY% engine\nfl\tests\test_nfl.py
echo.
echo NFL data setup finished. Tell Claude "NFL data done".
pause
