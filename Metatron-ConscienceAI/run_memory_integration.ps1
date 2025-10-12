# run_memory_integration.ps1
Param(
    [string]$Message = "",
    [string]$SessionId = "powershell_session",
    [switch]$NoRag,
    [int]$MaxTokens = 128,
    [string]$MemoryPath = "ai_chat_es_pdf_full/memory.json",
    [string]$MetatronUrl = "http://localhost:8003",
    [switch]$Stats,
    [string]$Context = "",
    [switch]$Clear,
    [switch]$Example
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  CONSCIENCEAI MEMORY SYSTEM INTEGRATION" -ForegroundColor Cyan
Write-Host "  METATRONV2 Integration" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Check Python availability
Write-Host "`n[1/2] Checking Python environment..." -ForegroundColor Yellow
python --version 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error: Python not found in PATH!" -ForegroundColor Red
    Write-Host "   Please install Python 3.8+ and add to PATH." -ForegroundColor Yellow
    exit 1
}
Write-Host "✅ Python environment OK" -ForegroundColor Green

# Check script existence
$ScriptPath = Join-Path $PSScriptRoot "scripts\integrate_memory_system.py"
if (-not (Test-Path $ScriptPath)) {
    Write-Host "❌ Error: Integration script not found at $ScriptPath" -ForegroundColor Red
    exit 1
}

Write-Host "`n[2/2] Running memory system integration..." -ForegroundColor Yellow

# Build command arguments
$ArgsList = @()

if ($Stats) {
    $ArgsList += "--stats"
} elseif ($Context) {
    $ArgsList += "--context"
    $ArgsList += $Context
} elseif ($Clear) {
    $ArgsList += "--clear"
} elseif ($Example) {
    # No additional args for example
} elseif ($Message) {
    $ArgsList += "--message"
    $ArgsList += $Message
    $ArgsList += "--session-id"
    $ArgsList += $SessionId
    if ($NoRag) {
        $ArgsList += "--no-rag"
    }
    $ArgsList += "--max-tokens"
    $ArgsList += $MaxTokens
} else {
    # Show help if no arguments provided
    python $ScriptPath --help
    exit 0
}

# Add common arguments
$ArgsList += "--memory-path"
$ArgsList += $MemoryPath
$ArgsList += "--metatron-url"
$ArgsList += $MetatronUrl

# Execute the integration script
Write-Host "`nExecuting: python $ScriptPath $($ArgsList -join ' ')" -ForegroundColor Gray
python $ScriptPath @ArgsList

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ Memory system integration completed successfully!" -ForegroundColor Green
} else {
    Write-Host "`n❌ Memory system integration failed!" -ForegroundColor Red
    exit $LASTEXITCODE
}

Write-Host "`n📝 Memory file location: $MemoryPath" -ForegroundColor Yellow
Write-Host "🌐 METATRON API: $MetatronUrl" -ForegroundColor Yellow

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Integration Complete" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan