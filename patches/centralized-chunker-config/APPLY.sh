#!/bin/bash
# Apply Centralized Chunker Configuration Patch
# This patch centralizes chunker configuration into a single helper function
# and makes it configurable via environment variables

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PATCH_FILE="$SCRIPT_DIR/0001-centralize-chunker-config-with-env-support.patch"

echo "=================================================="
echo "  Centralized Chunker Configuration Patch"
echo "=================================================="
echo ""
echo "This patch will:"
echo "  ✓ Add get_chunker_config() helper to src/memos/api/config.py"
echo "  ✓ Replace 3 hardcoded chunker configs with helper calls"
echo "  ✓ Add ENV variable documentation to docker-test1/.env"
echo "  ✓ Make chunker settings centrally configurable"
echo ""

# Check if we're in the right directory
if [ ! -f "$REPO_ROOT/src/memos/api/config.py" ]; then
    echo "❌ Error: Cannot find src/memos/api/config.py"
    echo "   Please run this script from the MemOS repository root or patches directory"
    exit 1
fi

# Check if patch file exists
if [ ! -f "$PATCH_FILE" ]; then
    echo "❌ Error: Patch file not found: $PATCH_FILE"
    exit 1
fi

# Check if patch is already applied
if grep -q "def get_chunker_config" "$REPO_ROOT/src/memos/api/config.py"; then
    echo "⚠️  Warning: Patch appears to be already applied"
    echo "   Found get_chunker_config() in config.py"
    echo ""
    read -p "Do you want to continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 1
    fi
fi

# Apply the patch
echo "Applying patch..."
cd "$REPO_ROOT"

if git apply --check "$PATCH_FILE" 2>/dev/null; then
    git apply "$PATCH_FILE"
    echo "✅ Patch applied successfully!"
else
    echo "⚠️  Standard git apply failed, trying with --reject..."
    if git apply --reject "$PATCH_FILE" 2>&1; then
        echo "✅ Patch applied with conflicts (see .rej files)"
    else
        echo "❌ Error: Failed to apply patch"
        echo "   You may need to apply changes manually"
        exit 1
    fi
fi

echo ""
echo "=================================================="
echo "  Patch Applied Successfully!"
echo "=================================================="
echo ""
echo "Changes made:"
echo "  ✓ src/memos/api/config.py - Added get_chunker_config() helper"
echo "  ✓ src/memos/api/config.py - Replaced 3 hardcoded configs"
echo "  ✓ docker-test1/.env - Added chunker documentation"
echo ""
echo "Next steps:"
echo "  1. Review changes: git diff src/memos/api/config.py"
echo "  2. (Optional) Customize ENV vars in docker-test1/.env"
echo "  3. Rebuild container: cd docker-test1 && docker-compose build --no-cache memos-api"
echo "  4. Restart services: docker-compose restart memos-api"
echo "  5. Test: bash patches/centralized-chunker-config/TEST.sh"
echo ""
echo "ENV Variables (optional overrides in docker-test1/.env):"
echo "  MOS_CHUNKER_BACKEND=sentence           # Default: sentence"
echo "  MOS_CHUNKER_TOKENIZER=bert-base-uncased # Default: bert-base-uncased"
echo "  MOS_CHUNK_SIZE=480                      # Default: 480"
echo "  MOS_CHUNK_OVERLAP=120                   # Default: 120"
echo "  MOS_MIN_SENTENCES_PER_CHUNK=1           # Default: 1"
echo ""
