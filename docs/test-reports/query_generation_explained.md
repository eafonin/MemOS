# Query Generation in MemOS Retrieval Testing

## How test_retrieval.py Generates Queries

### Strategy: Extract from Loaded Documents

The script reads actual document content and extracts meaningful queries:

```python
def generate_queries_from_docs(self, max_queries: int = 10):
    """Generate test queries by extracting key phrases from documents."""
    
    # Sample random documents
    sample_files = random.sample(all_files, min(max_queries, len(all_files)))
    
    for file_path in sample_files:
        content = file.read()
        lines = content.split('\n')
        
        # Look for significant lines
        for line in lines:
            if (line.startswith('#') or              # Markdown headers
                'architecture' in line.lower() or    # Key concepts
                'design' in line.lower() or
                'implementation' in line.lower() or
                'memory' in line.lower()):
                
                # Clean up and use as query
                query = line.lstrip('#').strip()
                if 10 < len(query) < 100:
                    queries.append(query)
```

### Extraction Patterns

1. **Headers** (lines starting with #)
   - "## Tree Textual Memory" → "Tree Textual Memory"
   - "### Configuration Options" → "Configuration Options"

2. **Concept Lines** (containing keywords)
   - Lines with "architecture", "design", "implementation", "memory"
   - Example: "MemOS architecture provides three layers" → extracted as query

3. **Length Filtering**
   - Too short (<10 chars): Skip (not meaningful)
   - Too long (>100 chars): Skip (too specific)
   - Sweet spot: 10-100 chars

### General Queries Added

In addition to extracted queries, the script adds these broad questions:

```python
general_queries = [
    "MemOS architecture and design",
    "memory management in language models",
    "chunking strategy for documents",
    "embedding models comparison",
    "Neo4j graph database integration",
]
```

## Query Types & Performance

Based on the demonstration results:

| Query Type | Example | Avg Similarity | Quality |
|------------|---------|----------------|---------|
| KEYWORD (technical) | "tree textual memory implementation" | 0.710 | 🟢 EXCELLENT |
| SEMANTIC (intent) | "best practices for memory optimization" | 0.702 | 🟢 EXCELLENT |
| SEMANTIC (question) | "How to configure MemOS..." | 0.656 | 🟡 GOOD |
| CONCEPT (broad) | "MemOS architecture layers" | 0.644 | 🟡 GOOD |
| OFF-TOPIC | "how to make coffee with MemOS" | 0.528 | 🟠 MODERATE |

## Why This Strategy Works

### Advantages:
1. **Real-world coverage**: Queries come from actual documentation
2. **Diverse topics**: Random sampling ensures variety
3. **Natural language**: Headers and sentences are human-readable
4. **Self-validating**: Queries should find their source documents

### Example Extraction from Real Doc:

**Document: contribution-overview.md**
```markdown
# Contributing to MemOS

## Getting Started

### Setting Up Development Environment
Install dependencies with Poetry...

### Understanding the Architecture
MemOS uses a three-layer design...
```

**Extracted Queries:**
- "Contributing to MemOS" (from H1)
- "Getting Started" (from H2)
- "Setting Up Development Environment" (from H3)
- "Understanding the Architecture" (from H3)

## Performance Analysis from Demonstration

### Success Cases:

**Query: "tree textual memory implementation"**
- Type: KEYWORD (precise technical term)
- Best match: 0.7787 similarity
- Why it worked: Exact terminology match in documentation

**Query: "best practices for memory optimization"**
- Type: SEMANTIC (user intent)
- Best match: 0.7319 similarity
- Why it worked: BGE-Large understands intent, matches related concepts

**Query: "How to configure MemOS with different embedding models"**
- Type: SEMANTIC (natural question)
- Best match: 0.6779 similarity
- Why it worked: Semantic understanding of configuration context

### Moderate Case:

**Query: "MemOS architecture layers"**
- Type: CONCEPT (broad topic)
- Best match: 0.6675 similarity
- Why moderate: Broad query matches many tangentially related docs

### Failure Case:

**Query: "how to make coffee with MemOS"**
- Type: OFF-TOPIC
- Best match: 0.5431 similarity
- Why it failed: 
  - "coffee" not in any documents
  - Vector similarity finds weak connections (bibliography references, random words)
  - Still returns ~52% match (random citations happen to have similar words)
  - ⚠️ This shows semantic search can't detect when query is completely invalid!

## Key Insights

1. **Technical keywords work best** (0.71 avg)
   - Precise terminology has exact matches
   
2. **User intent queries work well** (0.70 avg)
   - BGE-Large model understands semantic meaning
   
3. **Natural questions are good** (0.66 avg)
   - Slightly lower because of conversational phrasing
   
4. **Broad concepts are okay** (0.64 avg)
   - More noise, less precision
   
5. **Off-topic queries fail gracefully** (0.53 avg)
   - No hard failure, but low relevance
   - System can't detect query is invalid
   - User needs to judge result quality

## Limitations of Current Approach

### What Works:
- ✅ Finding relevant documentation
- ✅ Understanding semantic intent
- ✅ Handling synonyms and related concepts
- ✅ Fast retrieval (<1 second)

### What Doesn't Work Well:
- ❌ Detecting completely invalid queries
- ❌ Understanding negation ("not about X")
- ❌ Multi-hop reasoning ("given X, what about Y?")
- ❌ Temporal queries ("latest version of...")

### Recommendation:
Add query validation or relevance thresholding:
```python
if avg_similarity < 0.55:
    return "No relevant results found for this query"
```
