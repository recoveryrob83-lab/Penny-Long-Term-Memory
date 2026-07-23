@echo off
setlocal

if not exist ".git" (
  echo STOPPED: Run this activation from the Penny-Long-Term-Memory repository root.
  exit /b 2
)

for /f "delims=" %%S in ('git status --porcelain') do (
  echo STOPPED: The repository has uncommitted changes.
  git status --short
  exit /b 2
)

echo Fetching GitHub-first orchestration...
git fetch origin main
if errorlevel 1 exit /b %ERRORLEVEL%

echo Merging remote orchestration with the preserved local evidence history...
git merge --no-ff origin/main -m "Merge GitHub-first Worker orchestration"
if errorlevel 1 (
  echo STOPPED: The merge needs inspection. No rebase or reset was performed.
  exit /b %ERRORLEVEL%
)

echo Publishing the combined history...
git push origin main
if errorlevel 1 exit /b %ERRORLEVEL%

echo Starting the validated GitHub-first Worker system...
call "apps\lifeos-dashboard\automation\validate_and_run_worker_operations.cmd"
exit /b %ERRORLEVEL%
