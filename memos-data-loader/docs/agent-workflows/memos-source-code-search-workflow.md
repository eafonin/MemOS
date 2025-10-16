# MemOS Source Code Search Workflow - Agent Guide

This document provides systematic workflows for agents to search and analyze the MemOS source code (`src/memos/`) for integration planning, troubleshooting, and understanding system behavior.

## Directory Structure Overview

```
src/memos/
├── api/                    # API clients and server implementations
├── configs/                # Configuration schemas and factories
├── embedders/              # Embedding model implementations
├── llms/                   # LLM backend implementations
├── mem_cube/               # MemCube implementations
├── mem_os/                 # MOS (Memory Operating System) core
├── mem_reader/             # Memory reading/extraction modules
├── mem_scheduler/          # Memory scheduling system
├── memories/               # Memory type implementations
│   ├── textual/           # Text memory backends
│   ├── activation/        # KV cache and activation memory
│   └── parametric/        # LoRA and parametric memory
├── templates/              # Prompt templates
├── utils/                  # Utility functions
└── vector_dbs/             # Vector database backends
```

---

## Workflow 1: API Integration Planning

**Goal**: Understand existing API structure to design new endpoints or integrations.

### Step 1: Identify API Entry Points
```bash
# Find all API-related files
Glob: "src/memos/api/*.py"

# Expected files:
# - client.py          # Client SDK for dashboard API
# - config.py          # API configuration management
# - product_api.py     # Production API endpoints
# - start_api.py       # Development/startup API
# - mcp_serve.py       # MCP (Model Context Protocol) server
# - product_models.py  # Pydantic models for API
```

### Step 2: Analyze API Client Implementation
```bash
# Read the client SDK to understand:
Read: "src/memos/api/client.py"

# Key information to extract:
# - Authentication mechanism (line 29: Authorization: Token)
# - Base URL configuration (line 22: MEMOS_BASE_URL env var)
# - Available methods: add_message(), search_memory(), get_message()
# - Request/response formats
# - Error handling patterns
# - Retry logic (MAX_RETRY_COUNT)
```

### Step 3: Examine API Server Implementations
```bash
# For production API
Read: "src/memos/api/product_api.py"

# For development API
Read: "src/memos/api/start_api.py"

# Key information:
# - Endpoint definitions (FastAPI routes)
# - Request validators
# - Database interactions
# - User management integration
# - MemCube lifecycle management
```

### Step 4: Review API Models
```bash
# Understand request/response schemas
Read: "src/memos/api/product_models.py"

# Extract:
# - MemOSAddResponse structure
# - MemOSSearchResponse structure
# - MemOSGetMessagesResponse structure
# - Validation rules
```

### Step 5: Check Configuration Patterns
```bash
# Understand how APIs are configured
Read: "src/memos/api/config.py"

# Key patterns:
# - Environment variable usage
# - Factory pattern for backends
# - Default configurations
# - Multi-backend support (OpenAI, Ollama, HuggingFace, vLLM)
```

---

## Workflow 2: Troubleshooting API Call Failures

**Goal**: Diagnose why API calls are failing.

### Step 1: Check Authentication Issues
```bash
# Search for authentication logic
Grep: pattern="Authorization|auth|api_key" path="src/memos/api/"

# Verify:
# 1. API key format: "Token {api_key}" (client.py:29)
# 2. Environment variable: MEMOS_API_KEY (client.py:24)
# 3. Header construction in client.py:29
```

### Step 2: Identify Request Validation
```bash
# Find validation logic
Grep: pattern="_validate|validate_required" path="src/memos/api/"

# Check:
# - Required parameters (client.py:31-35)
# - Parameter types and constraints
# - Pydantic model validation
```

### Step 3: Analyze Error Responses
```bash
# Search for error handling
Grep: pattern="raise|error|exception|status_code" path="src/memos/api/" output_mode="content" -n

# Identify:
# - HTTP status codes used
# - Error message formats
# - Exception types raised
# - Retry logic (client.py:46-57)
```

