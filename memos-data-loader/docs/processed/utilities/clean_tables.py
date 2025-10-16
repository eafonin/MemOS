#!/usr/bin/env python3
"""
Script to clean HTML tables in markdown files.
Removes all HTML attributes except rowspan and colspan.
Keeps only essential table structure tags: table, tr, td, th, thead, tbody.
"""

import re
import sys
from pathlib import Path


def clean_html_tags(content: str) -> str:
    """
    Clean HTML tags in the content:
    - Keep only table structure tags: table, tr, td, th, thead, tbody
    - Remove all attributes except rowspan and colspan
    """

    # Define allowed tags
    allowed_tags = ['table', 'tr', 'td', 'th', 'thead', 'tbody']

    # Find all HTML tags
    def clean_tag(match):
        full_tag = match.group(0)
        tag_name = match.group(1).lower()
        is_closing = match.group(0).startswith('</')

        # If it's a closing tag, keep it simple
        if is_closing:
            if tag_name in allowed_tags:
                return f'</{tag_name}>'
            else:
                return ''  # Remove non-allowed closing tags

        # For opening tags
        if tag_name not in allowed_tags:
            return ''  # Remove non-allowed tags

        # Extract rowspan and colspan if present
        rowspan_match = re.search(r'rowspan=["\']?(\d+)["\']?', full_tag, re.IGNORECASE)
        colspan_match = re.search(r'colspan=["\']?(\d+)["\']?', full_tag, re.IGNORECASE)

        # Build cleaned tag
        cleaned_tag = f'<{tag_name}'
        if rowspan_match:
            cleaned_tag += f' rowspan="{rowspan_match.group(1)}"'
        if colspan_match:
            cleaned_tag += f' colspan="{colspan_match.group(1)}"'
        cleaned_tag += '>'

        return cleaned_tag

    # Pattern to match HTML tags
    tag_pattern = r'<(/?)(\w+)[^>]*>'

    # Clean all tags
    cleaned_content = re.sub(tag_pattern, clean_tag, content)

    return cleaned_content


def process_file(file_path: Path) -> None:
    """Process a single markdown file."""
    print(f"Processing {file_path}...")

    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Clean HTML tags
    cleaned_content = clean_html_tags(content)

    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)

    print(f"Cleaned {file_path}")


def main():
    # Process both files
    base_path = Path('/home/memos/Development/MemOS/memos-data-loader/docs/processed')

    files = [
        base_path / 'arxiv-2505.22101v1' / 'arxiv-2505.22101v1.md',
        base_path / 'arxiv-2507.03724v3' / 'arxiv-2507.03724v3.md'
    ]

    for file_path in files:
        if file_path.exists():
            process_file(file_path)
        else:
            print(f"Warning: {file_path} does not exist")

    print("Done!")


if __name__ == '__main__':
    main()
