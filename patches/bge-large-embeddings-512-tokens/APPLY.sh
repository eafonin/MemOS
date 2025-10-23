#!/bin/bash
# Apply BGE-Large 512-Token Embeddings Patch
#
# This script applies the patch to upgrade from all-mpnet-base-v2 (384 tokens)
# to BAAI/bge-large-en-v1.5 (512 tokens)
#
# Usage:
#   bash patches/bge-large-embeddings-512-tokens/APPLY.sh
#
# For specific container (optional):
#   bash patches/bge-large-embeddings-512-tokens/APPLY.sh my-container-name

set -e  # Exit on error

PATCH_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PATCH_FILE="$PATCH_DIR/0001-upgrade-to-bge-large-512-token-embeddings.patch"
REPO_ROOT="$(cd "$PATCH_DIR/../.." && pwd)"

echo "================================================================================"
echo "BGE-Large 512-Token Embeddings Patch - APPLY"
echo "================================================================================"
echo

# Check we're in MemOS repository
if [ ! -f "$REPO_ROOT/src/memos/configs/chunker.py" ]; then
    echo "❌ ERROR: Not in MemOS repository root!"
    echo "   Current directory: $(pwd)"
    echo "   Expected to find: src/memos/configs/chunker.py"
    exit 1
fi

echo "📂 Repository: $REPO_ROOT"
echo "📦 Patch file: $PATCH_FILE"
echo

# Check if patch already applied
if grep -q "chunk_size.*480" "$REPO_ROOT/src/memos/configs/chunker.py" 2>/dev/null; then
    echo "⚠️  WARNING: Patch appears already applied (chunk_size=480 found)"
    echo "   Continue anyway? (y/N): "
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 0
    fi
fi

# Apply patch
echo "Step 1: Applying code patch..."
cd "$REPO_ROOT"

if git apply --check "$PATCH_FILE" 2>&1; then
    git apply "$PATCH_FILE"
    echo "✅ Patch applied successfully!"
else
    echo "❌ Patch failed to apply cleanly."
    echo "   This might mean:"
    echo "   - Patch is already applied"
    echo "   - Code has been modified"
    echo "   - Using different MemOS version"
    echo
    echo "   Try manual application (see README.md)"
    exit 1
fi

# Verify application
echo
echo "Step 2: Verifying patch application..."

if grep -q "chunk_size.*480" "$REPO_ROOT/src/memos/configs/chunker.py"; then
    echo "✅ Chunker config updated (chunk_size=480)"
else
    echo "⚠️  WARNING: chunk_size not set to 480"
fi

if grep -q "BAAI/bge-large-en-v1.5" "$REPO_ROOT/src/memos/configs/chunker.py"; then
    echo "✅ Tokenizer updated to BGE-Large"
else
    echo "⚠️  WARNING: Tokenizer not updated to BGE-Large"
fi

if grep -q "TRUNCATION RISK" "$REPO_ROOT/src/memos/vec_dbs/qdrant.py"; then
    echo "✅ Truncation warning logging added"
else
    echo "⚠️  WARNING: Truncation warning not found in qdrant.py"
fi

# Docker compose instructions
echo
echo "================================================================================"
echo "Step 3: Update docker-compose.yml (MANUAL STEP REQUIRED)"
echo "================================================================================"
echo
echo "You must manually update your docker-compose.yml to use BGE-Large model."
echo
echo "Find the 'tei' service and update the command to:"
echo
cat << 'EOF'
  tei:
    image: ghcr.io/huggingface/text-embeddings-inference:cpu-1.8.1
    command: >
      --model-id BAAI/bge-large-en-v1.5
      --port 80
      --auto-truncate
    environment:
      - MODEL_ID=BAAI/bge-large-en-v1.5
EOF
echo
echo "See: patches/bge-large-embeddings-512-tokens/docker-compose-bge-large.yml.example"
echo

# Container-specific instructions
CONTAINER_NAME="${1:-test1-memos-api}"
echo "================================================================================"
echo "Step 4: Rebuild and Restart Services"
echo "================================================================================"
echo
echo "For container: $CONTAINER_NAME"
echo
echo "Run these commands:"
echo
echo "  # Navigate to deployment directory"
echo "  cd docker-test1  # or your deployment directory"
echo
echo "  # Update docker-compose.yml (see Step 3)"
echo "  nano docker-compose.yml"
echo
echo "  # Clear old model cache (optional, saves disk space)"
echo "  rm -rf data/hf-cache/hub/models--sentence-transformers--all-mpnet-base-v2"
echo
echo "  # Rebuild MemOS API"
echo "  docker-compose build --no-cache memos-api"
echo
echo "  # Restart all services"
echo "  docker-compose down"
echo "  docker-compose up -d"
echo
echo "  # Monitor TEI model download (first time, ~1.34 GB)"
echo "  docker logs -f test1-tei"
echo
echo "  # Verify installation"
echo "  bash ../patches/bge-large-embeddings-512-tokens/TEST.sh $CONTAINER_NAME"
echo

echo "================================================================================"
echo "Patch Applied Successfully!"
echo "================================================================================"
echo
echo "Next steps:"
echo "  1. Update docker-compose.yml (see Step 3 above)"
echo "  2. Rebuild and restart services (see Step 4 above)"
echo "  3. Run TEST.sh to verify"
echo
echo "Documentation: patches/bge-large-embeddings-512-tokens/README.md"
echo
