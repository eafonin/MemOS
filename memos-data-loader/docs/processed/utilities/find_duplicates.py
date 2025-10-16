#!/usr/bin/env python3
"""
Find duplicate documentation files by checking source URLs in metadata.
"""

import re
from pathlib import Path
from collections import defaultdict

def extract_metadata(filepath):
    """Extract YAML frontmatter metadata from markdown file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Look for YAML frontmatter
        match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL | re.MULTILINE)
        if not match:
            return None

        metadata = {}
        for line in match.group(1).split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip()

        return metadata
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None


def main():
    """Find duplicates by source URL."""
    processed_dir = Path(__file__).parent

    # Map source URLs to files
    url_to_files = defaultdict(list)
    files_without_metadata = []

    for filepath in sorted(processed_dir.glob('*.md')):
        # Skip utility files
        if filepath.name in ['find_duplicates.py', 'clean_tables.py']:
            continue

        metadata = extract_metadata(filepath)
        if metadata and 'source_url' in metadata:
            url = metadata['source_url']
            size = filepath.stat().st_size
            url_to_files[url].append((filepath.name, size))
        else:
            files_without_metadata.append(filepath.name)

    # Find duplicates
    duplicates = {url: files for url, files in url_to_files.items() if len(files) > 1}

    print("=" * 80)
    print("DUPLICATE DETECTION REPORT")
    print("=" * 80)
    print()

    if duplicates:
        print(f"Found {len(duplicates)} URLs with multiple files:\n")

        total_duplicate_files = 0
        total_wasted_space = 0

        for url, files in sorted(duplicates.items()):
            total_duplicate_files += len(files) - 1

            print(f"URL: {url}")
            print(f"Files ({len(files)}):")

            files_sorted = sorted(files, key=lambda x: x[1])  # Sort by size

            for filename, size in files_sorted:
                size_kb = size / 1024
                print(f"  - {filename:50s} {size_kb:8.1f} KB")

            # Calculate wasted space (all but the largest file)
            largest_size = max(f[1] for f in files)
            wasted = sum(f[1] for f in files) - largest_size
            total_wasted_space += wasted

            print(f"  Recommendation: Keep largest file, remove {len(files)-1} duplicates")
            print(f"  Space savings: {wasted/1024:.1f} KB")
            print()

        print("=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print(f"Total duplicate files: {total_duplicate_files}")
        print(f"Total wasted space: {total_wasted_space/1024:.1f} KB")
        print()
    else:
        print("No duplicates found!")
        print()

    if files_without_metadata:
        print("=" * 80)
        print(f"FILES WITHOUT METADATA ({len(files_without_metadata)})")
        print("=" * 80)
        for filename in files_without_metadata:
            print(f"  - {filename}")
        print()

    print("=" * 80)
    print(f"Total files scanned: {len(list(processed_dir.glob('*.md')))}")
    print("=" * 80)


if __name__ == '__main__':
    main()
