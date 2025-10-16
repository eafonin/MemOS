#!/usr/bin/env python3
"""
Build 2-level documentation indexes:
- Child indexes: one per doc folder with JSON Lines entries for each MD file
- Parent index: single file listing all child indexes
- claude.md: entry point with usage examples
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple
import re


# Priority mapping
FOLDER_PRIORITIES = {
    'memos-docs.openmem.net': 1,
    'github-memos-docs': 2,
    'memos-dashboard.openmem.net': 3,
    'arxiv-2507.03724v3': 4,
    'arxiv-2505.22101v1': 4,
    # Everything else gets priority 5
}


def get_file_type(filename: str, content_preview: str) -> str:
    """Determine file type based on filename and content."""
    filename_lower = filename.lower()

    if 'api' in filename_lower or 'reference' in filename_lower:
        return 'api-reference'
    elif 'cookbook' in filename_lower or 'example' in filename_lower:
        return 'tutorial'
    elif 'quick' in filename_lower or 'getting' in filename_lower or 'installation' in filename_lower:
        return 'guide'
    elif 'arxiv' in filename_lower:
        return 'research'
    elif any(blog in filename_lower for blog in ['plainenglish', 'xugj520', 'llmmultiagents']):
        return 'blog'
    elif 'overview' in filename_lower or 'introduction' in filename_lower:
        return 'overview'
    elif 'algorithm' in filename_lower or 'architecture' in filename_lower:
        return 'technical'
    else:
        return 'documentation'


def generate_description(file_path: Path) -> str:
    """Generate AI description by analyzing file content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Remove frontmatter
        content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

        # Extract title
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else ''

        # Extract first substantial paragraph (skip very short lines)
        paragraphs = [p.strip() for p in content.split('\n\n') if len(p.strip()) > 50]
        first_para = paragraphs[0] if paragraphs else ''

        # Clean up
        first_para = re.sub(r'[#*_`]', '', first_para)  # Remove markdown formatting
        first_para = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', first_para)  # Remove links, keep text
        first_para = re.sub(r'\s+', ' ', first_para)  # Normalize whitespace

        # Build description
        description_parts = []

        # Add context from filename
        filename = file_path.stem
        if 'introduction' in filename.lower():
            description_parts.append('Introduction to')
        elif 'overview' in filename.lower():
            description_parts.append('Overview of')
        elif 'api' in filename.lower():
            description_parts.append('API reference for')
        elif 'cookbook' in filename.lower() or 'example' in filename.lower():
            description_parts.append('Tutorial demonstrating')
        elif 'guide' in filename.lower() or 'quick' in filename.lower():
            description_parts.append('Guide for')
        elif 'architecture' in filename.lower():
            description_parts.append('Architecture documentation of')

        # Add title context
        if title:
            topic = title.lower()
            if 'memos' in topic:
                description_parts.append('MemOS')

        # Combine with content
        if first_para:
            # Take first 2-3 sentences
            sentences = re.split(r'[.!?]\s+', first_para)
            summary = '. '.join(sentences[:3])
            if not summary.endswith('.'):
                summary += '.'

            if description_parts:
                description = ' '.join(description_parts) + ' ' + summary
            else:
                description = summary
        else:
            # Fallback: use title and filename hints
            if title:
                description = f"Documentation about {title}"
            else:
                description = f"Documentation on {filename.replace('-', ' ').replace('_', ' ')}"

        # Ensure length is reasonable (3-5 sentences)
        sentences = re.split(r'[.!?]\s+', description)
        if len(sentences) > 5:
            description = '. '.join(sentences[:5])
            if not description.endswith('.'):
                description += '.'

        # Limit to ~200 chars to save tokens
        if len(description) > 250:
            description = description[:247] + '...'

        return description.strip()

    except Exception as e:
        print(f"    Warning: Could not generate description for {file_path.name}: {e}")
        return f"Documentation file: {file_path.stem.replace('-', ' ').replace('_', ' ')}"


def get_folder_priority(folder_name: str) -> int:
    """Get priority for a folder."""
    return FOLDER_PRIORITIES.get(folder_name, 5)


def create_child_index(folder_path: Path, project_root: Path) -> Tuple[Path, Dict]:
    """Create a child index for a documentation folder."""
    folder_name = folder_path.name
    priority = get_folder_priority(folder_name)

    print(f"\nProcessing folder: {folder_name} (priority={priority})")

    # Find all MD files (excluding index files)
    md_files = [f for f in folder_path.glob('*.md') if not f.name.endswith('-index.md')]

    if not md_files:
        print(f"  No MD files found, skipping")
        return None, None

    print(f"  Found {len(md_files)} MD files")

    # Create index entries
    entries = []
    total_bytes = 0

    for md_file in sorted(md_files):
        print(f"  Processing: {md_file.name}")

        # Generate description
        description = generate_description(md_file)

        # Get file info
        file_size = md_file.stat().st_size
        total_bytes += file_size

        # Determine type
        with open(md_file, 'r', encoding='utf-8') as f:
            preview = f.read(500)
        file_type = get_file_type(md_file.name, preview)

        # Create relative path from project root
        rel_path = md_file.relative_to(project_root)

        # Build entry
        entry = {
            'file': md_file.name,
            'path': str(rel_path),
            'description': description,
            'priority': priority,
            'bytes': file_size,
            'type': file_type
        }

        entries.append(entry)

    # Create index file
    index_filename = f"{folder_name}-index.md"
    index_path = folder_path / index_filename

    with open(index_path, 'w', encoding='utf-8') as f:
        for entry in entries:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')

    print(f"  ✓ Created {index_filename} with {len(entries)} entries")

    # Return metadata for parent index
    metadata = {
        'index': index_filename,
        'path': str(index_path.relative_to(project_root)),
        'folder_name': folder_name,
        'priority': priority,
        'file_count': len(entries),
        'total_bytes': total_bytes
    }

    return index_path, metadata


def create_parent_index(child_indexes: List[Dict], output_path: Path, project_root: Path):
    """Create parent index listing all child indexes."""
    print(f"\nCreating parent index: {output_path}")

    # Generate descriptions for each collection
    parent_entries = []

    for meta in sorted(child_indexes, key=lambda x: x['priority']):
        folder_name = meta['folder_name']

        # Generate collection description
        if folder_name == 'memos-docs.openmem.net':
            description = "Complete MemOS documentation from official website including API references, tutorials, cookbooks, modules documentation, and use cases - primary documentation source"
            topics = ["api", "tutorials", "modules", "use-cases"]
        elif folder_name == 'github-memos-docs':
            description = "Official GitHub documentation repository with technical details on open source implementation, contribution guidelines, best practices, and module specifications"
            topics = ["open-source", "architecture", "modules", "contribution"]
        elif folder_name == 'memos-dashboard.openmem.net':
            description = "Dashboard documentation covering API overview, quick start guide, usage limits, and error codes for MemOS cloud service"
            topics = ["dashboard", "api", "cloud-service"]
        elif folder_name == 'arxiv-2507.03724v3':
            description = "Academic research paper on MemOS system design including introduction, memory modeling, architecture, evaluation results, and applications"
            topics = ["research", "architecture", "evaluation"]
        elif folder_name == 'arxiv-2505.22101v1':
            description = "Short version research paper covering MemOS design philosophy, memory types, MemCube abstraction, and system architecture overview"
            topics = ["research", "design", "concepts"]
        elif 'plainenglish' in folder_name or 'xugj520' in folder_name or 'llmmultiagents' in folder_name:
            if len([m for m in child_indexes if 'plainenglish' in m['folder_name'] or 'xugj520' in m['folder_name'] or 'llmmultiagents' in m['folder_name']]) > 1:
                # Skip individual blog entries if we'll create a collection
                continue
            description = f"Blog article discussing MemOS features and implementation from {folder_name.replace('-', ' ')}"
            topics = ["blog", "community"]
        else:
            description = f"Documentation collection: {folder_name.replace('-', ' ')}"
            topics = ["documentation"]

        entry = {
            'index': meta['index'],
            'path': meta['path'],
            'description': description,
            'priority': meta['priority'],
            'file_count': meta['file_count'],
            'total_bytes': meta['total_bytes'],
            'topics': topics
        }

        parent_entries.append(entry)

    # Write parent index
    with open(output_path, 'w', encoding='utf-8') as f:
        for entry in parent_entries:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')

    print(f"  ✓ Created parent index with {len(parent_entries)} collections")


def create_claude_md(output_path: Path):
    """Create claude.md entry point with examples."""
    content = """# MemOS Documentation Index - Agent Guide

This documentation uses a 2-level JSON Lines indexing system optimized for LLM and agent use.

## Structure

```
docs/processed/
├── docs-index.md              # Parent index (Level 2)
├── memos-docs.openmem.net/
│   └── memos-docs-openmem-net-index.md  # Child index (Level 1)
├── github-memos-docs/
│   └── github-memos-docs-index.md
└── [other folders...]
    └── [folder-name]-index.md
```

## Index Format

**Parent Index** (`docs-index.md`): JSON Lines with collection metadata
```json
{"index": "memos-docs-openmem-net-index.md", "path": "docs/processed/memos-docs-openmem-net-index.md", "description": "...", "priority": 1, "file_count": 56, "total_bytes": 458234, "topics": ["api", "tutorials"]}
```

**Child Indexes** (`*-index.md`): JSON Lines with file metadata
```json
{"file": "overview-introduction.md", "path": "docs/processed/memos-docs.openmem.net/overview-introduction.md", "description": "...", "priority": 1, "bytes": 15420, "type": "overview"}
```

## Priority System

1. **Priority 1**: `memos-docs.openmem.net` - Official website docs (primary source)
2. **Priority 2**: `github-memos-docs` - GitHub repository docs
3. **Priority 3**: `memos-dashboard.openmem.net` - Dashboard docs
4. **Priority 4**: ArXiv research papers
5. **Priority 5**: Blog posts and other sources

## Usage Examples

### Example 1: Find API Documentation

**Task**: "Show me how to configure MemOS"

**Traversal**:
```bash
# 1. Read parent index
grep -i '"priority": 1' docs/processed/docs-index.md | grep -i '"topics":.*"api"'
# Result: memos-docs-openmem-net-index.md

# 2. Read child index
grep -i 'configure\|api' docs/processed/memos-docs.openmem.net/memos-docs-openmem-net-index.md
# Result: {"file": "api-reference-configure-memos.md", "path": "docs/processed/memos-docs.openmem.net/api-reference-configure-memos.md", ...}

# 3. Read source file
cat docs/processed/memos-docs.openmem.net/api-reference-configure-memos.md
```

### Example 2: Understand Architecture (Multi-Priority)

**Task**: "Explain MemOS architecture"

**Traversal**:
```bash
# 1. Search across all priorities
grep -i 'architecture' docs/processed/docs-index.md | sort -t':' -k2 -n
# Results: priority 1, 2, and 4 indexes

# 2. Check highest priority first (1)
grep -i 'architecture' docs/processed/memos-docs.openmem.net/memos-docs-openmem-net-index.md

# 3. If need more detail, check priority 2
grep -i 'architecture' docs/processed/github-memos-docs/github-memos-docs-index.md

# 4. For research depth, check priority 4
grep -i 'architecture' docs/processed/arxiv-2507.03724v3/arxiv-2507.03724v3-index.md
```

### Example 3: Quick Start Tutorial

**Task**: "Get started with MemOS"

**Traversal**:
```bash
# 1. Filter priority 1 (primary docs)
grep '"priority": 1' docs/processed/docs-index.md

# 2. Look for tutorials in child index
grep -i 'quick\|start\|tutorial\|"type": "tutorial"\|"type": "guide"' docs/processed/memos-docs-openmem-net/memos-docs-openmem-net-index.md

# 3. Read relevant files
cat docs/processed/memos-docs.openmem.net/getting_started-quick_start.md
```

### Example 4: Research Deep Dive

**Task**: "What does the research say about memory scheduling?"

**Traversal**:
```bash
# 1. Filter priority 4 (research papers)
grep '"priority": 4' docs/processed/docs-index.md

# 2. Search both paper indexes
grep -i 'scheduling\|algorithm' docs/processed/arxiv-2507.03724v3/arxiv-2507.03724v3-index.md
grep -i 'scheduling\|algorithm' docs/processed/arxiv-2505.22101v1/arxiv-2505.22101v1-index.md

# 3. Read relevant sections
cat docs/processed/arxiv-2507.03724v3/arxiv-2507.03724v3_5architecture-ofmemos.md
```

## Common Agent Tasks

### Task: Configuration
- **Priority**: 1 (official docs)
- **Filter**: `type="api-reference"` OR description contains "configure"
- **Target**: API reference files

### Task: Examples/Tutorials
- **Priority**: 1 (official docs)
- **Filter**: `type="tutorial"` OR path contains "cookbook" OR description contains "example"
- **Target**: Cookbook chapters, getting started guides

### Task: Technical Details
- **Priority**: 1-2 (official + GitHub)
- **Filter**: `type="technical"` OR description contains "architecture|algorithm|design"
- **Target**: Architecture docs, algorithm explanations

### Task: Research/Theory
- **Priority**: 4 (academic papers)
- **Filter**: `type="research"`
- **Target**: ArXiv paper sections

### Task: Community Insights
- **Priority**: 5 (blogs)
- **Filter**: `type="blog"`
- **Target**: Blog articles

## Token Optimization

- Use `grep` to filter indexes before reading full files
- Filter by priority to read most authoritative sources first
- Use `type` field to quickly find relevant content categories
- Check `bytes` to estimate content size before reading

## Integration with Tools

### With MCP Servers
```python
# Read index
with open('docs/processed/docs-index.md') as f:
    indexes = [json.loads(line) for line in f]

# Filter by priority and topic
relevant = [idx for idx in indexes
            if idx['priority'] <= 2 and 'api' in idx['topics']]

# Read child index
with open(relevant[0]['path']) as f:
    files = [json.loads(line) for line in f]
```

### With Search Tools
```bash
# Find all API references across priorities 1-2
for idx in $(grep -l '"priority": [12]' docs/processed/*-index.md); do
    grep '"type": "api-reference"' "$idx"
done
```

## Best Practices

1. **Start with parent index** - understand available collections
2. **Filter by priority** - check highest priority sources first
3. **Use grep efficiently** - filter indexes before reading full content
4. **Check metadata** - use `bytes`, `type`, `topics` to decide relevance
5. **Read progressively** - start with overview/intro, dive deeper as needed

---

**Quick Reference**: Start at `docs/processed/docs-index.md` for all documentation collections.
"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n✓ Created claude.md entry point")


def main():
    # Paths
    project_root = Path('/home/memos/Development/MemOS/memos-data-loader')
    processed_dir = project_root / 'docs' / 'processed'

    print("="*70)
    print("BUILDING DOCUMENTATION INDEXES")
    print("="*70)
    print(f"Project root: {project_root}")
    print(f"Processed dir: {processed_dir}")

    # Find all doc folders (exclude utilities, clean scripts, etc.)
    doc_folders = [
        d for d in processed_dir.iterdir()
        if d.is_dir() and d.name not in ['utilities', 'IMAGES', '__pycache__']
    ]

    print(f"\nFound {len(doc_folders)} documentation folders:")
    for folder in sorted(doc_folders):
        print(f"  - {folder.name}")

    # Create child indexes
    child_metadata = []

    for folder in sorted(doc_folders):
        index_path, metadata = create_child_index(folder, project_root)
        if metadata:
            child_metadata.append(metadata)

    # Create parent index
    parent_index_path = processed_dir / 'docs-index.md'
    create_parent_index(child_metadata, parent_index_path, project_root)

    # Create claude.md entry point
    claude_md_path = project_root / 'docs' / 'claude.md'
    create_claude_md(claude_md_path)

    print("\n" + "="*70)
    print("INDEXING COMPLETE")
    print("="*70)
    print(f"Child indexes: {len(child_metadata)}")
    print(f"Parent index: {parent_index_path}")
    print(f"Entry point: {claude_md_path}")
    print("="*70)


if __name__ == '__main__':
    main()
