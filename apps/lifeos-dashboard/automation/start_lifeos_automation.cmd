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

echo Starting GitHub-first Life OS orchestration...
start "Life OS Orchestrator" /min cmd /c "".venv\Scripts\python.exe" automation\run_github_worker_orchestrator.py --poll-seconds 30"

echo Starting LifeOS Dashboard...
echo Open http://127.0.0.1:8765 in the current Edge window.
".venv\Scripts\python.exe" run_dashboard.py
exit /b %ERRORLEVEL%
