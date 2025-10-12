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

Write-Host "CONSCIENCEAI MEMORY SYSTEM INTEGRATION"
Write-Host "METATRONV2 Integration"

# Check Python availability
python --version 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Python not found in PATH!"
    exit 1
}

# Check script existence
$ScriptPath = Join-Path $PSScriptRoot "scripts\integrate_memory_system.py"
if (-not (Test-Path $ScriptPath)) {
    Write-Host "Error: Integration script not found at $ScriptPath"
    exit 1
}

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
python $ScriptPath @ArgsList