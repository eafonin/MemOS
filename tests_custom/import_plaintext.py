#!/usr/bin/env python3
import requests
import json
import os
from pathlib import Path

API_BASE = "http://localhost:8000"

def register_user():
    """Register a user for data import"""
    try:
        response = requests.post(f"{API_BASE}/product/users/register", json={})
        response.raise_for_status()  # Raise error for bad status codes
        
        data = response.json()
        print(f"Registration response: {json.dumps(data, indent=2)}")
        
        # Handle different possible response structures
        if 'data' in data and data['data'] is not None:
            # Expected format from documentation
            return data['data']['user_id'], data['data']['mem_cube_id']
        elif 'user_id' in data and 'mem_cube_id' in data:
            # Alternative format (direct keys)
            return data['user_id'], data['mem_cube_id']
        else:
            # Fallback: print response and raise error
            raise ValueError(f"Unexpected response format. Full response: {data}")
            
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to API: {e}")
        raise
    except Exception as e:
        print(f"Error parsing response: {e}")
        raise

def import_text_file(user_id, mem_cube_id, file_path):
    """Import a single text file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    payload = {
        "user_id": user_id,
        "mem_cube_id": mem_cube_id,
        "messages": [
            {
                "role": "user",
                "content": content
            }
        ],
        "memory_content": "",
        "doc_path": str(file_path),
        "source": file_path.name,
        "user_profile": False
    }
    
    try:
        response = requests.post(f"{API_BASE}/product/add", json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error adding memory: {e}")
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        raise

def import_json_file(user_id, mem_cube_id, file_path):
    """Import a JSON file (assumes it contains text data)"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Adjust this based on your JSON structure
    if isinstance(data, dict) and 'content' in data:
        content = data['content']
    elif isinstance(data, list):
        content = "\n".join([str(item) for item in data])
    else:
        content = json.dumps(data, indent=2)
    
    payload = {
        "user_id": user_id,
        "mem_cube_id": mem_cube_id,
        "messages": [
            {
                "role": "user",
                "content": content
            }
        ],
        "memory_content": "",
        "doc_path": str(file_path),
        "source": file_path.name,
        "user_profile": False
    }
    
    try:
        response = requests.post(f"{API_BASE}/product/add", json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error adding memory: {e}")
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        raise

def test_connection():
    """Test if the API is accessible"""
    try:
        response = requests.get(f"{API_BASE}/docs", timeout=5)
        response.raise_for_status()
        print("✅ API connection successful")
        return True
    except Exception as e:
        print(f"❌ Cannot connect to API at {API_BASE}")
        print(f"Error: {e}")
        print("\nMake sure:")
        print("1. Docker container is running (docker compose up)")
        print("2. API is accessible at http://localhost:8000")
        return False

def import_directory(data_dir, user_id=None, mem_cube_id=None):
    """Import all .txt and .json files from a directory"""
    
    # Test connection first
    if not test_connection():
        return None, None
    
    if not user_id or not mem_cube_id:
        print("\nRegistering new user...")
        try:
            user_id, mem_cube_id = register_user()
            print(f"✅ Created user: {user_id}")
            print(f"✅ MemCube ID: {mem_cube_id}")
        except Exception as e:
            print(f"❌ Failed to register user: {e}")
            return None, None
    
    data_path = Path(data_dir)
    imported = 0
    failed = 0
    
    # Import .txt files
    txt_files = list(data_path.glob("**/*.txt"))
    json_files = list(data_path.glob("**/*.json"))
    
    total_files = len(txt_files) + len(json_files)
    print(f"\nFound {total_files} files to import ({len(txt_files)} .txt, {len(json_files)} .json)")
    print("="*60)
    
    for txt_file in txt_files:
        print(f"\nImporting: {txt_file.name}")
        try:
            result = import_text_file(user_id, mem_cube_id, txt_file)
            print(f" ✅ Success: {result.get('message', 'OK')}")
            imported += 1
        except Exception as e:
            print(f" ❌ Error: {e}")
            failed += 1
    
    # Import .json files
    for json_file in json_files:
        print(f"\nImporting: {json_file.name}")
        try:
            result = import_json_file(user_id, mem_cube_id, json_file)
            print(f" ✅ Success: {result.get('message', 'OK')}")
            imported += 1
        except Exception as e:
            print(f" ❌ Error: {e}")
            failed += 1
    
    print(f"\n{'='*60}")
    print(f"Import complete:")
    print(f"  ✅ Successfully imported: {imported} files")
    if failed > 0:
        print(f"  ❌ Failed: {failed} files")
    print(f"\nUser ID: {user_id}")
    print(f"MemCube ID: {mem_cube_id}")
    print(f"{'='*60}")
    
    return user_id, mem_cube_id

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 import_plaintext.py <data_directory> [user_id] [mem_cube_id]")
        print("\nExamples:")
        print("  python3 import_plaintext.py ./my_documents")
        print("  python3 import_plaintext.py ./my_documents user123 cube456")
        sys.exit(1)
    
    data_dir = sys.argv[1]
    
    if not os.path.exists(data_dir):
        print(f"Error: Directory '{data_dir}' does not exist")
        sys.exit(1)
    
    # Optional: use existing user_id and mem_cube_id
    user_id = sys.argv[2] if len(sys.argv) > 2 else None
    mem_cube_id = sys.argv[3] if len(sys.argv) > 3 else None
    
    import_directory(data_dir, user_id, mem_cube_id)
