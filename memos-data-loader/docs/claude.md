# MemOS Documentation Index - Agent Guide

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
