#!/usr/bin/env python3
"""
Chat interface test for docker-test1 API
Tests SSE streaming chat with memory retrieval
"""
import requests
import json
import re

BASE_URL = "http://localhost:8001"
USER_ID = "test1_user"

def chat_stream(query, internet_search=False, session_id=None):
    """Send a chat query and handle SSE stream response"""
    payload = {
        "user_id": USER_ID,
        "query": query,
        "internet_search": internet_search
    }

    if session_id:
        payload["session_id"] = session_id

    try:
        response = requests.post(
            f"{BASE_URL}/product/chat",
            json=payload,
            headers={
                "Content-Type": "application/json",
                "Accept": "text/event-stream"
            },
            stream=True,
            timeout=60
        )

        response.raise_for_status()

        # Parse SSE stream
        full_response = ""
        memories_retrieved = []
        metadata = {}

        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')

                # SSE format: "data: {json}"
                if line.startswith('data: '):
                    data_str = line[6:]  # Remove "data: " prefix

                    # Skip [DONE] marker
                    if data_str.strip() == '[DONE]':
                        continue

                    try:
                        data = json.loads(data_str)

                        # Accumulate response chunks
                        if 'chunk' in data:
                            full_response += data['chunk']

                        # Capture memories if present
                        if 'memories' in data:
                            memories_retrieved = data['memories']

                        # Capture any other metadata
                        if 'metadata' in data:
                            metadata = data['metadata']

                    except json.JSONDecodeError:
                        # Some SSE events might not be JSON
                        continue

        return {
            "response": full_response,
            "memories": memories_retrieved,
            "metadata": metadata
        }

    except requests.exceptions.RequestException as e:
        return {
            "error": str(e),
            "status_code": getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None
        }

def print_chat_result(query, result, test_num):
    """Pretty print chat results"""
    print("=" * 80)
    print(f"TEST {test_num}: Chat Query")
    print("=" * 80)
    print(f"Query: {query}")
    print("-" * 80)

    if "error" in result:
        print(f"❌ Error: {result['error']}")
        if result.get('status_code'):
            print(f"   Status Code: {result['status_code']}")
        return

    response = result.get("response", "").strip()
    memories = result.get("memories", [])
    metadata = result.get("metadata", {})

    if response:
        print(f"\n💬 Assistant Response:")
        print(f"{response}")
    else:
        print("\n⚠️  No response generated")

    if memories:
        print(f"\n🧠 Memories Retrieved ({len(memories)}):")
        for i, memory in enumerate(memories[:3], 1):  # Show top 3
            print(f"\n  {i}. {memory.get('memory', memory.get('content', 'N/A'))[:150]}")
            if 'score' in memory:
                print(f"     Score: {memory['score']:.4f}")
    else:
        print("\n⚠️  No memories retrieved")

    if metadata:
        print(f"\n📊 Metadata:")
        print(f"   {json.dumps(metadata, indent=4)[:200]}")

    print("\n")

# Test queries based on our loaded memories
test_queries = [
    "What test message did I send?",
    "What was I testing?",
    "Tell me about the docker environment",
    "What do you remember about my recent activity?",
]

print("\n" + "💬" * 40)
print("CHAT INTERFACE TEST SUITE")
print("Testing memory-augmented chat with 3 loaded vectors")
print("💬" * 40 + "\n")

for i, query in enumerate(test_queries, 1):
    result = chat_stream(query, internet_search=False)
    print_chat_result(query, result, i)

print("=" * 80)
print("CHAT TESTS COMPLETE")
print("=" * 80)
