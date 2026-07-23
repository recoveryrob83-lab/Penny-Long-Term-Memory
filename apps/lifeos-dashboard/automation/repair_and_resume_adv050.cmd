@echo off
setlocal

if not exist ".git" (
  echo STOPPED: run this recovery from the Penny-Long-Term-Memory repository root.
  exit /b 2
)

for /f "delims=" %%A in ('git status --porcelain') do set LIFEOS_DIRTY=1
if defined LIFEOS_DIRTY (
  echo STOPPED: local Git checkout has uncommitted changes.
  git status --short
  exit /b 2
)

echo Fetching the Worker submit repair...
git fetch origin main
if errorlevel 1 exit /b %ERRORLEVEL%
git merge --ff-only origin/main
if errorlevel 1 (
  echo STOPPED: local and remote Git history require inspection.
  exit /b %ERRORLEVEL%
)

cd apps\lifeos-dashboard
if not exist ".venv\Scripts\python.exe" (
  echo STOPPED: dashboard virtual environment was not found.
  exit /b 2
)

echo Validating the exact send and same-row recovery paths...
".venv\Scripts\python.exe" -m pytest -q ^
  tests\test_worker_browser_submit_recovery.py ^
  tests\test_worker_github_orchestrator_resume.py
if errorlevel 1 (
  echo STOPPED: focused recovery validation failed.
  exit /b %ERRORLEVEL%
)

echo Replacing the old orchestration process...
taskkill /FI "WINDOWTITLE eq LifeOS Orchestrator*" /T /F >nul 2>&1

set LIFEOS_OPEN_BROWSER=0
set LIFEOS_GITHUB_AUTO_SYNC=0
set LIFEOS_WORKER_ORCHESTRATOR_ENABLED=1
set LIFEOS_WORKER_ORCHESTRATOR_POLL_SECONDS=30
start "LifeOS Orchestrator" /min cmd /c "".venv\Scripts\python.exe" automation\run_github_worker_orchestrator.py --poll-seconds 30"

echo ADV-050 recovery conductor is running.
echo The exact GitHub wake will be refilled or resumed without creating another advisory.
exit /b 0
