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

echo Fetching the unified dashboard-orchestrator repair...
git fetch origin main
if errorlevel 1 exit /b %ERRORLEVEL%
git merge --ff-only origin/main
if errorlevel 1 (
  echo STOPPED: local and remote Git history require inspection.
  exit /b %ERRORLEVEL%
)

echo Stopping the obsolete standalone orchestrator...
taskkill /FI "WINDOWTITLE eq Life OS Orchestrator*" /T /F >nul 2>&1

echo Stopping the current dashboard listener on port 8765...
powershell -NoProfile -Command "$p=(Get-NetTCPConnection -LocalPort 8765 -State Listen -ErrorAction SilentlyContinue).OwningProcess | Sort-Object -Unique; foreach($processId in $p){Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue}" >nul 2>&1

echo Starting one unified dashboard and orchestration process...
call apps\lifeos-dashboard\automation\start_lifeos_automation.cmd
exit /b %ERRORLEVEL%
