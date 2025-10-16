#!/usr/bin/env python3
"""
Clean up bracket artifacts left from scraping.
Remove patterns like [ [ text ] ] and convert to clean text.
"""

import re
from pathlib import Path

def clean_brackets(content):
    """Remove bracket artifacts while preserving markdown links."""

    # Pattern 1: [ [ text ] ] -> text (but preserve markdown links)
    # Be careful not to break [![...](link)] patterns

    # Remove empty bracket pairs
    content = re.sub(r'\[\s*\]\s*\[\s*\]', '', content)
    content = re.sub(r'\[\s*\[\s*\]\s*\]', '', content)

    # Remove standalone [ [ or ] ] patterns with spaces
    content = re.sub(r'\s*\[\s+\[\s+', ' ', content)
    content = re.sub(r'\s+\]\s+\]\s*', ' ', content)

    # Clean up lines that start with [ and have trailing brackets
    lines = content.split('\n')
    cleaned_lines = []

    for line in lines:
        # Skip if it's an image reference (preserve those)
        if '![' in line or '](' in line and ')' in line:
            cleaned_lines.append(line)
            continue

        # Remove leading [ with optional spaces
        line = re.sub(r'^\[\s+', '', line)

        # Remove trailing ] with optional spaces
        line = re.sub(r'\s+\]$', '', line)

        # Remove patterns like ] [ ] [
        line = re.sub(r'\]\s*\[\s*\]\s*\[', '', line)

        # Remove double brackets [ [ and ] ]
        line = re.sub(r'\[\s*\[', '[', line)
        line = re.sub(r'\]\s*\]', ']', line)

        cleaned_lines.append(line)

    content = '\n'.join(cleaned_lines)

    # Final cleanup - remove multiple spaces
    content = re.sub(r'  +', ' ', content)

    # Remove blank lines with just brackets
    content = re.sub(r'\n\[\s*\]\n', '\n', content)

    return content


def process_file(filepath):
    """Process a single markdown file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_size = len(content)
        cleaned = clean_brackets(content)
        new_size = len(cleaned)

        if original_size != new_size:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(cleaned)

            reduction = original_size - new_size
            pct = (reduction / original_size * 100) if original_size > 0 else 0
            print(f"✓ {filepath.name:50s} -{reduction:6d} bytes ({pct:5.1f}%)")
            return reduction
        else:
            return 0

    except Exception as e:
        print(f"✗ {filepath.name}: ERROR - {e}")
        return -1


def main():
    """Main processing function."""
    processed_dir = Path(__file__).parent.parent

    print("=" * 70)
    print("CLEANING BRACKET ARTIFACTS")
    print("=" * 70)
    print()

    md_files = sorted(processed_dir.glob('*.md'))

    cleaned_count = 0
    total_bytes_saved = 0

    for filepath in md_files:
        reduction = process_file(filepath)
        if reduction > 0:
            cleaned_count += 1
            total_bytes_saved += reduction

    print()
    print("=" * 70)
    print(f"Files cleaned: {cleaned_count}/{len(md_files)}")
    print(f"Total bytes removed: {total_bytes_saved:,} ({total_bytes_saved/1024:.1f} KB)")
    print("=" * 70)


if __name__ == '__main__':
    main()
