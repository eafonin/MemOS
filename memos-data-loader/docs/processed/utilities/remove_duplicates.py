#!/usr/bin/env python3
"""
Remove duplicate documentation files, keeping only the largest version of each URL.
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
        return None


def main():
    """Remove duplicate files, keeping only the largest."""
    processed_dir = Path(__file__).parent

    # Map source URLs to files
    url_to_files = defaultdict(list)

    for filepath in sorted(processed_dir.glob('*.md')):
        # Skip utility files
        if filepath.name in ['find_duplicates.py', 'clean_tables.py', 'remove_duplicates.py']:
            continue

        metadata = extract_metadata(filepath)
        if metadata and 'source_url' in metadata:
            url = metadata['source_url']
            size = filepath.stat().st_size
            url_to_files[url].append((filepath, size))

    # Find duplicates and remove smaller files
    duplicates = {url: files for url, files in url_to_files.items() if len(files) > 1}

    if not duplicates:
        print("No duplicates found!")
        return

    print("=" * 80)
    print(f"REMOVING DUPLICATES - Found {len(duplicates)} URLs with multiple files")
    print("=" * 80)
    print()

    total_removed = 0
    total_saved_space = 0

    for url, files in sorted(duplicates.items()):
        # Sort by size (ascending)
        files_sorted = sorted(files, key=lambda x: x[1])

        # Keep the largest file (last one)
        keep_file, keep_size = files_sorted[-1]

        # Remove all smaller files
        for filepath, size in files_sorted[:-1]:
            print(f"✗ Removing: {filepath.name:50s} ({size/1024:6.1f} KB)")
            filepath.unlink()
            total_removed += 1
            total_saved_space += size

        print(f"✓ Keeping:  {keep_file.name:50s} ({keep_size/1024:6.1f} KB)")
        print()

    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Files removed: {total_removed}")
    print(f"Space saved: {total_saved_space/1024:.1f} KB")
    print(f"Remaining files: {len(list(processed_dir.glob('*.md')))}")
    print("=" * 80)


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == '--dry-run':
        print("DRY RUN MODE - No files will be deleted")
        print("Run without --dry-run to actually remove duplicates")
        print()
    elif len(sys.argv) > 1 and sys.argv[1] == '--confirm':
        main()
    else:
        print("=" * 80)
        print("DUPLICATE REMOVAL SCRIPT")
        print("=" * 80)
        print()
        print("This script will remove duplicate files with the same source_url,")
        print("keeping only the largest version of each file.")
        print()
        print("Usage:")
        print("  python3 remove_duplicates.py --dry-run   # See what would be removed")
        print("  python3 remove_duplicates.py --confirm   # Actually remove files")
        print()
        print("=" * 80)
