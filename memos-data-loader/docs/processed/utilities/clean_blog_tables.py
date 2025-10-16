#!/usr/bin/env python3
"""
Clean HTML tables in blog post markdown files.
Removes all HTML attributes except colspan/rowspan.
Keeps only essential table structure tags.
"""

import re
from pathlib import Path

# Table-related tags to preserve
TABLE_TAGS = ['table', 'thead', 'tbody', 'tfoot', 'tr', 'th', 'td', 'caption']

# Attributes to preserve (only for table structure)
PRESERVE_ATTRS = ['colspan', 'rowspan']


def clean_html_tag(match):
    """Clean a single HTML tag, preserving only table tags and structure attributes."""
    full_tag = match.group(0)
    tag_content = match.group(1)

    # Extract tag name (first word)
    tag_parts = tag_content.split(None, 1)
    if not tag_parts:
        return full_tag

    tag_name = tag_parts[0].lower().rstrip('>')

    # Check if it's a closing tag
    if tag_name.startswith('/'):
        base_tag = tag_name[1:]
        if base_tag in TABLE_TAGS:
            return f'</{base_tag}>'
        else:
            return ''  # Remove non-table closing tags

    # Check if it's a self-closing tag or regular opening tag
    is_self_closing = tag_content.rstrip().endswith('/')

    # If not a table tag, remove it
    if tag_name not in TABLE_TAGS:
        return ''

    # For table tags, preserve only colspan and rowspan attributes
    preserved_attrs = []
    if len(tag_parts) > 1:
        attr_string = tag_parts[1].rstrip('/>').strip()

        # Extract colspan and rowspan if present
        for attr in PRESERVE_ATTRS:
            attr_pattern = rf'{attr}\s*=\s*["\']([^"\']+)["\']'
            attr_match = re.search(attr_pattern, attr_string, re.IGNORECASE)
            if attr_match:
                preserved_attrs.append(f'{attr}="{attr_match.group(1)}"')

    # Rebuild the tag
    if preserved_attrs:
        clean_tag = f'<{tag_name} {" ".join(preserved_attrs)}>'
    else:
        clean_tag = f'<{tag_name}>'

    if is_self_closing:
        clean_tag = clean_tag.rstrip('>') + ' />'

    return clean_tag


def clean_table_html(content):
    """Remove all HTML tags and attributes except table structure."""
    # Pattern to match HTML tags
    html_tag_pattern = r'<([^>]+)>'

    # Replace all HTML tags using the cleaning function
    cleaned = re.sub(html_tag_pattern, clean_html_tag, content)

    # Clean up extra whitespace created by removed tags
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)

    return cleaned


def process_blog(blog_dir: Path):
    """Process a single blog directory."""
    article_file = blog_dir / 'article.md'

    if not article_file.exists():
        print(f"  Warning: {article_file} does not exist")
        return False

    print(f"\nProcessing {blog_dir.name}...")

    # Read the file
    with open(article_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if there are tables
    if '<table' not in content.lower():
        print("  No tables found, skipping")
        return True

    # Clean HTML tables
    print("  Cleaning HTML tables...")
    cleaned_content = clean_table_html(content)

    # Count tables
    table_count = cleaned_content.lower().count('<table>')

    # Write cleaned content back
    with open(article_file, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)

    print(f"  ✓ Cleaned {table_count} table(s)")
    return True


def main():
    base_path = Path('/home/memos/Development/MemOS/memos-data-loader/docs/processed')

    blogs = [
        base_path / 'ai-plainenglish-io-memos',
        base_path / 'xugj520-cn-memos',
        base_path / 'llmmultiagents-com-memos'
    ]

    print("="*70)
    print("CLEANING BLOG TABLES")
    print("="*70)

    success_count = 0
    for blog_dir in blogs:
        if blog_dir.exists():
            if process_blog(blog_dir):
                success_count += 1
        else:
            print(f"\nWarning: {blog_dir} does not exist")

    print("\n" + "="*70)
    print(f"COMPLETE: {success_count}/{len(blogs)} blogs processed")
    print("="*70)


if __name__ == '__main__':
    main()
