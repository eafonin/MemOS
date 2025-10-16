#!/usr/bin/env python3
"""
Script to split markdown files by headings (level 1-2).
Each section will be saved as a separate file with the format:
{arxiv_id}_{heading_name}.md
"""

import re
from pathlib import Path
from typing import List, Tuple


def slugify(text: str) -> str:
    """Convert heading text to a filesystem-safe slug."""
    # Remove special characters and convert to lowercase
    text = text.lower()
    # Remove markdown formatting like ** or __
    text = re.sub(r'[*_`]', '', text)
    # Remove LaTeX commands and special characters
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


def process_file(file_path: Path, output_dir: Path, arxiv_id: str) -> None:
    """Process a single markdown file and split it into sections."""
    print(f"\nProcessing {file_path}...")

    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by headings
    sections = split_by_headings(content, arxiv_id)

    print(f"Found {len(sections)} sections")

    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Write each section to a separate file
    for filename, heading, section_content in sections:
        output_path = output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(section_content)
        print(f"  Created: {filename} - {heading}")

    print(f"Split {file_path.name} into {len(sections)} files in {output_dir}")


def main():
    base_path = Path('/home/memos/Development/MemOS/memos-data-loader/docs/processed')

    # Define papers to process
    papers = [
        {
            'arxiv_id': 'arxiv-2505.22101v1',
            'input_file': base_path / 'arxiv-2505.22101v1' / 'arxiv-2505.22101v1.md',
            'output_dir': base_path / 'arxiv-2505.22101v1' / 'sections'
        },
        {
            'arxiv_id': 'arxiv-2507.03724v3',
            'input_file': base_path / 'arxiv-2507.03724v3' / 'arxiv-2507.03724v3.md',
            'output_dir': base_path / 'arxiv-2507.03724v3' / 'sections'
        }
    ]

    for paper in papers:
        if paper['input_file'].exists():
            process_file(paper['input_file'], paper['output_dir'], paper['arxiv_id'])
        else:
            print(f"Warning: {paper['input_file']} does not exist")

    print("\nAll done!")


if __name__ == '__main__':
    main()
