# Qdrant Connection Information

## Docker-Test1 Setup

### Container Details
- **Container Name**: test1-qdrant
- **Image**: qdrant/qdrant:v1.7.4
- **Network**: test1_network

### Ports
- **HTTP (REST API)**: 6334:6333
  - External: http://localhost:6334
  - Internal: http://qdrant:6333
- **gRPC**: 6335:6334
  - External: localhost:6335
  - Internal: qdrant:6334

### Persistent Storage
- Data: `./data/qdrant`

### Authentication
- **Default**: No authentication (open access)
- **API Key**: Not configured in docker-test1

## Connection Patterns

### From Host Machine (Python)
```python
from qdrant_client import QdrantClient

client = QdrantClient(
    host="localhost",
    port=6334
)
```

### From Host Machine (HTTP)
```bash
# List collections
curl http://localhost:6334/collections

# Get collection info
curl http://localhost:6334/collections/memos_embeddings

# Health check
curl http://localhost:6334/health
```

### From Docker Container (in test1_network)
```python
from qdrant_client import QdrantClient

client = QdrantClient(
    host="qdrant",
    port=6333  # Internal port
)
```

### From MemOS API Container
The MemOS API reads from environment variables in .env file:
- QDRANT_HOST=qdrant
- QDRANT_PORT=6333

## Accessing Web UI

Qdrant provides a web dashboard at:
```
http://localhost:6334/dashboard
```

Features:
- Browse collections
- View metrics
- Inspect vectors
- Run searches

## Common Issues

### Can't Connect from Host
1. Check container is running: `docker ps | grep qdrant`
2. Check port is mapped: `docker port test1-qdrant`
3. Test HTTP: `curl http://localhost:6334/collections`

### Can't Connect from Container
1. Check network: `docker network inspect test1_network`
2. Try: `docker exec test1-memos-api ping qdrant`
3. Use service name `qdrant` not `localhost`
4. Use internal port 6333 not 6334

### Collection Not Found
1. List collections: `curl http://localhost:6334/collections`
2. Check collection was created
3. Check MemOS data loader logs

### Performance Issues
1. Check optimizer status in collection info
2. Indexing happens automatically
3. Wait for `optimizer_status: "ok"`
4. Check disk space in persistent volume

## REST API Examples

### List Collections
```bash
curl http://localhost:6334/collections
```

### Get Collection Info
```bash
curl http://localhost:6334/collections/memos_embeddings
```

### Count Vectors
```bash
curl http://localhost:6334/collections/memos_embeddings/points/count
```

### Scroll (List Vectors)
```bash
curl -X POST http://localhost:6334/collections/memos_embeddings/points/scroll \
  -H 'Content-Type: application/json' \
  -d '{"limit": 10, "with_payload": true, "with_vector": false}'
```

### Search
```bash
curl -X POST http://localhost:6334/collections/memos_embeddings/points/search \
  -H 'Content-Type: application/json' \
  -d '{
    "vector": [0.1, 0.2, 0.3, ...],
    "limit": 5
  }'
```
