#!/usr/bin/env python3
"""
Test search functionality with loaded documentation
"""
import os
import sys
import json
import requests
from dotenv import load_dotenv


def search_memory(base_url: str, user_id: str, query: str, top_k: int = 5):
    """Search for memories"""
    url = f"{base_url}/product/search"
    payload = {
        "user_id": user_id,
        "query": query,
        "top_k": top_k
    }

    print(f"\n{'='*70}")
    print(f"Query: {query}")
    print(f"{'='*70}")

    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()

        if result.get("code") == 200:
            data = result.get("data", {})
            text_mem_list = data.get("text_mem", [])

            # Extract all memories from all cubes
            text_results = []
            for item in text_mem_list:
                if isinstance(item, dict):
                    memories = item.get("memories", [])
                    text_results.extend(memories)

            print(f"✓ Found {len(text_results)} results")

            for i, mem in enumerate(text_results[:3], 1):
                metadata = mem.get('metadata', {})
                relativity = metadata.get('relativity', 0)
                key = metadata.get('key', 'N/A')
                memory_type = metadata.get('memory_type', 'N/A')
                memory_text = mem.get('memory', '')[:200]

                print(f"\n[{i}] Relevance: {relativity:.4f}")
                print(f"    Key: {key[:80]}...")
                print(f"    Type: {memory_type}")
                print(f"    Memory: {memory_text}...")

            return len(text_results)
        else:
            print(f"✗ Error: {result}")
            return 0

    except Exception as e:
        print(f"✗ Exception: {e}")
        return 0


def main():
    load_dotenv()

    base_url = os.getenv('MEMOS_BASE_URL', 'http://localhost:8001')
    user_id = os.getenv('MEMOS_USER_ID', 'test1_user')

    print(f"\n{'='*70}")
    print(f"MemOS Search Functionality Test")
    print(f"{'='*70}")
    print(f"Base URL: {base_url}")
    print(f"User ID: {user_id}")

    # Test queries covering different topics from the loaded docs
    test_queries = [
        "What is MemOS and how does it work?",
        "Neo4j graph database configuration",
        "How to install and set up MemOS?",
        "Memory types in MemOS architecture",
        "REST API endpoints and usage",
        "Chunking and embedding strategies"
    ]

    total_results = 0
    successful_queries = 0

    for query in test_queries:
        count = search_memory(base_url, user_id, query, top_k=5)
        if count > 0:
            successful_queries += 1
            total_results += count

    print(f"\n{'='*70}")
    print(f"SEARCH TEST SUMMARY")
    print(f"{'='*70}")
    print(f"Total queries: {len(test_queries)}")
    print(f"Successful queries: {successful_queries}/{len(test_queries)}")
    print(f"Total results returned: {total_results}")
    print(f"Average results per query: {total_results/len(test_queries):.1f}")

    if successful_queries == len(test_queries) and total_results > 0:
        print(f"\n✓ SEARCH FUNCTIONALITY WORKING CORRECTLY")
    else:
        print(f"\n⚠ SEARCH FUNCTIONALITY NEEDS INVESTIGATION")


if __name__ == "__main__":
    main()
