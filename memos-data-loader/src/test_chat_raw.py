#!/usr/bin/env python3
"""
Raw SSE stream capture for chat debugging
"""
import requests
import json

BASE_URL = "http://localhost:8001"
USER_ID = "test1_user"

def chat_raw(query):
    """Capture raw SSE stream"""
    payload = {
        "user_id": USER_ID,
        "query": query,
        "internet_search": False
    }

    print(f"Query: {query}")
    print("=" * 80)

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

        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print("\nSSE Stream Content:")
        print("-" * 80)

        event_count = 0
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                print(line_str)
                event_count += 1

                if event_count > 100:  # Safety limit
                    print("\n[... truncated after 100 events]")
                    break

        print("-" * 80)
        print(f"Total events: {event_count}")

    except Exception as e:
        print(f"Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response text: {e.response.text[:500]}")

print("\n" + "=" * 80)
print("RAW SSE STREAM TEST")
print("=" * 80 + "\n")

chat_raw("What test message did I send?")

print("\n" + "=" * 80)
print("TEST COMPLETE")
print("=" * 80)
