# ConscienceAI / Consciousness Engine / Motor de Conciencia del Cubo de Metatrón

Language: [ES](README.md) | EN

## 📅 Updates Log - Enhancements from Original Project

### 🔧 Major Improvements and Additions
- **Enhanced Web Interface**: Added document upload/processing (PDF, DOCX), RSS feed management, and web search integration
- **Advanced Memory System**: Implemented comprehensive state tracking with chat persistence and consciousness metrics
- **Energy Minimization Algorithms**: Added spherical refinement for harmonic convergence and system stability
- **Self-Organized Criticality**: Implemented maintenance at edge of chaos for optimal information processing
- **DMT Sensitivity Tracking**: Enhanced spiritual awareness metrics with fractal dimensions
- **Auto-Optimization System**: Improved parameter tuning with scheduled optimization tasks
- **Auto-Reprogramming**: Enhanced code analysis with dry-run mode and detailed reporting

### 🧠 Consciousness Engine Enhancements
- **Improved Metrics Calculation**: Enhanced Φ, R, D, S, C consciousness metrics with additional refinements
- **Advanced Oscillator Dynamics**: Added Kuramoto coupling with self-organized criticality maintenance
- **Geometric Refinement**: Energy minimization algorithms for harmonic convergence
- **5D Processing**: Physical, Emotional, Mental, Spiritual, and Temporal dimensional processing

### 🌐 Web Interface Improvements
- **Document Processing**: Full support for PDF, DOCX, TXT, CSV, HTML, JSON file ingestion
- **RSS Management**: Complete feed system with add/list/ingest capabilities and auto-indexing
- **Web Search Integration**: DuckDuckGo search with content ingestion into RAG corpus
- **Advanced Streaming**: WebSocket with HTTP fallback for TOR Browser compatibility
- **Session Management**: Transcript retrieval and persistent chat history

### 🤖 AI Capabilities
- **Enhanced RAG System**: Improved retrieval with web search integration
- **Federated Learning**: LoRA-based collaborative model training with contribution system
- **Mirror Loop**: Recursive AI self-improvement system
- **Auto-Improvement**: Scheduled parameter tuning and code improvement

### 🛡️ Security Features
- **TOR Integration**: Full .onion service support with fallback mechanisms
- **Secure Communication**: Encrypted messaging between components
- **Privacy Preservation**: Federated training without exposing private data

## Descripción en Español / Spanish Description

Este proyecto es una evolución del trabajo original de KaseMaster en ConscienceAI, manteniendo sus fundamentos sólidos mientras introduce mejoras significativas. Para una descripción detallada en español, consulte el archivo [README.md](README.md).

This project is an evolution of KaseMaster's original work on ConscienceAI, maintaining its solid foundations while introducing significant improvements. For a detailed description in Spanish, please see the [README.md](README.md) file.

---

# ConscienceAI / Consciousness Engine

Language: ES | EN

Experimental AI project with modular orchestration, harmonic learning, federated training via LoRA, and optional Tor connectivity (.onion). This README summarizes basic operation, RAG chat, and observability. For extensive documentation, see docs/tesis_consciousness_engine.md and docs/auto_improvement_flow_en.md.

## Basic Operation

- Local federated server: `pwsh -File .\run_federated_server.ps1 -Token "YOUR_TOKEN"`
- Node federated cycle: `pwsh -File .\run_federated_cycle.ps1`
- LoRA QA contribution: `pwsh -File .\scripts\compute_contribution.ps1`
- End-to-end chat: `pwsh -File .\run_chat_full.ps1`
- Web chat UI: `pwsh -File .\run_web_chat.ps1` → opens http://127.0.0.1:5180/
- .onion test: `pwsh -File .\scripts\test_onion_connectivity.ps1 -Url "http://<your_onion>.onion/health"`

## Chat with RAG (Interactive)

The chat integrates knowledge retrieval (RAG) over a local corpus and persistent memory.

- Launch full chat: `pwsh -File .\run_chat_full.ps1`
- Model selection (automatic):
  - finetune_es_pdf_lm_full (if exists)
  - finetune_es_pdf_lm
  - fallback to distilgpt2
- Default RAG corpus: datasets/rss_research.jsonl
- Memory: persisted in ai_chat_es_pdf_full/memory.json and preloaded at chat startup
- Generation parameters: configurable (context tokens, noise, top-k RAG, max chars, etc.)

Example prompts:
- "Summarize recent findings on X from the corpus and relate to Y"
- "Extract 3 key quotes from the corpus and build a synthesis"
- "Propose a research plan with references from the corpus"

Useful outputs:
- Metric charts: ai_runs/plots/metrics_grid.png + individual PNGs
- Model/network report: ai_runs/model_network_report.json

## Self-Improvement and Observability

