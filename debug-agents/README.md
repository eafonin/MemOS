# MemOS Debug Agents

Debug utilities for inspecting and managing data in the MemOS docker-test1 environment.

## Overview

This directory contains two specialized debug agents:

1. **Neo4j Agent** - For graph database debugging
2. **Qdrant Agent** - For vector database debugging

Both agents provide CLI and Python API interfaces for:
- Testing connections
- Inspecting data structure
- Verifying data was loaded correctly
- Cleaning/resetting test data
- Troubleshooting issues

## Quick Start

### Prerequisites

**IMPORTANT**: Python 3.11+ uses PEP 668 and requires virtual environments. Each agent has its own isolated venv.

**First Time Setup** (one-time):

```bash
# Setup Neo4j agent
cd /home/memos/Development/MemOS/debug-agents/neo4j-agent
./setup.sh

# Setup Qdrant agent
cd /home/memos/Development/MemOS/debug-agents/qdrant-agent
./setup.sh
```

See [VENV_GUIDE.md](VENV_GUIDE.md) for detailed virtual environment documentation.

### Test All Connections

**Option 1: Using run.sh wrapper (Recommended)**

```bash
# From project root
cd /home/memos/Development/MemOS

# Test Neo4j
cd debug-agents/neo4j-agent
./run.sh --test

# Test Qdrant
cd debug-agents/qdrant-agent
./run.sh --test
```

**Option 2: Manual venv activation**

```bash
# From project root
cd /home/memos/Development/MemOS

# Test Neo4j
cd debug-agents/neo4j-agent
source venv/bin/activate
python scripts/neo4j_utils.py --test
deactivate

# Test Qdrant
cd debug-agents/qdrant-agent
source venv/bin/activate
python scripts/qdrant_utils.py --test
deactivate
```

### Verify Data Loading

```bash
# From project root
cd /home/memos/Development/MemOS

# Check Neo4j data
cd debug-agents/neo4j-agent
./run.sh --verify

# Check Qdrant data
cd debug-agents/qdrant-agent
./run.sh --verify
```

## Directory Structure

```
debug-agents/
├── README.md                      # This file
├── VENV_GUIDE.md                  # Virtual environment guide (IMPORTANT!)
├── VERSION_COMPATIBILITY.md       # Client/server version compatibility report
├── neo4j-agent/                   # Neo4j debug utilities
│   ├── venv/                      # Virtual environment (gitignored)
│   ├── requirements.txt           # Python dependencies
│   ├── setup.sh                   # Setup script (creates venv)
│   ├── run.sh                     # Run script (auto-activates venv)
│   ├── config.env                 # Connection configuration
│   ├── scripts/
│   │   └── neo4j_utils.py         # Main utility script
│   ├── docs/
│   │   └── README.md              # Neo4j agent documentation
│   └── notes/                     # Developer notes
└── qdrant-agent/                  # Qdrant debug utilities
    ├── venv/                      # Virtual environment (gitignored)
    ├── requirements.txt           # Python dependencies
    ├── setup.sh                   # Setup script (creates venv)
    ├── run.sh                     # Run script (auto-activates venv)
    ├── config.env                 # Connection configuration
    ├── scripts/
    │   └── qdrant_utils.py        # Main utility script
    ├── docs/
    │   └── README.md              # Qdrant agent documentation
    └── notes/                     # Developer notes
```

## Common Workflows

### 1. Debugging Data Loading Issues

```bash
# Step 1: Check if services are running
cd /home/memos/Development/MemOS/docker-test1
docker-compose ps

# Step 2: Test connections
cd /home/memos/Development/MemOS/debug-agents/neo4j-agent
./run.sh --test
cd /home/memos/Development/MemOS/debug-agents/qdrant-agent
./run.sh --test

# Step 3: Check data statistics
cd /home/memos/Development/MemOS/debug-agents/neo4j-agent
./run.sh --stats
cd /home/memos/Development/MemOS/debug-agents/qdrant-agent
./run.sh --stats

# Step 4: Verify MemOS data structure
cd /home/memos/Development/MemOS/debug-agents/neo4j-agent
./run.sh --verify
cd /home/memos/Development/MemOS/debug-agents/qdrant-agent
./run.sh --verify

# Step 5: Inspect sample data
cd /home/memos/Development/MemOS/debug-agents/neo4j-agent
./run.sh --inspect
cd /home/memos/Development/MemOS/debug-agents/qdrant-agent
./run.sh --inspect
```

### 2. Clean Data for Fresh Test

```bash
# WARNING: This deletes all data!

# Option A: Stop containers and remove persistent data
cd /home/memos/Development/MemOS/docker-test1
docker-compose down
rm -rf data/neo4j/data/* data/neo4j/logs/*
rm -rf data/qdrant/*
docker-compose up -d

# Option B: Use debug agents to clean data
cd /home/memos/Development/MemOS/debug-agents/neo4j-agent
./run.sh --delete-all --confirm
cd /home/memos/Development/MemOS/debug-agents/qdrant-agent
./run.sh --delete-all --confirm
```

### 3. Monitor Data Loading Progress

```bash
# Terminal 1: Monitor Neo4j
cd /home/memos/Development/MemOS/debug-agents/neo4j-agent
watch -n 5 './run.sh --stats'

# Terminal 2: Monitor Qdrant
cd /home/memos/Development/MemOS/debug-agents/qdrant-agent
watch -n 5 './run.sh --stats'

# Terminal 3: Run your data loader
cd /home/memos/Development/MemOS/memos-data-loader
python src/load_data.py
```

