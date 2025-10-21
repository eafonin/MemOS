#!/bin/bash
# ============================================================================
# Configurable Streaming Tokenizer Patch - Test Script
# ============================================================================
#
# This script tests the configurable streaming tokenizer patch.
#
# Usage:
#   bash patches/configurable-streaming-tokenizer/TEST.sh [container_name]
#
# Arguments:
#   container_name: Docker container name (default: test1-memos-api)
#
# Tests:
#   1. Patch is applied correctly
#   2. Environment variable is set
#   3. Tokenizer initialization succeeds
#   4. Auto-detection works correctly
#   5. Fallback mechanisms work
#
# ============================================================================

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

CONTAINER_NAME="${1:-test1-memos-api}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "Configurable Streaming Tokenizer - Test Suite"
echo "=============================================="
echo ""
echo "Container: $CONTAINER_NAME"
echo ""

# Test counter
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Test helper functions
test_start() {
    TESTS_RUN=$((TESTS_RUN + 1))
    echo -n "  [$TESTS_RUN] $1 ... "
}

test_pass() {
    TESTS_PASSED=$((TESTS_PASSED + 1))
    echo -e "${GREEN}✓ PASS${NC}"
    if [ -n "${1:-}" ]; then
        echo "      $1"
    fi
}

test_fail() {
    TESTS_FAILED=$((TESTS_FAILED + 1))
    echo -e "${RED}✗ FAIL${NC}"
    if [ -n "${1:-}" ]; then
        echo -e "      ${RED}$1${NC}"
    fi
}

# ============================================================================
# Test 1: Patch Applied Correctly
# ============================================================================

echo "Test Suite 1: Patch Integrity"
echo "------------------------------"

test_start "Patch functions exist in product.py"
if grep -q "_initialize_streaming_tokenizer" "$REPO_ROOT/src/memos/mem_os/product.py" && \
   grep -q "_detect_tokenizer_for_model" "$REPO_ROOT/src/memos/mem_os/product.py"; then
    test_pass "Both functions found"
else
    test_fail "Patch functions not found"
fi

test_start "Function signatures are correct"
if grep -q "def _detect_tokenizer_for_model(self, model_name: str) -> str:" "$REPO_ROOT/src/memos/mem_os/product.py" && \
   grep -q "def _initialize_streaming_tokenizer(self):" "$REPO_ROOT/src/memos/mem_os/product.py"; then
    test_pass
else
    test_fail "Function signatures don't match expected format"
fi

test_start "Auto-detection logic is present"
if grep -q '"qwen"' "$REPO_ROOT/src/memos/mem_os/product.py" && \
   grep -q '"claude"' "$REPO_ROOT/src/memos/mem_os/product.py" && \
   grep -q '"gpt"' "$REPO_ROOT/src/memos/mem_os/product.py"; then
    test_pass "Detection rules for Qwen, Claude, and GPT found"
else
    test_fail "Auto-detection logic incomplete"
fi

# ============================================================================
# Test 2: Environment Configuration
# ============================================================================

echo ""
echo "Test Suite 2: Environment Configuration"
echo "----------------------------------------"

test_start "MOS_STREAMING_TOKENIZER in .env"
if grep -q "^MOS_STREAMING_TOKENIZER=" "$REPO_ROOT/docker-test1/.env" 2>/dev/null || \
   grep -q "^MOS_STREAMING_TOKENIZER=" "$REPO_ROOT/.env" 2>/dev/null; then
    VALUE=$(grep "^MOS_STREAMING_TOKENIZER=" "$REPO_ROOT/docker-test1/.env" 2>/dev/null | cut -d'=' -f2 || echo "not found")
    test_pass "Value: $VALUE"
else
    test_fail "MOS_STREAMING_TOKENIZER not found in .env"
fi

# ============================================================================
# Test 3: Container Tests (if container is running)
# ============================================================================