### Step 4: Check Network Configuration
```bash
# Find base URL and endpoint construction
Grep: pattern="base_url|BASE_URL|endpoint" path="src/memos/api/"

# Verify:
# - Default base URL: https://memos.memtensor.cn/api/openmem/v1
# - Endpoint paths: /add/message, /search/memory, /get/message
# - Timeout settings (client.py:49, timeout=30)
```

### Step 5: Review Request/Response Logging
```bash
# Find logging statements
Grep: pattern="logger|log\\.error|log\\.info" path="src/memos/api/" output_mode="content" -n

# Check logged information:
# - Error messages (client.py:55, 79, 107)
# - Request parameters
# - Response data
```

---

## Workflow 3: Troubleshooting Data Load/Retrieve Failures

**Goal**: Diagnose why data fails to load or retrieve from memory.

### Step 1: Identify Memory Backend Type
```bash
# Find memory implementations
Glob: "src/memos/memories/**/*.py"

# Memory types:
# - textual/general_text_memory.py      # Vector-based text memory
# - textual/tree_text_memory/           # Graph-based tree memory
# - textual/naive_text_memory.py        # Simple in-memory text
# - activation/kv_cache_memory.py       # KV cache for LLM
# - parametric/lora_memory.py           # LoRA adapters
```

### Step 2: Check Vector Database Connection
```bash
# Find vector DB implementations
Glob: "src/memos/vector_dbs/*.py"

# Read the relevant backend:
Read: "src/memos/vector_dbs/qdrant_db.py"

# Or search for connection issues:
Grep: pattern="connect|client|host|port" path="src/memos/vector_dbs/"

# Common issues:
# - QDRANT_HOST environment variable
# - Port configuration (default 6333)
# - Collection creation/initialization
```

### Step 3: Check Graph Database Connection (for Tree Memory)
```bash
# Find graph DB implementations
Glob: "src/memos/memories/textual/tree_text_memory/graphdbs/*.py"

# Read Neo4j implementation:
Read: "src/memos/memories/textual/tree_text_memory/graphdbs/neo4j_graphdb.py"

# Verify:
# - NEO4J_URI environment variable
# - Authentication (NEO4J_USER, NEO4J_PASSWORD)
# - Database creation (auto_create flag)
# - Multi-database support
```

### Step 4: Analyze Memory Operations
```bash
# Search for add/search/get operations
Grep: pattern="def add|def search|def get|def retrieve" path="src/memos/memories/" output_mode="content" -n

# Check:
# - Method signatures
# - Required parameters
# - Return types
# - Error handling
```

### Step 5: Check Embedder Functionality
```bash
# Find embedder implementations
Glob: "src/memos/embedders/*.py"

# Read relevant backend:
Read: "src/memos/embedders/ollama.py"
# or
Read: "src/memos/embedders/universal_api.py"

# Verify:
# - Model name/path configuration
# - API endpoint availability
# - Embedding dimension matching
# - Token limits
```

### Step 6: Review MemCube Loading
```bash
# Check MemCube initialization
Read: "src/memos/mem_cube/general.py"

# Look for:
# - load() method implementation
# - dump() method implementation
# - init_from_dir() class method
# - File path handling
# - Serialization/deserialization
```

---

## Workflow 4: Understanding MemOS Core Functions

**Goal**: Understand how core MemOS functions work.

### Step 1: Analyze MOS (Memory Operating System) Core
```bash
# Read the main MOS implementation
Read: "src/memos/mem_os/main.py"

# Key methods to understand:
# - __init__(): System initialization
# - create_user(): User registration
# - register_mem_cube(): MemCube attachment
# - chat(): Conversation handling
# - add(): Memory addition
# - search(): Memory retrieval
# - get_suggestion_queries(): Query suggestions
```

### Step 2: Understand Memory Reading Process
```bash
# Find MemReader implementations
Glob: "src/memos/mem_reader/*.py"

# Read the main reader:
Read: "src/memos/mem_reader/simple_struct_mem_reader.py"

# Understand:
# - extract_conversation(): How conversations become memories
# - Chunking strategy
# - LLM-based extraction
# - Memory structuring
```

### Step 3: Analyze Memory Scheduling
```bash
# Read scheduler implementation
Read: "src/memos/mem_scheduler/scheduler.py"

# Key concepts:
# - Working memory management
# - Long-term memory promotion
# - Activation memory lifecycle
# - Parallel dispatch
# - Context window management
```

