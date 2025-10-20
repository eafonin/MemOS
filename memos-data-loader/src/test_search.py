#!/usr/bin/env python3
"""
Search functionality test for docker-test1 API
"""
import requests
import json

BASE_URL = "http://localhost:8001"
USER_ID = "test1_user"

def search_memories(query, top_k=10):
    """Search for memories using the docker-test1 API"""
    payload = {
        "user_id": USER_ID,
        "query": query,
        "top_k": top_k
    }

    try:
        response = requests.post(
            f"{BASE_URL}/product/search",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )

        response.raise_for_status()
        return response.json()

    except Exception as e:
        return {"error": str(e), "status_code": getattr(response, 'status_code', None)}

def print_search_results(query, results, test_num):
    """Pretty print search results"""
    print("=" * 80)
    print(f"TEST {test_num}: Search Query: '{query}'")
    print("=" * 80)

    if "error" in results:
        print(f"❌ Error: {results['error']}")
        print(f"   Status Code: {results.get('status_code')}")
        return

    print(f"Status: {results.get('code', 'N/A')}")
    print(f"Message: {results.get('message', 'N/A')}")

    data = results.get('data', {})

    # Check for memories in the response
    if isinstance(data, dict):
        memories = data.get('memories', [])

        if not memories:
            print("\n⚠️  No memories found")
            print(f"Response data: {json.dumps(data, indent=2)[:500]}")
        else:
            print(f"\n✅ Found {len(memories)} memories:\n")

            for i, memory in enumerate(memories, 1):
                print(f"  Result {i}:")
                print(f"    Memory: {memory.get('memory_content', 'N/A')[:100]}")

                # Show score if available
                if 'score' in memory:
                    print(f"    Score: {memory['score']:.4f}")

                # Show metadata
                if 'metadata' in memory:
                    metadata = memory['metadata']
                    print(f"    Type: {metadata.get('memory_type', 'N/A')}")
                    print(f"    Created: {metadata.get('created_at', 'N/A')}")
                    if 'tags' in metadata:
                        print(f"    Tags: {metadata.get('tags')}")

                print()
    else:
        print(f"\n⚠️  Unexpected response format:")
        print(f"{json.dumps(data, indent=2)[:500]}")

    print()

# Test queries
test_queries = [
    "test message",
    "docker environment",
    "greeting hello",
    "assistant response",
    "MemOS testing",
    "What was I testing?",
    "Tell me about the environment",
    "What messages did I send?"
]

print("\n" + "🔍" * 40)
print("MEMORY SEARCH TEST SUITE")
print("Testing with 3 loaded vectors")
print("🔍" * 40 + "\n")

for i, query in enumerate(test_queries, 1):
    results = search_memories(query, top_k=3)
    print_search_results(query, results, i)

print("=" * 80)
print("SEARCH TESTS COMPLETE")
print("=" * 80)
