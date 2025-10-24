#!/usr/bin/env python3
"""
Load documents into MemOS with comprehensive monitoring.
Tracks chunking quality, patch-specific issues, and metrics.
"""

import json
import os
import sys
import time
import requests
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Configuration
API_BASE = "http://localhost:8001"
DOCS_DIR = Path("/home/memos/Development/MemOS/docs/processed")

class DocumentLoader:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.stats = {
            "total_files": 0,
            "successful": 0,
            "failed": 0,
            "total_chars": 0,
            "total_time": 0,
            "errors": [],
            "warnings": [],
            "documents": []
        }
        self.start_time = None

    def register_user(self) -> bool:
        """Register user in MemOS."""
        print(f"🔐 Registering user: {self.user_id}")
        try:
            response = requests.post(
                f"{API_BASE}/product/users/register",
                json={
                    "user_id": self.user_id,
                    "mem_cube_id": f"{self.user_id}_default_cube"
                },
                timeout=30
            )
            if response.status_code == 200:
                print("✅ User registered successfully")
                return True
            else:
                print(f"⚠️  User might already exist or registration failed: {response.text}")
                return True  # Continue anyway
        except Exception as e:
            print(f"❌ Error registering user: {e}")
            return False

    def load_document(self, file_path: Path) -> Dict[str, Any]:
        """Load a single document into MemOS."""
        try:
            # Read document content
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            if not content.strip():
                return {
                    "success": False,
                    "error": "Empty file",
                    "file": str(file_path),
                    "chars": 0,
                    "time": 0
                }

            # Prepare metadata
            doc_name = file_path.stem
            doc_info = {
                "file": str(file_path.relative_to(DOCS_DIR)),
                "name": doc_name,
                "chars": len(content),
                "size_category": self._categorize_size(len(content))
            }

            # Send to MemOS
            start = time.time()
            response = requests.post(
                f"{API_BASE}/product/add",
                json={
                    "user_id": self.user_id,
                    "memory_content": content,
                    "metadata": doc_info
                },
                timeout=120
            )
            elapsed = time.time() - start

            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "file": doc_info["file"],
                    "chars": doc_info["chars"],
                    "time": elapsed,
                    "response": result
                }
            else:
                return {
                    "success": False,
                    "file": doc_info["file"],
                    "chars": doc_info["chars"],
                    "time": elapsed,
                    "error": f"HTTP {response.status_code}: {response.text[:200]}"
                }

        except Exception as e:
            return {
                "success": False,
                "file": str(file_path.relative_to(DOCS_DIR)) if file_path else "unknown",
                "chars": 0,
                "time": 0,
                "error": str(e)
            }

    def _categorize_size(self, chars: int) -> str:
        """Categorize document size."""
        if chars < 1000:
            return "tiny"
        elif chars < 5000:
            return "small"
        elif chars < 20000:
            return "medium"
        elif chars < 50000:
            return "large"
        else:
            return "xlarge"

    def collect_files(self, max_files: int = None) -> List[Path]:
        """Collect markdown files from docs directory."""
        all_files = []

        for ext in ['*.md', '*.txt']:
            all_files.extend(DOCS_DIR.rglob(ext))

        # Filter out JSON metadata index files
        all_files = [f for f in all_files if not f.name.endswith('-index.md')]

        # Sort by size (small to large) for better progress visibility
        all_files.sort(key=lambda p: p.stat().st_size)

        if max_files:
            all_files = all_files[:max_files]

        return all_files

    def load_batch(self, files: List[Path], batch_name: str = "documents"):
        """Load a batch of documents."""
        print()
        print("=" * 70)
        print(f"  Loading {len(files)} {batch_name}")
        print("=" * 70)
        print()

        self.start_time = time.time()
        self.stats["total_files"] = len(files)

        for idx, file_path in enumerate(files, 1):
            print(f"\n[{idx}/{len(files)}] {file_path.name}")
            print(f"  Size: {file_path.stat().st_size:,} bytes")

            result = self.load_document(file_path)

            # Update stats
            if result["success"]:
                self.stats["successful"] += 1
                self.stats["total_chars"] += result["chars"]
                self.stats["total_time"] += result["time"]
                print(f"  ✅ Loaded in {result['time']:.2f}s ({result['chars']:,} chars)")
            else:
                self.stats["failed"] += 1
                self.stats["errors"].append(result)
                print(f"  ❌ Failed: {result.get('error', 'Unknown error')}")

            self.stats["documents"].append(result)

            # Progress indicator
            progress = (idx / len(files)) * 100
            elapsed = time.time() - self.start_time
            avg_time = elapsed / idx if idx > 0 else 0
            remaining = (len(files) - idx) * avg_time
            print(f"  Progress: {progress:.1f}% | Elapsed: {elapsed:.1f}s | Est. remaining: {remaining:.1f}s")

        print()
        self.print_summary()

    def print_summary(self):
        """Print loading summary."""
        total_time = time.time() - self.start_time if self.start_time else 0

        print()
        print("=" * 70)
        print("  Loading Summary")
        print("=" * 70)
        print(f"Total files: {self.stats['total_files']}")
        print(f"Successful: {self.stats['successful']} ({self.stats['successful']/max(self.stats['total_files'],1)*100:.1f}%)")
        print(f"Failed: {self.stats['failed']}")
        print(f"Total characters: {self.stats['total_chars']:,}")
        print(f"Total API time: {self.stats['total_time']:.1f}s")
        print(f"Total elapsed: {total_time:.1f}s")

        if self.stats['successful'] > 0:
            avg_time = self.stats['total_time'] / self.stats['successful']
            avg_chars = self.stats['total_chars'] / self.stats['successful']
            print(f"Average time per doc: {avg_time:.2f}s")
            print(f"Average chars per doc: {avg_chars:,.0f}")

        if self.stats['failed'] > 0:
            print()
            print("Errors:")
            for err in self.stats['errors'][:10]:  # Show first 10 errors
                print(f"  - {err['file']}: {err.get('error', 'Unknown')[:100]}")
            if len(self.stats['errors']) > 10:
                print(f"  ... and {len(self.stats['errors']) - 10} more")

        print()

    def save_report(self, report_path: str):
        """Save detailed report to file."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "user_id": self.user_id,
            "stats": self.stats,
            "documents": self.stats["documents"]
        }

        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"📄 Detailed report saved to: {report_path}")

def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python load_documents.py <max_files|all> [user_id]")
        print("Example: python load_documents.py 20")
        print("Example: python load_documents.py all test_user_123")
        sys.exit(1)

    # Parse arguments
    max_files_arg = sys.argv[1]
    max_files = None if max_files_arg.lower() == "all" else int(max_files_arg)
    user_id = sys.argv[2] if len(sys.argv) > 2 else f"doc_loader_{int(time.time())}"

    # Create loader
    loader = DocumentLoader(user_id)

    # Register user
    if not loader.register_user():
        print("❌ Failed to register user, exiting")
        return 1

    # Collect files
    files = loader.collect_files(max_files)
    print(f"📁 Found {len(files)} documents to load")

    if not files:
        print("❌ No documents found!")
        return 1

    # Warn before long loads
    if len(files) > 50:
        print()
        print("⚠️" * 35)
        print("  LONG LOAD WARNING")
        print("⚠️" * 35)
        print(f"Loading {len(files)} documents will take approximately {len(files)*2//60} minutes")
        print("This process can run UNATTENDED - you may leave now")
        print("Press Ctrl+C within 10 seconds to cancel...")
        print()
        try:
            time.sleep(10)
        except KeyboardInterrupt:
            print("\n❌ Cancelled by user")
            return 1

    # Load documents
    loader.load_batch(files, batch_name=f"{len(files)} documents")

    # Save report
    report_path = f"/tmp/memos_load_report_{user_id}_{int(time.time())}.json"
    loader.save_report(report_path)

    return 0 if loader.stats['failed'] == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
