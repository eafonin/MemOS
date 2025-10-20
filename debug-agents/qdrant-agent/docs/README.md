# Qdrant Debug Agent

Debug utilities for inspecting and managing Qdrant vector database used by MemOS.

## Features

- **Connection Testing**: Verify Qdrant connectivity
- **Collection Management**: List, inspect, and manage collections
- **Data Inspection**: View collection statistics, sample vectors
- **Data Verification**: Check if MemOS embeddings were loaded correctly
- **Data Management**: Delete collections, clear data
- **Vector Search**: Test similarity search functionality

## Installation

### Requirements

```bash
pip install qdrant-client
```

### Environment Variables

The agent reads these environment variables (or you can pass them as CLI arguments):

```bash
# Connection Settings
QDRANT_HOST=localhost
QDRANT_PORT=6334
QDRANT_API_KEY=  # Optional, if authentication enabled
```

## Quick Start

### 1. Test Connection

```bash
python scripts/qdrant_utils.py --test
```

Output:
```
✓ Connected to Qdrant at localhost:6334
✓ Found 2 collection(s)

============================================================
Qdrant Connection Test Results
============================================================
Status:      ✓ Connected
Host:        localhost:6334
Collections: 2

Collections:
  - memos_embeddings
  - test_collection
============================================================
```

### 2. List All Collections

```bash
python scripts/qdrant_utils.py --list
```

Shows all collections in the database.

### 3. View Database Statistics

```bash
python scripts/qdrant_utils.py --stats
```

Shows:
- Total collections
- Vector counts per collection
- Vector dimensions
- Distance metrics

### 4. Get Collection Info

```bash
python scripts/qdrant_utils.py --info memos_embeddings
```

Shows detailed information about a specific collection.

### 5. Inspect Collection Data

```bash
python scripts/qdrant_utils.py --inspect memos_embeddings
```

Shows sample vectors and their payloads.

### 6. Verify MemOS Data

```bash
python scripts/qdrant_utils.py --verify
```

Checks for MemOS-related collections and verifies data.

## Usage Examples

### Get Collection Information

```bash
python scripts/qdrant_utils.py --info memos_embeddings
```

Output:
```
============================================================
Collection Info: memos_embeddings
============================================================
Vectors Count:        1,250
Indexed Vectors:      1,250
Segments:             1
Status:               green
Optimizer Status:     ok
Vector Size:          768
Distance Metric:      Cosine
============================================================
```

### Inspect Collection Contents

```bash
python scripts/qdrant_utils.py --inspect memos_embeddings
```

Shows sample vectors with their metadata.

### Delete Collection

```bash
# WARNING: This deletes the entire collection (REQUIRES --confirm)
python scripts/qdrant_utils.py --delete memos_embeddings --confirm
```

### Delete All Collections

```bash
# WARNING: This deletes ALL collections (REQUIRES --confirm)
python scripts/qdrant_utils.py --delete-all --confirm
```

### Clear Collection (Keep Structure)

```bash
# Clear all vectors but keep collection structure (REQUIRES --confirm)
python scripts/qdrant_utils.py --clear memos_embeddings --confirm
```

## Using as Python Module

```python
from qdrant_utils import QdrantDebugAgent

# Create agent with context manager
with QdrantDebugAgent(
    host="localhost",
    port=6334
) as agent:
    # Test connection
    info = agent.test_connection()
    print(f"Connected to {info['host']}:{info['port']}")

    # Get all statistics
    stats = agent.get_all_stats()
    print(f"Total vectors: {stats['_total_vectors']}")

    # List collections
    collections = agent.list_collections()

    # Get collection info
    col_info = agent.get_collection_info("memos_embeddings")

    # Inspect collection
    samples = agent.inspect_collection("memos_embeddings", limit=5)

    # Verify MemOS data
    verification = agent.verify_memos_data()
```

### Search Similar Vectors

```python
from qdrant_utils import QdrantDebugAgent
import numpy as np

with QdrantDebugAgent() as agent:
    # Create a random query vector (must match collection dimension)
    col_info = agent.get_collection_info("memos_embeddings")
    vector_size = col_info["vector_size"]
    query_vector = np.random.rand(vector_size).tolist()

    # Search
    results = agent.search_similar(
        collection_name="memos_embeddings",
        query_vector=query_vector,
        limit=5
    )

    for result in results:
        print(f"Score: {result['score']}, ID: {result['id']}")
```

