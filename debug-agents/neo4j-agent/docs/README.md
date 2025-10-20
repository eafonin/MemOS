# Neo4j Debug Agent

Debug utilities for inspecting and managing Neo4j graph database used by MemOS.

## Features

- **Connection Testing**: Verify Neo4j connectivity and authentication
- **Data Inspection**: View database statistics, node/relationship counts
- **Data Verification**: Check if MemOS data was loaded correctly
- **Data Management**: Delete test data, clear databases
- **Custom Queries**: Execute Cypher queries for debugging

## Installation

### Requirements

```bash
pip install neo4j
```

### Environment Variables

The agent reads these environment variables (or you can pass them as CLI arguments):

```bash
# Connection Settings
NEO4J_URI=bolt://localhost:7688
NEO4J_USER=neo4j
NEO4J_PASSWORD=memospassword123
NEO4J_DB_NAME=test1_memos_db
```

## Quick Start

### 1. Test Connection

```bash
python scripts/neo4j_utils.py --test
```

Output:
```
✓ Connected to Neo4j at bolt://localhost:7688
✓ Database: test1_memos_db

============================================================
Neo4j Connection Test Results
============================================================
Status:     ✓ Connected
URI:        bolt://localhost:7688
Database:   test1_memos_db
Name:       Neo4j
Version:    5.14.0
Edition:    enterprise
============================================================
```

### 2. View Database Statistics

```bash
python scripts/neo4j_utils.py --stats
```

Shows:
- Node counts by label
- Relationship counts by type
- Total nodes and relationships

### 3. Inspect Data Structure

```bash
python scripts/neo4j_utils.py --inspect
```

Shows:
- All node labels in the database
- Sample nodes for each label
- Node properties and values

### 4. Verify MemOS Data

```bash
python scripts/neo4j_utils.py --verify
```

Checks for:
- MemoryNode nodes
- Chunk nodes
- Document nodes
- Relationships between them

## Usage Examples

### Custom Cypher Query

```bash
# Count all nodes
python scripts/neo4j_utils.py --query "MATCH (n) RETURN count(n) as total"

# Find recent documents
python scripts/neo4j_utils.py --query "MATCH (d:Document) RETURN d.title, d.created_at ORDER BY d.created_at DESC LIMIT 10"

# Check relationships
python scripts/neo4j_utils.py --query "MATCH ()-[r]->() RETURN type(r), count(r) ORDER BY count(r) DESC"
```

### Delete User Data

```bash
# Delete data for specific user (REQUIRES --confirm)
python scripts/neo4j_utils.py --delete-user test1_user --confirm
```

### Delete All Data

```bash
# WARNING: This deletes EVERYTHING (REQUIRES --confirm)
python scripts/neo4j_utils.py --delete-all --confirm
```

## Using as Python Module

```python
from neo4j_utils import Neo4jDebugAgent

# Create agent with context manager
with Neo4jDebugAgent(
    uri="bolt://localhost:7688",
    user="neo4j",
    password="memospassword123",
    database="test1_memos_db"
) as agent:
    # Test connection
    info = agent.test_connection()
    print(f"Connected to Neo4j {info['versions'][0]}")

    # Get statistics
    stats = agent.get_database_stats()
    print(f"Total nodes: {stats['total_nodes']}")
    print(f"Total relationships: {stats['total_relationships']}")

    # Verify MemOS data
    verification = agent.verify_memos_data()

    # Custom query
    results = agent.query("MATCH (n:Document) RETURN n LIMIT 5")

    # Inspect data structure
    samples = agent.inspect_data_structure(limit=3)
```

## Connection Settings

### Connecting from Host Machine

When connecting from your host machine (outside Docker):

```bash
export NEO4J_URI=bolt://localhost:7688
export NEO4J_USER=neo4j
export NEO4J_PASSWORD=memospassword123
export NEO4J_DB_NAME=test1_memos_db
```

### Connecting from Docker Container

When running inside the docker-test1 network:

```bash
export NEO4J_URI=bolt://neo4j:7687
export NEO4J_USER=neo4j
export NEO4J_PASSWORD=memospassword123
export NEO4J_DB_NAME=test1_memos_db
```

## Troubleshooting

### Connection Refused

```
✗ Connection failed: Neo4j service unavailable at bolt://localhost:7688
```

**Solutions:**
1. Check if Neo4j is running: `docker ps | grep neo4j`
2. Start Neo4j: `cd docker-test1 && docker-compose up -d neo4j`
3. Check port mapping: Port 7688 should map to container port 7687

### Authentication Failed

```
✗ Authentication failed: Invalid credentials
```

**Solutions:**
1. Verify credentials in docker-compose.yml
2. Check environment variable: `NEO4J_AUTH: "neo4j/memospassword123"`
3. Reset password if needed

### Database Not Found

```
✗ Database 'test1_memos_db' not found
```

**Solutions:**
1. Use default database: `--database neo4j`
2. Create database in Neo4j Browser
3. Check .env file for correct database name

## Common Tasks

### Clean Data for Fresh Test

```bash
# Stop containers
cd /home/memos/Development/MemOS/docker-test1
docker-compose down

# Remove persistent data
rm -rf data/neo4j/data/*
rm -rf data/neo4j/logs/*

# Start containers
docker-compose up -d

# Verify empty database
python debug-agents/neo4j-agent/scripts/neo4j_utils.py --stats
```

### Check Data Load Progress

```bash
# Monitor node counts
watch -n 5 'python debug-agents/neo4j-agent/scripts/neo4j_utils.py --stats'
```

### Export Sample Data

```python
from neo4j_utils import Neo4jDebugAgent
import json

with Neo4jDebugAgent() as agent:
    # Get all documents
    results = agent.query("MATCH (d:Document) RETURN d")

    # Save to file
    with open('documents.json', 'w') as f:
        json.dump(results, f, indent=2)
```

## CLI Reference

```
usage: neo4j_utils.py [-h] [--uri URI] [--user USER] [--password PASSWORD]
                      [--database DATABASE] [--test] [--stats] [--inspect]
                      [--verify] [--query QUERY] [--delete-all]
                      [--delete-user DELETE_USER] [--confirm]

Neo4j Debug Agent for MemOS

optional arguments:
  -h, --help            show this help message and exit
  --uri URI             Neo4j URI (default: bolt://localhost:7688)
  --user USER           Neo4j username
  --password PASSWORD   Neo4j password
  --database DATABASE   Database name
  --test                Test connection and show server info
  --stats               Show database statistics
  --inspect             Inspect data structure
  --verify              Verify MemOS data was loaded
  --query QUERY         Execute custom Cypher query
  --delete-all          Delete all data (requires --confirm)
  --delete-user DELETE_USER
                        Delete data for specific user (requires --confirm)
  --confirm             Confirm destructive operations
```

## Safety Features

- Destructive operations require `--confirm` flag
- Batch deletion to prevent memory issues
- Connection verification before operations
- Clear error messages and troubleshooting hints

## Related Documentation

- [Neo4j Cypher Manual](https://neo4j.com/docs/cypher-manual/)
- [MemOS Graph Memory](https://docs.openmem.net/modules/memories/neo4j_graph_db)
- [Troubleshooting Guide](../notes/troubleshooting.md)
