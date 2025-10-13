@echo off
title AEGIS Project Updater

echo ======================================================
echo        AEGIS (Autonomous Governance and Intelligent Systems)
echo              Project Update Utility
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

REM Check if git is available
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Git is not installed or not available in PATH.
    echo Please install Git from https://git-scm.com/ and try again.
    echo.
    pause
    exit /b 1
)

echo [1/5] Checking current status...
echo ----------------------------------------
git status --short
echo.

echo [2/5] Fetching latest changes from GitHub...
echo ----------------------------------------
git fetch origin
if %errorlevel% neq 0 (
    echo ERROR: Failed to fetch updates from GitHub.
    echo Please check your internet connection and try again.
    echo.
    pause
    exit /b 1
)

echo.
echo [3/5] Stashing any local changes (if any)...
echo ----------------------------------------
git stash
if %errorlevel% neq 0 (
    echo WARNING: Failed to stash local changes. Proceeding anyway...
)

echo.
echo [4/5] Pulling latest changes...
echo ----------------------------------------
git pull origin master
if %errorlevel% neq 0 (
    echo ERROR: Failed to pull updates.
    echo You may have local changes that conflict with the remote repository.
    echo.
    echo Attempting to restore stashed changes...
    git stash pop
    echo.
    pause
    exit /b 1
)

echo.
echo [5/5] Updating submodules (if any)...
echo ----------------------------------------
git submodule update --init --recursive
if %errorlevel% neq 0 (
    echo WARNING: Failed to update submodules. Continuing...
)

echo.
echo Update completed successfully!
echo ----------------------------------------
echo Your AEGIS project is now up to date with the latest version from GitHub.
echo.

REM Check if Python is available and offer to update dependencies
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found. Skipping dependency update.
) else (
    echo Updating Python dependencies...
    if exist "requirements.txt" (
        pip install -r requirements.txt --upgrade
    )
    if exist "unified_requirements.txt" (
        pip install -r unified_requirements.txt --upgrade
    )
    echo Python dependencies updated.
)

echo.
echo ======================================================
echo        AEGIS Update Complete!
echo ======================================================
echo.
echo You can now run START-AI.bat to launch the updated system.
echo.
echo For more information, visit: https://github.com/RealDaniG/AEGIS
echo.
pause