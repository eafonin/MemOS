#!/usr/bin/env python3
"""
MemOS Query Script - Search and retrieve memories from MemOS
"""
import requests
import json
import sys
import argparse

API_BASE = "http://localhost:8000"

def search_memory(user_id, mem_cube_id, query):
    """Search for memories matching the query"""
    try:
        response = requests.post(
            f"{API_BASE}/product/search",
            json={
                'user_id': user_id,
                'mem_cube_id': mem_cube_id,
                'query': query
            }
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error querying memory: {e}", file=sys.stderr)
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}", file=sys.stderr)
        sys.exit(1)

def chat_with_memory(user_id, mem_cube_id, message):
    """Chat with MemOS using stored memories"""
    try:
        response = requests.post(
            f"{API_BASE}/product/chat",
            json={
                'user_id': user_id,
                'mem_cube_id': mem_cube_id,
                'query': message
            }
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error in chat: {e}", file=sys.stderr)
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}", file=sys.stderr)
        sys.exit(1)

def format_search_results(data):
    """Format search results in a readable way"""
    print("\n" + "="*60)
    print("SEARCH RESULTS")
    print("="*60)
    
    if 'data' in data and data['data']:
        results = data['data']
        if isinstance(results, dict):
            print(json.dumps(results, indent=2))
        elif isinstance(results, list):
            for i, result in enumerate(results, 1):
                print(f"\n--- Result {i} ---")
                if isinstance(result, dict):
                    for key, value in result.items():
                        print(f"{key}: {value}")
                else:
                    print(result)
        else:
            print(results)
    else:
        print("\nNo results found or empty response")
        print(f"\nFull response:\n{json.dumps(data, indent=2)}")
    
    print("\n" + "="*60)

def format_chat_response(data):
    """Format chat response in a readable way"""
    print("\n" + "="*60)
    print("CHAT RESPONSE")
    print("="*60)
    
    if 'data' in data:
        response_text = data['data']
        print(f"\n{response_text}\n")
    else:
        print(f"\n{json.dumps(data, indent=2)}\n")
    
    print("="*60)

def main():
    parser = argparse.ArgumentParser(
        description='Query and chat with MemOS memories',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Search for memories
  python3 query_memory.py <user_id> <mem_cube_id> search "What is Docker?"
  
  # Chat with memories (uses AI to generate response)
  python3 query_memory.py <user_id> <mem_cube_id> chat "Tell me about Docker"
  
  # Output as JSON
  python3 query_memory.py <user_id> <mem_cube_id> search "Docker" --json
        """
    )
    
    parser.add_argument('user_id', help='User ID from registration')
    parser.add_argument('mem_cube_id', help='MemCube ID from registration')
    parser.add_argument('action', choices=['search', 'chat'], 
                       help='Action to perform: search (retrieve memories) or chat (AI response)')
    parser.add_argument('query', help='Query or message to send')
    parser.add_argument('--json', action='store_true', 
                       help='Output raw JSON response')
    parser.add_argument('--api-base', default="http://localhost:8000",
                       help='API base URL (default: http://localhost:8000)')
    
    args = parser.parse_args()
    
    # Update API base if provided
    if args.api_base != "http://localhost:8000":
        global API_BASE
        API_BASE = args.api_base
    
    # Execute action
    if args.action == 'search':
        print(f"🔍 Searching for: '{args.query}'")
        result = search_memory(args.user_id, args.mem_cube_id, args.query)
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            format_search_results(result)
    
    elif args.action == 'chat':
        print(f"💬 Chatting with MemOS: '{args.query}'")
        result = chat_with_memory(args.user_id, args.mem_cube_id, args.query)
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            format_chat_response(result)

if __name__ == "__main__":
    main()