### Step 4: Review Configuration System
```bash
# Understand configuration factories
Glob: "src/memos/configs/*.py"

# Read key configs:
Read: "src/memos/configs/mem_os.py"      # MOSConfig
Read: "src/memos/configs/llm.py"         # LLMConfigFactory
Read: "src/memos/configs/memory.py"      # MemoryConfigFactory
Read: "src/memos/configs/embedder.py"    # EmbedderConfigFactory

# Understand:
# - Factory pattern usage
# - Backend switching mechanism
# - Validation rules
# - Default values
```

### Step 5: Examine Prompt Templates
```bash
# Check prompt engineering
Read: "src/memos/templates/mos_prompts.py"

# Understand:
# - System prompts
# - Memory extraction prompts
# - Context assembly
# - Instruction completion
```

---

## Workflow 5: Tracing End-to-End Data Flow

**Goal**: Trace how data flows from API call to storage to retrieval.

### Trace 1: Message Addition Flow
```bash
# 1. API entry point
Read: "src/memos/api/product_api.py"
# Find: /product/add endpoint

# 2. MOS add method
Read: "src/memos/mem_os/main.py"
# Find: add() method

# 3. Memory reader extraction
Read: "src/memos/mem_reader/simple_struct_mem_reader.py"
# Find: extract_conversation() method

# 4. LLM call for extraction
Read: "src/memos/llms/openai.py"
# Find: generate() method

# 5. Embedder call
Read: "src/memos/embedders/universal_api.py"
# Find: embed() method

# 6. Storage in memory backend
Read: "src/memos/memories/textual/general_text_memory.py"
# Find: add() method

# 7. Vector DB insertion
Read: "src/memos/vector_dbs/qdrant_db.py"
# Find: add() method
```

### Trace 2: Memory Search Flow
```bash
# 1. API entry point
Read: "src/memos/api/product_api.py"
# Find: /product/search endpoint

# 2. MOS search method
Read: "src/memos/mem_os/main.py"
# Find: search() method

# 3. Memory backend search
Read: "src/memos/memories/textual/general_text_memory.py"
# Find: search() method

# 4. Vector DB retrieval
Read: "src/memos/vector_dbs/qdrant_db.py"
# Find: search() method

# 5. Reranking (if enabled)
Grep: pattern="rerank|reranker" path="src/memos/"
# Find reranker implementations

# 6. Response formatting
Read: "src/memos/api/product_models.py"
# Find: MemOSSearchResponse model
```

---

## Workflow 6: Finding Configuration Examples

**Goal**: Find configuration examples for specific use cases.

### Step 1: Check Default Configurations
```bash
# Find default config utilities
Read: "src/memos/mem_os/utils/default_config.py"

# Or check API config
Read: "src/memos/api/config.py"

# Extract default values for:
# - LLM backends
# - Embedder backends
# - Memory types
# - Database connections
```

### Step 2: Search Example Files
```bash
# Find example configurations
Glob: "examples/**/*.py"
Glob: "examples/data/config/**/*.json"
Glob: "examples/data/config/**/*.yaml"

# Common examples:
# - examples/mem_os/simple_openapi_memos.py
# - examples/mem_os/persistent_memos_example.py
# - examples/data/config/simple_memos_config.json
```

### Step 3: Check Test Configurations
```bash
# Find test configs
Glob: "tests/configs/*.py"
Glob: "tests/**/test_*.py"

# Look for:
# - Mock configurations
# - Integration test setups
# - Backend-specific configs
```

---

## Workflow 7: Debugging Specific Error Messages

**Goal**: Find where specific errors originate and how to fix them.

### Step 1: Search for Error Message
```bash
# Search for the exact error text
Grep: pattern="<error_message_text>" path="src/memos/" output_mode="content" -n

# Example:
Grep: pattern="API key is required" path="src/memos/" output_mode="content" -n
# Result: src/memos/api/client.py:27
```

### Step 2: Find Related Exception Classes
```bash
# Search for exception definitions
Grep: pattern="class.*Error|class.*Exception|raise.*Error" path="src/memos/" output_mode="content" -n

# Check custom exceptions
Glob: "src/memos/**/exceptions.py"
```

