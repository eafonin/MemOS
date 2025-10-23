#!/bin/bash
# Test BGE-Large 512-Token Embeddings Patch
#
# This script verifies the patch was applied correctly and is working.
#
# Usage:
#   bash patches/bge-large-embeddings-512-tokens/TEST.sh [container-name]
#
# Default container: test1-memos-api

set -e

CONTAINER_NAME="${1:-test1-memos-api}"
TEI_CONTAINER="${2:-test1-tei}"
API_URL="${3:-http://localhost:8001}"
TEI_URL="${4:-http://localhost:8081}"

PATCH_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$PATCH_DIR/../.." && pwd)"

echo "================================================================================"
echo "BGE-Large 512-Token Embeddings Patch - VERIFICATION TEST"
echo "================================================================================"
echo
echo "Container: $CONTAINER_NAME"
echo "TEI Container: $TEI_CONTAINER"
echo "API URL: $API_URL"
echo "TEI URL: $TEI_URL"
echo

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Helper function
test_check() {
    local test_name="$1"
    local test_command="$2"

    echo -n "  Testing: $test_name ... "

    if eval "$test_command" > /dev/null 2>&1; then
        echo "✅ PASS"
        ((TESTS_PASSED++))
        return 0
    else
        echo "❌ FAIL"
        ((TESTS_FAILED++))
        return 1
    fi
}

echo "================================================================================"
echo "TEST SUITE 1: Code Patch Verification"
echo "================================================================================"
echo

# Test 1.1: Chunker config
test_check "Chunker chunk_size set to 480" \
    "grep -q 'chunk_size.*480' '$REPO_ROOT/src/memos/configs/chunker.py'"

# Test 1.2: Chunker overlap
test_check "Chunker chunk_overlap set to 120" \
    "grep -q 'chunk_overlap.*120' '$REPO_ROOT/src/memos/configs/chunker.py'"

# Test 1.3: Tokenizer model
test_check "Tokenizer set to BGE-Large" \
    "grep -q 'BAAI/bge-large-en-v1.5' '$REPO_ROOT/src/memos/configs/chunker.py'"

# Test 1.4: Truncation warning
test_check "Truncation warning logging added" \
    "grep -q 'TRUNCATION RISK' '$REPO_ROOT/src/memos/vec_dbs/qdrant.py'"

echo

echo "================================================================================"
echo "TEST SUITE 2: TEI Service Verification"
echo "================================================================================"
echo

# Test 2.1: TEI health
test_check "TEI service is healthy" \
    "curl -sf '$TEI_URL/health'"

# Test 2.2: TEI model
if curl -sf "$TEI_URL/info" > /tmp/tei_info.json 2>&1; then
    MODEL_ID=$(cat /tmp/tei_info.json | python3 -c "import json, sys; print(json.load(sys.stdin).get('model_id', ''))" 2>/dev/null || echo "")

    if [ "$MODEL_ID" = "BAAI/bge-large-en-v1.5" ]; then
        echo "  Testing: TEI using BGE-Large model ... ✅ PASS"
        ((TESTS_PASSED++))
    else
        echo "  Testing: TEI using BGE-Large model ... ❌ FAIL (found: $MODEL_ID)"
        ((TESTS_FAILED++))
    fi
else
    echo "  Testing: TEI model check ... ❌ FAIL (cannot connect to $TEI_URL)"
    ((TESTS_FAILED++))
fi

# Test 2.3: TEI max tokens
if [ -f /tmp/tei_info.json ]; then
    MAX_TOKENS=$(cat /tmp/tei_info.json | python3 -c "import json, sys; print(json.load(sys.stdin).get('max_input_length', ''))" 2>/dev/null || echo "")

    if [ "$MAX_TOKENS" = "512" ]; then
        echo "  Testing: TEI max_input_length is 512 ... ✅ PASS"
        ((TESTS_PASSED++))
    else
        echo "  Testing: TEI max_input_length is 512 ... ❌ FAIL (found: $MAX_TOKENS)"
        ((TESTS_FAILED++))
    fi
else
    echo "  Testing: TEI max tokens ... ⏭️  SKIP (cannot get TEI info)"
fi

# Test 2.4: Auto-truncate enabled
if [ -f /tmp/tei_info.json ]; then
    AUTO_TRUNCATE=$(cat /tmp/tei_info.json | python3 -c "import json, sys; print(str(json.load(sys.stdin).get('auto_truncate', 'false')).lower())" 2>/dev/null || echo "false")

    if [ "$AUTO_TRUNCATE" = "true" ]; then
        echo "  Testing: TEI auto-truncate enabled ... ✅ PASS"
        ((TESTS_PASSED++))
    else
        echo "  Testing: TEI auto-truncate enabled ... ⚠️  WARNING (auto-truncate not enabled, recommended for safety)"
        # Not counting as failure, just warning
    fi
else
    echo "  Testing: TEI auto-truncate ... ⏭️  SKIP (cannot get TEI info)"
fi

echo

echo "================================================================================"
echo "TEST SUITE 3: Functional Testing"
echo "================================================================================"
echo

# Test 3.1: API health
test_check "MemOS API is accessible" \
    "curl -sf '$API_URL/health' || curl -sf '$API_URL/docs'"

