#!/usr/bin/env python3
"""
Quick test script for docker-test1 API
"""
import requests
import json

BASE_URL = "http://localhost:8001"
USER_ID = "test1_user"

print("=" * 60)
print("Step 1: Register User")
print("=" * 60)

register_payload = {
    "user_id": USER_ID,
    "user_name": "Test User",
    "interests": "Testing MemOS docker-test1 environment"
}

print(f"Endpoint: {BASE_URL}/product/users/register")
print(f"Payload: {json.dumps(register_payload, indent=2)}")
print()

try:
    response = requests.post(
        f"{BASE_URL}/product/users/register",
        json=register_payload,
        headers={"Content-Type": "application/json"},
        timeout=30
    )

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text[:500]}")

    if response.status_code == 200:
        print("\n✅ User registered successfully!")
    else:
        print(f"\n⚠️  Registration response: {response.status_code}")
        print("(User might already be registered)")

except Exception as e:
    print(f"❌ Exception during registration: {e}")

print("\n" + "=" * 60)
print("Step 2: Add Memory")
print("=" * 60)

add_payload = {
    "user_id": USER_ID,
    "messages": [
        {
            "role": "user",
            "content": "Test message: Hello MemOS docker-test1!"
        },
        {
            "role": "assistant",
            "content": "I have stored your test message."
        }
    ],
    "source": "manual_test"
}

print(f"Endpoint: {BASE_URL}/product/add")
print(f"Payload: {json.dumps(add_payload, indent=2)}")
print()

try:
    response = requests.post(
        f"{BASE_URL}/product/add",
        json=add_payload,
        headers={"Content-Type": "application/json"},
        timeout=30
    )

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

    if response.status_code == 200:
        print("\n✅ SUCCESS: Memory added successfully!")
    else:
        print(f"\n❌ ERROR: {response.status_code}")

except Exception as e:
    print(f"❌ Exception: {e}")
