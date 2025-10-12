# Flujo de Auto‑Mejora del Nodo y de la Red

Documento técnico dedicado que describe el proceso continuo de auto‑mejora de ConscienceAI / Consciousness Engine: ingesta, recuperación (RAG), entrenamiento federado con LoRA, empaquetado y subida, agregación, validación, despliegue y observabilidad.

Autor: KaseMaster

## 1. Propósito y resultados esperados
El flujo de auto‑mejora busca que cada nodo:
- Ingerir y refrescar conocimiento local (p. ej., RSS científicos) para nutrir el corpus de RAG.
- Entrenar mejoras incrementales sobre el modelo base mediante LoRA, sin exponer datos privados.
- Subir deltas al servidor federado (idealmente sobre Tor) para su agregación, validación y despliegue.
- Medir métricas clave (entropía, coherencia, valencia, arousal, decisión, logic_truth, empathy_score, insight_strength) y generar gráficos automáticos.
- Mantener observabilidad del entorno (modelo activo, GPU/CPU, IP externa, versiones de librerías).

Resultados esperados por ciclo:
- Un adapter LoRA actualizado (delta compacto) y subido.
- Corpus de RAG actualizado.
- Métricas y visualizaciones publicadas en `ai_runs/plots/`.
- Reporte de entorno y red en `ai_runs/model_network_report.json`.

## 2. Principios de diseño
- Incremental y federado: LoRA sobre modelo base; comparte mejoras sin exponer datos.
- Privacidad: transporte por Tor (.onion) cuando sea posible; no subir datos brutos.
- Resiliencia: reintentos, tolerancia a fallos y fallback de modelo.
- Observabilidad: métricas y diagnósticos automáticos, trazabilidad por artefactos en `ai_runs/`.
- Portabilidad: scripts PowerShell y Python, uso en Windows con entorno virtual recomendado.

## 3. Componentes involucrados
- Ingesta y RAG:
  - `scripts/rss_ingest.py`: genera/actualiza `datasets/rss_research.jsonl`.
  - `consciousness_engine/scripts/simple_rag.py`: utilidades básicas de recuperación.
  - `consciousness_engine/scripts/chat_with_rag.py`: chat con RAG (CLI).
  - `run_chat_full.ps1`: lanza chat interactivo con RAG y memoria persistente.
- Entrenamiento y contribución:
  - `scripts/train_llm_qa.py` y `scripts/train_lm.py`: entrenamiento LoRA sobre base.
  - `scripts/compute_contribution.ps1`: orquesta el ciclo de entrenamiento, empaquetado y subida.
  - `scripts/package_lora_delta.py`: empaqueta adapter LoRA.
  - `scripts/upload_delta_client.py`: sube delta al servidor.
- Agregación y servidor:
  - `scripts/federated_server.py` y `run_federated_server.ps1`: servidor federado.
  - `scripts/federated_collect_and_merge.py`: proceso de colección/merge de deltas.
  - `scripts/aggregate_lora_adapters.py`: agrega/mezcla adapters.
- Observabilidad:
  - `scripts/plot_metrics.py`: genera `ai_runs/plots/metrics_grid.png` y PNGs individuales.
  - `scripts/model_network_report.py` + `run_model_network_report.ps1`: reporte de entorno/modelo/red.
  - `scripts/node_resources.py`: inventario local a `ai_runs/node_resources.json`.
- Infraestructura y utilidades:
  - `scripts/setup_onion_service.ps1`, `scripts/test_onion_connectivity.ps1`, `scripts/start_onion_chat.ps1`.
  - Programación: `run_compute_contribution_scheduled.ps1`, `scripts/schedule_compute_contribution.ps1`, `run_ingest_cycle.ps1`.

## 4. Flujo recomendado (timeline diario)
Ajusta horarios según recursos y carga. Ejemplo orientativo:

- 08:00 – Ingesta y refresco de corpus RAG
  - Ejecutar `pwsh -File .\run_ingest_cycle.ps1` (si disponible) o `python .\scripts\rss_ingest.py`.
  - Resultado: `datasets/rss_research.jsonl` actualizado.

- 10:00 – Validación ligera de RAG
  - Realizar smoke test: `python .\scripts\smoke_test.py` (si aplica) o lanzar `run_chat_full.ps1` y probar 2–3 preguntas con referencias.
  - Opcional: regenerar índices si se utilizan estrategias de RAG avanzadas.

- 20:00 – Entrenamiento incremental (LoRA)
  - Ejecutar: `pwsh -File .\scripts\compute_contribution.ps1`.
  - Acciones:
    - Selección automática de modelo (prioridad: `finetune_es_pdf_lm_full` → `finetune_es_pdf_lm` → `distilgpt2`).
    - Entrenamiento con `train_llm_qa.py` o `train_lm.py` según configuración.
    - Empaquetado del delta con `package_lora_delta.py`.
    - Subida al servidor vía `upload_delta_client.py` (idealmente sobre `.onion`).
    - Generación automática de gráficos con `plot_metrics.py`.

- 23:00 – Diagnóstico de entorno y red
  - Ejecutar: `pwsh -File .\run_model_network_report.ps1`.
  - Resultado: `ai_runs/model_network_report.json` con modelo, GPU/CPU, IP externa y versiones.

