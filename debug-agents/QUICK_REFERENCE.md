# Debug Agents - Quick Reference

## Installation

```bash
cd /home/memos/Development/MemOS/debug-agents
pip install -r requirements.txt
```

## Quick Test (Both Agents)

```bash
cd /home/memos/Development/MemOS/debug-agents
./quick-test.sh
```

## Neo4j Agent - Common Commands

```bash
# From project root
cd /home/memos/Development/MemOS

# Source configuration
source debug-agents/neo4j-agent/config.env

# Test connection
python3 debug-agents/neo4j-agent/scripts/neo4j_utils.py --test

# Show statistics
python3 debug-agents/neo4j-agent/scripts/neo4j_utils.py --stats

# Verify MemOS data
python3 debug-agents/neo4j-agent/scripts/neo4j_utils.py --verify

# Inspect data structure
python3 debug-agents/neo4j-agent/scripts/neo4j_utils.py --inspect

# Custom query
python3 debug-agents/neo4j-agent/scripts/neo4j_utils.py --query "MATCH (n) RETURN count(n)"

# Delete all data (DANGEROUS!)
python3 debug-agents/neo4j-agent/scripts/neo4j_utils.py --delete-all --confirm
```

## Qdrant Agent - Common Commands

```bash
# From project root
cd /home/memos/Development/MemOS

# Source configuration
source debug-agents/qdrant-agent/config.env

# Test connection
python3 debug-agents/qdrant-agent/scripts/qdrant_utils.py --test

# List collections
python3 debug-agents/qdrant-agent/scripts/qdrant_utils.py --list

# Show statistics
python3 debug-agents/qdrant-agent/scripts/qdrant_utils.py --stats

# Verify MemOS data
python3 debug-agents/qdrant-agent/scripts/qdrant_utils.py --verify

# Get collection info
python3 debug-agents/qdrant-agent/scripts/qdrant_utils.py --info memos_embeddings

# Inspect collection
python3 debug-agents/qdrant-agent/scripts/qdrant_utils.py --inspect memos_embeddings

# Delete collection (DANGEROUS!)
python3 debug-agents/qdrant-agent/scripts/qdrant_utils.py --delete memos_embeddings --confirm
```

## Python Usage

### Neo4j
```python
from neo4j_agent.scripts.neo4j_utils import Neo4jDebugAgent

with Neo4jDebugAgent() as agent:
    agent.test_connection()
    agent.get_database_stats()
    agent.verify_memos_data()
```

### Qdrant
```python
from qdrant_agent.scripts.qdrant_utils import QdrantDebugAgent

with QdrantDebugAgent() as agent:
    agent.test_connection()
    agent.get_all_stats()
    agent.verify_memos_data()
```

## Connection Info

### Neo4j
- **URL**: bolt://localhost:7688
- **User**: neo4j
- **Password**: memospassword123
- **Database**: test1_memos_db
- **Browser**: http://localhost:7475

### Qdrant
- **URL**: http://localhost:6334
- **Dashboard**: http://localhost:6334/dashboard
- **No Auth**: Open access

## Clean Data (Start Fresh)

```bash
# Stop containers
cd /home/memos/Development/MemOS/docker-test1
docker-compose down

# Remove persistent data
rm -rf data/neo4j/data/* data/neo4j/logs/*
rm -rf data/qdrant/*

# Start containers
docker-compose up -d

# Verify empty
cd /home/memos/Development/MemOS
python3 debug-agents/neo4j-agent/scripts/neo4j_utils.py --stats
python3 debug-agents/qdrant-agent/scripts/qdrant_utils.py --stats
```

## Troubleshooting

### Check Services
```bash
docker ps | grep -E "neo4j|qdrant"
```

### View Logs
```bash
docker logs test1-neo4j --tail 50
docker logs test1-qdrant --tail 50
```

### Restart Services
```bash
docker-compose restart neo4j
docker-compose restart qdrant
```

### Test HTTP
```bash
# Qdrant
curl http://localhost:6334/collections

# Neo4j
curl http://localhost:7475
```

## Documentation

- **Main README**: [README.md](README.md)
- **Neo4j Agent**: [neo4j-agent/docs/README.md](neo4j-agent/docs/README.md)
- **Qdrant Agent**: [qdrant-agent/docs/README.md](qdrant-agent/docs/README.md)
