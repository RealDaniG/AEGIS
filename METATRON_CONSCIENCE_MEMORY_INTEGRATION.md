# METATRONV2 Memory System Integration with Legacy ConscienceAI Data

## Where and How is the Memory System Stored?

### Memory Storage Locations

The METATRONV2 system stores memory in several key locations:

1. **Primary Memory File**: `ai_chat_es_pdf_full/memory.json`
   - This is the main persistent storage for all memory entries
   - Uses JSON format with structured entries
   - Contains chat conversations, consciousness states, and RAG context

2. **RAG Corpus**: `datasets/rss_research.jsonl`
   - Knowledge base for retrieval-augmented generation
   - Uses JSONL format (one JSON object per line)
   - Each entry contains text content and metadata

3. **Consciousness States**: `consciousness_state.json`
   - Current state of the consciousness engine
   - Contains metrics like Φ (Integrated Information), coherence, etc.

4. **Session Files**: `sessions/*.json`
   - Individual user session histories
   - Short-term conversation storage

### Memory Structure

The memory system uses a structured approach with different entry types:

1. **Chat Entries**: Store user/assistant conversations with metadata
2. **Consciousness State Entries**: Store consciousness metrics and states
3. **RAG Context Entries**: Store retrieved context for queries

Each entry contains:
- Unique ID
- Timestamp
- Entry type
- Content (structured data)
- Metadata

## How to Add Files from Older Version as Context

### Method 1: RAG Corpus Integration (Recommended)

For text documents and knowledge base content:

1. Convert legacy text files to JSONL format
2. Add them to `datasets/rss_research.jsonl`
3. The RAG system will automatically index and retrieve from this content

Example using the provided script:
```bash
python scripts/add_legacy_context.py
```

Then use the function:
```python
convert_text_to_rag_jsonl("legacy_knowledge.txt", "datasets/rss_research.jsonl", "Legacy Knowledge")
```

### Method 2: Direct Memory Import

For chat histories and consciousness states:

1. Load legacy memory files
2. Parse the content appropriately
3. Add entries to `ai_chat_es_pdf_full/memory.json` using the memory system API

This requires running from within the Metatron-ConscienceAI directory:
```bash
cd Metatron-ConscienceAI
python -c "
from consciousness_engine.memory_system import ConscienceMemorySystem
memory = ConscienceMemorySystem()
# Add your legacy data here
memory.add_chat_entry('user message', 'assistant response')
memory.save_memory()
"
```

## Legacy Data Migration Process

### For Text Documents:
1. Identify legacy text files (`.txt`, `.md`, etc.)
2. Convert to JSONL format using the script
3. Append to `datasets/rss_research.jsonl`

### For Chat Histories:
1. Locate session files in the legacy system
2. Extract user/assistant message pairs
3. Import using the memory system API

### For Consciousness States:
1. Extract state data from legacy files
2. Format according to the new memory structure
3. Add as consciousness state entries

## Memory System API

The ConscienceMemorySystem provides these key methods:

- `add_chat_entry(user_message, assistant_response, consciousness_state)`: Add chat conversations
- `add_consciousness_state(state_dict)`: Add consciousness metrics
- `add_rag_context(query, context, sources)`: Add RAG context
- `save_memory()`: Persist to disk
- `load_memory()`: Load from disk

## Best Practices

1. **Backup First**: Always backup existing memory files before importing
2. **Batch Processing**: Process multiple files in batches for efficiency
3. **Validation**: Verify imported data matches expected format
4. **Incremental Imports**: Add data incrementally to avoid overwhelming the system
5. **Metadata**: Include source information in metadata for traceability

This approach allows you to leverage your legacy ConscienceAI data as context for enhanced training in METATRONV2.