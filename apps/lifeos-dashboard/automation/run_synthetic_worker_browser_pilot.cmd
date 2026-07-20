@echo off
setlocal
cd /d "%~dp0.."

if not exist ".venv\Scripts\python.exe" (
  echo STOPPED: dashboard virtual environment was not found.
  echo Expected: %CD%\.venv\Scripts\python.exe
  exit /b 2
)

".venv\Scripts\python.exe" ^
  "automation\run_synthetic_worker_browser_pilot.py" ^
  --send --confirm-send SYNTHETIC_SEND
exit /b %ERRORLEVEL%