## Connection Settings

### Connecting from Host Machine

When connecting from your host machine (outside Docker):

```bash
export QDRANT_HOST=localhost
export QDRANT_PORT=6334
```

### Connecting from Docker Container

When running inside the docker-test1 network:

```bash
export QDRANT_HOST=qdrant
export QDRANT_PORT=6333
```

Note: Port 6333 is the internal container port, 6334 is the external mapped port.

## Troubleshooting

### Connection Refused

```
✗ Connection failed to localhost:6334
```

**Solutions:**
1. Check if Qdrant is running: `docker ps | grep qdrant`
2. Start Qdrant: `cd docker-test1 && docker-compose up -d qdrant`
3. Check port mapping: Port 6334 should map to container port 6333
4. Test with curl: `curl http://localhost:6334/collections`

### Collection Not Found

```
✗ Error getting collection info: Collection 'xyz' not found
```

**Solutions:**
1. List all collections: `python qdrant_utils.py --list`
2. Check collection name spelling
3. Verify data was loaded

### Timeout Errors

```
✗ Connection failed: Timeout
```

**Solutions:**
1. Increase timeout: `QdrantDebugAgent(timeout=60)`
2. Check network connectivity
3. Check Qdrant logs: `docker logs test1-qdrant`

## Common Tasks

### Clean Data for Fresh Test

```bash
# Stop containers
cd /home/memos/Development/MemOS/docker-test1
docker-compose down

# Remove persistent data
rm -rf data/qdrant/*

# Start containers
docker-compose up -d

# Verify empty database
python debug-agents/qdrant-agent/scripts/qdrant_utils.py --stats
```

### Monitor Data Load Progress

```bash
# Watch collection size grow
watch -n 5 'python debug-agents/qdrant-agent/scripts/qdrant_utils.py --stats'
```

### Export Collection Metadata

```python
from qdrant_utils import QdrantDebugAgent
import json

with QdrantDebugAgent() as agent:
    # Get all points
    samples = agent.inspect_collection("memos_embeddings", limit=1000)

    # Save to file
    with open('vectors_metadata.json', 'w') as f:
        json.dump(samples, f, indent=2)
```

### Check Vector Dimensions

```python
from qdrant_utils import QdrantDebugAgent

with QdrantDebugAgent() as agent:
    collections = agent.list_collections()

    for col_name in collections:
        info = agent.get_collection_info(col_name)
        print(f"{col_name}: {info['vector_size']} dimensions")
```

## CLI Reference

```
usage: qdrant_utils.py [-h] [--host HOST] [--port PORT] [--api-key API_KEY]
                       [--test] [--list] [--stats] [--info COLLECTION]
                       [--inspect COLLECTION] [--verify] [--delete COLLECTION]
                       [--delete-all] [--clear COLLECTION] [--confirm]

Qdrant Debug Agent for MemOS

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           Qdrant host (default: localhost)
  --port PORT           Qdrant port (default: 6334)
  --api-key API_KEY     Qdrant API key
  --test                Test connection and show server info
  --list                List all collections
  --stats               Show database statistics
  --info COLLECTION     Get collection info
  --inspect COLLECTION  Inspect collection data
  --verify              Verify MemOS data was loaded
  --delete COLLECTION   Delete collection (requires --confirm)
  --delete-all          Delete all collections (requires --confirm)
  --clear COLLECTION    Clear collection (requires --confirm)
  --confirm             Confirm destructive operations
```

## Safety Features

- Destructive operations require `--confirm` flag
- Connection verification before operations
- Clear error messages and troubleshooting hints
- Safe vector sampling (vectors not shown by default to save space)

## Performance Tips

- Use `--stats` for quick overview
- Use `--inspect` with small limit for large collections
- Collections are indexed automatically by Qdrant
- Check optimizer status for indexing progress

## Related Documentation

- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [MemOS Vector Memory](https://docs.openmem.net/)
- [Troubleshooting Guide](../notes/troubleshooting.md)
