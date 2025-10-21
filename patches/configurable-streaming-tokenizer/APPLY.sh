#!/bin/bash
# ============================================================================
# Configurable Streaming Tokenizer Patch - Application Script
# ============================================================================
#
# This script applies the configurable streaming tokenizer patch to MemOS.
#
# Usage:
#   bash patches/configurable-streaming-tokenizer/APPLY.sh
#
# What it does:
#   1. Applies the patch to src/memos/mem_os/product.py
#   2. Adds MOS_STREAMING_TOKENIZER to .env (if not present)
#   3. Downloads required tokenizer to cache (optional)
#   4. Verifies the patch was applied successfully
#
# Requirements:
#   - Git working directory should be clean (or changes stashed)
#   - Run from MemOS repository root
#
# ============================================================================

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "Configurable Streaming Tokenizer - Patch Application"
echo "====================================================="
echo ""

# Determine patch directory (handles both relative and absolute paths)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PATCH_DIR="$SCRIPT_DIR"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "Patch directory: $PATCH_DIR"
echo "Repository root: $REPO_ROOT"
echo ""

# Check we're in the right directory
if [ ! -f "$REPO_ROOT/src/memos/mem_os/product.py" ]; then
    echo -e "${RED}✗ Error: Cannot find src/memos/mem_os/product.py${NC}"
    echo "  Please run this script from the MemOS repository root."
    exit 1
fi

# Step 1: Apply the patch
echo "✓ Applying patches..."

cd "$REPO_ROOT"

if git apply --check "$PATCH_DIR/0001-add-configurable-streaming-tokenizer.patch" 2>/dev/null; then
    git apply "$PATCH_DIR/0001-add-configurable-streaming-tokenizer.patch"
    echo -e "${GREEN}  ✓ Patch applied successfully${NC}"
else
    echo -e "${YELLOW}  ⚠ Patch may already be applied or conflicts exist${NC}"
    echo "  Attempting to apply with --reverse to check..."
    if git apply --reverse --check "$PATCH_DIR/0001-add-configurable-streaming-tokenizer.patch" 2>/dev/null; then
        echo -e "${BLUE}  ℹ Patch is already applied${NC}"
    else
        echo -e "${RED}  ✗ Patch conflicts with current code${NC}"
        echo "  Please review manually or stash your changes."
        exit 1
    fi
fi

# Step 2: Check .env file exists and add configuration if needed
echo ""
echo "✓ Checking .env configuration..."

# Find .env file (check multiple locations)
ENV_FILE=""
for location in ".env" "docker-test1/.env" ".env.example"; do
    if [ -f "$REPO_ROOT/$location" ]; then
        ENV_FILE="$REPO_ROOT/$location"
        break
    fi
done

if [ -n "$ENV_FILE" ]; then
    echo -e "${BLUE}  Found .env at: $ENV_FILE${NC}"

    # Check if MOS_STREAMING_TOKENIZER already exists
    if grep -q "^MOS_STREAMING_TOKENIZER=" "$ENV_FILE" 2>/dev/null; then
        echo -e "${BLUE}  ℹ MOS_STREAMING_TOKENIZER already configured${NC}"
    else
        echo -e "${YELLOW}  ⚠ MOS_STREAMING_TOKENIZER not found in .env${NC}"
        echo ""
        echo "  Would you like to add it now? [Y/n]"
        read -r response
        if [[ ! "$response" =~ ^[Nn]$ ]]; then
            cat >> "$ENV_FILE" << 'EOL'

# ============================================
# Streaming Tokenizer Configuration
# ============================================
# The tokenizer used for chunking chat responses during streaming.
# IMPORTANT: Should match your LLM family for accurate token boundaries.
#
# Supported values:
#   - "auto" (recommended): Automatically selects based on MOS_CHAT_MODEL
#   - HuggingFace model path (e.g., "Qwen/Qwen3-0.6B", "bert-base-uncased", "gpt2")
#
# Auto-detection logic:
#   - Qwen models → "Qwen/Qwen3-0.6B"
#   - Claude/GPT/OpenAI → "gpt2" (GPT-2 tokenizer is compatible)
#   - Other models → "bert-base-uncased" (general fallback)
#
# If tokenizer fails to load, falls back to character-based chunking (functional but suboptimal).
# For offline deployments, ensure the tokenizer model is cached in HF_HOME.
MOS_STREAMING_TOKENIZER=auto
EOL
            echo -e "${GREEN}  ✓ Added MOS_STREAMING_TOKENIZER=auto to $ENV_FILE${NC}"
        fi
    fi
else
    echo -e "${YELLOW}  ⚠ No .env file found${NC}"
    echo "  You'll need to add MOS_STREAMING_TOKENIZER=auto manually"
fi

# Step 3: Offer to download tokenizer to cache
echo ""
echo "✓ Checking tokenizer cache..."

# Determine which tokenizer to download based on .env
CHAT_MODEL=$(grep "^MOS_CHAT_MODEL=" "$ENV_FILE" 2>/dev/null | cut -d'=' -f2 || echo "")
TOKENIZER_TO_DOWNLOAD="gpt2"  # Default

if [[ "$CHAT_MODEL" == *"qwen"* ]] || [[ "$CHAT_MODEL" == *"Qwen"* ]]; then
    TOKENIZER_TO_DOWNLOAD="Qwen/Qwen3-0.6B"
fi

echo -e "${BLUE}  Detected chat model: ${CHAT_MODEL:-Not configured}${NC}"
echo -e "${BLUE}  Recommended tokenizer: $TOKENIZER_TO_DOWNLOAD${NC}"
echo ""
echo "  Download tokenizer to cache for offline use? [Y/n]"
read -r response

if [[ ! "$response" =~ ^[Nn]$ ]]; then
    echo "  Downloading $TOKENIZER_TO_DOWNLOAD..."
    if python3 -c "from transformers import AutoTokenizer; AutoTokenizer.from_pretrained('$TOKENIZER_TO_DOWNLOAD')" 2>/dev/null; then
        echo -e "${GREEN}  ✓ Tokenizer cached successfully${NC}"
    else
        echo -e "${YELLOW}  ⚠ Failed to download tokenizer (may require internet)${NC}"
        echo "  You can download it later or use bert-base-uncased fallback"
    fi
fi

# Step 4: Verification
echo ""
echo "✓ Verification..."

if grep -q "_initialize_streaming_tokenizer" "$REPO_ROOT/src/memos/mem_os/product.py"; then
    echo -e "${GREEN}  ✓ Patch functions found in product.py${NC}"
else
    echo -e "${RED}  ✗ Patch verification failed${NC}"
    exit 1
fi

# Summary
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}Patch Applied Successfully!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "Next steps:"
echo "  1. Restart MemOS: docker-compose restart memos-api"
echo "  2. Check logs: docker logs memos-api 2>&1 | grep -i tokenizer"
echo "  3. Run tests: bash $PATCH_DIR/TEST.sh"
echo ""
echo "Expected log output:"
echo "  [INFO] Auto-detected tokenizer 'gpt2' for model '...'"
echo "  [INFO] Successfully loaded tokenizer 'gpt2' from cache for streaming"
echo ""
echo "For more information, see:"
echo "  $PATCH_DIR/README.md"
echo ""