### Step 3: Trace Error Context
```bash
# Read the file containing the error
Read: "<file_from_step_1>"

# Look for:
# - Try-except blocks around the error
# - Validation logic before the error
# - Required conditions to avoid the error
# - Error handling patterns
```

### Step 4: Find Error Documentation
```bash
# Search for error code definitions
Grep: pattern="error.*code|ERROR.*CODE|status.*code" path="src/memos/api/" output_mode="content" -n

# Check API models
Read: "src/memos/api/product_models.py"
# Look for error response structures
```

---

## Workflow 8: Understanding Multi-Backend Support

**Goal**: Understand how to switch between different backends (LLMs, embedders, DBs).

### Step 1: Identify Backend Types
```bash
# Find all backend implementations
Glob: "src/memos/llms/*.py"
Glob: "src/memos/embedders/*.py"
Glob: "src/memos/vector_dbs/*.py"

# Common backends:
# LLMs: openai.py, ollama.py, huggingface.py, vllm.py
# Embedders: universal_api.py, ollama.py, sentence_transformer.py
# Vector DBs: qdrant_db.py, chroma_db.py
```

### Step 2: Check Factory Pattern
```bash
# Read factory implementations
Read: "src/memos/configs/llm.py"

# Understand:
# - LLMConfigFactory class
# - Backend registration
# - How "backend" parameter selects implementation
# - Config validation per backend
```

### Step 3: Find Backend-Specific Config
```bash
# Search for backend-specific config classes
Grep: pattern="class.*Config.*Backend|class.*LLMConfig|class.*EmbedderConfig" path="src/memos/configs/" output_mode="content" -n

# Example:
# - OpenAILLMConfig
# - OllamaLLMConfig
# - HuggingFaceLLMConfig
```

### Step 4: Check Environment Variables
```bash
# Find env var usage
Grep: pattern="os\\.getenv|environ\\[" path="src/memos/api/config.py" output_mode="content" -n

# Common variables:
# - OPENAI_API_KEY
# - OPENAI_API_BASE
# - MOS_EMBEDDER_BACKEND
# - MOS_CHAT_MODEL_PROVIDER
# - NEO4J_URI
# - QDRANT_HOST
```

---

## Workflow 9: Adding New Features or Endpoints

**Goal**: Understand patterns to add new functionality.

### Step 1: Study Existing Endpoint Pattern
```bash
# Read existing API implementation
Read: "src/memos/api/product_api.py"

# Identify pattern:
# 1. FastAPI route decorator
# 2. Pydantic request model
# 3. Validation
# 4. MOS method call
# 5. Response model construction
# 6. Error handling
```

### Step 2: Check Request/Response Models
```bash
# Read model definitions
Read: "src/memos/api/product_models.py"

# Pattern to follow:
# - BaseModel inheritance
# - Field validation
# - Type hints
# - Optional vs required fields
```

### Step 3: Find MOS Extension Points
```bash
# Read MOS main class
Read: "src/memos/mem_os/main.py"

# Identify:
# - Public methods
# - Private helper methods
# - Method naming conventions
# - Return type patterns
```

### Step 4: Check Testing Patterns
```bash
# Find related tests
Glob: "tests/api/*.py"

# Read test structure
Read: "tests/api/test_start_api.py"

# Understand:
# - Test setup/teardown
# - Mock patterns
# - Assertion patterns
```

---

## Workflow 10: Performance Investigation

**Goal**: Find performance bottlenecks and optimization opportunities.

### Step 1: Check Async/Concurrent Code
```bash
# Search for async patterns
Grep: pattern="async def|await |asyncio" path="src/memos/" output_mode="files_with_matches"

# Find thread pool usage
Grep: pattern="ThreadPool|concurrent\\.futures" path="src/memos/" output_mode="content" -n
```

### Step 2: Analyze Scheduler Performance
```bash
# Read scheduler implementation
Read: "src/memos/mem_scheduler/scheduler.py"

# Check:
# - Parallel dispatch settings
# - Thread pool configuration
# - Queue processing intervals
# - Memory update intervals
```

