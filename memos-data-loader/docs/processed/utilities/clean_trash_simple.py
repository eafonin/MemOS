#!/usr/bin/env python3
"""
Remove trash data from markdown files - simplified, faster version.
"""

import re
from pathlib import Path

def clean_trash(content):
    """Remove all types of trash data from markdown content."""

    lines = content.split('\n')
    cleaned_lines = []
    skip_mode = False

    for line in lines:
        # Skip very long lines with menu concatenation (Type 1 trash)
        if len(line) > 500 and '[ [' in line and 'Overview' in line:
            continue

        # Skip Contact Us sections (Type 2)
        if re.match(r'^##\s+\d*\.?\s*Contact Us', line):
            skip_mode = True
            continue

        # Exit skip mode when next section starts
        if skip_mode and line.startswith('##') and 'Contact Us' not in line:
            skip_mode = False

        if skip_mode:
            continue

        # Skip CSS/Shiki lines (Type 3)
        if 'html' in line and 'shiki' in line and '--shiki' in line:
            continue

        # Skip footer navigation (Type 4)
        if '](/open_source/' in line or '](/overview/' in line:
            if line.count('[') > 3:
                continue

        # Skip "On this page" sections (Type 5)
        if 'On this page' in line and line.count('On this page') > 1:
            continue

        cleaned_lines.append(line)

    # Join and clean up
    content = '\n'.join(cleaned_lines)

    # Remove multiple blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)

    # Remove empty brackets
    content = re.sub(r'\[\s*\]\s*\[\s*\]', '', content)

    return content.strip() + '\n'


def process_file(filepath):
    """Process a single markdown file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_size = len(content)
        cleaned = clean_trash(content)
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
    print("CLEANING TRASH DATA FROM MARKDOWN FILES")
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
        elif reduction < 0:
            print(f"  Skipped due to error")

    print()
    print("=" * 70)
    print(f"Files cleaned: {cleaned_count}/{len(md_files)}")
    print(f"Total bytes removed: {total_bytes_saved:,} ({total_bytes_saved/1024:.1f} KB)")
    print("=" * 70)


if __name__ == '__main__':
    main()
