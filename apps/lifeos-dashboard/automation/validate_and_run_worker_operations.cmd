@echo off
setlocal
cd /d "%~dp0.."

if not exist ".venv\Scripts\python.exe" (
  echo STOPPED: dashboard virtual environment was not found.
  echo Expected: %CD%\.venv\Scripts\python.exe
  exit /b 2
)

echo Updating the local dashboard environment...
".venv\Scripts\python.exe" -m pip install -e ".[dev]"
if errorlevel 1 exit /b %ERRORLEVEL%

echo.
echo Validating Worker Operations and GitHub-first orchestration...
".venv\Scripts\python.exe" -m pytest -q ^
  tests\test_app.py ^
  tests\test_worker_operations.py ^
  tests\test_worker_response_receiver.py ^
  tests\test_worker_response_runtime.py ^
  tests\test_worker_profile_resolution.py ^
  tests\test_worker_result_contract.py ^
  tests\test_worker_result_ingester.py ^
  tests\test_worker_result_ingester_history.py ^
  tests\test_worker_result_repair.py ^
  tests\test_worker_hq_review.py ^
  tests\test_worker_rob_validation.py ^
  tests\test_worker_github_orchestrator.py ^
  tests\test_worker_github_orchestrator_resume.py ^
  tests\test_worker_browser_submit_recovery.py ^
  tests\test_slice6_advisory_contract.py ^
  tests\test_worker_operations_ui.py ^
  tests\test_server_availability_ui.py ^
  tests\test_worker_browser_readiness.py ^
  tests\test_synthetic_worker_browser_pilot.py
if errorlevel 1 (
  echo.
  echo STOPPED: focused Worker Operations validation failed.
  exit /b %ERRORLEVEL%
)

echo.
echo Validation passed. Launching LifeOS Dashboard with GitHub-first orchestration...
set LIFEOS_OPEN_BROWSER=0
set LIFEOS_GITHUB_AUTO_SYNC=0
set LIFEOS_WORKER_ORCHESTRATOR_ENABLED=1
set LIFEOS_WORKER_ORCHESTRATOR_POLL_SECONDS=30
echo Open this address in a new tab of the current Edge window:
echo http://127.0.0.1:8765
".venv\Scripts\python.exe" run_dashboard.py
exit /b %ERRORLEVEL%
