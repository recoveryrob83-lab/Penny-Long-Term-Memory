@echo off
setlocal

if not exist ".git" (
  echo STOPPED: run this activation from the Penny-Long-Term-Memory repository root.
  exit /b 2
)

for /f "delims=" %%A in ('git status --porcelain') do set LIFEOS_DIRTY=1
if defined LIFEOS_DIRTY (
  echo STOPPED: local Git checkout has uncommitted changes.
  git status --short
  exit /b 2
)

echo Fetching the GitHub operational desk...
git fetch origin main
if errorlevel 1 exit /b %ERRORLEVEL%

echo Merging remote orchestration and ADV-050 while preserving local evidence commits...
git merge --no-ff origin/main -m "Merge GitHub orchestration and ADV-050 test"
if errorlevel 1 (
  echo STOPPED: Git merge requires inspection. Do not rebase or reset.
  exit /b %ERRORLEVEL%
)

echo Publishing the combined history...
git push origin main
if errorlevel 1 exit /b %ERRORLEVEL%

echo Starting the dashboard and GitHub-first orchestration loop...
call apps\lifeos-dashboard\automation\start_lifeos_automation.cmd
exit /b %ERRORLEVEL%
