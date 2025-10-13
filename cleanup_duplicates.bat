@echo off
title AEGIS Project Cleanup Utility

echo ======================================================
echo        AEGIS (Autonomous Governance and Intelligent Systems)
echo              Project Structure Cleanup
echo ======================================================
echo.

REM Check if we're in the right directory
if not exist ".git" (
    echo ERROR: This script must be run from the root of the AEGIS project directory.
    echo Please navigate to your AEGIS project folder and try again.
    echo.
    echo Current directory: %CD%
    echo.
    pause
    exit /b 1
)

echo This script will remove duplicate module files from the root directory.
echo These files already exist in the Open-A.G.I directory and are causing redundancy.
echo.

echo Files to be removed:
echo - alert_system.py
echo - api_server.py
echo - backup_system.py
echo - config_manager.py
echo - consensus_algorithm.py
echo - consensus_protocol.py
echo - crypto_framework.py
echo - logging_system.py
echo - memory_integration.py
echo - metrics_collector.py
echo - p2p_network.py
echo - resource_manager.py
echo - security_protocols.py
echo - tor_integration.py
echo.

echo Temporary files to be removed:
echo - README_CHANGES_SUMMARY.md
echo - UPDATE_SUMMARY.md
echo.

echo WARNING: This action cannot be undone. Please ensure you have committed any
echo important changes before proceeding.
echo.

set /p confirm=Do you want to proceed with the cleanup? (yes/no): 

if /i not "%confirm%"=="yes" (
    echo Cleanup cancelled.
    pause
    exit /b 0
)

echo.
echo [1/3] Removing duplicate module files...
echo ----------------------------------------

if exist "alert_system.py" (
    del "alert_system.py"
    echo Removed alert_system.py
)

if exist "api_server.py" (
    del "api_server.py"
    echo Removed api_server.py
)

if exist "backup_system.py" (
    del "backup_system.py"
    echo Removed backup_system.py
)

if exist "config_manager.py" (
    del "config_manager.py"
    echo Removed config_manager.py
)

if exist "consensus_algorithm.py" (
    del "consensus_algorithm.py"
    echo Removed consensus_algorithm.py
)

if exist "consensus_protocol.py" (
    del "consensus_protocol.py"
    echo Removed consensus_protocol.py
)

if exist "crypto_framework.py" (
    del "crypto_framework.py"
    echo Removed crypto_framework.py
)

if exist "logging_system.py" (
    del "logging_system.py"
    echo Removed logging_system.py
)

if exist "memory_integration.py" (
    del "memory_integration.py"
    echo Removed memory_integration.py
)

if exist "metrics_collector.py" (
    del "metrics_collector.py"
    echo Removed metrics_collector.py
)

if exist "p2p_network.py" (
    del "p2p_network.py"
    echo Removed p2p_network.py
)

if exist "resource_manager.py" (
    del "resource_manager.py"
    echo Removed resource_manager.py
)

if exist "security_protocols.py" (
    del "security_protocols.py"
    echo Removed security_protocols.py
)

if exist "tor_integration.py" (
    del "tor_integration.py"
    echo Removed tor_integration.py
)

echo.
echo [2/3] Removing temporary documentation files...
echo ----------------------------------------

if exist "README_CHANGES_SUMMARY.md" (
    del "README_CHANGES_SUMMARY.md"
    echo Removed README_CHANGES_SUMMARY.md
)

if exist "UPDATE_SUMMARY.md" (
    del "UPDATE_SUMMARY.md"
    echo Removed UPDATE_SUMMARY.md
)

echo.
echo [3/3] Checking for other redundant files...
echo ----------------------------------------

REM Check for any quick run scripts that might be redundant
if exist "run_everything.bat" (
    del "run_everything.bat"
    echo Removed run_everything.bat
)

if exist "run_everything.sh" (
    del "run_everything.sh"
    echo Removed run_everything.sh
)

echo.
echo Cleanup completed successfully!
echo ----------------------------------------
echo Duplicate module files have been removed from the root directory.
echo These files are available in the Open-A.G.I directory.
echo.

echo Next steps:
echo 1. Verify that the system still works correctly
echo 2. Update any scripts that might reference the old file locations
echo 3. Commit the changes to Git
echo.

echo For more information, see the FILES_TO_REMOVE.md documentation.
echo.

pause