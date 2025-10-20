# Neo4j Connection Information

## Docker-Test1 Setup

### Container Details
- **Container Name**: test1-neo4j
- **Image**: neo4j:5.14.0
- **Network**: test1_network

### Ports
- **HTTP (Browser)**: 7475:7474
  - External: http://localhost:7475
  - Internal: http://neo4j:7474
- **Bolt (Driver)**: 7688:7687
  - External: bolt://localhost:7688
  - Internal: bolt://neo4j:7687

### Credentials
- **Username**: neo4j
- **Password**: memospassword123
- **Default Database**: test1_memos_db

### Persistent Storage
- Data: `./data/neo4j/data`
- Logs: `./data/neo4j/logs`

## Connection Patterns

### From Host Machine
```python
from neo4j import GraphDatabase

driver = GraphDatabase.driver(
    "bolt://localhost:7688",
    auth=("neo4j", "memospassword123")
)
```

### From Docker Container (in test1_network)
```python
from neo4j import GraphDatabase

driver = GraphDatabase.driver(
    "bolt://neo4j:7687",
    auth=("neo4j", "memospassword123")
)
```

### From MemOS API Container
The MemOS API reads from environment variables in .env file:
- NEO4J_URI=bolt://neo4j:7687
- NEO4J_USER=neo4j
- NEO4J_PASSWORD=memospassword123
- NEO4J_DB_NAME=test1_memos_db

## Memory Configuration

From docker-compose.yml:
- Initial heap: 512m
- Max heap: 2G
- Page cache: 512m

## Accessing Neo4j Browser

Open in your browser:
```
http://localhost:7475
```

Login with:
- Username: neo4j
- Password: memospassword123
- Database: test1_memos_db

## Common Issues

### Can't Connect from Host
1. Check container is running: `docker ps | grep neo4j`
2. Check port is mapped: `docker port test1-neo4j`
3. Try: `telnet localhost 7688`

### Can't Connect from Container
1. Check network: `docker network inspect test1_network`
2. Try: `docker exec test1-memos-api ping neo4j`
3. Check DNS: Use service name `neo4j` not `localhost`

### Database Not Found
- Use default: `neo4j` database
- Or create in Browser: `CREATE DATABASE test1_memos_db`
