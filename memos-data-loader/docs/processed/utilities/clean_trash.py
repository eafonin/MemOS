#!/usr/bin/env python3
"""
Remove trash data from markdown files:
1. Navigation breadcrumbs (long text with menu items)
2. "Contact Us" sections
3. CSS/Shiki styling blocks
4. Footer navigation sections
"""

import re
from pathlib import Path

def clean_trash(content):
    """Remove all types of trash data from markdown content."""

    # Type 1: Remove navigation breadcrumbs
    # Pattern: [ [ OverviewIntroduction...API Reference [ [ [
    # These are very long lines with concatenated menu items
    content = re.sub(
        r'\[\s*\[\s*Overview.*?API Reference.*?\[\s*\[\s*\[',
        '',
        content,
        flags=re.DOTALL
    )

    # More aggressive breadcrumb removal - any [ [ with lots of concatenated words
    content = re.sub(
        r'\[\s*\[\s*(?:Overview|Introduction|Quick Start|Memory|Cloud platform|Use Cases|Open Source|Getting Started|MOS|Memories|Scenario|Best Practice|Contribution|API Reference)(?:[A-Za-z\s]+){20,}?\[\s*\[\s*\[',
        '',
        content,
        flags=re.DOTALL
    )

    # Type 2: Remove "Contact Us" sections completely
    # Match from ## N. Contact Us header to the next ## or end of section
    content = re.sub(
        r'^##\s+\d*\.?\s*Contact Us.*?(?=^##|\Z)',
        '',
        content,
        flags=re.MULTILINE | re.DOTALL
    )

    # Type 3: Remove CSS/Shiki styling blocks
    # Pattern: html pre.shiki code ... followed by long CSS definitions
    content = re.sub(
        r'html\s+(?:pre\.shiki|\.light|\.dark|\.default).*?(?=\n\n|^#|\Z)',
        '',
        content,
        flags=re.DOTALL
    )

    # Remove standalone shiki/CSS lines
    content = re.sub(
        r'html[^\n]*shiki[^\n]*\{[^}]+\}',
        '',
        content
    )

    # Type 4: Remove footer navigation sections
    # Pattern: [ [ [PageTitle/path](/path) ] ] ]
    content = re.sub(
        r'\[\s*\[\s*\[.*?\]\(/[^\)]+\).*?\]\s*\]\s*\]',
        '',
        content,
        flags=re.DOTALL
    )

    # Type 5: Remove "On this page" sections at the end
    # Pattern: [ On this pageOn this page...Community...GitHub ] ] ] ] ]
    content = re.sub(
        r'\[\s*On this page.*?GitHub\s*\]\s*\]\s*\]\s*\]\s*\]',
        '',
        content,
        flags=re.DOTALL
    )

    # Clean up multiple blank lines left by removal
    content = re.sub(r'\n{3,}', '\n\n', content)

    # Clean up brackets and whitespace artifacts
    content = re.sub(r'\[\s*\]\s*\[\s*\]', '', content)
    content = re.sub(r'\[\s*\[\s*\]\s*\]', '', content)

    # Remove trailing whitespace from lines
    content = '\n'.join(line.rstrip() for line in content.split('\n'))

    return content


def process_file(filepath):
    """Process a single markdown file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_size = len(content)
        cleaned = clean_trash(content)
        new_size = len(cleaned)

        # Only write if something changed
        if original_size != new_size:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(cleaned)

            reduction = original_size - new_size
            pct = (reduction / original_size * 100) if original_size > 0 else 0
            print(f"✓ {filepath.name:50s} {reduction:6d} bytes removed ({pct:5.1f}%)")
            return True
        else:
            return False

    except Exception as e:
        print(f"✗ {filepath.name}: ERROR - {e}")
        return None


def main():
    """Main processing function."""
    processed_dir = Path(__file__).parent.parent

    print("=" * 80)
    print("CLEANING TRASH DATA FROM MARKDOWN FILES")
    print("=" * 80)
    print()
    print("Removing:")
    print("  1. Navigation breadcrumbs (menu concatenation)")
    print("  2. 'Contact Us' sections")
    print("  3. CSS/Shiki styling blocks")
    print("  4. Footer navigation sections")
    print("  5. 'On this page' sections")
    print()
    print("=" * 80)
    print()

    # Process all markdown files in the root
    md_files = sorted(processed_dir.glob('*.md'))

    cleaned_count = 0
    unchanged_count = 0
    error_count = 0
    total_bytes_saved = 0

    for filepath in md_files:
        result = process_file(filepath)
        if result is True:
            cleaned_count += 1
        elif result is False:
            unchanged_count += 1
        else:
            error_count += 1

    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Files cleaned: {cleaned_count}")
    print(f"Files unchanged: {unchanged_count}")
    if error_count > 0:
        print(f"Errors: {error_count}")
    print(f"Total files processed: {len(md_files)}")
    print("=" * 80)


if __name__ == '__main__':
    main()
