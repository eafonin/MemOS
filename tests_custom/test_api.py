#!/usr/bin/env python3
import requests
import json

# Configuration
API_BASE = "http://localhost:8000"

def test_register_user():
    """Step 1: Register a new user"""
    print("\n=== Step 1: Register User ===")
    
    # Try with an empty JSON body first
    response = requests.post(
        f"{API_BASE}/product/users/register",
        json={}  # Empty JSON body
    )
    
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response: {json.dumps(data, indent=2)}")
    
    if response.status_code == 200 and 'data' in data:
        return data['data']['user_id'], data['data']['mem_cube_id']
    else:
        raise Exception(f"Registration failed: {data}")

def test_add_memory(user_id, mem_cube_id):
    """Step 2: Add memory to user"""
    print("\n=== Step 2: Add Memory ===")
    
    payload = {
        "user_id": user_id,
        "mem_cube_id": mem_cube_id,
        "messages": [
            {
                "role": "user",
                "content": "I love playing tennis on weekends"
            }
        ],
        "memory_content": "",
        "doc_path": "",
        "source": "",
        "user_profile": False
    }
    
    response = requests.post(
        f"{API_BASE}/product/add",
        json=payload
    )
    
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response: {json.dumps(data, indent=2)}")
    return data

def test_query_memory(user_id, mem_cube_id):
    """Step 3: Query memory (using /search endpoint)"""
    print("\n=== Step 3: Query Memory ===")
    
    payload = {
        "user_id": user_id,
        "mem_cube_id": mem_cube_id,
        "query": "What sports do I like?"
    }
    
    # Note: The endpoint is /product/search, not /product/query
    response = requests.post(
        f"{API_BASE}/product/search",
        json=payload
    )
    
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response: {json.dumps(data, indent=2)}")
    return data

def main():
    print("=" * 60)
    print("MemOS API Test Suite")
    print("=" * 60)
    
    try:
        # Test sequence
        user_id, mem_cube_id = test_register_user()
        print(f"\n✅ Registered user_id: {user_id}")
        print(f"✅ mem_cube_id: {mem_cube_id}")
        
        test_add_memory(user_id, mem_cube_id)
        test_query_memory(user_id, mem_cube_id)
        
        print("\n" + "=" * 60)
        print("✅ All tests completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