### Step 3: Check Caching Mechanisms
```bash
# Search for cache usage
Grep: pattern="cache|lru_cache|@cache" path="src/memos/" output_mode="content" -n

# Check activation memory
Read: "src/memos/memories/activation/kv_cache_memory.py"
```

### Step 4: Review Database Query Patterns
```bash
# Check vector DB queries
Read: "src/memos/vector_dbs/qdrant_db.py"

# Look for:
# - Batch operations
# - Query limits (top_k)
# - Filter optimization
# - Index usage
```

---

## Quick Reference Commands

### Find by Functionality
```bash
# Authentication
Grep: pattern="auth|token|api_key" path="src/memos/api/"

# Configuration
Grep: pattern="Config|config" path="src/memos/configs/"

# Memory operations
Grep: pattern="def add|def search|def get" path="src/memos/memories/"

# Error handling
Grep: pattern="raise|Exception|Error" path="src/memos/"

# Environment variables
Grep: pattern="os\\.getenv|environ" path="src/memos/"
```

### Find by File Type
```bash
# All API files
Glob: "src/memos/api/*.py"

# All memory implementations
Glob: "src/memos/memories/**/*.py"

# All configuration files
Glob: "src/memos/configs/*.py"

# All LLM backends
Glob: "src/memos/llms/*.py"

# All tests
Glob: "tests/**/*.py"
```

### Find by Pattern
```bash
# Class definitions
Grep: pattern="^class " path="src/memos/" output_mode="content" -n

# Function definitions
Grep: pattern="^def |^    def " path="src/memos/" output_mode="content" -n

# TODO comments
Grep: pattern="TODO|FIXME|HACK" path="src/memos/" output_mode="content" -n

# Type hints
Grep: pattern="-> |: List\\[|: Dict\\[|: Optional\\[" path="src/memos/" output_mode="content" -n
```

---

## Best Practices for Agents

1. **Start Broad, Then Narrow**: Use Glob to find relevant files, then Grep for specific patterns, then Read for details.

2. **Check Related Files**: If you find something in `client.py`, also check `config.py` and `product_models.py`.

3. **Follow Imports**: When you see `from memos.x import Y`, read that file next to understand dependencies.

4. **Check Tests**: Tests in `tests/` often show how to use the code correctly.

5. **Look for Examples**: The `examples/` directory has working code for common use cases.

6. **Trace Data Flow**: Follow data from API → MOS → Memory → Storage to understand the full pipeline.

7. **Check Environment Variables**: Many issues are configuration problems - check `src/memos/api/config.py`.

8. **Read Error Context**: Don't just find the error line - read 10-20 lines before and after to understand context.

9. **Compare Implementations**: If troubleshooting one backend (e.g., OpenAI), compare with another (e.g., Ollama) to spot differences.

10. **Document Your Findings**: When you find a solution, note the file path and line numbers for future reference.

---

## Common Issue Resolution Patterns

### Issue: "API key is required"
- **File**: `src/memos/api/client.py:27`
- **Solution**: Set `MEMOS_API_KEY` environment variable or pass to `MemOSClient(api_key=...)`

### Issue: "Connection refused" to vector DB
- **Files**: `src/memos/vector_dbs/qdrant_db.py`
- **Solution**: Check `QDRANT_HOST` and `QDRANT_PORT` environment variables, ensure service is running

### Issue: "Memory not found" after adding
- **Files**: `src/memos/memories/textual/`, `src/memos/mem_os/main.py`
- **Solution**: Check MemCube registration, verify user_id matches, check embedding dimension consistency

### Issue: "Model not found" error
- **Files**: `src/memos/llms/`, `src/memos/embedders/`
- **Solution**: Verify model name/path, check API base URL, ensure model is downloaded (for local backends)

### Issue: Configuration validation errors
- **Files**: `src/memos/configs/`
- **Solution**: Use factory pattern correctly, check required fields, verify backend name matches available options

---

## Version Note

This workflow is optimized for the MemOS codebase structure as of 2025-10-16. File paths and implementations may change in future versions. Always verify current structure with:

```bash
Glob: "src/memos/**/*.py"
```
