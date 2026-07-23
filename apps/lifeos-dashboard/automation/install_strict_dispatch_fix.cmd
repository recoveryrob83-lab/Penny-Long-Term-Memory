@echo off
setlocal

if not exist ".git" (
  echo STOPPED: run this command from the Penny-Long-Term-Memory repository root.
  exit /b 2
)

for /f "delims=" %%A in ('git status --porcelain') do set LIFEOS_DIRTY=1
if defined LIFEOS_DIRTY (
  echo STOPPED: local Git checkout has uncommitted changes.
  git status --short
  exit /b 2
)

echo Fetching the strict Worker dispatch fix...
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
  echo Expected: %CD%\.venv\Scripts\python.exe
  exit /b 2
)

echo.
echo Syntax-checking the strict browser transport...
".venv\Scripts\python.exe" -m py_compile automation\chatgpt_worker_browser_dispatch.py
if errorlevel 1 (
  echo STOPPED: strict browser transport failed syntax validation.
  exit /b %ERRORLEVEL%
)

echo.
echo Running focused dispatch and orchestration regression tests...
".venv\Scripts\python.exe" -m pytest -q ^
  tests\test_worker_browser_submit_recovery.py ^
  tests\test_worker_github_orchestrator.py ^
  tests\test_worker_github_orchestrator_resume.py
if errorlevel 1 (
  echo STOPPED: focused dispatch validation failed.
  exit /b %ERRORLEVEL%
)

echo.
echo Stopping any obsolete standalone orchestrator...
taskkill /FI "WINDOWTITLE eq Life OS Orchestrator*" /T /F >nul 2>&1

echo Stopping any stale dashboard listener on port 8765...
powershell -NoProfile -Command "$p=(Get-NetTCPConnection -LocalPort 8765 -State Listen -ErrorAction SilentlyContinue).OwningProcess | Sort-Object -Unique; foreach($processId in $p){Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue}" >nul 2>&1

echo.
echo Validation passed. Starting the unified dashboard and orchestrator...
call automation\start_lifeos_automation.cmd
exit /b %ERRORLEVEL%
