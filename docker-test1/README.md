# MemOS Test Instance 1

**Created:** 2025-10-17
**Purpose:** Fresh MemOS instance for testing data loading with tree-text memory
**Status:** Ready for testing

## Overview

This is a standalone MemOS instance configured with:
- **Memory Type:** Tree-text (hierarchical graph-based)
- **Embeddings:** Local CPU via TEI (sentence-transformers/all-mpnet-base-v2)
- **LLM:** OpenRouter (Claude 3.5 Sonnet)
- **Databases:** Neo4j 5.14.0 + Qdrant v1.7.4

## Quick Start

```bash
# Start the instance
./manage.sh start

# Check status
./manage.sh status

# View logs
./manage.sh logs

# Test API
./manage.sh test-api
```

## Architecture

```
┌─────────────────┐
│  MemOS API      │  Port: 8001
│  (test1-memos)  │  http://localhost:8001
└────────┬────────┘
         │
    ┌────┴──────────┬──────────────┬──────────────┐
    │               │              │              │
┌───▼────┐    ┌────▼─────┐   ┌───▼──────┐   ┌──▼──────┐
│ Neo4j  │    │  Qdrant  │   │   TEI    │   │ OpenRT  │
│  :7688 │    │   :6334  │   │   :8081  │   │ (cloud) │
└────────┘    └──────────┘   └──────────┘   └─────────┘
 Graph DB      Vector DB      Embeddings      LLM API
```

## Services

| Service | Port | URL | Credentials |
|---------|------|-----|-------------|
| MemOS API | 8001 | http://localhost:8001/docs | - |
| Neo4j Browser | 7475 | http://localhost:7475 | neo4j / memospassword123 |
| Qdrant API | 6334 | http://localhost:6334/dashboard | - |
| TEI | 8081 | http://localhost:8081/health | - |

## Configuration

### Memory Configuration
- **Type:** `tree_text` - Hierarchical memory with graph structure
- **Embedding Model:** sentence-transformers/all-mpnet-base-v2 (768 dim)
- **Reranker:** cosine_local
- **Top-K:** 50 memories per retrieval
- **Max Turns:** 10 conversation turns in context

### Key Differences from docker-dev
1. **Fresh databases** - Clean Neo4j and Qdrant instances
2. **Clear naming** - All containers prefixed with `test1-`
3. **Different ports** - API on 8001, Neo4j on 7688/7475
4. **Isolated network** - `test1_network`
5. **Better health checks** - All services have health monitoring

## Data Loading

### Using simple_loader.py

```bash
# From memos-data-loader directory
python src/simple_loader.py \
  --file test-samples/sample-ssh-scan.txt \
  --api-url http://localhost:8001/api/openmem/v1 \
  --user-id test1_user
```

### Using Product API directly

```bash
# Register user
curl -X POST http://localhost:8001/product/users/register \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test1_user"}'

# Add memory
curl -X POST http://localhost:8001/product/add \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test1_user",
    "mem_cube_id": "YOUR_CUBE_ID",
    "messages": [
      {"role": "user", "content": "SSH scan result: Port 22 open on 192.168.1.1"}
    ]
  }'

# Search memory
curl -X POST http://localhost:8001/product/search \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test1_user",
    "mem_cube_id": "YOUR_CUBE_ID",
    "query": "SSH"
  }'
```

## Management Commands

```bash
# Lifecycle
./manage.sh start      # Start all services
./manage.sh stop       # Stop services (preserve data)
./manage.sh restart    # Restart services
./manage.sh down       # Remove containers (preserve data)
./manage.sh clean      # DESTRUCTIVE: Remove all data

# Monitoring
./manage.sh status     # Show service status
./manage.sh logs       # Follow memos-api logs
./manage.sh logs neo4j # Follow specific service logs

# Debugging
./manage.sh shell           # Shell in memos-api
./manage.sh shell neo4j     # Shell in neo4j
./manage.sh test-api        # Test API endpoints

# Maintenance
./manage.sh rebuild    # Rebuild memos-api image
```

## Directory Structure

```
docker-test1/
├── manage.sh              # Management script
├── docker-compose.yml     # Service definitions
├── .env                   # Environment config
├── requirements.txt       # Python dependencies
├── constraints.txt        # Pip constraints
├── README.md             # This file
├── data/                 # Persistent data
│   ├── neo4j/           # Graph database
│   ├── qdrant/          # Vector database
│   ├── memos/           # MemOS data
│   └── hf-cache/        # HuggingFace cache
└── logs/                # Application logs
```

## Troubleshooting

### Services won't start
```bash
# Check logs
./manage.sh logs

# Check individual service
docker-compose logs tei
docker-compose logs neo4j
```

### API not responding
```bash
# Check health
curl http://localhost:8001/health

# Check logs
./manage.sh logs memos-api
```

### Embeddings not working
```bash
# Test TEI directly
curl http://localhost:8081/health

# Check if model is loaded
docker-compose logs tei | grep -i "model"
```

### Neo4j authentication issues
```bash
# Reset Neo4j
./manage.sh down
rm -rf data/neo4j
./manage.sh start
```

### Clean slate
```bash
# Nuclear option - removes everything
./manage.sh clean
./manage.sh start
```

## Environment Variables

See `.env` file for all configuration options. Key variables:

- `MOS_TEXT_MEM_TYPE=tree_text` - Memory architecture
- `EMBEDDING_DIMENSION=768` - Must match TEI model
- `NEO4J_PASSWORD=memospassword123` - Database password
- `OPENAI_API_KEY` - OpenRouter API key
- `MOS_TOP_K=50` - Number of memories to retrieve

## Creating New Instances

To create docker-test2, docker-test3, etc:

```bash
# Copy this directory
cp -r docker-test1 docker-test2

# Edit docker-test2/.env and docker-compose.yml:
# 1. Change all "test1" to "test2"
# 2. Change ports (8001 -> 8002, 7688 -> 7689, etc)
# 3. Update user_id and session_id
# 4. Clean data directory

cd docker-test2
./manage.sh clean  # Remove data
./manage.sh start
```

## Next Steps

1. Start the instance: `./manage.sh start`
2. Verify health: `./manage.sh test-api`
3. Test data loading with simple_loader.py
4. Check Neo4j browser to see graph structure
5. Query memories via search endpoint
6. Monitor logs for errors

## Support

- MemOS Docs: https://memos-docs.openmem.net/
- GitHub: https://github.com/MemTensor/MemOS
- Local docs: `../memos-data-loader/docs/processed/`
