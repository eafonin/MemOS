#!/bin/bash
# Quick apply script for Chonkie tokenizer fix patches

set -e

PATCH_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$PATCH_DIR/../.." && pwd)"

echo "Chonkie Tokenizer Fix - Patch Application"
echo "=========================================="
echo ""
echo "Patch directory: $PATCH_DIR"
echo "Repository root: $REPO_ROOT"
echo ""

cd "$REPO_ROOT"

# Check if patches are already applied
if git diff --quiet src/memos/chunkers/sentence_chunker.py; then
    echo "✓ Applying patches..."
    
    # Apply patch 0001
    echo "  [1/2] Applying tokenizer loading fix..."
    if git apply "$PATCH_DIR/0001-fix-chonkie-tokenizer-loading-from-cache.patch"; then
        echo "  ✓ Patch 0001 applied successfully"
    else
        echo "  ✗ Failed to apply patch 0001"
        exit 1
    fi
    
    # Apply patch 0002 (if requirements.txt exists in docker/)
    if [ -f "$REPO_ROOT/docker/requirements.txt" ]; then
        echo "  [2/2] Applying tiktoken dependency..."
        if git apply "$PATCH_DIR/0002-add-tiktoken-dependency.patch"; then
            echo "  ✓ Patch 0002 applied successfully"
        else
            echo "  ⚠ Failed to apply patch 0002 - may need manual addition to requirements.txt"
            echo "  Add this line after threadpoolctl: tiktoken==0.8.0"
        fi
    else
        echo "  [2/2] Skipping tiktoken patch (docker/requirements.txt not found)"
        echo "  ℹ Manually add 'tiktoken==0.8.0' to your requirements file"
    fi
    
    echo ""
    echo "✓ Patches applied successfully!"
    echo ""
    echo "Next steps:"
    echo "  1. Review changes: git diff"
    echo "  2. Test changes: docker-compose build && docker-compose up -d"
    echo "  3. Verify: docker exec <container> python3 -c 'from memos.chunkers.sentence_chunker import SentenceChunker; ...'"
    echo "  4. Commit: git commit -m 'Fix Chonkie tokenizer loading from cache'"
else
    echo "⚠ Changes detected in src/memos/chunkers/sentence_chunker.py"
    echo "Patches may already be applied, or you have local modifications."
    echo ""
    echo "To force apply: git apply --check <patch-file>"
    echo "To view diff: git diff src/memos/chunkers/sentence_chunker.py"
fi
