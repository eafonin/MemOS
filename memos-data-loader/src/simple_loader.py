#!/usr/bin/env python3
"""
MemOS Data Loader - Simple Prototype
Budget-conscious loader for testing MemOS Dashboard API
"""
import os
import sys
import json
import argparse
from datetime import datetime
from typing import List, Dict, Optional
import requests
from dotenv import load_dotenv


class MemosLoader:
    """Simple MemOS API client for data loading"""

    def __init__(self, api_key: str, base_url: str, dry_run: bool = False):
        self.base_url = base_url
        self.dry_run = dry_run
        self.headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Token {api_key}"
        }

    def add_message(
        self,
        user_id: str,
        conversation_id: str,
        messages: List[Dict[str, str]]
    ) -> Dict:
        """Add messages to MemOS"""
        url = f"{self.base_url}/add/message"
        payload = {
            "user_id": user_id,
            "conversation_id": conversation_id,
            "messages": messages
        }

        # Log the request
        print(f"\n{'[DRY-RUN] ' if self.dry_run else ''}POST {url}")
        print(f"Payload: {json.dumps(payload, indent=2, ensure_ascii=False)[:500]}...")

        if self.dry_run:
            return {"status": "dry-run", "message": "No actual API call made"}

        try:
            response = requests.post(
                url,
                json=payload,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            print(f"✓ Success: {result}")
            return result
        except requests.exceptions.RequestException as e:
            print(f"✗ Error: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            raise

    def search_memory(
        self,
        user_id: str,
        query: str,
        conversation_id: Optional[str] = None,
        memory_limit: int = 6
    ) -> Dict:
        """Search memories in MemOS"""
        url = f"{self.base_url}/search/memory"
        payload = {
            "user_id": user_id,
            "query": query,
            "conversation_id": conversation_id,
            "memory_limit_number": memory_limit
        }

        print(f"\n{'[DRY-RUN] ' if self.dry_run else ''}POST {url}")
        print(f"Query: {query}")

        if self.dry_run:
            return {"status": "dry-run", "message": "No actual API call made"}

        try:
            response = requests.post(
                url,
                json=payload,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            print(f"✓ Found memories: {json.dumps(result, indent=2, ensure_ascii=False)[:500]}...")
            return result
        except requests.exceptions.RequestException as e:
            print(f"✗ Error: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            raise


def text_to_messages(text: str, source: str = "cli") -> List[Dict[str, str]]:
    """Convert plain text to MemOS message format"""
    # Simple conversation format: user provides the scan result
    messages = [
        {
            "role": "user",
            "content": f"Here is output from {source}:\n\n{text}"
        },
        {
            "role": "assistant",
            "content": f"I've stored the {source} output for future reference."
        }
    ]
    return messages


def load_from_file(filepath: str, loader: MemosLoader, user_id: str):
    """Load data from a file"""
    print(f"\n📂 Loading file: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Use filename as conversation ID
    filename = os.path.basename(filepath)
    conv_id = f"file_{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    messages = text_to_messages(content, source=filename)

    loader.add_message(
        user_id=user_id,
        conversation_id=conv_id,
        messages=messages
    )


def load_from_stdin(loader: MemosLoader, user_id: str, source: str = "stdin"):
    """Load data from stdin"""
    print(f"\n⌨️  Reading from stdin (Ctrl+D to finish)...")

    content = sys.stdin.read()

    if not content.strip():
        print("✗ No input received")
        return

    conv_id = f"stdin_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    messages = text_to_messages(content, source=source)

    loader.add_message(
        user_id=user_id,
        conversation_id=conv_id,
        messages=messages
    )


def main():
    parser = argparse.ArgumentParser(
        description="MemOS Data Loader - Load CLI output and files into MemOS"
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be sent without making API calls (BUDGET SAVER!)'
    )
    parser.add_argument(
        '--file',
        type=str,
        help='Load data from file'
    )
    parser.add_argument(
        '--stdin',
        action='store_true',
        help='Read data from stdin'
    )
    parser.add_argument(
        '--search',
        type=str,
        help='Search for memories instead of adding'
    )
    parser.add_argument(
        '--user-id',
        type=str,
        help='User ID (overrides env)'
    )
    parser.add_argument(
        '--source',
        type=str,
        default='cli',
        help='Source description (e.g., "nmap", "ssh-scan")'
    )

    args = parser.parse_args()

    # Load environment variables
    load_dotenv()

    api_key = os.getenv('MEMOS_API_KEY')
    base_url = os.getenv('MEMOS_BASE_URL', 'https://memos.memtensor.cn/api/openmem/v1')
    user_id = args.user_id or os.getenv('MEMOS_USER_ID', 'test_user_001')

    if not api_key:
        print("✗ Error: MEMOS_API_KEY not set")
        print("Set it in .env file or environment variable")
        sys.exit(1)

    print(f"🔧 MemOS Data Loader")
    print(f"   Base URL: {base_url}")
    print(f"   User ID: {user_id}")
    print(f"   Dry Run: {args.dry_run}")

    loader = MemosLoader(api_key, base_url, dry_run=args.dry_run)

    # Execute command
    if args.search:
        loader.search_memory(user_id, args.search)
    elif args.file:
        load_from_file(args.file, loader, user_id)
    elif args.stdin:
        load_from_stdin(loader, user_id, source=args.source)
    else:
        parser.print_help()
        print("\n💡 Examples:")
        print("  # Dry run (no API calls):")
        print("  python src/simple_loader.py --file test-samples/sample-ssh-scan.txt --dry-run")
        print()
        print("  # Load from file:")
        print("  python src/simple_loader.py --file test-samples/sample-ssh-scan.txt")
        print()
        print("  # Pipe command output:")
        print("  nmap -sV 192.168.1.1 | python src/simple_loader.py --stdin --source nmap")
        print()
        print("  # Search memories:")
        print("  python src/simple_loader.py --search 'SSH ports'")


if __name__ == "__main__":
    main()
