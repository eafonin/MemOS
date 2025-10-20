#!/bin/bash
# APPLY.sh - Apply Neo4j Complex Object Serialization Fix
# Usage: bash patches/neo4j-complex-object-serialization/APPLY.sh

set -e  # Exit on error

echo "========================================================================"
echo "  Neo4j Complex Object Serialization Fix - Patch Application"
echo "========================================================================"
echo ""

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PATCH_FILE="$SCRIPT_DIR/0001-fix-neo4j-complex-object-serialization.patch"

# Navigate to repo root
cd "$SCRIPT_DIR/../.."

echo "📍 Current directory: $(pwd)"
echo "📦 Patch file: $PATCH_FILE"
echo ""

# Check if patch file exists
if [ ! -f "$PATCH_FILE" ]; then
    echo "❌ Error: Patch file not found at $PATCH_FILE"
    exit 1
fi

echo "🔍 Checking if patch can be applied..."
if git apply --check "$PATCH_FILE" 2>/dev/null; then
    echo "✅ Patch can be applied cleanly"
else
    echo "⚠️  Warning: Patch may not apply cleanly. Checking details..."
    git apply --check "$PATCH_FILE" 2>&1 || true
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Aborted"
        exit 1
    fi
fi

echo ""
echo "📝 Applying patch..."
if git apply "$PATCH_FILE"; then
    echo "✅ Patch applied successfully!"
else
    echo "❌ Failed to apply patch"
    echo ""
    echo "Troubleshooting:"
    echo "  1. Check if file has been modified: git status src/memos/graph_dbs/neo4j_community.py"
    echo "  2. Stash changes: git stash"
    echo "  3. Try again: git apply $PATCH_FILE"
    echo "  4. Restore changes: git stash pop"
    exit 1
fi

echo ""
echo "🔍 Verifying changes..."
if grep -q "_serialize_complex_metadata" src/memos/graph_dbs/neo4j_community.py; then
    echo "✅ Function _serialize_complex_metadata() found"
else
    echo "❌ Verification failed: Function not found"
    exit 1
fi

if grep -q "neo4j_metadata = _serialize_complex_metadata(metadata)" src/memos/graph_dbs/neo4j_community.py; then
    echo "✅ Serialization call found in add_node()"
else
    echo "❌ Verification failed: Serialization call not found"
    exit 1
fi

if grep -q "json.loads(value)" src/memos/graph_dbs/neo4j_community.py; then
    echo "✅ Deserialization logic found in _parse_node()"
else
    echo "❌ Verification failed: Deserialization not found"
    exit 1
fi

echo ""
echo "========================================================================"
echo "✅ SUCCESS: Patch applied and verified!"
echo "========================================================================"
echo ""
echo "Next steps:"
echo "  1. Review changes: git diff src/memos/graph_dbs/neo4j_community.py"
echo "  2. Rebuild Docker: docker-compose build memos-api"
echo "  3. Restart API: docker-compose restart memos-api"
echo "  4. Test: bash patches/neo4j-complex-object-serialization/TEST.sh <container-name>"
echo "  5. Commit: git commit -am 'Apply Neo4j complex object serialization fix'"
echo ""