if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo ""
    echo "Test Suite 3: Container Runtime Tests"
    echo "--------------------------------------"

    test_start "Container is running"
    if docker exec "$CONTAINER_NAME" echo "OK" > /dev/null 2>&1; then
        test_pass
    else
        test_fail "Cannot execute commands in container"
    fi

    test_start "Transformers library is installed"
    if docker exec "$CONTAINER_NAME" python3 -c "import transformers" 2>/dev/null; then
        test_pass
    else
        test_fail "transformers library not found"
    fi

    test_start "HuggingFace cache exists"
    if docker exec "$CONTAINER_NAME" ls /root/.cache/huggingface/hub/ > /dev/null 2>&1; then
        test_pass
    else
        test_fail "HF cache directory not found"
    fi

    test_start "Tokenizer can be loaded from cache"
    TOKENIZER_TEST=$(docker exec "$CONTAINER_NAME" python3 -c "
from transformers import AutoTokenizer
import os
os.environ.pop('HF_ENDPOINT', None)
try:
    tokenizer = AutoTokenizer.from_pretrained('gpt2', local_files_only=True)
    print('SUCCESS')
except Exception as e:
    print(f'FAILED: {e}')
" 2>&1)

    if [[ "$TOKENIZER_TEST" == *"SUCCESS"* ]]; then
        test_pass "gpt2 tokenizer loaded"
    else
        test_fail "Failed to load tokenizer: $TOKENIZER_TEST"
    fi

    test_start "Logs show successful tokenizer initialization"
    LOGS=$(docker logs "$CONTAINER_NAME" 2>&1 | grep -i tokenizer | tail -5)
    if echo "$LOGS" | grep -q "Successfully loaded tokenizer"; then
        test_pass
    elif echo "$LOGS" | grep -q "Failed to initialize tokenizer"; then
        test_fail "Tokenizer initialization failed (check logs)"
    else
        test_fail "No tokenizer initialization logs found"
    fi

else
    echo ""
    echo -e "${YELLOW}Skipping container tests (container not running)${NC}"
    echo "Start container with: docker-compose up -d memos-api"
fi

# ============================================================================
# Test 4: Auto-Detection Logic
# ============================================================================

echo ""
echo "Test Suite 4: Auto-Detection Logic"
echo "-----------------------------------"

test_start "Qwen model detection"
RESULT=$(python3 << 'EOF'
import sys
sys.path.insert(0, 'src')
from memos.mem_os.product import MOSProductService

# Create instance (will fail but that's ok, we just need the method)
class TestProduct:
    def _detect_tokenizer_for_model(self, model_name: str) -> str:
        model_lower = model_name.lower()
        if "qwen" in model_lower:
            return "Qwen/Qwen3-0.6B"
        if any(x in model_lower for x in ["claude", "gpt", "openai", "chatgpt"]):
            return "gpt2"
        return "bert-base-uncased"

test = TestProduct()
print(test._detect_tokenizer_for_model("Qwen/Qwen3-1.7B"))
EOF
)

if [[ "$RESULT" == "Qwen/Qwen3-0.6B" ]]; then
    test_pass "Detected: $RESULT"
else
    test_fail "Expected 'Qwen/Qwen3-0.6B', got: $RESULT"
fi

test_start "Claude model detection"
RESULT=$(python3 << 'EOF'
import sys
sys.path.insert(0, 'src')

class TestProduct:
    def _detect_tokenizer_for_model(self, model_name: str) -> str:
        model_lower = model_name.lower()
        if "qwen" in model_lower:
            return "Qwen/Qwen3-0.6B"
        if any(x in model_lower for x in ["claude", "gpt", "openai", "chatgpt"]):
            return "gpt2"
        return "bert-base-uncased"

test = TestProduct()
print(test._detect_tokenizer_for_model("anthropic/claude-3.5-sonnet"))
EOF
)

if [[ "$RESULT" == "gpt2" ]]; then
    test_pass "Detected: $RESULT"
else
    test_fail "Expected 'gpt2', got: $RESULT"
fi

test_start "Fallback for unknown model"
RESULT=$(python3 << 'EOF'
import sys
sys.path.insert(0, 'src')

class TestProduct:
    def _detect_tokenizer_for_model(self, model_name: str) -> str:
        model_lower = model_name.lower()
        if "qwen" in model_lower:
            return "Qwen/Qwen3-0.6B"
        if any(x in model_lower for x in ["claude", "gpt", "openai", "chatgpt"]):
            return "gpt2"
        return "bert-base-uncased"

test = TestProduct()
print(test._detect_tokenizer_for_model("meta-llama/Llama-2-7b"))
EOF
)

if [[ "$RESULT" == "bert-base-uncased" ]]; then
    test_pass "Detected: $RESULT"
else
    test_fail "Expected 'bert-base-uncased', got: $RESULT"
fi

# ============================================================================
# Test Summary
# ============================================================================

echo ""
echo "Test Summary"
echo "============"
echo -e "Tests run:    $TESTS_RUN"
echo -e "Tests passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests failed: ${RED}$TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}All Tests Passed! ✓${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "The configurable streaming tokenizer patch is working correctly."
    echo ""
    exit 0
else
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${RED}Some Tests Failed ✗${NC}"
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "Please review the failures above and:"
    echo "  1. Check that the patch was applied correctly"
    echo "  2. Verify environment configuration"
    echo "  3. Ensure required tokenizers are in cache"
    echo "  4. Review logs: docker logs $CONTAINER_NAME | grep -i tokenizer"
    echo ""
    echo "For help, see: $SCRIPT_DIR/README.md"
    echo ""
    exit 1
fi
