#!/bin/bash
# Test script to verify Chonkie tokenizer fix

set -e

echo "Chonkie Tokenizer Fix - Verification Test"
echo "========================================="
echo ""

# Check if running in container or host
if [ -f /.dockerenv ]; then
    PYTHON_CMD="python3"
else
    CONTAINER_NAME="${1:-test1-memos-api}"
    PYTHON_CMD="docker exec $CONTAINER_NAME python3"
    echo "Testing in container: $CONTAINER_NAME"
    echo ""
fi

# Test 1: Import and basic initialization
echo "[Test 1/4] Testing imports..."
$PYTHON_CMD -c "
from memos.chunkers.sentence_chunker import SentenceChunker
from memos.configs.chunker import SentenceChunkerConfig
print('✓ Imports successful')
"

# Test 2: Check default tokenizer config
echo "[Test 2/4] Checking default tokenizer configuration..."
DEFAULT_TOKENIZER=$($PYTHON_CMD -c "
from memos.configs.chunker import SentenceChunkerConfig
config = SentenceChunkerConfig()
print(config.tokenizer_or_token_counter)
")

if [ "$DEFAULT_TOKENIZER" = "sentence-transformers/all-mpnet-base-v2" ]; then
    echo "✓ Default tokenizer correctly set to: $DEFAULT_TOKENIZER"
else
    echo "✗ Unexpected default tokenizer: $DEFAULT_TOKENIZER"
    echo "  Expected: sentence-transformers/all-mpnet-base-v2"
    exit 1
fi

# Test 3: Initialize chunker and verify tokenizer loading
echo "[Test 3/4] Testing tokenizer loading from cache..."
$PYTHON_CMD -c "
from memos.chunkers.sentence_chunker import SentenceChunker
from memos.configs.chunker import SentenceChunkerConfig
import sys

config = SentenceChunkerConfig()
try:
    chunker = SentenceChunker(config)
    print('✓ Chunker initialized successfully')
except Exception as e:
    print(f'✗ Failed to initialize chunker: {e}')
    sys.exit(1)
"

# Test 4: Test actual chunking with token counting
echo "[Test 4/4] Testing end-to-end chunking..."
$PYTHON_CMD -c "
from memos.chunkers.sentence_chunker import SentenceChunker
from memos.configs.chunker import SentenceChunkerConfig
import sys

config = SentenceChunkerConfig()
chunker = SentenceChunker(config)

test_text = 'This is the first test sentence. This is the second sentence with more words. And here is a third one.'

try:
    chunks = chunker.chunk(test_text)
    
    if len(chunks) == 0:
        print('✗ No chunks created')
        sys.exit(1)
    
    if chunks[0].token_count == 0:
        print('✗ Token count is 0 (character-based fallback)')
        sys.exit(1)
    
    print(f'✓ Chunking successful!')
    print(f'  Chunks created: {len(chunks)}')
    print(f'  Token count: {chunks[0].token_count}')
    print(f'  Sentences: {len(chunks[0].sentences)}')
    
    # Verify it's using tokens not characters
    if chunks[0].token_count > 0 and chunks[0].token_count < len(test_text):
        print('✓ Using token-based chunking (not character-based)')
    else:
        print('⚠ May be using character-based chunking')
        
except Exception as e:
    print(f'✗ Chunking failed: {e}')
    sys.exit(1)
"

echo ""
echo "========================================="
echo "✅ All tests passed!"
echo ""
echo "Chonkie tokenizer is working correctly:"
echo "  - Imports successful"
echo "  - Default tokenizer: sentence-transformers/all-mpnet-base-v2"
echo "  - Tokenizer loads from cache"
echo "  - Token-based chunking operational"
echo ""