### 4. Troubleshoot Connection Issues

```bash
# Check if containers are running
docker ps | grep -E "neo4j|qdrant"

# Check container logs
docker logs test1-neo4j --tail 50
docker logs test1-qdrant --tail 50

# Check network connectivity
docker network inspect test1_network

# Test from inside container
docker exec -it test1-memos-api bash
# Then run agents from inside container (remember to change connection settings!)
```

## Connection Settings

### From Host Machine (Recommended)

Use the external ports mapped in docker-compose.yml:

- **Neo4j**: `bolt://localhost:7688`
- **Qdrant**: `http://localhost:6334`

### From Docker Container

Use the internal service names:

- **Neo4j**: `bolt://neo4j:7687`
- **Qdrant**: `http://qdrant:6333`

## Python API Examples

### Neo4j Agent

```python
from neo4j_agent.scripts.neo4j_utils import Neo4jDebugAgent

with Neo4jDebugAgent() as agent:
    # Test connection
    agent.test_connection()

    # Get statistics
    stats = agent.get_database_stats()
    print(f"Total nodes: {stats['total_nodes']}")

    # Verify MemOS data
    agent.verify_memos_data()

    # Custom query
    results = agent.query("""
        MATCH (d:Document)-[r]->(c:Chunk)
        RETURN d.title, count(c) as chunk_count
        ORDER BY chunk_count DESC
        LIMIT 10
    """)
```

### Qdrant Agent

```python
from qdrant_agent.scripts.qdrant_utils import QdrantDebugAgent

with QdrantDebugAgent() as agent:
    # Test connection
    agent.test_connection()

    # Get all statistics
    stats = agent.get_all_stats()
    print(f"Total vectors: {stats['_total_vectors']}")

    # Verify MemOS data
    agent.verify_memos_data()

    # Inspect collection
    samples = agent.inspect_collection("memos_embeddings", limit=5)
```

## Troubleshooting

### Neo4j Connection Issues

```bash
# Check if Neo4j is running
docker ps | grep neo4j

# View Neo4j logs
docker logs test1-neo4j --tail 100

# Restart Neo4j
docker-compose restart neo4j

# Check health
docker exec test1-neo4j wget -qO- http://localhost:7474
```

### Qdrant Connection Issues

```bash
# Check if Qdrant is running
docker ps | grep qdrant

# View Qdrant logs
docker logs test1-qdrant --tail 100

# Restart Qdrant
docker-compose restart qdrant

# Check health
curl http://localhost:6334/collections
```

### Port Conflicts

If ports are already in use:

```bash
# Check what's using the ports
lsof -i :7688  # Neo4j
lsof -i :6334  # Qdrant

# Either stop the conflicting service or change ports in docker-compose.yml
```

## Safety Notes

⚠️ **Important Safety Information**

1. **Destructive Operations**: All delete operations require the `--confirm` flag
2. **Data Backup**: Always backup important data before cleaning/deleting
3. **Test Environment**: These agents are designed for the test1 environment
4. **Credentials**: Never commit real credentials to version control

## Best Practices

1. **Use Environment Variables**: Source config.env files before running scripts
2. **Verify Before Delete**: Always run `--verify` or `--stats` before delete operations
3. **Monitor Progress**: Use `watch` command to monitor data loading in real-time
4. **Check Logs**: When issues occur, always check Docker logs first
5. **Isolate Tests**: Use separate databases/collections for different tests

## Common Cypher Queries (Neo4j)

```cypher
# Count nodes by label
MATCH (n)
RETURN labels(n) as label, count(n) as count
ORDER BY count DESC

# Find documents with most chunks
MATCH (d:Document)-[:HAS_CHUNK]->(c:Chunk)
RETURN d.title, count(c) as chunks
ORDER BY chunks DESC
LIMIT 10

# Check relationships
MATCH ()-[r]->()
RETURN type(r), count(r)
ORDER BY count(r) DESC

# Find orphaned nodes
MATCH (n)
WHERE NOT (n)--()
RETURN labels(n), count(n)
```

## Useful Qdrant Queries

```python
# List all collections
agent.list_collections()

# Get collection info
agent.get_collection_info("memos_embeddings")

# Count vectors
stats = agent.get_all_stats()
print(stats["_total_vectors"])

# Inspect payloads
samples = agent.inspect_collection("memos_embeddings", limit=10)
for sample in samples:
    print(sample["payload"])
```

## Contributing

When adding new debug utilities:

1. Place Python scripts in the `scripts/` directory
2. Document usage in the respective `docs/README.md`
3. Add examples to this main README
4. Update config.env if new environment variables are needed
5. Add notes/findings to the `notes/` directory

## Related Documentation

- **[VENV_GUIDE.md](VENV_GUIDE.md)** - Complete virtual environment setup guide (READ THIS FIRST!)
- **[VERSION_COMPATIBILITY.md](VERSION_COMPATIBILITY.md)** - Client/server version compatibility report
- [Neo4j Agent Documentation](neo4j-agent/docs/README.md)
- [Qdrant Agent Documentation](qdrant-agent/docs/README.md)
- [MemOS Documentation](https://docs.openmem.net/)
- [Docker Test1 Setup](../docker-test1/README.md)

## Support

For issues or questions:

1. Check the troubleshooting sections in agent-specific READMEs
2. Review Docker logs for the relevant services
3. Check MemOS documentation at https://docs.openmem.net/
4. Review notes in the `notes/` directories
