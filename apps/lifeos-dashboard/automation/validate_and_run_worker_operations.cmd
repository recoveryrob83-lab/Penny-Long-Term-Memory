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
echo Validating the Worker Operations rebuild...
".venv\Scripts\python.exe" -m pytest -q ^
  tests\test_app.py ^
  tests\test_worker_operations.py ^
  tests\test_worker_operations_ui.py ^
  tests\test_server_availability_ui.py ^
  tests\test_synthetic_worker_browser_pilot.py
if errorlevel 1 (
  echo.
  echo STOPPED: focused Worker Operations validation failed.
  exit /b %ERRORLEVEL%
)

echo.
echo Validation passed. Launching LifeOS Dashboard...
".venv\Scripts\python.exe" run_dashboard.py
exit /b %ERRORLEVEL%
