---
source_url: https://memos-docs.openmem.net/open_source/modules/memories/tree_textual_memory
section: Memories
scraped_date: 2025-10-16
title: TreeTextMemory: Structured Hierarchical Textual Memory
has_images: no
has_tables: yes
---

# TreeTextMemory: Structured Hierarchical Textual Memory
 [ 
[Letâs build your first **graph-based, tree-structured memory** in MemOS!]
 
[**TreeTextMemory** helps you organize, link, and retrieve memories with rich context and explainability.]
 
[[Neo4j](/open_source/modules/memories/neo4j_graph_db) is the current backend, with support for additional graph stores planned in the future.]
 
## What Youâll Learn
 
[By the end of this guide, you will:]
 
- [Extract structured memories from raw text or conversations.]
- [Store them as **nodes** in a graph database.]
- [Link memories into **hierarchies** and semantic graphs.]
- [Search them using **vector similarity + graph traversal**.]
 
## How It Works
 
### Memory Structure
 
[Every node in your `TreeTextMemory` is a `TextualMemoryItem`:]
 
- [`id`: Unique memory ID (auto-generated if omitted).]
- [`memory`: the main text.]
- [`metadata`: includes hierarchy info, embeddings, tags, entities, source, and status.]
 
### Metadata Fields (TreeNodeTextualMemoryMetadata)
 
<table><thead><tr><th>Field</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td>memory_type</td><td>"WorkingMemory", "LongTermMemory", "UserMemory"</td><td>Lifecycle category</td></tr><tr><td>status</td><td>"activated", "archived", "deleted"</td><td>Node status</td></tr><tr><td>visibility</td><td>"private", "public", "session"</td><td>Access scope</td></tr><tr><td>sources</td><td>list[str]</td><td>List of sources (e.g. files, URLs)</td></tr><tr><td>source</td><td>"conversation", "retrieved", "web", "file"</td><td>Original source type</td></tr><tr><td>confidence</td><td>float (0-100)</td><td>Certainty score</td></tr><tr><td>entities</td><td>list[str]</td><td>Mentioned entities or concepts</td></tr><tr><td>tags</td><td>list[str]</td><td>Thematic tags</td></tr><tr><td>embedding</td><td>list[float]</td><td>Vector embedding for similarity search</td></tr><tr><td>created_at</td><td>str</td><td>Creation timestamp (ISO 8601)</td></tr><tr><td>updated_at</td><td>str</td><td>Last update timestamp (ISO 8601)</td></tr><tr><td>usage</td><td>list[str]</td><td>Usage history</td></tr><tr><td>background</td><td>str</td><td>Additional context</td></tr></tbody></table> **Best Practice** 
 Use meaningful tags and background â they help organize your graph for
multi-hop reasoning. ### Core Steps
 
[When you run this example, your workflow will:]
 
1. [**Extract:** Use an LLM to pull structured memories from raw text.]
2. [**Embed:** Generate vector embeddings for similarity search.]
3. [**Store & Link:** Add nodes to your graph database (Neo4j) with relationships.]
4. [**Search:** Query by vector similarity, then expand results by graph hops.] **Hint** 
 Graph links help retrieve context that pure vector search might miss! ## API Summary (TreeTextMemory)
 
### Initialization
 
```
TreeTextMemory(config: TreeTextMemoryConfig)

```
 
### Core Methods
 
<table><thead><tr><th>Method</th><th>Description</th></tr></thead><tbody><tr><td>add(memories)</td><td>Add one or more memories (items or dicts)</td></tr><tr><td>replace_working_memory()</td><td>Replace all WorkingMemory nodes</td></tr><tr><td>get_working_memory()</td><td>Get all WorkingMemory nodes</td></tr><tr><td>search(query, top_k)</td><td>Retrieve top-k memories using vector + graph search</td></tr><tr><td>get(memory_id)</td><td>Fetch single memory by ID</td></tr><tr><td>get_by_ids(ids)</td><td>Fetch multiple memories by IDs</td></tr><tr><td>get_all()</td><td>Export the full memory graph as dictionary</td></tr><tr><td>update(memory_id, new)</td><td>Update a memory by ID</td></tr><tr><td>delete(ids)</td><td>Delete memories by IDs</td></tr><tr><td>delete_all()</td><td>Delete all memories and relationships</td></tr><tr><td>dump(dir)</td><td>Serialize the graph to JSON in directory</td></tr><tr><td>load(dir)</td><td>Load graph from saved JSON file</td></tr><tr><td>drop(keep_last_n)</td><td>Backup graph &amp; drop database, keeping N backups</td></tr></tbody></table>
 
## File Storage
 
[When calling `dump(dir)`, the system writes to:]
 
```
/

```
 
[This file contains a JSON structure with `nodes` and `edges`. It can be reloaded using `load(dir)`.]
 
## Your First TreeTextMemory â Step by Step
 [ 
### Create TreeTextMemory Config
 
[Define:]
 
- [your embedder (to create vectors),]
- [your graph DB backend (Neo4j),]
- [and your extractor LLM (optional).]
 
```
from memos.configs.memory import TreeTextMemoryConfig

config = TreeTextMemoryConfig.from_json_file("examples/data/config/tree_config.json")

```
 
### Initialize TreeTextMemory
 
```
from memos.memories.textual.tree import TreeTextMemory

tree_memory = TreeTextMemory(config)

```
 
### Extract Structured Memories
 
[Use your extractor to parse conversations, files, or docs into `TextualMemoryItem`s.]
 
```
from memos.mem_reader.simple_struct import SimpleStructMemReader

reader = SimpleStructMemReader.from_json_file("examples/data/config/simple_struct_reader_config.json")

scene_data = [
 {"role": "user", "content": "Tell me about your childhood."},
 {"role": "assistant", "content": "I loved playing in the garden with my dog."}
]

memories = reader.get_memory(scene_data, type="chat", info={"user_id": "1234"})
for m_list in memories:
 tree_memory.add(m_list)

```
 
### Search Memories
 
[Try a vector + graph search:]
 
```
results = tree_memory.search("Talk about the garden", top_k=5)
for i, node in enumerate(results):
 print(f"{i}: {node.memory}")

```
 
### Retrieve Memories from the Internet (Optional)
 
[You can also fetch real-time web content using search engines such as Google, Bing, or Bocha, and automatically extract them into structured memory nodes. MemOS provides a unified interface for this purpose.]
 
[The following example demonstrates how to retrieve web content related to **âAlibaba 2024 ESG reportâ** and convert it into structured memories:]
 
```
# Create the embedder
embedder = EmbedderFactory.from_config(
 EmbedderConfigFactory.model_validate({
 "backend": "ollama",
 "config": {"model_name_or_path": "nomic-embed-text:latest"},
 })
)

# Configure the retriever (using BochaAI as an example)
retriever_config = InternetRetrieverConfigFactory.model_validate({
 "backend": "bocha",
 "config": {
 "api_key": "sk-xxx", # Replace with your BochaAI API Key
 "max_results": 5,
 "reader": { # Reader config for automatic chunking
 "backend": "simple_struct",
 "config": ..., # Your mem-reader config
 },
 }
})

# Instantiate the retriever
retriever = InternetRetrieverFactory.from_config(retriever_config, embedder)

# Perform internet search
results = retriever.retrieve_from_internet("Alibaba 2024 ESG report")

# Add results to the memory graph
for m in results:
 tree_memory.add(m)

```
 
[Alternatively, you can configure the `internet_retriever` field directly in the `TreeTextMemoryConfig`. For example:]
 
```
{
 "internet_retriever": {
 "backend": "bocha",
 "config": {
 "api_key": "sk-xxx",
 "max_results": 5,
 "reader": {
 "backend": "simple_struct",
 "config": ...
 }
 }
 }
}

```
 
[With this setup, when you call `tree_memory.search(query)`, the system will automatically trigger an internet search (via BochaAI, Google, or Bing), and merge the results with local memory nodes in a unified ranked list â no need to manually call `retriever.retrieve_from_internet`.]
 
### Replace Working Memory
 
[Replace your current `WorkingMemory` nodes with new ones:]
 
```
tree_memory.replace_working_memory(
 [{
 "memory": "User is discussing gardening tips.",
 "metadata": {"memory_type": "WorkingMemory"}
 }]
)

```
 
### Backup & Restore
 
[Dump your entire tree structure to disk and reload anytime:]
 
```
tree_memory.dump("tmp/tree_memories")
tree_memory.load("tmp/tree_memories")

```
 ] 
### Whole Code
 
[This combines all the steps above into one end-to-end example â copy & run!]
 
```
from memos.configs.embedder import EmbedderConfigFactory
from memos.configs.memory import TreeTextMemoryConfig
from memos.configs.mem_reader import SimpleStructMemReaderConfig
from memos.embedders.factory import EmbedderFactory
from memos.mem_reader.simple_struct import SimpleStructMemReader
from memos.memories.textual.tree import TreeTextMemory

# Setup Embedder
embedder_config = EmbedderConfigFactory.model_validate({
 "backend": "ollama",
 "config": {"model_name_or_path": "nomic-embed-text:latest"}
})
embedder = EmbedderFactory.from_config(embedder_config)

# Create TreeTextMemory
tree_config = TreeTextMemoryConfig.from_json_file("examples/data/config/tree_config.json")
my_tree_textual_memory = TreeTextMemory(tree_config)
my_tree_textual_memory.delete_all()

# Setup Reader
reader_config = SimpleStructMemReaderConfig.from_json_file(
 "examples/data/config/simple_struct_reader_config.json"
)
reader = SimpleStructMemReader(reader_config)

# Extract from conversation
scene_data = [
 {
 "role": "user",
 "content": "Tell me about your childhood."
 },
 {
 "role": "assistant",
 "content": "I loved playing in the garden with my dog."
 },
]
memory = reader.get_memory(scene_data, type="chat", info={"user_id": "1234", "session_id": "2222"})
for m_list in memory:
 my_tree_textual_memory.add(m_list)

# Search
results = my_tree_textual_memory.search(
 "Talk about the user's childhood story?",
 top_k=10
)
for i, r in enumerate(results):
 print(f"{i}'th result: {r.memory}")

# [Optional] Add from documents
doc_paths = ["./text1.txt", "./text2.txt"]
doc_memory = reader.get_memory(
 doc_paths, "doc", info={
 "user_id": "your_user_id",
 "session_id": "your_session_id",
 }
)
for m_list in doc_memory:
 my_tree_textual_memory.add(m_list)

# [Optional] Dump & Drop
my_tree_textual_memory.dump("tmp/my_tree_textual_memory")
my_tree_textual_memory.drop()

```
 
## What Makes TreeTextMemory Different?
 
- [**Structured Hierarchy:** Organize memories like a mind map â nodes can
have parents, children, and cross-links.]
- [**Graph-Style Linking:** Beyond pure hierarchy â build multi-hop reasoning
chains.]
- [**Semantic Search + Graph Expansion:** Combine the best of vectors and
graphs.]
- [**Explainability:** Trace how memories connect, merge, or evolve over time.] **Try This** 
 Add memory nodes from documents or web content. Link them
manually or auto-merge similar nodes! ## Whatâs Next?
 
- [**Know more about Neo4j:** TreeTextMemory is powered by a graph database backend.
Understanding how Neo4j handles nodes, edges, and traversal will help you design more efficient memory hierarchies, multi-hop reasoning, and context linking strategies.]
- [**Add Activation Memory:**
Experiment with
runtime KV-cache for session
state.]
- [**Explore Graph Reasoning:** Build workflows for multi-hop retrieval and answer synthesis.]
- [**Go Deep:** Check the [API Reference](/api-reference/configure-memos) for advanced usage, or run more examples in `examples/`.]
 
[Now your agent remembers not just facts â but the connections between them!]
