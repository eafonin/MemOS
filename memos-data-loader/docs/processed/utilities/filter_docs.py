#!/usr/bin/env python3
"""
Filter and list only documentation pages (files with source_url metadata).
"""

import re
from pathlib import Path

def has_source_url(filepath):
    """Check if file has source_url in YAML frontmatter."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            # Read first 20 lines (metadata should be near top)
            lines = [f.readline() for _ in range(20)]
            content = ''.join(lines)

        # Check for source_url in YAML frontmatter
        return 'source_url:' in content
    except:
        return False

def main():
    """List all documentation files."""
    processed_dir = Path(__file__).parent

    doc_files = []
    for filepath in sorted(processed_dir.glob('*.md')):
        if has_source_url(filepath):
            doc_files.append(filepath)

    print(f"Found {len(doc_files)} documentation pages:\n")

    for filepath in doc_files:
        size = filepath.stat().st_size / 1024
        print(f"{filepath.name:50s} {size:8.1f} KB")

    print(f"\nTotal: {len(doc_files)} files")

if __name__ == '__main__':
    main()
