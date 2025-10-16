#!/usr/bin/env python3
"""
Clean HTML tables and split markdown files by headings.
Based on the working utilities/clean_tables.py approach.
"""

import re
from pathlib import Path
from typing import List, Tuple

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


def slugify(text: str) -> str:
    """Convert heading text to a filesystem-safe slug."""
    text = text.lower()
    # Remove markdown formatting
    text = re.sub(r'[*_`]', '', text)
    # Remove LaTeX commands
    text = re.sub(r'\\[a-zA-Z]+', '', text)
    # Replace spaces and special chars with hyphens
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    # Trim hyphens from ends
    text = text.strip('-')
    # Limit length
    if len(text) > 80:
        text = text[:80].rsplit('-', 1)[0]
    return text or 'section'


def split_by_headings(content: str, arxiv_id: str) -> List[Tuple[str, str, str]]:
    """
    Split markdown content by level 1 and 2 headings.
    Returns list of tuples: (filename, heading, content)
    """
    lines = content.split('\n')
    sections = []
    current_heading = None
    current_content = []
    frontmatter_lines = []
    in_frontmatter = False
    past_frontmatter = False

    for i, line in enumerate(lines):
        # Handle YAML frontmatter
        if i == 0 and line.strip() == '---':
            in_frontmatter = True
            frontmatter_lines.append(line)
            continue

        if in_frontmatter:
            frontmatter_lines.append(line)
            if line.strip() == '---':
                in_frontmatter = False
                past_frontmatter = True
            continue

        # Match level 1 or 2 headings
        heading_match = re.match(r'^(#{1,2})\s+(.+)$', line)

        if heading_match and past_frontmatter:
            # Save previous section if exists
            if current_heading:
                section_content = '\n'.join(current_content).strip()
                if section_content:
                    heading_slug = slugify(current_heading)
                    filename = f"{arxiv_id}_{heading_slug}.md"
                    sections.append((filename, current_heading, section_content))

            # Start new section
            current_heading = heading_match.group(2).strip()
            current_content = [line]  # Include the heading in content
        else:
            current_content.append(line)

    # Save last section
    if current_heading and current_content:
        section_content = '\n'.join(current_content).strip()
        if section_content:
            heading_slug = slugify(current_heading)
            filename = f"{arxiv_id}_{heading_slug}.md"
            sections.append((filename, current_heading, section_content))

    # Add frontmatter to each section
    frontmatter_text = '\n'.join(frontmatter_lines)
    if frontmatter_text:
        sections = [
            (filename, heading, f"{frontmatter_text}\n\n{content}")
            for filename, heading, content in sections
        ]

    return sections


def process_paper(paper_dir: Path, arxiv_id: str):
    """Process a single paper: clean tables and split by headings."""
    input_file = paper_dir / 'paper.md'

    if not input_file.exists():
        print(f"Warning: {input_file} does not exist")
        return

    print(f"\nProcessing {arxiv_id}...")

    # Read the file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Clean HTML tables
    print("  Cleaning HTML tables...")
    cleaned_content = clean_table_html(content)

    # Write cleaned content back to paper.md
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)

    # Split by headings
    print("  Splitting by headings...")
    sections = split_by_headings(cleaned_content, arxiv_id)

    print(f"  Found {len(sections)} sections")

    # Write each section to a separate file in the paper root
    for filename, heading, section_content in sections:
        output_path = paper_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(section_content)
        print(f"    Created: {filename}")

    print(f"✓ Completed {arxiv_id}: {len(sections)} files created")


def main():
    base_path = Path('/home/memos/Development/MemOS/memos-data-loader/docs/processed')

    papers = [
        {'arxiv_id': 'arxiv-2505.22101v1', 'dir': base_path / 'arxiv-2505.22101v1'},
        {'arxiv_id': 'arxiv-2507.03724v3', 'dir': base_path / 'arxiv-2507.03724v3'}
    ]

    print("="*70)
    print("CLEANING TABLES AND SPLITTING PAPERS")
    print("="*70)

    for paper in papers:
        process_paper(paper['dir'], paper['arxiv_id'])

    print("\n" + "="*70)
    print("ALL PROCESSING COMPLETE")
    print("="*70)


if __name__ == '__main__':
    main()
