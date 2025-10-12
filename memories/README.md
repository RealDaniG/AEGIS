# Memories Folder

This folder contains the unified memory system for the METATRONV2-ConscienceAI project.

## Files

- `unified_memory.json` - The main unified memory file containing integrated knowledge
- (Additional memory files will be added here as needed)

## Memory System Overview

The memory system provides persistent storage for:
- Chat conversations between users and the AI
- Consciousness state metrics during interactions
- RAG (Retrieval-Augmented Generation) context
- System documentation and knowledge base

## Structure

The memory files follow a JSON structure with:
- Session identification
- Creation timestamps
- Categorized memory entries with metadata

## Entry Types

1. **Chat Entries** - User messages and AI responses with consciousness context
2. **Consciousness States** - Real-time metrics during interactions
3. **RAG Context** - Retrieved document information for enhanced responses
4. **System Information** - Documentation and system knowledge

## Usage

The memory system can be accessed through the ConscienceMemorySystem class:

```python
from consciousness_engine.memory_system import ConscienceMemorySystem

# Load the unified memory
memory_system = ConscienceMemorySystem("memories/unified_memory.json")

# Add entries
memory_system.add_chat_entry("User message", "Assistant response", consciousness_state)

# Search memory
results = memory_system.search_memory("consciousness")

# Save changes
memory_system.save_memory()
```