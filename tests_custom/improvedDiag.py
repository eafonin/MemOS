#!/usr/bin/env python3
"""
Improved MemOS Test Script with Better Error Handling
"""

import requests
import json
import re
import time
import sys
from pathlib import Path
from typing import Tuple, Optional, Dict, Any, List

API_BASE = "http://localhost:8000"

class MemOSClient:
    def __init__(self, base_url: str = API_BASE):
        self.base_url = base_url
        self.user_id = None
        self.mem_cube_id = None
    
    def check_health(self) -> bool:
        """Check if API is healthy"""
        try:
            response = requests.get(f"{self.base_url}/docs", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def register_user(self) -> Tuple[Optional[str], Optional[str]]:
        """Register a new user with proper error handling"""
        print("\n📝 Registering new user...")
        
        try:
            # Try with empty JSON body
            response = requests.post(
                f"{self.base_url}/product/users/register",
                json={},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            print(f"   Status: {response.status_code}")
            
            # Check if response has content
            if not response.content:
                print("   ⚠️ Empty response received")
                return None, None
            
            # Try to parse JSON
            try:
                data = response.json()
            except json.JSONDecodeError as e:
                print(f"   ❌ Invalid JSON: {e}")
                print(f"   Raw response: {response.text[:200]}")
                return None, None
            
            # Handle successful registration
            if response.status_code == 200:
                if 'data' in data and data['data']:
                    self.user_id = data['data'].get('user_id')
                    self.mem_cube_id = data['data'].get('mem_cube_id')
                    print(f"   ✅ User ID: {self.user_id}")
                    print(f"   ✅ MemCube ID: {self.mem_cube_id}")
                    return self.user_id, self.mem_cube_id
                else:
                    print(f"   ⚠️ Unexpected response structure: {data}")
            else:
                print(f"   ❌ Registration failed: {data.get('message', 'Unknown error')}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Request failed: {e}")
        
        return None, None
    
    def add_memory_from_text(self, content: str, source: str = "test") -> bool:
        """Add memory with simplified structure to avoid Neo4j issues"""
        if not self.user_id or not self.mem_cube_id:
            print("❌ No user registered")
            return False
        
        print(f"\n💾 Adding memory from {source}...")
        
        # Simplified payload structure
        payload = {
            "user_id": self.user_id,
            "mem_cube_id": self.mem_cube_id,
            "messages": [
                {
                    "role": "user",
                    "content": content
                }
            ],
            "memory_content": "",  # Keep empty to avoid duplication
            "doc_path": "",        # Keep empty to avoid Neo4j issues
            "source": source,
            "user_profile": False
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/product/add",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            print(f"   Status: {response.status_code}")
            
            if response.content:
                try:
                    data = response.json()
                    if response.status_code == 200:
                        print(f"   ✅ {data.get('message', 'Memory added')}")
                        # Wait for processing
                        time.sleep(1)
                        return True
                    else:
                        print(f"   ❌ {data.get('message', 'Failed')}")
                except json.JSONDecodeError:
                    print(f"   ⚠️ Non-JSON response: {response.text[:100]}")
            
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Request failed: {e}")
        
        return False
    
    def search_memory(self, query: str) -> Dict[str, Any]:
        """Search memories with detailed results"""
        if not self.user_id or not self.mem_cube_id:
            print("❌ No user registered")
            return {}
        
        print(f"\n🔍 Searching for: '{query}'")
        
        payload = {
            "user_id": self.user_id,
            "mem_cube_id": self.mem_cube_id,
            "query": query
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/product/search",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            print(f"   Status: {response.status_code}")
            
            if response.content:
                try:
                    data = response.json()
                    if response.status_code == 200:
                        # Extract memories
                        results = data.get('data', {})
                        text_mems = results.get('text_mem', [])
                        
                        if text_mems and len(text_mems) > 0:
                            memories = text_mems[0].get('memories', [])
                            if memories:
                                print(f"   ✅ Found {len(memories)} memories:")
                                for i, mem in enumerate(memories[:3], 1):
                                    print(f"      {i}. {mem[:100]}...")
                            else:
                                print("   ⚠️ No memories found")
                        else:
                            print("   ⚠️ Empty results")
                        
                        return results
                    else:
                        print(f"   ❌ Search failed: {data.get('message', 'Unknown error')}")
                        
                except json.JSONDecodeError as e:
                    print(f"   ⚠️ Invalid JSON: {e}")
            
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Request failed: {e}")
        
        return {}
    
    def chat(self, message: str) -> str:
        """Chat with MemOS"""
        if not self.user_id or not self.mem_cube_id:
            print("❌ No user registered")
            return ""
        
        print(f"\n💬 Chatting: '{message}'")
        
        payload = {
            "user_id": self.user_id,
            "mem_cube_id": self.mem_cube_id,
            "query": message,
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ]
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/product/chat",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=60
            )
            
            print(f"   Status: {response.status_code}")
            
            # Handle empty or non-JSON responses
            if not response.content or len(response.content) == 0:
                print("   ⚠️ Empty response from chat endpoint")
                return ""
            
            try:
                # First check if it's JSON
                data = response.json()
                
                if response.status_code == 200:
                    # Different possible response structures
                    if isinstance(data, dict):
                        answer = data.get('answer') or data.get('response') or data.get('message', '')
                    elif isinstance(data, str):
                        answer = data
                    else:
                        answer = str(data)
                    
                    if answer:
                        print(f"   ✅ Response: {answer[:200]}...")
                        return answer
                    else:
                        print("   ⚠️ No answer in response")
                        print(f"   Full response: {json.dumps(data, indent=2)}")
                else:
                    print(f"   ❌ Chat failed: {data.get('message', 'Unknown error')}")
                    
            except json.JSONDecodeError:
                # Maybe it's plain text?
                text = response.text.strip()
                if text:
                    print(f"   ℹ️ Plain text response: {text[:200]}...")
                    return text
                else:
                    print("   ❌ Invalid response format")
            
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Request failed: {e}")
        
        return ""

def is_valid_text_content(content: str) -> bool:
    """
    Check if content is meaningful text (not embeddings/vectors).

    Returns False if content looks like numeric vector data.
    """
    if not content or len(content.strip()) < 20:
        return False

    # Count numeric tokens vs total tokens
    tokens = content.split()
    if len(tokens) == 0:
        return False

    numeric_tokens = len(re.findall(r'^-?\d+\.?\d*$', ' '.join(tokens)))
    numeric_ratio = numeric_tokens / len(tokens)

    # If more than 80% numeric, it's probably vector data
    if numeric_ratio > 0.8:
        return False

    # Check for comma-separated float pattern (embeddings)
    if re.search(r'^[\d\.,\s-]+$', content.strip()):
        comma_count = content.count(',')
        if comma_count > 50:  # Embeddings typically have 100+ values
            return False

    return True

def smart_chunk(content: str, max_size: int = 1000) -> List[str]:
    """
    Split content intelligently on sentence boundaries.

    Better than fixed-size chunking because it:
    - Preserves sentence integrity
    - Avoids breaking mid-sentence
    - Provides better context for LLM processing
    """
    # First filter out obvious vector data
    if not is_valid_text_content(content):
        return []

    # Split on sentence boundaries
    sentences = re.split(r'(?<=[.!?])\s+', content)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        # Skip if sentence itself looks like vector data
        if not is_valid_text_content(sentence):
            continue

        if len(current_chunk) + len(sentence) + 1 < max_size:
            current_chunk += sentence + " "
        else:
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
            current_chunk = sentence + " "

    # Add final chunk
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks

def load_sample_data(client: MemOSClient, data_dir: str = "./sample_docs"):
    """Load sample documents"""
    print("\n📂 Loading sample data...")
    
    data_path = Path(data_dir)
    if not data_path.exists():
        print(f"   ❌ Directory {data_dir} not found")
        return False
    
    success_count = 0
    
    # Load text files
    for txt_file in data_path.glob("*.txt"):
        print(f"\n   📄 Loading {txt_file.name}")
        try:
            content = txt_file.read_text(encoding='utf-8')

            # Use smart chunking with validation
            chunks = smart_chunk(content, max_size=1000)

            if not chunks:
                print(f"      ⚠️ No valid text content found (possibly vector data)")
                continue

            print(f"      ℹ️ Split into {len(chunks)} chunks")

            for i, chunk in enumerate(chunks):
                if client.add_memory_from_text(chunk, f"{txt_file.name}_chunk{i}"):
                    success_count += 1

        except Exception as e:
            print(f"      ❌ Error: {e}")
    
    # Load JSON files
    for json_file in data_path.glob("*.json"):
        print(f"\n   📋 Loading {json_file.name}")
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Extract text content from JSON
            if isinstance(data, dict) and 'content' in data:
                content = data['content']
            else:
                content = json.dumps(data)

            # Validate and chunk JSON content
            chunks = smart_chunk(content, max_size=1000)

            if not chunks:
                print(f"      ⚠️ No valid text content found")
                continue

            print(f"      ℹ️ Split into {len(chunks)} chunks")

            for i, chunk in enumerate(chunks):
                if client.add_memory_from_text(chunk, f"{json_file.name}_chunk{i}"):
                    success_count += 1

        except Exception as e:
            print(f"      ❌ Error: {e}")
    
    print(f"\n   ✅ Loaded {success_count} documents")
    return success_count > 0

def run_tests(client: MemOSClient):
    """Run comprehensive tests"""
    print("\n" + "="*60)
    print("🧪 RUNNING TESTS")
    print("="*60)
    
    # Test 1: Direct memory addition
    print("\n1️⃣ Testing direct memory addition...")
    test_memories = [
        "Docker is a containerization platform that packages applications",
        "MemOS is an advanced memory management system",
        "Python is a high-level programming language"
    ]
    
    for mem in test_memories:
        client.add_memory_from_text(mem, "test_direct")
    
    # Wait for indexing
    print("\n⏳ Waiting for indexing...")
    time.sleep(3)
    
    # Test 2: Search functionality
    print("\n2️⃣ Testing search functionality...")
    test_queries = ["Docker", "MemOS", "Python", "containerization", "memory management"]
    
    for query in test_queries:
        results = client.search_memory(query)
    
    # Test 3: Chat functionality
    print("\n3️⃣ Testing chat functionality...")
    test_chats = [
        "What do you know about Docker?",
        "Tell me about memory management",
        "What programming languages are mentioned?"
    ]
    
    for chat in test_chats:
        response = client.chat(chat)

def main():
    print("="*60)
    print("🚀 MemOS Improved Test Suite")
    print("="*60)
    
    client = MemOSClient()
    
    # Check health
    print("\n🏥 Checking API health...")
    if not client.check_health():
        print("❌ API is not responding. Please check Docker containers.")
        sys.exit(1)
    print("✅ API is healthy")
    
    # Register user
    user_id, mem_cube_id = client.register_user()
    if not user_id:
        print("\n❌ Failed to register user. Aborting.")
        sys.exit(1)
    
    # Load sample data if directory exists
    if Path("./sample_docs").exists():
        load_sample_data(client, "./sample_docs")
    
    # Run tests
    run_tests(client)
    
    print("\n" + "="*60)
    print("✅ Test suite completed")
    print(f"User ID: {client.user_id}")
    print(f"MemCube ID: {client.mem_cube_id}")
    print("="*60)

if __name__ == "__main__":
    main()