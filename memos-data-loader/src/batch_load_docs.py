#!/usr/bin/env python3
"""
Batch Documentation Loader for MemOS docker-test1
Loads all processed markdown files from docs/processed/
"""
import os
import sys
import json
import time
import requests
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv


class DocBatchLoader:
    """Batch loader for markdown documentation"""

    def __init__(self, base_url: str, user_id: str):
        self.base_url = base_url
        self.user_id = user_id
        self.stats = {
            "total": 0,
            "success": 0,
            "failed": 0,
            "errors": []
        }

    def load_document(self, filepath: Path) -> bool:
        """Load a single document into MemOS"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Create messages in MemOS format
            messages = [
                {
                    "role": "user",
                    "content": f"Here is documentation from {filepath.name}:\n\n{content[:1000]}..."
                },
                {
                    "role": "assistant",
                    "content": f"I've stored the documentation from {filepath.name} for future reference."
                }
            ]

            # Add to MemOS
            url = f"{self.base_url}/product/add"
            payload = {
                "user_id": self.user_id,
                "messages": messages,
                "source": f"doc_loader_{filepath.stem}"
            }

            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()

            if result.get("code") == 200:
                print(f"✓ [{self.stats['success']+1:3d}] {filepath.name}")
                self.stats["success"] += 1
                return True
            else:
                print(f"✗ [{self.stats['failed']+1:3d}] {filepath.name} - API returned: {result}")
                self.stats["failed"] += 1
                self.stats["errors"].append({
                    "file": str(filepath),
                    "error": str(result)
                })
                return False

        except Exception as e:
            print(f"✗ [{self.stats['failed']+1:3d}] {filepath.name} - Error: {e}")
            self.stats["failed"] += 1
            self.stats["errors"].append({
                "file": str(filepath),
                "error": str(e)
            })
            return False

    def load_directory(self, docs_dir: Path, delay: float = 0.5):
        """Load all markdown files from directory"""
        # Find all markdown files
        md_files = sorted(docs_dir.rglob("*.md"))
        self.stats["total"] = len(md_files)

        print(f"\n{'='*70}")
        print(f"MemOS Batch Documentation Loader")
        print(f"{'='*70}")
        print(f"Base URL: {self.base_url}")
        print(f"User ID: {self.user_id}")
        print(f"Documents: {len(md_files)} files")
        print(f"Delay: {delay}s between requests")
        print(f"{'='*70}\n")

        start_time = time.time()

        for i, filepath in enumerate(md_files, 1):
            self.load_document(filepath)

            # Progress update every 10 files
            if i % 10 == 0:
                elapsed = time.time() - start_time
                rate = i / elapsed
                remaining = (self.stats["total"] - i) / rate if rate > 0 else 0
                print(f"\n[Progress] {i}/{self.stats['total']} files | "
                      f"Success: {self.stats['success']} | "
                      f"Failed: {self.stats['failed']} | "
                      f"Rate: {rate:.1f} docs/sec | "
                      f"ETA: {remaining:.0f}s\n")

            # Rate limiting
            if delay > 0 and i < len(md_files):
                time.sleep(delay)

        elapsed = time.time() - start_time

        # Final report
        print(f"\n{'='*70}")
        print(f"BATCH LOAD COMPLETE")
        print(f"{'='*70}")
        print(f"Total documents: {self.stats['total']}")
        print(f"Successfully loaded: {self.stats['success']}")
        print(f"Failed: {self.stats['failed']}")
        print(f"Time elapsed: {elapsed:.1f}s")
        print(f"Average rate: {self.stats['total']/elapsed:.1f} docs/sec")
        print(f"{'='*70}\n")

        if self.stats["errors"]:
            print(f"\n⚠️  ERRORS ({len(self.stats['errors'])}):")
            for err in self.stats["errors"][:10]:  # Show first 10 errors
                print(f"  - {Path(err['file']).name}: {err['error']}")
            if len(self.stats["errors"]) > 10:
                print(f"  ... and {len(self.stats['errors']) - 10} more errors")


def main():
    # Load environment
    load_dotenv()

    base_url = os.getenv('MEMOS_BASE_URL', 'http://localhost:8001')
    user_id = os.getenv('MEMOS_USER_ID', 'test1_user')

    # Find docs directory
    script_dir = Path(__file__).parent
    docs_dir = script_dir.parent / "docs" / "processed"

    if not docs_dir.exists():
        print(f"✗ Error: Documentation directory not found: {docs_dir}")
        sys.exit(1)

    # Create loader and run
    loader = DocBatchLoader(base_url, user_id)

    try:
        loader.load_directory(docs_dir, delay=0.5)
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        print(f"Loaded {loader.stats['success']}/{loader.stats['total']} documents before interrupt")
        sys.exit(1)


if __name__ == "__main__":
    main()
