#!/usr/bin/env python3
"""
Chat test with assembled responses
"""
import requests
import json

BASE_URL = "http://localhost:8001"
USER_ID = "test1_user"

def chat_and_assemble(query):
    """Send chat query and assemble full response"""
    payload = {
        "user_id": USER_ID,
        "query": query,
        "internet_search": False
    }

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

        full_text = ""
        references = []
        suggestions = []
        time_data = {}

        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')

                if line_str.startswith('data: '):
                    data_str = line_str[6:]

                    try:
                        data = json.loads(data_str)
                        data_type = data.get('type')

                        if data_type == 'text':
                            full_text += data.get('data', '')
                        elif data_type == 'reference':
                            references = data.get('data', [])
                        elif data_type == 'suggestion':
                            suggestions = data.get('data', [])
                        elif data_type == 'time':
                            time_data = data.get('data', {})

                    except json.JSONDecodeError:
                        continue

        return {
            "response": full_text,
            "references": references,
            "suggestions": suggestions,
            "time": time_data
        }

    except Exception as e:
        return {"error": str(e)}

# Test queries
test_queries = [
    "What test message did I send?",
    "What was I testing?",
    "Hello! Can you help me?",
]

print("\n" + "💬" * 40)
print("CHAT INTERFACE TEST - ASSEMBLED RESPONSES")
print("💬" * 40 + "\n")

for i, query in enumerate(test_queries, 1):
    print(f"\n{'=' * 80}")
    print(f"TEST {i}")
    print('=' * 80)
    print(f"Query: {query}\n")

    result = chat_and_assemble(query)

    if "error" in result:
        print(f"❌ Error: {result['error']}")
    else:
        print(f"💬 Response:")
        print(result['response'])

        if result['references']:
            print(f"\n📚 References ({len(result['references'])}):")
            for ref in result['references'][:3]:
                print(f"  - {ref}")
        else:
            print(f"\n⚠️  No memories referenced")

        if result['suggestions']:
            print(f"\n💡 Suggestions:")
            for sug in result['suggestions']:
                print(f"  - {sug}")

        if result['time']:
            print(f"\n⏱️  Performance:")
            print(f"  Total time: {result['time'].get('total_time', 'N/A')}s")
            print(f"  Speed improvement: {result['time'].get('speed_improvement', 'N/A')}")

print("\n" + "=" * 80)
print("CHAT TESTS COMPLETE")
print("=" * 80)
