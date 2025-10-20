#!/usr/bin/env python3
"""
Test Neo4j fix by adding a new memory
"""
import requests
import json

BASE_URL = "http://localhost:8001"
USER_ID = "test1_user"

print("=" * 80)
print("TESTING NEO4J FIX")
print("=" * 80)
print()

# Add a new test memory
print("Step 1: Adding new test memory...")
payload = {
    "user_id": USER_ID,
    "messages": [
        {
            "role": "user",
            "content": "This is a test after the Neo4j fix was applied!"
        },
        {
            "role": "assistant",
            "content": "Great! I've stored your message with the fixed Neo4j storage."
        }
    ],
    "source": "neo4j_fix_test"
}

try:
    response = requests.post(
        f"{BASE_URL}/product/add",
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=30
    )

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

    if response.status_code == 200:
        print("\n✅ SUCCESS: Memory added without errors!")
    else:
        print(f"\n❌ ERROR: {response.status_code}")
        exit(1)

except Exception as e:
    print(f"❌ Exception: {e}")
    exit(1)

print()
print("=" * 80)
print("TEST COMPLETE - Checking API logs for errors...")
print("=" * 80)
