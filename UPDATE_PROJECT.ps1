#requires -version 5.1
param(
    [switch]$SkipDependencies
)

Write-Host "======================================================" -ForegroundColor Cyan
Write-Host "       AEGIS (Autonomous Governance and Intelligent Systems)" -ForegroundColor Cyan
Write-Host "             Project Update Utility" -ForegroundColor Cyan
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path ".git")) {
    Write-Host "ERROR: This script must be run from the root of the AEGIS project directory." -ForegroundColor Red
    Write-Host "Please navigate to your AEGIS project folder and try again." -ForegroundColor Red
    Write-Host ""
    Write-Host "Current directory: $((Get-Location).Path)" -ForegroundColor Yellow
    Write-Host ""
    pause
    exit 1
}

# Check if git is available
try {
    $gitVersion = git --version 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Git not found"
    }
    Write-Host "Git version: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Git is not installed or not available in PATH." -ForegroundColor Red
    Write-Host "Please install Git from https://git-scm.com/ and try again." -ForegroundColor Red
    Write-Host ""
    pause
    exit 1
}

Write-Host "[1/5] Checking current status..." -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor DarkGray
git status --short

Write-Host ""
Write-Host "[2/5] Fetching latest changes from GitHub..." -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor DarkGray
git fetch origin
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to fetch updates from GitHub." -ForegroundColor Red
    Write-Host "Please check your internet connection and try again." -ForegroundColor Red
    Write-Host ""
    pause
    exit 1
}

Write-Host ""
Write-Host "[3/5] Stashing any local changes (if any)..." -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor DarkGray
git stash
if ($LASTEXITCODE -ne 0) {
    Write-Host "WARNING: Failed to stash local changes. Proceeding anyway..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[4/5] Pulling latest changes..." -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor DarkGray
git pull origin master
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to pull updates." -ForegroundColor Red
    Write-Host "You may have local changes that conflict with the remote repository." -ForegroundColor Red
    Write-Host ""
    Write-Host "Attempting to restore stashed changes..." -ForegroundColor Yellow
    git stash pop
    Write-Host ""
    pause
    exit 1
}

Write-Host ""
Write-Host "[5/5] Updating submodules (if any)..." -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor DarkGray
git submodule update --init --recursive
if ($LASTEXITCODE -ne 0) {
    Write-Host "WARNING: Failed to update submodules. Continuing..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Update completed successfully!" -ForegroundColor Green
Write-Host "----------------------------------------" -ForegroundColor DarkGray
Write-Host "Your AEGIS project is now up to date with the latest version from GitHub." -ForegroundColor Green

if (-not $SkipDependencies) {
    # Check if Python is available and offer to update dependencies
    try {
        $pythonVersion = python --version 2>$null
        if ($LASTEXITCODE -ne 0) {
            throw "Python not found"
        }
        Write-Host ""
        Write-Host "Python version: $pythonVersion" -ForegroundColor Green
        
        Write-Host ""
        Write-Host "Updating Python dependencies..." -ForegroundColor Yellow
        if (Test-Path "requirements.txt") {
            Write-Host "Updating requirements.txt dependencies..." -ForegroundColor Cyan
            pip install -r requirements.txt --upgrade
        }
        if (Test-Path "unified_requirements.txt") {
            Write-Host "Updating unified_requirements.txt dependencies..." -ForegroundColor Cyan
            pip install -r unified_requirements.txt --upgrade
        }
        Write-Host "Python dependencies updated." -ForegroundColor Green
    } catch {
        Write-Host "Python not found. Skipping dependency update." -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host "       AEGIS Update Complete!" -ForegroundColor Cyan
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "You can now run START-AI.bat to launch the updated system." -ForegroundColor Green
Write-Host ""
Write-Host "For more information, visit: https://github.com/RealDaniG/AEGIS" -ForegroundColor Gray
Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")