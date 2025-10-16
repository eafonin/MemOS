---
source_url: https://memos-docs.openmem.net/open_source/modules/mos/users_configurations
section: Mos
scraped_date: 2025-10-16
title: MemOS Configuration Guide
has_images: no
has_tables: yes
---

# MemOS Configuration Guide
 [ This document provides a comprehensive overview of all configuration fields and initialization methods across the different components in the MemOS system. 
1. [[[Configuration Overview](#configuration-overview)]]
2. [[[MOS Configuration](#mos-configuration)]]
3. [[[LLM Configuration](#llm-configuration)]]
4. [[[MemReader Configuration](#memreader-configuration)]]
5. [[[MemCube Configuration](#memcube-configuration)]]
6. [[[Memory Configuration](#memory-configuration)]]
7. [[[Embedder Configuration](#embedder-configuration)]]
8. [[[Vector Database Configuration](#vector-database-configuration)]]
9. [[[Graph Database Configuration](#graph-database-configuration)]]
10. [[[Scheduler Configuration](#scheduler-configuration)]]
11. [[[Initialization Methods](#initialization-methods)]]
12. [[[Configuration Examples](#configuration-examples)]]
 
## Configuration Overview
 
[MemOS uses a hierarchical configuration system with factory patterns for different backends. Each component has:]
 
- [A base configuration class]
- [Backend-specific configuration classes]
- [A factory class that creates the appropriate configuration based on the backend]
 
## MOS Configuration
 
[The main MOS configuration that orchestrates all components.]
 
### MOSConfig Fields
 
<table><thead><tr><th>Field</th><th>Type</th><th>Default</th><th>Description</th></tr></thead><tbody><tr><td>user_id</td><td>str</td><td>"root"</td><td>User ID for the MOS this Config User ID will as default</td></tr><tr><td>session_id</td><td>str</td><td>auto-generated UUID</td><td>Session ID for the MOS</td></tr><tr><td>chat_model</td><td>LLMConfigFactory</td><td>required</td><td>LLM configuration for chat</td></tr><tr><td>mem_reader</td><td>MemReaderConfigFactory</td><td>required</td><td>MemReader configuration</td></tr><tr><td>mem_scheduler</td><td>SchedulerFactory</td><td>not required</td><td>Scheduler configuration</td></tr><tr><td>max_turns_window</td><td>int</td><td>15</td><td>Maximum conversation turns to keep</td></tr><tr><td>top_k</td><td>int</td><td>5</td><td>Maximum memories to retrieve per query</td></tr><tr><td>enable_textual_memory</td><td>bool</td><td>True</td><td>Enable textual memory</td></tr><tr><td>enable_activation_memory</td><td>bool</td><td>False</td><td>Enable activation memory</td></tr><tr><td>enable_parametric_memory</td><td>bool</td><td>False</td><td>Enable parametric memory</td></tr><tr><td>enable_mem_scheduler</td><td>bool</td><td>False</td><td>Enable scheduler memory</td></tr></tbody></table>
 
### Example MOS Configuration
 
```
{
 "user_id": "root",
 "chat_model": {
 "backend": "huggingface",
 "config": {
 "model_name_or_path": "Qwen/Qwen3-1.7B",
 "temperature": 0.1,
 "remove_think_prefix": true,
 "max_tokens": 4096
 }
 },
 "mem_reader": {
 "backend": "simple_struct",
 "config": {
 "llm": {
 "backend": "ollama",
 "config": {
 "model_name_or_path": "qwen3:0.6b",
 "temperature": 0.8,
 "max_tokens": 1024,
 "top_p": 0.9,
 "top_k": 50
 }
 },
 "embedder": {
 "backend": "ollama",
 "config": {
 "model_name_or_path": "nomic-embed-text:latest"
 }
 },
 "chunker": {
 "backend": "sentence",
 "config": {
 "tokenizer_or_token_counter": "gpt2",
 "chunk_size": 512,
 "chunk_overlap": 128,
 "min_sentences_per_chunk": 1
 }
 }
 }
 },
 "max_turns_window": 20,
 "top_k": 5,
 "enable_textual_memory": true,
 "enable_activation_memory": false,
 "enable_parametric_memory": false
}

```
 
## LLM Configuration
 
[Configuration for different Large Language Model backends.]
 
### Base LLM Fields
 
<table><thead><tr><th>Field</th><th>Type</th><th>Default</th><th>Description</th></tr></thead><tbody><tr><td>model_name_or_path</td><td>str</td><td>required</td><td>Model name or path</td></tr><tr><td>temperature</td><td>float</td><td>0.8</td><td>Temperature for sampling</td></tr><tr><td>max_tokens</td><td>int</td><td>1024</td><td>Maximum tokens to generate</td></tr><tr><td>top_p</td><td>float</td><td>0.9</td><td>Top-p sampling parameter</td></tr><tr><td>top_k</td><td>int</td><td>50</td><td>Top-k sampling parameter</td></tr><tr><td>remove_think_prefix</td><td>bool</td><td>False</td><td>Remove think tags from output</td></tr></tbody></table>
 
### Backend-Specific Fields
 
#### OpenAI LLM
 
<table><thead><tr><th>Field</th><th>Type</th><th>Default</th><th>Description</th></tr></thead><tbody><tr><td>api_key</td><td>str</td><td>required</td><td>OpenAI API key</td></tr><tr><td>api_base</td><td>str</td><td>"https://api.openai.com/v1"</td><td>OpenAI API base URL</td></tr></tbody></table>
 
#### Ollama LLM
 
<table><thead><tr><th>Field</th><th>Type</th><th>Default</th><th>Description</th></tr></thead><tbody><tr><td>api_base</td><td>str</td><td>"http://localhost:11434"</td><td>Ollama API base URL</td></tr></tbody></table>
 
#### HuggingFace LLM
 
<table><thead><tr><th>Field</th><th>Type</th><th>Default</th><th>Description</th></tr></thead><tbody><tr><td>do_sample</td><td>bool</td><td>False</td><td>Use sampling vs greedy decoding</td></tr><tr><td>add_generation_prompt</td><td>bool</td><td>True</td><td>Apply generation template</td></tr></tbody></table>
 
### Example LLM Configurations
 
```
// OpenAI
{
 "backend": "openai",
 "config": {
 "model_name_or_path": "gpt-4o",
 "temperature": 0.8,
 "max_tokens": 1024,
 "top_p": 0.9,
 "top_k": 50,
 "api_key": "sk-...",
 "api_base": "https://api.openai.com/v1"
 }
}

// Ollama
{
 "backend": "ollama",
 "config": {
 "model_name_or_path": "qwen3:0.6b",
 "temperature": 0.8,
 "max_tokens": 1024,
 "top_p": 0.9,
 "top_k": 50,
 "api_base": "http://localhost:11434"
 }
}

// HuggingFace
{
 "backend": "huggingface",
 "config": {
 "model_name_or_path": "Qwen/Qwen3-1.7B",
 "temperature": 0.1,
 "remove_think_prefix": true,
 "max_tokens": 4096,
 "do_sample": false,
 "add_generation_prompt": true
 }
}

```
 
## MemReader Configuration
 
[Configuration for memory reading components.]
 
### Base MemReader Fields
 
<table><thead><tr><th>Field</th><th>Type</th><th>Default</th><th>Description</th></tr></thead><tbody><tr><td>created_at</td><td>datetime</td><td>auto-generated</td><td>Creation timestamp</td></tr><tr><td>llm</td><td>LLMConfigFactory</td><td>required</td><td>LLM configuration</td></tr><tr><td>embedder</td><td>EmbedderConfigFactory</td><td>required</td><td>Embedder configuration</td></tr><tr><td>chunker</td><td>chunkerConfigFactory</td><td>required</td><td>chunker configuration</td></tr></tbody></table>
 
### Backend Types
 
- [`simple_struct`: Structured memory reader]
 
### Example MemReader Configuration
 
```
{
 "backend": "simple_struct",
 "config": {
 "llm": {
 "backend": "ollama",
 "config": {
 "model_name_or_path": "qwen3:0.6b",
 "temperature": 0.0,
 "remove_think_prefix": true,
 "max_tokens": 8192
 }
 },
 "embedder": {
 "backend": "ollama",
 "config": {
 "model_name_or_path": "nomic-embed-text:latest"
 }
 },
 "chunker": {
 "backend": "sentence",
 "config": {
 "tokenizer_or_token_counter": "gpt2",
 "chunk_size": 512,
 "chunk_overlap": 128,
 "min_sentences_per_chunk": 1
 }
 }
 }
}

```
 
## MemCube Configuration
 
[Configuration for memory cube components.]
 
### GeneralMemCubeConfig Fields
 
<table><thead><tr><th>Field</th><th>Type</th><th>Default</th><th>Description</th></tr></thead><tbody><tr><td>user_id</td><td>str</td><td>"default_user"</td><td>User ID for the MemCube</td></tr><tr><td>cube_id</td><td>str</td><td>auto-generated UUID</td><td>Cube ID for the MemCube</td></tr><tr><td>text_mem</td><td>MemoryConfigFactory</td><td>required</td><td>Textual memory configuration</td></tr><tr><td>act_mem</td><td>MemoryConfigFactory</td><td>required</td><td>Activation memory configuration</td></tr><tr><td>para_mem</td><td>MemoryConfigFactory</td><td>required</td><td>Parametric memory configuration</td></tr></tbody></table>
 
### Allowed Backends
 
- [**Text Memory**: `naive_text`, `general_text`, `tree_text`, `uninitialized`]
- [**Activation Memory**: `kv_cache`, `uninitialized`]
- [**Parametric Memory**: `lora`, `uninitialized`]
 
### Example MemCube Configuration
 
```
{
 "user_id": "root",
 "cube_id": "root/mem_cube_kv_cache",
 "text_mem": {},
 "act_mem": {
 "backend": "kv_cache",
 "config": {
 "memory_filename": "activation_memory.pickle",
 "extractor_llm": {
 "backend": "huggingface",
 "config": {
 "model_name_or_path": "Qwen/Qwen3-1.7B",
 "temperature": 0.8,
 "max_tokens": 1024,
 "top_p": 0.9,
 "top_k": 50,
 "add_generation_prompt": true,
 "remove_think_prefix": false
 }
 }
 }
 },
 "para_mem": {
 "backend": "lora",
 "config": {
 "memory_filename": "parametric_memory.adapter",
 "extractor_llm": {
 "backend": "huggingface",
 "config": {
 "model_name_or_path": "Qwen/Qwen3-1.7B",
 "temperature": 0.8,
 "max_tokens": 1024,
 "top_p": 0.9,
 "top_k": 50,
 "add_generation_prompt": true,
 "remove_think_prefix": false
 }
 }
 }
 }
}

```
 
## Memory Configuration
 
[Configuration for different types of memory systems.]
 
### Base Memory Fields
 
<table><thead><tr><th>Field</th><th>Type</th><th>Default</th><th>Description</th></tr></thead><tbody><tr><td>cube_id</td><td>str</td><td>None</td><td>Unique MemCube identifier is can be cube_name or path as default</td></tr></tbody></table>
 
### Textual Memory Configurations
 
#### Base Text Memory
 
<table><thead><tr><th>Field</th><th>Type</th><th>Default</th><th>Description</th></tr></thead><tbody><tr><td>memory_filename</td><td>str</td><td>"textual_memory.json"</td><td>Filename for storing memories</td></tr></tbody></table>
 
#### Naive Text Memory
 
<table><thead><tr><th>Field</th><th>Type</th><th>Default</th><th>Description</th></tr></thead><tbody><tr><td>extractor_llm</td><td>LLMConfigFactory</td><td>required</td><td>LLM for memory extraction</td></tr></tbody></table>
 
#### General Text Memory
 
<table><thead><tr><th>Field</th><th>Type</th><th>Default</th><th>Description</th></tr></thead><tbody><tr><td>extractor_llm</td><td>LLMConfigFactory</td><td>required</td><td>LLM for memory extraction</td></tr><tr><td>vector_db</td><td>VectorDBConfigFactory</td><td>required</td><td>Vector database configuration</td></tr><tr><td>embedder</td><td>EmbedderConfigFactory</td><td>required</td><td>Embedder configuration</td></tr></tbody></table>
 
#### Tree Text Memory
 
<table><thead><tr><th>Field</th><th>Type</th><th>Default</th><th>Description</th></tr></thead><tbody><tr><td>extractor_llm</td><td>LLMConfigFactory</td><td>required</td><td>LLM for memory extraction</td></tr><tr><td>dispatcher_llm</td><td>LLMConfigFactory</td><td>required</td><td>LLM for memory dispatching</td></tr><tr><td>embedder</td><td>EmbedderConfigFactory</td><td>required</td><td>Embedder configuration</td></tr><tr><td>graph_db</td><td>GraphDBConfigFactory</td><td>required</td><td>Graph database configuration</td></tr></tbody></table>
 
### Activation Memory Configurations
 
#### Base Activation Memory
 
<table><thead><tr><th>Field</th><th>Type</th><th>Default</th><th>Description</th></tr></thead><tbody><tr><td>memory_filename</td><td>str</td><td>"activation_memory.pickle"</td><td>Filename for storing memories</td></tr></tbody></table>
 
#### KV Cache Memory
 
<table><thead><tr><th>Field</th><th>Type</th><th>Default</th><th>Description</th></tr></thead><tbody><tr><td>extractor_llm</td><td>LLMConfigFactory</td><td>required</td><td>LLM for memory extraction (must be huggingface)</td></tr></tbody></table>
 
### Parametric Memory Configurations
 
#### Base Parametric Memory
 
<table><thead><tr><th>Field</th><th>Type</th><th>Default</th><th>Description</th></tr></thead><tbody><tr><td>memory_filename</td><td>str</td><td>"parametric_memory.adapter"</td><td>Filename for storing memories</td></tr></tbody></table>
 
#### LoRA Memory
 
<table><thead><tr><th>Field</th><th>Type</th><th>Default</th><th>Description</th></tr></thead><tbody><tr><td>extractor_llm</td><td>LLMConfigFactory</td><td>required</td><td>LLM for memory extraction (must be huggingface)</td></tr></tbody></table>
 
### Example Memory Configurations
 
```
// Tree Text Memory
{
 "backend": "tree_text",
 "config": {
 "memory_filename": "tree_memory.json",
 "extractor_llm": {
 "backend": "ollama",
 "config": {
 "model_name_or_path": "qwen3:0.6b",
 "temperature": 0.0,
 "remove_think_prefix": true,
 "max_tokens": 8192
 }
 },
 "dispatcher_llm": {
 "backend": "ollama",
 "config": {
 "model_name_or_path": "qwen3:0.6b",
 "temperature": 0.0,
 "remove_think_prefix": true,
 "max_tokens": 8192
 }
 },
 "embedder": {
 "backend": "ollama",
 "config": {
 "model_name_or_path": "nomic-embed-text:latest"
 }
 },
 "graph_db": {
 "backend": "neo4j",
 "config": {
 "uri": "bolt://localhost:7687",
 "user": "neo4j",
 "password": "12345678",
 "db_name": "user08alice",
 "auto_create": true,
 "embedding_dimension": 768
 }
 }
 }
}

```
 
## Embedder Configuration
 
[Configuration for embedding models.]
 
### Base Embedder Fields
 
<table><thead><tr><th>Field</th><th>Type</th><th>Default</th><th>Description</th></tr></thead><tbody><tr><td>model_name_or_path</td><td>str</td><td>required</td><td>Model name or path</td></tr><tr><td>embedding_dims</td><td>int</td><td>None</td><td>Number of embedding dimensions</td></tr></tbody></table>
 
### Backend-Specific Fields
 
#### Ollama Embedder
 
<table><thead><tr><th>Field</th><th>Type</th><th>Default</th><th>Description</th></tr></thead><tbody><tr><td>api_base</td><td>str</td><td>"http://localhost:11434"</td><td>Ollama API base URL</td></tr></tbody></table>
 
#### Sentence Transformer Embedder
 
[No additional fields beyond base configuration.]
 
### Example Embedder Configurations
 
```
// Ollama Embedder
{
 "backend": "ollama",
 "config": {
 "model_name_or_path": "nomic-embed-text:latest",
 "api_base": "http://localhost:11434"
 }
}

// Sentence Transformer Embedder
{
 "backend": "sentence_transformer",
 "config": {
 "model_name_or_path": "all-MiniLM-L6-v2",
 "embedding_dims": 384
 }
}

```
 
## Vector Database Configuration
 
[Configuration for vector databases.]
 
### Base Vector DB Fields
 
<table><thead><tr><th>Field</th><th>Type</th><th>Default</th><th>Description</th></tr></thead><tbody><tr><td>collection_name</td><td>str</td><td>required</td><td>Name of the collection</td></tr><tr><td>vector_dimension</td><td>int</td><td>None</td><td>Dimension of the vectors</td></tr><tr><td>distance_metric</td><td>str</td><td>None</td><td>Distance metric (cosine, euclidean, dot)</td></tr></tbody></table>
 
### Qdrant Vector DB Fields
 
<table><thead><tr><th>Field</th><th>Type</th><th>Default</th><th>Description</th></tr></thead><tbody><tr><td>host</td><td>str</td><td>None</td><td>Qdrant host</td></tr><tr><td>port</td><td>int</td><td>None</td><td>Qdrant port</td></tr><tr><td>path</td><td>str</td><td>None</td><td>Qdrant local path</td></tr></tbody></table>
 
### Example Vector DB Configuration
 
```
{
 "backend": "qdrant",
 "config": {
 "collection_name": "memories",
 "vector_dimension": 768,
 "distance_metric": "cosine",
 "path": "/path/to/qdrant"
 }
}

```
 
## Graph Database Configuration
 
[Configuration for graph databases.]
 
### Base Graph DB Fields
 
<table><thead><tr><th>Field</th><th>Type</th><th>Default</th><th>Description</th></tr></thead><tbody><tr><td>uri</td><td>str</td><td>required</td><td>Database URI</td></tr><tr><td>user</td><td>str</td><td>required</td><td>Database username</td></tr><tr><td>password</td><td>str</td><td>required</td><td>Database password</td></tr></tbody></table>
 
### Neo4j Graph DB Fields
 
<table><thead><tr><th>Field</th><th>Type</th><th>Default</th><th>Description</th></tr></thead><tbody><tr><td>db_name</td><td>str</td><td>required</td><td>Target database name</td></tr><tr><td>auto_create</td><td>bool</td><td>False</td><td>Create DB if it doesn't exist</td></tr><tr><td>embedding_dimension</td><td>int</td><td>768</td><td>Vector embedding dimension</td></tr></tbody></table>
 
### Example Graph DB Configuration
 
```
{
 "backend": "neo4j",
 "config": {
 "uri": "bolt://localhost:7687",
 "user": "neo4j",
 "password": "12345678",
 "db_name": "user08alice",
 "auto_create": true,
 "embedding_dimension": 768
 }
}

```
 
## Scheduler Configuration
 
[Configuration for memory scheduling systems that manage memory retrieval and activation.]
 
### Base Scheduler Fields
 
<table><thead><tr><th>Field</th><th>Type</th><th>Default</th><th>Description</th></tr></thead><tbody><tr><td>top_k</td><td>int</td><td>10</td><td>Number of top candidates to consider in initial retrieval</td></tr><tr><td>top_n</td><td>int</td><td>5</td><td>Number of final results to return after processing</td></tr><tr><td>enable_parallel_dispatch</td><td>bool</td><td>True</td><td>Whether to enable parallel message processing using thread pool</td></tr><tr><td>thread_pool_max_workers</td><td>int</td><td>5</td><td>Maximum worker threads in pool (1-20)</td></tr><tr><td>consume_interval_seconds</td><td>int</td><td>3</td><td>Interval for consuming messages from queue in seconds (0-60)</td></tr></tbody></table>
 
### General Scheduler Fields
 
<table><thead><tr><th>Field</th><th>Type</th><th>Default</th><th>Description</th></tr></thead><tbody><tr><td>act_mem_update_interval</td><td>int</td><td>300</td><td>Interval in seconds for updating activation memory</td></tr><tr><td>context_window_size</td><td>int</td><td>5</td><td>Size of the context window for conversation history</td></tr><tr><td>activation_mem_size</td><td>int</td><td>5</td><td>Maximum size of the activation memory</td></tr><tr><td>act_mem_dump_path</td><td>str</td><td>auto-generated</td><td>File path for dumping activation memory</td></tr></tbody></table>
 
### Backend Types
 
- [`general_scheduler`: Advanced scheduler with activation memory management]
 
### Example Scheduler Configuration
 
```
{
 "backend": "general_scheduler",
 "config": {
 "top_k": 10,
 "top_n": 5,
 "act_mem_update_interval": 300,
 "context_window_size": 5,
 "activation_mem_size": 1000,
 "thread_pool_max_workers": 10,
 "consume_interval_seconds": 3,
 "enable_parallel_dispatch": true
 }
}

```
 
## Initialization Methods
 
### From JSON File
 
```
from memos.configs.mem_os import MOSConfig

# Load configuration from JSON file
mos_config = MOSConfig.from_json_file("path/to/config.json")

```
 
### From Dictionary
 
```
from memos.configs.mem_os import MOSConfig

# Create configuration from dictionary
config_dict = {
 "user_id": "root",
 "chat_model": {
 "backend": "huggingface",
 "config": {
 "model_name_or_path": "Qwen/Qwen3-1.7B",
 "temperature": 0.1
 }
 }
 # ... other fields
}

mos_config = MOSConfig(**config_dict)

```
 
### Factory Pattern Usage
 
```
from memos.configs.llm import LLMConfigFactory

# Create LLM configuration using factory
llm_config = LLMConfigFactory(
 backend="huggingface",
 config={
 "model_name_or_path": "Qwen/Qwen3-1.7B",
 "temperature": 0.1
 }
)

```
 
## Configuration Examples
 
### Complete MOS Setup
 
```
from memos.configs.mem_os import MOSConfig
from memos.mem_os.main import MOS

# Load configuration
mos_config = MOSConfig.from_json_file("examples/data/config/simple_memos_config.json")

# Initialize MOS
mos = MOS(mos_config)

# Create user and register cube
user_id = "user_123"
mos.create_user(user_id=user_id)
mos.register_mem_cube("path/to/mem_cube", user_id=user_id)

# Use MOS
response = mos.chat("Hello, how are you?", user_id=user_id)

```
 
### Tree Memory Configuration
 
```
from memos.configs.memory import MemoryConfigFactory

# Create tree memory configuration
tree_memory_config = MemoryConfigFactory(
 backend="tree_text",
 config={
 "memory_filename": "tree_memory.json",
 "extractor_llm": {
 "backend": "ollama",
 "config": {
 "model_name_or_path": "qwen3:0.6b",
 "temperature": 0.0,
 "max_tokens": 8192
 }
 },
 "dispatcher_llm": {
 "backend": "ollama",
 "config": {
 "model_name_or_path": "qwen3:0.6b",
 "temperature": 0.0,
 "max_tokens": 8192
 }
 },
 "embedder": {
 "backend": "ollama",
 "config": {
 "model_name_or_path": "nomic-embed-text:latest"
 }
 },
 "graph_db": {
 "backend": "neo4j",
 "config": {
 "uri": "bolt://localhost:7687",
 "user": "neo4j",
 "password": "password",
 "db_name": "memories",
 "auto_create": True,
 "embedding_dimension": 768
 }
 }
 }
)

```
 
### Multi-Backend LLM Configuration
 
```
from memos.configs.llm import LLMConfigFactory

# OpenAI configuration
openai_config = LLMConfigFactory(
 backend="openai",
 config={
 "model_name_or_path": "gpt-4o",
 "temperature": 0.8,
 "max_tokens": 1024,
 "api_key": "sk-...",
 "api_base": "https://api.openai.com/v1"
 }
)

# Ollama configuration
ollama_config = LLMConfigFactory(
 backend="ollama",
 config={
 "model_name_or_path": "qwen3:0.6b",
 "temperature": 0.8,
 "max_tokens": 1024,
 "api_base": "http://localhost:11434"
 }
)

# HuggingFace configuration
hf_config = LLMConfigFactory(
 backend="huggingface",
 config={
 "model_name_or_path": "Qwen/Qwen3-1.7B",
 "temperature": 0.1,
 "remove_think_prefix": True,
 "max_tokens": 4096,
 "do_sample": False,
 "add_generation_prompt": True
 }
)

```
 
[This comprehensive configuration system allows for flexible and extensible setup of the MemOS system with different backends and components.]
