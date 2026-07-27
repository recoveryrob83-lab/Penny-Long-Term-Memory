@echo off
setlocal
cd /d "%~dp0.."

if not exist ".venv\Scripts\python.exe" (
  echo STOPPED: dashboard virtual environment was not found.
  echo Expected: %CD%\.venv\Scripts\python.exe
  exit /b 2
)

set LIFEOS_OPEN_BROWSER=0
set LIFEOS_LEGACY_SCHEDULER_ENABLED=0
set LIFEOS_GITHUB_AUTO_SYNC=0
set LIFEOS_WORKER_ORCHESTRATOR_ENABLED=1
set LIFEOS_WORKER_AUTO_DISPATCH_ENABLED=0
set LIFEOS_WORKER_ORCHESTRATOR_POLL_SECONDS=30

rem The dashboard process is the sole owner of automatic continuation for existing runs.
rem New advisory dispatch remains operator-controlled unless separately enabled.
echo Starting LifeOS Dashboard with guarded Worker continuation...
echo Open http://127.0.0.1:8765 in the current Edge window.
".venv\Scripts\python.exe" run_dashboard.py
exit /b %ERRORLEVEL%
