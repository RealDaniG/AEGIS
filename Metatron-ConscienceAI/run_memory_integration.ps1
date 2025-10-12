# PowerShell Script to Run Memory Integration for ConscienceAI-METATRONV2
#
# This script automates the process of integrating existing memories
# from the ai_chat_es_pdf_full directory into the ConscienceAI system.

# Set working directory
Set-Location -Path "D:\metatronV2\Metatron-ConscienceAI"

# Display header
Write-Host "=========================================" -ForegroundColor Green
Write-Host "ConscienceAI-METATRONV2 Memory Integration" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = & python --version 2>&1
    Write-Host "✅ Python is available: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is not available. Please install Python 3.7 or later." -ForegroundColor Red
    exit 1
}

# Check if required files exist
$requiredFiles = @(
    "scripts/integrate_existing_memories.py",
    "ai_chat_es_pdf_full/memory.json",
    "ai_chat_es_pdf_full/rss_research.jsonl",
    "ai_chat_es_pdf_full/pdf_es_qa.jsonl"
)

$allFilesExist = $true
foreach ($file in $requiredFiles) {
    if (-not (Test-Path $file)) {
        Write-Host "❌ Required file not found: $file" -ForegroundColor Red
        $allFilesExist = $false
    } else {
        Write-Host "✅ Found required file: $file" -ForegroundColor Green
    }
}

if (-not $allFilesExist) {
    Write-Host "❌ Some required files are missing. Cannot proceed with integration." -ForegroundColor Red
    exit 1
}

# Run the memory integration script
Write-Host ""
Write-Host "Running memory integration..." -ForegroundColor Yellow
Write-Host "This may take a few minutes depending on the amount of data..." -ForegroundColor Yellow
Write-Host ""

try {
    & python scripts/integrate_existing_memories.py
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ Memory integration completed successfully!" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "❌ Memory integration failed with exit code: $LASTEXITCODE" -ForegroundColor Red
        exit $LASTEXITCODE
    }
} catch {
    Write-Host ""
    Write-Host "❌ Error running memory integration script: $_" -ForegroundColor Red
    exit 1
}

# Run the test script to verify integration
Write-Host ""
Write-Host "Running integration verification tests..." -ForegroundColor Yellow
Write-Host ""

try {
    & python scripts/test_integrated_memory.py
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ Integration verification tests passed!" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "❌ Integration verification tests failed with exit code: $LASTEXITCODE" -ForegroundColor Red
        exit $LASTEXITCODE
    }
} catch {
    Write-Host ""
    Write-Host "❌ Error running integration verification tests: $_" -ForegroundColor Red
    exit 1
}

# Display completion message
Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host "Memory Integration Process Completed!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""
Write-Host "The integrated memory is now available at:" -ForegroundColor Cyan
Write-Host "  ai_chat_es_pdf_full/integrated_memory.json" -ForegroundColor Cyan
Write-Host ""
Write-Host "You can now use this memory with the ConscienceAI-METATRONV2 chat system." -ForegroundColor Cyan
Write-Host ""