Param(
    [string]$Corpus = "datasets/rss_research.jsonl",
    [string]$Model = "distilgpt2",
    [int]$TopK = 3,
    [int]$MaxChars = 1200,
    [int]$MaxNewTokens = 128
)

Write-Host "[RAG] Iniciando demo con corpus: $Corpus" -ForegroundColor Cyan

if (-not (Test-Path $Corpus)) {
    Write-Warning "No se encontró el corpus en $Corpus. Genera uno desde RSS o especifica otra ruta."
}

python "consciousness_engine/scripts/chat_with_rag.py" --rag-corpus "$Corpus" --model "$Model" --top-k $TopK --max-chars $MaxChars --max-new-tokens $MaxNewTokens