- 00:00 – Agregación/merge (lado servidor)
  - En servidor: `pwsh -File .\run_federated_server.ps1 -Token "<TOKEN>"` permanece activo.
  - Colecta y merge: `python .\scripts\federated_collect_and_merge.py` + `python .\scripts\aggregate_lora_adapters.py`.
  - Validación y despliegue del adapter global.

- 08:30 – Inicio de jornada
  - Lanzar chat `pwsh -File .\run_chat_full.ps1` con el adapter global más reciente.
  - Confirmar memoria precargada y funcionalidad RAG.

## 5. Configuración clave (node_config.json)
Ajusta `node_config.json` (no versionado) con valores típicos:
- `token`: credencial para servidor federado.
- `server_url`: URL del servidor (idealmente `.onion`).
- `model`: id HF base (ej.: `distilgpt2` o modelos en español).
- `qa_subset_size`, `epochs`, `learning_rate`, `batch_size`: hiperparámetros.
- `rag_corpus_path`: ruta al JSONL del corpus.
- `memory_path`: ruta de memoria del chat.
- `use_tor`: booleano para usar servicio `.onion`.

## 6. Observabilidad y métricas
Artefactos generados por ciclo:
- `metrics.csv`: series temporales de métricas propias.
- `ai_runs/plots/`: `metrics_grid.png` y PNGs individuales (entropy, coherence, valence, arousal, decision, logic_truth, empathy_score, insight_strength).
- `ai_runs/model_network_report.json`: modelo, GPU, IP externa, versiones (transformers, torch, python).
- `ai_runs/node_resources.json`: inventario local.

KPIs sugeridos:
- Calidad de respuestas (coherence, logic_truth, empathy_score, insight_strength).
- Estabilidad/variabilidad (entropy, arousal, valence).
- Latencia y throughput del chat.
- Éxito de subida y aceptación de deltas por el servidor.

## 7. Automatización (Windows Task Scheduler)
- Programar ingestión diaria:
  - `pwsh -File .\run_ingest_cycle.ps1` o `python .\scripts\rss_ingest.py` a las 08:00.
- Programar contribución nocturna:
  - `pwsh -File .\run_compute_contribution_scheduled.ps1` o usar `scripts/schedule_compute_contribution.ps1` para crear tareas programadas.
- Programar diagnóstico:
  - `pwsh -File .\run_model_network_report.ps1` a las 23:00.

Mejoras adicionales desatendidas:
- Programar optimización diaria de parámetros del chat:
  - Registrar: `pwsh -File .\scripts\schedule_auto_optimize.ps1 -StartTime "08:45" -Workspace "." -ServerUrl "http://127.0.0.1:5180"`
  - Ejecución: `run_auto_optimize_scheduled.ps1` → ejecuta `scripts/auto_optimize.py --server_url <URL>` y guarda los mejores parámetros en `ai_runs/webchat_settings.json` con logs en `ai_runs/`.
- Programar auto‑reprogramación segura (dry‑run):
  - Registrar: `pwsh -File .\scripts\schedule_auto_reprogram.ps1 -StartTime "09:00" -Workspace "." -ServerUrl "http://127.0.0.1:5180" -DryRun $true`
  - Ejecución: `run_auto_reprogram_scheduled.ps1` → ejecuta `scripts/auto_reprogram.py --dry_run --server_url <URL>`, genera reportes de cumplimiento y propuestas de cambio sin aplicar código, logs en `ai_runs/`.

Recomendación: ejecutar bajo usuario con permisos adecuados y entorno virtual activable. Los scripts de scheduling proveen ejemplos para registro y logs.

## 8. Manejo de fallos y reintentos
- Conectividad `.onion`: usar `scripts/test_onion_connectivity.ps1` para health checks, con backoff exponencial y logs.
- Entrenamiento fallido: conservar últimos checkpoints; si no hay GPU, usar CPU y reducir batch.
- Subida de delta: reintentos con tiempos escalonados; si falla, guardar delta local y reintentar al día siguiente.
- Import paths: `ai_adapter_llm.py` y `orchestrator/harmonic_orchestrator.py` incluyen fallbacks para ejecución desde raíz y como paquete.

## 9. Seguridad y privacidad
- Nunca subir datos brutos ni secretos. `node_config.json` no se versiona.
- Token: rotar con `scripts/rotate_token.ps1` y verificar conectividad.
- Tor: mantener servicio y endpoints `.onion` fuera de registros públicos.

## 10. Buenas prácticas de operación
- Mantener `requirements.txt` actualizado y entorno virtual limpio.
- Validar el chat con prompts de verificación cada mañana (RAG + referencias).
- Revisión semanal de métricas y de la calidad de las respuestas.
- Documentar cambios en `CHANGELOG.md` y preferir PRs pequeños.

## 11. Próximos pasos
- Añadir conteo de parámetros del modelo al `ai_runs/model_network_report.json`.
- Tests de latencia `.onion` y pruebas de ancho de banda con reporte.
- Métricas adicionales: latencia del chat, tamaño promedio de respuesta, ratio de aciertos RAG.
- Automatizar publicación de un release semanal con adapters agregados.

## 12. Referencias
- `README.md`, `README_RAG.md`, `consciousness_engine/README.md`.
- Scripts en `scripts/` y `run_*.ps1`.
- `CHANGELOG.md` para evolución funcional.

---

Firmado: KaseMaster