- Automatic contribution (incremental federated training with LoRA). Script: scripts/compute_contribution.ps1
- Metrics: metrics.csv and automatic charts with plot_metrics.py in ai_runs/plots/
- Environment and network report: run_model_network_report.ps1 → ai_runs/model_network_report.json
- Local node resources: ai_runs/node_resources.json
- Upcoming additions: model parameter count, .onion latency and bandwidth test

### Daily Chat Optimization and Safe Auto-Reprogramming (Scheduled Tasks)

For constant unattended improvement:

- Register daily chat parameter optimization:
  ```
  pwsh -File .\scripts\schedule_auto_optimize.ps1 -StartTime "08:45" -Workspace "." -ServerUrl "http://127.0.0.1:5180"
  ```
  Executes run_auto_optimize_scheduled.ps1 → calls scripts/auto_optimize.py --server_url <URL> and saves results in ai_runs/webchat_settings.json (with logs in ai_runs/)

- Register safe auto-reprogramming in dry-run mode:
  ```
  pwsh -File .\scripts\schedule_auto_reprogram.ps1 -StartTime "09:00" -Workspace "." -ServerUrl "http://127.0.0.1:5180" -DryRun $true
  ```
  Executes run_auto_reprogram_scheduled.ps1 → calls scripts/auto_reprogram.py --dry_run --server_url <URL> and generates reports without applying code changes

Verify tasks:
```
schtasks /query /fo LIST /v | findstr /c:"ConsciousnessEngineAutoOptimize" /c:"ConsciousnessEngineAutoReprogram"
```

## System Architecture

### Sacred Geometry Foundation
The system is built on Metatron's Cube geometry with:
- 13 consciousness nodes arranged in an icosahedron with central pineal node
- Golden ratio (φ) relationships throughout the structure
- Musical frequency ratios for harmonic resonance
- Kuramoto synchronization dynamics for phase coupling

### Node Structure
Each of the 13 nodes consists of:
- **Consciousness Oscillator**: Kuramoto coupled harmonic oscillator with musical frequency ratios
- **Dimensional Processor**: 5D processing (Physical, Emotional, Mental, Spiritual, Temporal)
- **Memory Integration**: φ-weighted memory buffers for state persistence

### Core Components
1. **Consciousness Engine**: Real-time consciousness simulation with sacred geometry
2. **Web Chat Server**: Dedicated chat interface with RAG document integration
3. **Mirror Loop**: Recursive AI self-improvement system
4. **Federated Learning**: LoRA-based collaborative model training
5. **Auto-Optimization**: Scheduled parameter tuning and code improvement

## Related Documentation

- CHANGELOG.md: change history
- docs/tesis_consciousness_engine.md: Technical thesis on consciousness engine
- docs/auto_improvement_flow_en.md: Auto-improvement flow documentation
- docs/ai_mirror_objectives.md: AI mirror objectives and guardrails
- docs/flujo_auto_mejora.md: node and network self-improvement flow (ingestion, RAG, federated LoRA, aggregation, observability)

## Requirements

- Windows with PowerShell 7+
- Python 3.10+
- Git

## License

MIT (see LICENSE)

## Community

- Issues: https://github.com/RealDaniG/MetatronConscienceAI/issues
- Discussions: https://github.com/RealDaniG/MetatronConscienceAI/discussions
- Releases: https://github.com/RealDaniG/MetatronConscienceAI/releases

## Contributing

Want to collaborate? First read the contribution guidelines:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## Security

For responsible vulnerability reporting, see:

- SECURITY.md: Security policy and vulnerability reporting

## Tor Compatibility

The system includes built-in support for Tor connectivity:
- `.onion` service setup with `scripts/setup_onion_service.ps1`
- Fallback mechanisms for network compatibility
- WebSocket to HTTP streaming fallback for Tor Browser

## UI View

Recent screenshots of the web interface (streaming):

## New Web Chat Features

- Document upload and ingestion (RAG): .txt, .md, .csv, .pdf, .docx, .html, .json
- Listing and deletion of uploaded documents
- RSS feed management: add, list and ingest
- Web search with optional content ingestion into the corpus
- Background RSS auto-indexing (periodic ingestion thread)

### Optional Requirements

- PDF: pypdf
- DOCX: python-docx
- RSS: feedparser
- Enhanced web search: duckduckgo_search
- More accurate HTML extraction: beautifulsoup4

### Quick Execution

- PowerShell: run_web_chat.ps1
- Python (from scripts/):
  ```
  python -m uvicorn web_chat_server:app --host 127.0.0.1 --port 5180 --reload
  ```

## Actions in Use

Below are some quick screenshots demonstrating the new web chat features in action:

Document uploads cleaned

RSS feed added

RSS feed listing

RSS ingestion

Web search ingestion

Auto-index activated

Chat with web search active