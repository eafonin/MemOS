# VS Code Investigation Guide for MemOS Issues

## 1. Find and Fix the eval() Issue

### Search for the problematic eval() usage:
```
Search in files (Ctrl+Shift+F):
- Search term: eval(response)
- Include: src/**/*.py
- Look in: /app/src/memos/memories/textual/tree_text_memory/retrieve/
```

**File to fix:** `task_goal_parser.py`
- Around line 90, replace:
```python
response_json = eval(response)
```
with:
```python
response_json = json.loads(response)
```

## 2. Fix Neo4j Property Storage Issues

### Search for Neo4j add_node calls:
```
Search in files:
- Search term: self.graph_store.add_node
- Include: src/**/*.py
```

**File to fix:** `/app/src/memos/memories/textual/tree_text_memory/organize/manager.py`
- Around line 161, find the metadata preparation
- The issue is that `metadata` contains nested dictionaries

### Add this fix before line 161:
```python
# Flatten metadata to prevent Neo4j type errors
def flatten_metadata(metadata):
    """Flatten nested dictionaries to strings for Neo4j compatibility"""
    flat_metadata = {}
    for key, value in metadata.items():
        if isinstance(value, dict):
            # Convert dict to JSON string
            flat_metadata[key] = json.dumps(value)
        elif isinstance(value, list):
            # Convert list to JSON string if contains complex types
            if value and isinstance(value[0], dict):
                flat_metadata[key] = json.dumps(value)
            else:
                flat_metadata[key] = value
        else:
            flat_metadata[key] = value
    return flat_metadata

# Before the add_node call:
metadata = flatten_metadata(metadata)
self.graph_store.add_node(working_memory.id, working_memory.memory, metadata)
```

## 3. Debug the Memory Addition Timeout

### Add debug logging to track where it hangs:
```
Search for: _process_memory
File: /app/src/memos/memories/textual/tree_text_memory/organize/manager.py
```

Add logging at key points:
```python
import logging
logger = logging.getLogger(__name__)

def _process_memory(self, memory):
    logger.info(f"Starting memory processing: {memory.id}")
    
    # Add logging before each major operation
    logger.info("Adding to working memory...")
    working_id = self._add_memory_to_db(memory, "WorkingMemory")
    
    logger.info("Processing with LLM...")
    # ... rest of the code
```

## 4. Fix the Chat SSE Response Issue

### Find the chat endpoint:
```
Search: def chat
Include: src/**/*.py
```

The chat endpoint is returning Server-Sent Events (SSE) format. Look for:
- StreamingResponse
- EventSourceResponse
- yield statements in the response

### To handle SSE in the client, modify your test script:
```python
def parse_sse_response(response_text):
    """Parse SSE format to extract text"""
    lines = response_text.split('\n')
    full_text = []
    
    for line in lines:
        if line.startswith('data: '):
            try:
                data = json.loads(line[6:])  # Remove 'data: ' prefix
                if data.get('type') == 'text':
                    full_text.append(data.get('data', ''))
            except json.JSONDecodeError:
                continue
    
    return ' '.join(full_text)
```

## 5. Check Configuration Issues

### Verify LLM configuration:
```
File: /app/src/memos/configs/
Search: OpenAILLMConfig or LLMConfig
```

Make sure the OpenRouter configuration is correct:
- API base URL should be: https://openrouter.ai/api/v1
- Model should include provider: anthropic/claude-3.5-sonnet

## 6. Database Cleanup Script

Create this script to clean Neo4j:
```python
# cleanup_neo4j.py
from neo4j import GraphDatabase

driver = GraphDatabase.driver(
    "bolt://localhost:7687", 
    auth=("neo4j", "memospassword123")
)

with driver.session() as session:
    # Remove all nodes with complex properties
    session.run("""
        MATCH (n)
        WHERE ANY(key in keys(n) WHERE 
            n[key] IS NOT NULL AND 
            NOT type(n[key]) IN ['STRING', 'INTEGER', 'FLOAT', 'BOOLEAN', 'NULL'])
        DETACH DELETE n
    """)
    
    # Count remaining nodes
    result = session.run("MATCH (n) RETURN count(n) as count")
    count = result.single()['count']
    print(f"Remaining nodes: {count}")

driver.close()
```

## 7. Key Files to Check

Priority files to investigate:
1. `/app/src/memos/memories/textual/tree_text_memory/organize/manager.py` - Memory processing
2. `/app/src/memos/memories/textual/tree_text_memory/retrieve/task_goal_parser.py` - eval() issue
3. `/app/src/memos/graph_dbs/neo4j_community.py` - Neo4j operations
4. `/app/src/memos/api/routes/product.py` - API endpoints
5. `/app/src/memos/services/chat.py` or similar - Chat service

## VS Code Debug Configuration

Add to `.vscode/launch.json`:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Remote Attach",
            "type": "python",
            "request": "attach",
            "connect": {
                "host": "localhost",
                "port": 5678
            },
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}/src",
                    "remoteRoot": "/app/src"
                }
            ],
            "justMyCode": false
        }
    ]
}
```

Set breakpoints in:
- `manager.py` line 137 (_process_memory)
- `manager.py` line 161 (add_node call)

## Quick Fixes Commands

```bash
# 1. Clear all data
docker compose -f docker-compose-dev.yml down
sudo rm -rf ./data/neo4j/* ./data/qdrant/* ./data/memos/*
docker compose -f docker-compose-dev.yml up -d

# 2. Watch logs
docker compose -f docker-compose-dev.yml logs -f memos-api | grep -E "ERROR|WARNING|manager.py"

# 3. Restart just the API container after code changes
docker compose -f docker-compose-dev.yml restart memos-api
```