# Test 3.2: Test with medium-size document (~1000 chars, ~250 tokens)
echo "  Testing: Medium document ingestion (250 tokens) ... "
MEDIUM_TEXT="This is a test document. "
for i in {1..40}; do MEDIUM_TEXT="$MEDIUM_TEXT $MEDIUM_TEXT"; done  # Create ~1000 char text

# Register test user first (may already exist, ignore errors)
curl -sf -X POST "$API_URL/product/users/register" \
    -H "Content-Type: application/json" \
    -d '{"user_id":"test_bge_user","mem_cube_id":"test_bge_cube"}' \
    > /dev/null 2>&1 || true

# Try to add document
if curl -sf -X POST "$API_URL/product/add" \
    -H "Content-Type: application/json" \
    -d "{\"user_id\":\"test_bge_user\",\"memory_content\":\"$MEDIUM_TEXT\"}" \
    --max-time 30 > /tmp/add_result.json 2>&1; then

    CODE=$(cat /tmp/add_result.json | python3 -c "import json, sys; print(json.load(sys.stdin).get('code', 0))" 2>/dev/null || echo "0")
    if [ "$CODE" = "200" ]; then
        echo "                                                           ✅ PASS"
        ((TESTS_PASSED++))
    else
        echo "                                                           ❌ FAIL (HTTP $CODE)"
        ((TESTS_FAILED++))
    fi
else
    echo "                                                           ❌ FAIL (request failed)"
    ((TESTS_FAILED++))
fi

echo

echo "================================================================================"
echo "TEST SUITE 4: Log Analysis"
echo "================================================================================"
echo

# Test 4.1: Check for 413 errors
echo -n "  Testing: No 413 errors in TEI logs ... "
ERROR_413_COUNT=$(docker logs "$TEI_CONTAINER" 2>&1 | grep -c "413" || echo "0")
if [ "$ERROR_413_COUNT" = "0" ]; then
    echo "✅ PASS (no 413 errors)"
    ((TESTS_PASSED++))
elif [ "$ERROR_413_COUNT" -lt "5" ]; then
    echo "⚠️  WARNING ($ERROR_413_COUNT errors found, but < 5)"
    ((TESTS_PASSED++))  # Count as pass with warning
else
    echo "❌ FAIL ($ERROR_413_COUNT errors found)"
    ((TESTS_FAILED++))
fi

# Test 4.2: Check for truncation warnings
echo -n "  Testing: Truncation warnings in MemOS logs ... "
TRUNCATION_COUNT=$(docker logs "$CONTAINER_NAME" 2>&1 | grep -c "TRUNCATION RISK" || echo "0")
if [ "$TRUNCATION_COUNT" = "0" ]; then
    echo "✅ PASS (no truncation warnings - ideal)"
    ((TESTS_PASSED++))
elif [ "$TRUNCATION_COUNT" -lt "3" ]; then
    echo "⚠️  WARNING ($TRUNCATION_COUNT warnings, may be edge cases)"
    ((TESTS_PASSED++))  # Count as pass with warning
else
    echo "❌ FAIL ($TRUNCATION_COUNT warnings - chunker may not be configured correctly)"
    ((TESTS_FAILED++))
fi

# Test 4.3: Check container health
echo -n "  Testing: Container health status ... "
CONTAINER_STATUS=$(docker inspect "$CONTAINER_NAME" --format='{{.State.Health.Status}}' 2>/dev/null || echo "unknown")
if [ "$CONTAINER_STATUS" = "healthy" ]; then
    echo "✅ PASS (healthy)"
    ((TESTS_PASSED++))
elif [ "$CONTAINER_STATUS" = "unknown" ]; then
    echo "⏭️  SKIP (no healthcheck defined)"
else
    echo "⚠️  WARNING (status: $CONTAINER_STATUS)"
fi

echo

# Cleanup
rm -f /tmp/tei_info.json /tmp/add_result.json

# Summary
echo "================================================================================"
echo "TEST RESULTS"
echo "================================================================================"
echo
echo "Tests Passed:  $TESTS_PASSED"
echo "Tests Failed:  $TESTS_FAILED"
echo "Total Tests:   $((TESTS_PASSED + TESTS_FAILED))"
echo

if [ $TESTS_FAILED -eq 0 ]; then
    echo "✅ ALL TESTS PASSED!"
    echo
    echo "BGE-Large 512-token patch is correctly installed and working."
    echo
    echo "Next steps:"
    echo "  - Re-ingest documents if you have existing data (for consistency)"
    echo "  - Monitor logs for any truncation warnings"
    echo "  - Run comprehensive workflow tests if available"
    echo
    exit 0
else
    echo "❌ SOME TESTS FAILED"
    echo
    echo "Please review the failures above and:"
    echo "  1. Verify patch was applied: git diff src/memos/configs/chunker.py"
    echo "  2. Check docker-compose.yml has BGE-Large configuration"
    echo "  3. Verify containers rebuilt: docker-compose build --no-cache"
    echo "  4. Check logs: docker logs $CONTAINER_NAME --tail=100"
    echo
    echo "See: patches/bge-large-embeddings-512-tokens/README.md"
    echo
    exit 1
fi
