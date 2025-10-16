---
source_url: https://memos-docs.openmem.net/open_source/getting_started/your_first_memory
section: Getting Started
scraped_date: 2025-10-16
title: Your First Memory
has_images: no
has_tables: yes
---

# Your First Memory
 [ Letâs build your first plaintext memory in MemOS! **GeneralTextMemory** is the easiest way to get hands-on with extracting, embedding, and searching simple text memories. 
## What You'll Learn
 
[By the end of this guide, you will:]
 
- [Extract memories from plain text or chat messages.]
- [Store them as semantic vectors.]
- [Search and manage them using vector similarity.]
 
## How It Works
 
### Memory Structure
 
[Every memory is stored as a `TextualMemoryItem`:]
 
- [`memory`: the main text content (e.g., "The user loves tomatoes.")]
- [`metadata`: extra details to make the memory searchable and manageable â type,
time, source, confidence, entities, tags, visibility, and updated_at.]
 
[These fields make each piece of memory queryable, filterable, and easy to govern.]
 
[For each `TextualMemoryItem`:]
 
<table><thead><tr><th>Field</th><th>Example</th><th>What it means</th></tr></thead><tbody><tr><td>type</td><td>"opinion"</td><td>Classify if it's a fact, event, or opinion</td></tr><tr><td>memory_time</td><td>"2025-07-02"</td><td>When it happened</td></tr><tr><td>source</td><td>"conversation"</td><td>Where it came from</td></tr><tr><td>confidence</td><td>100.0</td><td>Certainty score (0â100)</td></tr><tr><td>entities</td><td>["tomatoes"]</td><td>Key concepts</td></tr><tr><td>tags</td><td>["food", "preferences"]</td><td>Extra labels for grouping</td></tr><tr><td>visibility</td><td>"private"</td><td>Who can access it</td></tr><tr><td>updated_at</td><td>"2025-07-02T00:00:00Z"</td><td>Last modified</td></tr></tbody></table> **Best Practice** 
 You can define any metadata fields that make sense for your use case! ### The Core Steps
 
[When you run this example:]
 
1. [**Extract:**
Your messages go through an `extractor_llm`, which returns a JSON list of `TextualMemoryItem`s.]
2. [**Embed:**
Each memory's `memory` field is turned into an embedding vector via `embedder`.]
3. [**Store:**
The embeddings are saved into a local **Qdrant** collection.]
4. [**Search & Manage:**
You can now `search` by semantic similarity, `update` by ID, or `delete` memories.] **Hint** 
 Make sure your embedder's output dimension matches your vector DB's `vector_dimension` .
Mismatch may cause search errors! **Hint** 
 If your search results are too noisy or irrelevant, check whether your `embedder` config and vector DB are properly initialized. ### Example Flow
 
[**Input Messages:**]
 
```
[
 {"role": "user", "content": "I love tomatoes."},
 {"role": "assistant", "content": "Great! Tomatoes are healthy."}
]

```
 
[**Extracted Memory:**]
 
```
{
 "memory": "The user loves tomatoes.",
 "metadata": {
 "type": "opinion",
 "memory_time": "2025-07-02",
 "source": "conversation",
 "confidence": 100.0,
 "entities": ["tomatoes"],
 "tags": ["food", "preferences"],
 "visibility": "private",
 "updated_at": "2025-07-02T00:00:00"
 }
}

```
 
[Here's a minimal script to create, extract, store, and search a memory:]
 [ 
#### Create a Memory Config
 
[First, create your minimal GeneralTextMemory config.
It contains three key parts:]
 
- [extractor_llm: uses an LLM to extract plaintext memories from conversations.]
- [embedder: turns each memory into a vector.]
- [vector_db: stores vectors and supports similarity search.]
 
```
from memos.configs.memory import MemoryConfigFactory
from memos.memories.factory import MemoryFactory

config = MemoryConfigFactory(
 backend="general_text",
 config={
 "extractor_llm": {
 "backend": "ollama",
 "config": {
 "model_name_or_path": "qwen3:0.6b",
 "temperature": 0.0,
 "remove_think_prefix": True,
 "max_tokens": 8192,
 },
 },
 "vector_db": {
 "backend": "qdrant",
 "config": {
 "collection_name": "test_textual_memory",
 "distance_metric": "cosine",
 "vector_dimension": 768,
 },
 },
 "embedder": {
 "backend": "ollama",
 "config": {
 "model_name_or_path": "nomic-embed-text:latest",
 },
 },
 },
)

m = MemoryFactory.from_config(config)

```
 
#### Extract Memories from Messages
 
[Give your LLM a simple dialogue and see how it extracts structured plaintext memories.]
 
```
memories = m.extract(
 [
 {"role": "user", "content": "I love tomatoes."},
 {"role": "assistant", "content": "Great! Tomatoes are delicious."},

)
print("Extracted:", memories)

```
 
[You'll get a list of TextualMemoryItem, with each of them like:]
 
```
TextualMemoryItem(
 id='...',
 memory='The user loves tomatoes.',
 metadata=...
)

```
 
#### Add Memories to Your Vector DB
 
[Save the extracted memories to your vector DB and demonstrate adding a custom plaintext memory manually (with a custom ID).]
 
```
m.add(memories)
m.add([
 {
 "id": "a19b6caa-5d59-42ad-8c8a-e4f7118435b4",
 "memory": "User is Chinese.",
 "metadata": {"type": "opinion"},
 }
])

```
 
#### Search Memories
 
[Now test similarity search!
Type any natural language query and find related memories.]
 
```
results = m.search("Tell me more about the user", top_k=2)
print("Search results:", results)

```
 
#### Get Memories by ID
 
[Fetch any memory directly by its ID:]
 
```
print("Get one by ID:", m.get("a19b6caa-5d59-42ad-8c8a-e4f7118435b4"))

```
 
#### Update a Memory
 
[Need to fix or refine a memory?
Update it by ID and re-embed the new version.]
 
```
m.update(
 "a19b6caa-5d59-42ad-8c8a-e4f7118435b4",
 {
 "memory": "User is Canadian.",
 "metadata": {
 "type": "opinion",
 "confidence": 85,
 "memory_time": "2025-05-24",
 "source": "conversation",
 "entities": ["Canadian"],
 "tags": ["happy"],
 "visibility": "private",
 "updated_at": "2025-05-19T00:00:00",
 },
 }
)
print("Updated:", m.get("a19b6caa-5d59-42ad-8c8a-e4f7118435b4"))

```
 
#### Delete Memories
 
[Remove one or more memories cleanly]
 
```
m.delete(["a19b6caa-5d59-42ad-8c8a-e4f7118435b4"])
print("Remaining:", m.get_all())

```
 
#### Dump Memories to Disk
 
[Finally, dump all your memories to local storage:]
 
```
m.dump("tmp/mem")
print("Memory dumped to tmp/mem")

```
 
[By default, your memories are saved to:]
 
```
/

```
 
[They can be reloaded anytime with `load()`.] By default, your dumped memories are saved to the file path you set in your config.
Always check `config.memory_filename` if you want to customize it. ] 
[Now your agent remembers â no more stateless chatbots!]
 
## What's Next?
 
[Ready to level up?]
 
- [**Try your own LLM backend:** Swap to OpenAI, HuggingFace, or Ollama.]
- [**Explore TreeTextMemory:** Build a graph-based,
hierarchical memory.]
- [**Add Activation Memory:** Cache key-value
states for faster inference.]
- [**Dive deeper:** Check the [API Reference](/api-reference/configure-memos) and [Examples](/open_source/getting_started/examples) for advanced workflows.] **Try Graph Textual Memory** 
 Try switching to `TreeTextMemory` to add a graph-based, hierarchical structure to your memories.
