#!/bin/bash
# Quick test script for both debug agents

set -e

echo "============================================================"
echo "MemOS Debug Agents - Quick Test"
echo "============================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    exit 1
fi

# Check if required packages are installed
echo "Checking required packages..."
python3 -c "import neo4j" 2>/dev/null || {
    echo -e "${YELLOW}Warning: neo4j package not installed${NC}"
    echo "Install with: pip install neo4j"
    NEO4J_AVAILABLE=0
}

python3 -c "import qdrant_client" 2>/dev/null || {
    echo -e "${YELLOW}Warning: qdrant-client package not installed${NC}"
    echo "Install with: pip install qdrant-client"
    QDRANT_AVAILABLE=0
}

echo ""

# Get the directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Test Neo4j
if [ "${NEO4J_AVAILABLE}" != "0" ]; then
    echo "============================================================"
    echo "Testing Neo4j Connection"
    echo "============================================================"
    echo ""

    # Source config
    source "$DIR/neo4j-agent/config.env"

    # Run test
    if python3 "$DIR/neo4j-agent/scripts/neo4j_utils.py" --test; then
        echo -e "${GREEN}✓ Neo4j connection successful${NC}"
    else
        echo -e "${RED}✗ Neo4j connection failed${NC}"
        echo "Troubleshooting:"
        echo "  1. Check if container is running: docker ps | grep neo4j"
        echo "  2. Start container: cd /home/memos/Development/MemOS/docker-test1 && docker-compose up -d neo4j"
        echo "  3. Check logs: docker logs test1-neo4j"
    fi

    echo ""

    # Get stats
    echo "Getting Neo4j statistics..."
    python3 "$DIR/neo4j-agent/scripts/neo4j_utils.py" --stats || true

    echo ""
fi

# Test Qdrant
if [ "${QDRANT_AVAILABLE}" != "0" ]; then
    echo "============================================================"
    echo "Testing Qdrant Connection"
    echo "============================================================"
    echo ""

    # Source config
    source "$DIR/qdrant-agent/config.env"

    # Run test
    if python3 "$DIR/qdrant-agent/scripts/qdrant_utils.py" --test; then
        echo -e "${GREEN}✓ Qdrant connection successful${NC}"
    else
        echo -e "${RED}✗ Qdrant connection failed${NC}"
        echo "Troubleshooting:"
        echo "  1. Check if container is running: docker ps | grep qdrant"
        echo "  2. Start container: cd /home/memos/Development/MemOS/docker-test1 && docker-compose up -d qdrant"
        echo "  3. Check logs: docker logs test1-qdrant"
        echo "  4. Test HTTP: curl http://localhost:6334/collections"
    fi

    echo ""

    # Get stats
    echo "Getting Qdrant statistics..."
    python3 "$DIR/qdrant-agent/scripts/qdrant_utils.py" --stats || true

    echo ""
fi

echo "============================================================"
echo "Quick test completed!"
echo "============================================================"
echo ""
echo "Next steps:"
echo "  - Verify data: python3 neo4j-agent/scripts/neo4j_utils.py --verify"
echo "  - Inspect data: python3 neo4j-agent/scripts/neo4j_utils.py --inspect"
echo "  - List collections: python3 qdrant-agent/scripts/qdrant_utils.py --list"
echo "  - Read documentation: cat README.md"
echo ""
