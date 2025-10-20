#!/usr/bin/env python3
"""
Direct Qdrant search test to verify vectors are searchable
"""
import requests
import json

QDRANT_URL = "http://localhost:6334"
COLLECTION = "neo4j_vec_db"
TEI_URL = "http://localhost:8081"

def get_embedding(text):
    """Get embedding from TEI service"""
    response = requests.post(
        f"{TEI_URL}/embed",
        json={"inputs": text},
        headers={"Content-Type": "application/json"},
        timeout=30
    )
    response.raise_for_status()
    # TEI returns a list of embeddings
    return response.json()[0]

def search_qdrant(query_text, limit=3):
    """Search Qdrant directly with a query"""
    # Get query embedding
    print(f"Getting embedding for: '{query_text}'")
    query_vector = get_embedding(query_text)
    print(f"✓ Embedding generated (dim: {len(query_vector)})")

    # Search Qdrant
    search_payload = {
        "vector": query_vector,
        "limit": limit,
        "with_payload": True,
        "with_vector": False,
        "filter": {
            "must": [
                {"key": "user_id", "match": {"value": "test1_user"}}
            ]
        }
    }

    response = requests.post(
        f"{QDRANT_URL}/collections/{COLLECTION}/points/search",
        json=search_payload,
        headers={"Content-Type": "application/json"},
        timeout=30
    )
    response.raise_for_status()
    return response.json()

# Test queries
test_queries = [
    "test message",
    "docker environment testing",
    "greeting hello",
    "assistant stored message"
]

print("=" * 80)
print("DIRECT QDRANT SEARCH TEST")
print("=" * 80)
print()

for i, query in enumerate(test_queries, 1):
    print(f"\n{'=' * 80}")
    print(f"TEST {i}: '{query}'")
    print('=' * 80)

    try:
        results = search_qdrant(query)

        points = results.get('result', [])

        if not points:
            print("⚠️  No results found")
        else:
            print(f"✅ Found {len(points)} results:\n")

            for j, point in enumerate(points, 1):
                payload = point.get('payload', {})
                score = point.get('score', 0)

                print(f"  Result {j}:")
                print(f"    Score: {score:.4f}")
                print(f"    Memory: {payload.get('memory', 'N/A')}")
                print(f"    Type: {payload.get('memory_type', 'N/A')}")
                print(f"    Status: {payload.get('status', 'N/A')}")
                print(f"    Tags: {payload.get('tags', [])}")
                print()

    except Exception as e:
        print(f"❌ Error: {e}")

print("=" * 80)
print("DIRECT SEARCH COMPLETE")
print("=" * 80)
