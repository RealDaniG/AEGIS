# Ciclo federado (simulación local):
# 1) Registrar recursos del nodo
# 2) Ingesta RSS
# 3) (Opcional) Generación QA y fine-tune LoRA
# 4) Empaquetar adapter LoRA y métricas
# 5) Agregar adapters compatibles (promedio) para versión global

$ErrorActionPreference = "Stop"

Push-Location $PSScriptRoot
try {
  Write-Host "[Federado] Paso 1: Recursos del nodo" -ForegroundColor Cyan
  python .\scripts\node_resources.py

  Write-Host "[Federado] Paso 2: Ingesta RSS" -ForegroundColor Cyan
  powershell -ExecutionPolicy Bypass -File .\run_ingest_cycle.ps1

  # Paso 3: Opcional (placeholder). Se puede añadir generate_qa_responses.py y train_llm_qa.py
  Write-Host "[Federado] Paso 3: QA/Fine-tune (opcional, omitiendo en esta simulación)" -ForegroundColor Yellow

  Write-Host "[Federado] Paso 4: Empaquetar delta LoRA" -ForegroundColor Cyan
  # Ejemplo: empaquetar uno de los adapters existentes
  python .\scripts\package_lora_delta.py --model-dir .\models\qwen2_5_0_5b_pdf_es_lora_full3e --eval-dir .\ai_eval_qwen25_lora_over_base_research --out .\federated\out\qwen2_5_pdf_full3e.zip

  Write-Host "[Federado] Paso 5: Agregar adapters compatibles (promedio)" -ForegroundColor Cyan
  # Fusionar adapters qwen2.5 0.5B (mismo base) como ejemplo
  python .\scripts\aggregate_lora_adapters.py --adapters .\models\qwen2_5_0_5b_pdf_es_lora .\models\qwen2_5_0_5b_pdf_es_lora_full3e .\models\qwen2_5_0_5b_math_es_lora --weights 0.4 0.4 0.2 --out .\models\qwen2_5_0_5b_pdf_es_lora_merged

  Write-Host "[Federado] Ciclo completado." -ForegroundColor Green
} finally {
  Pop-Location
}