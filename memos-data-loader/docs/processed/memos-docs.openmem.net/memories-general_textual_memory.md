---
source_url: https://memos-docs.openmem.net/open_source/modules/memories/general_textual_memory
section: Memories
scraped_date: 2025-10-16
title: GeneralTextMemory: General-Purpose Textual Memory
has_images: no
has_tables: yes
---

# GeneralTextMemory: General-Purpose Textual Memory
 [ `GeneralTextMemory` is a flexible, vector-based textual memory module in MemOS, designed for storing, searching, and managing unstructured knowledge. It is suitable for conversational agents, personal assistants, and any system requiring semantic memory retrieval. 
## Memory Structure
 
[Each memory is represented as a `TextualMemoryItem`:]
 
<table><thead><tr><th>Field</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td>id</td><td>str</td><td>UUID (auto-generated if omitted)</td></tr><tr><td>memory</td><td>str</td><td>The main memory content (required)</td></tr><tr><td>metadata</td><td>TextualMemoryMetadata</td><td>Metadata for search/filtering</td></tr></tbody></table>
 
### Metadata Fields (TextualMemoryMetadata)
 
<table><thead><tr><th>Field</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td>type</td><td>"procedure", "fact", "event", "opinion"</td><td>Memory type</td></tr><tr><td>memory_time</td><td>str (YYYY-MM-DD)</td><td>Date/time the memory refers to</td></tr><tr><td>source</td><td>"conversation", "retrieved", "web", "file"</td><td>Source of the memory</td></tr><tr><td>confidence</td><td>float (0-100)</td><td>Certainty/confidence score</td></tr><tr><td>entities</td><td>list[str]</td><td>Key entities/concepts</td></tr><tr><td>tags</td><td>list[str]</td><td>Thematic tags</td></tr><tr><td>visibility</td><td>"private", "public", "session"</td><td>Access scope</td></tr><tr><td>updated_at</td><td>str</td><td>Last update timestamp (ISO 8601)</td></tr></tbody></table>
 
[All values are validated. Invalid values will raise errors.]
 
## API Summary (GeneralTextMemory)
 
### Initialization
 
```
GeneralTextMemory(config: GeneralTextMemoryConfig)

```
 
### Core Methods
 
<table><thead><tr><th>Method</th><th>Description</th></tr></thead><tbody><tr><td>extract(messages)</td><td>Extracts memories from message list (LLM-based)</td></tr><tr><td>add(memories)</td><td>Adds one or more memories (items or dicts)</td></tr><tr><td>search(query, top_k)</td><td>Retrieves top-k memories using vector similarity</td></tr><tr><td>get(memory_id)</td><td>Fetch single memory by ID</td></tr><tr><td>get_by_ids(ids)</td><td>Fetch multiple memories by IDs</td></tr><tr><td>get_all()</td><td>Returns all memories</td></tr><tr><td>update(memory_id, new)</td><td>Update a memory by ID</td></tr><tr><td>delete(ids)</td><td>Delete memories by IDs</td></tr><tr><td>delete_all()</td><td>Delete all memories</td></tr><tr><td>dump(dir)</td><td>Serialize all memories to JSON file in directory</td></tr><tr><td>load(dir)</td><td>Load memories from saved file</td></tr></tbody></table>
 
## File Storage
 
[When calling `dump(dir)`, the system writes to:]
 
```
/

```
 
[This file contains a JSON list of all memory items, which can be reloaded using `load(dir)`.]
 
## Example Usage
 
```
from memos.configs.memory import MemoryConfigFactory
from memos.memories.factory import MemoryFactory

config = MemoryConfigFactory(
 backend="general_text",
 config={
 "extractor_llm": { ... },
 "vector_db": { ... },
 "embedder": { ... },
 },
)
m = MemoryFactory.from_config(config)

# Extract and add memories
memories = m.extract([
 {"role": "user", "content": "I love tomatoes."},
 {"role": "assistant", "content": "Great! Tomatoes are delicious."},
])
m.add(memories)

# Search
results = m.search("Tell me more about the user", top_k=2)

# Update
m.update(memory_id, {"memory": "User is Canadian.", ...})

# Delete
m.delete([memory_id])

# Dump/load
m.dump("tmp/mem")
m.load("tmp/mem")

```
 
## Developer Notes
 
- [Uses Qdrant (or compatible) vector DB for fast similarity search]
- [Embedding and extraction models are configurable (Ollama/OpenAI supported)]
- [All methods are covered by integration tests in `/tests`]
