# Integrated Memory System

This directory contains the integrated memory system for the ConscienceAI-METATRONV2 chatbot.

## Files

- `integrated_memory.json` - The main integrated memory file containing all processed data
- `memory.json` - Original memory file (before integration)
- `rss_research.jsonl` - AI research papers and articles
- `pdf_es_qa.jsonl` - QA pairs from PDF documents on quantum physics and unified field theory
- `sample_quantum_math_es.jsonl` - Quantum mathematics explanations
- `pdf_es_qa.small.jsonl` - Smaller subset of PDF QA pairs
- `pdf_es_qa_filled.jsonl` - Enhanced PDF QA pairs
- `pdf_es_qa_filled_head500.jsonl` - First 500 enhanced PDF QA pairs
- `pdf_es_raw.jsonl` - Raw PDF content
- `quick_test.jsonl` - Test data
- `rss_feeds.json` - RSS feed sources

## Integrated Memory Structure

The `integrated_memory.json` file contains:

1. **Chat Entries** - Conversation history with consciousness state metadata
2. **RAG Context Entries** - Research papers, QA pairs, and educational content

## Usage

The integrated memory can be loaded and used with the ConscienceAI system:

```python
from consciousness_engine.memory_system import ConscienceMemorySystem

# Load the integrated memory
memory_system = ConscienceMemorySystem("ai_chat_es_pdf_full/integrated_memory.json")

# Access memory content
recent_chat = memory_system.get_recent_chat_history(5)
search_results = memory_system.search_memory("consciousness")
```

## Memory Integration Process

To re-integrate memory from source files:

1. Run the integration script:
   ```bash
   python ../scripts/integrate_existing_memories.py
   ```

2. Or use the PowerShell script:
   ```powershell
   ../run_memory_integration.ps1
   ```

## Memory Statistics

Current integrated memory contains:
- Total entries: 314
- Chat entries: 1
- RAG context entries: 313 (research papers, QA pairs, educational content)

## Content Sources

1. **RSS Research Papers** - Current AI and consciousness research (100 papers)
2. **PDF QA Pairs** - Quantum physics and unified field theory content (200 pairs)
3. **Quantum Math** - Educational content on quantum mathematics (10 entries)
4. **System Knowledge** - Foundational principles about METATRONV2 (3 entries)