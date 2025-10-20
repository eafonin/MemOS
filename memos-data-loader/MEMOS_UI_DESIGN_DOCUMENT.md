# MemOS Explorer UI - Design Document

**Version:** 1.0
**Date:** 2025-10-20
**Status:** Design Phase
**Tech Stack:** Streamlit (Python)

---

## 1. Executive Summary

A standalone web UI for visualizing, exploring, and testing MemOS memory systems. Built with Streamlit for rapid development, deployed as an independent Docker container that can connect to any MemOS instance (local, docker-test1, production, etc.).

### Key Features:
1. **Neo4j Memory Explorer** - Visualize loaded memories with table/list and timeline views
2. **Qdrant Embeddings Tester** - Test semantic search and relevance calculations
3. **Chat with Fact Tracking** - Interactive chat showing fact extraction and injection

---

## 2. Architecture Overview

### Deployment Model: Standalone Container

```
┌─────────────────────────────────────────────────┐
│  Docker Network (e.g., docker-test1_default)    │
│                                                  │
│  ┌──────────────┐    ┌──────────────┐          │
│  │ memos-ui     │───▶│ memos-api    │          │
│  │ (Streamlit)  │    │ (port 8001)  │          │
│  │ port 8501    │    └──────────────┘          │
│  └──────────────┘                               │
│         │                                        │
│         ├─────────▶ Neo4j (bolt://...:7687)     │
│         │                                        │
│         └─────────▶ Qdrant (http://...:6333)    │
│                                                  │
└─────────────────────────────────────────────────┘
```

**Connection Strategy:**
- UI container joins the same Docker network as MemOS services
- All connections configurable via environment variables
- Can be started/stopped independently without affecting MemOS

### Tech Stack Rationale

**Streamlit** chosen for:
- ✅ Python-native (matches MemOS ecosystem)
- ✅ Rapid prototyping (minutes to add features)
- ✅ Built-in data visualization (charts, tables, metrics)
- ✅ Native support for Neo4j, Qdrant clients
- ✅ Auto-reload during development
- ✅ Simple deployment (single `streamlit run` command)
- ✅ Great for data exploration and ML apps

---

## 3. Feature Specifications

### 3.1 Neo4j Memory Explorer (Priority 1)

**Purpose:** Visualize and explore the 319+ Memory nodes loaded into Neo4j.

#### View 1: Memory Table/List with Details Panel

**Layout:**
```
┌────────────────────────────────────────────────────────────┐
│ Filters: [Type ▼] [Tags] [Date Range] [Search: ______]    │
├────────────────────────────────────────────────────────────┤
│ Total: 319 memories | Filtered: 45                         │
├─────────────────────────┬──────────────────────────────────┤
│ Memory List (Left)      │ Details Panel (Right)            │
│                         │                                  │
│ ☑ LongTerm | 2025-10-20│ Memory ID: c9fe5906-302...       │
│   MemOS Documentation.. │                                  │
│   Relevance: 0.99      │ Key: MemOS Documentation Review   │
│   Tags: [doc, MemOS]   │                                  │
│                        │ Memory Type: LongTermMemory       │
│ ☐ Working | 2025-10-20 │ Status: activated                 │
│   Neo4j configuration..│ Confidence: 0.99                  │
│   Relevance: 0.85      │                                  │
│   Tags: [neo4j, db]    │ Memory Content:                   │
│                        │ ┌──────────────────────────────┐ │
│ ☐ LongTerm | 2025-10-20│ │ [user viewpoint] The user    │ │
│   API endpoints...     │ │ shared documentation about   │ │
│   Relevance: 0.78      │ │ MemOS from help.md...        │ │
│                        │ └──────────────────────────────┘ │
│ [Load More...]         │                                  │
│                        │ Tags: documentation, MemOS, te..  │
│                        │                                  │
│                        │ Sources: (2 messages) [Expand]   │
│                        │ Created: 2025-10-20 14:39:59     │
│                        │ Updated: 2025-10-20 14:39:59     │
└─────────────────────────┴──────────────────────────────────┘
```

**Features:**
- **Filters:**
  - Memory Type (LongTerm, Working, User)
  - Tags (multi-select)
  - Date Range (from/to)
  - Full-text search in memory content
  - User ID (for multi-user systems)

- **List Display:**
  - Checkbox for bulk operations (future: export, delete)
  - Memory type icon/badge
  - Truncated title (from `key` field)
  - Relevance/confidence score
  - Date created
  - Tags preview

- **Details Panel:**
  - Full memory content with word wrap
  - All metadata fields
  - Expandable sources (show message history)
  - Copy button for ID
  - Link to Qdrant vector (if sync successful)
  - Usage history (who/when accessed)

- **Actions:**
  - Export to JSON/CSV
  - Copy memory content
  - View in timeline
  - Jump to related memories (future: if relationships exist)

#### View 2: Timeline View by Creation Date

**Layout:**
```
┌────────────────────────────────────────────────────────────┐
│ Timeline: [Daily ▼] [Date Range: _____ to _____] [Filter] │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  October 20, 2025                                          │
│  ├─ 10:38 AM ─────────────────────────────────────────    │
│  │  ● API.md (LongTerm)                                    │
│  │  ● ARCHITECTURE.md (LongTerm)                           │
│  │  ● CONFIGURATION.md (LongTerm)                          │
│  │  ... [+7 more]                                          │
│  │                                                          │
│  ├─ 10:45 AM ─────────────────────────────────────────    │
│  │  ● arxiv-2505.22101v1 (LongTerm)                        │
│  │  ● Memory types doc (Working)                           │
│  │  ... [+12 more]                                         │
│  │                                                          │
│  └─ 11:00 AM ─────────────────────────────────────────    │
│     ● INDEX.md (LongTerm)                                  │
│     ● memos-quickstart (LongTerm)                          │
│     ... [+25 more]                                         │
│                                                             │
│  [Click any memory to view details] →                     │
└────────────────────────────────────────────────────────────┘
```

**Features:**
- **Grouping:**
  - Daily (default)
  - Hourly (for dense data)
  - Weekly (for long-term view)

- **Visualization:**
  - Collapsible time sections
  - Color-coded by memory type
  - Memory count per time slot
  - Click to expand details

- **Statistics Panel:**
  - Total memories loaded
  - Memories per day/hour
  - Peak loading time
  - Memory type distribution chart

- **Filters:**
  - Same as table view
  - Date range selector
  - Memory type legend (click to toggle)

#### View 3: Statistics Dashboard

**Layout:**
```
┌────────────────────────────────────────────────────────────┐
│ Memory Statistics Overview                                  │
├──────────────────┬──────────────────┬─────────────────────┤
│ Total Memories   │ LongTerm Mem     │ Working Mem         │
│      319         │      293         │       20            │
├──────────────────┴──────────────────┴─────────────────────┤
│                                                             │
│ Memory Type Distribution:                                  │
│ ████████████████████████ 91.8% LongTerm (293)             │
│ ██ 6.3% Working (20)                                       │
│ █ 1.9% User (6)                                            │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ Top 10 Tags:                                               │
│ 1. documentation (245)    6. API (32)                      │
│ 2. MemOS (189)            7. configuration (28)            │
│ 3. technical (156)        8. neo4j (24)                    │
│ 4. architecture (87)      9. memory (22)                   │
│ 5. installation (45)     10. chunking (18)                 │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ Memory Creation Timeline (Last 7 Days):                    │
│ [Interactive line chart showing memories created per day]  │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ Data Quality Metrics:                                      │
│ • Confidence: Avg 0.99 (Min: 0.95, Max: 0.99)             │
│ • Sources: 319/319 have sources (100%)                     │
│ • Vector Sync: 612/612 success (100%)                      │
│ • Status: 319 activated, 0 archived                        │
└─────────────────────────────────────────────────────────────┘
```

**Features:**
- Key metrics cards
- Memory type distribution (pie/bar chart)
- Tag cloud or top tags list
- Timeline chart (creation over time)
- Data quality indicators
- User distribution (for multi-user systems)

---

### 3.2 Qdrant Embeddings Tester (Priority 2)

**Purpose:** Test semantic search quality and explore embedding space.

#### View 1: Semantic Search Explorer

**Layout:**
```
┌────────────────────────────────────────────────────────────┐
│ Semantic Search Tester                                      │
├────────────────────────────────────────────────────────────┤
│                                                             │
│ Query: [What is MemOS and how does it work? ___________]   │
│                                                             │
│ Parameters:                                                 │
│ • Top K: [5 ▼]  • Memory Type: [All ▼]  • Threshold: 0.5  │
│                                                             │
│ [Search] [Clear]                                            │
│                                                             │
├────────────────────────────────────────────────────────────┤
│ Results (5 found):                                          │
│                                                             │
│ 1. ┌─ Score: 0.7484 ──────────────────────────────┐       │
│    │ Key: MemOS Documentation Review              │       │
│    │ Type: LongTermMemory                          │       │
│    │                                               │       │
│    │ Memory: [user viewpoint] The user shared...  │       │
│    │                                               │       │
│    │ Tags: documentation, MemOS, memory management │       │
│    │ [View Details] [View Vector]                  │       │
│    └───────────────────────────────────────────────┘       │
│                                                             │
│ 2. ┌─ Score: 0.7350 ──────────────────────────────┐       │
│    │ Key: MemOS core architecture                  │       │
│    │ ...                                           │       │
│                                                             │
│ [Export Results] [Visualize Similarity]                    │
└────────────────────────────────────────────────────────────┘
```

**Features:**
- **Query Input:**
  - Free-text query
  - Example queries (dropdown)
  - Query history

- **Parameters:**
  - Top K (number of results)
  - Memory type filter
  - Similarity threshold
  - User ID filter
  - Custom metadata filters

- **Results Display:**
  - Relevance score (color-coded)
  - Memory preview
  - Metadata preview
  - Expandable full content
  - Link to Neo4j node

- **Analysis:**
  - Score distribution histogram
  - Average relevance
  - Query-result similarity matrix
  - Export to CSV/JSON

#### View 2: Vector Space Explorer

**Layout:**
```
┌────────────────────────────────────────────────────────────┐
│ Vector Space Explorer                                       │
├────────────────────────────────────────────────────────────┤
│                                                             │
│ Select Memory: [MemOS Documentation Review ▼]              │
│ Vector ID: a4688f10-766c-413d-8d1c-f83f6c885a44           │
│                                                             │
│ Vector Statistics:                                          │
│ • Dimension: 768                                            │
│ • L2 Norm: 1.024                                           │
│ • Non-zero elements: 652 (84.9%)                           │
│                                                             │
├────────────────────────────────────────────────────────────┤
│                                                             │
│ Find Similar Vectors:                                       │
│ Top 10 Most Similar:                                        │
│                                                             │
│ 1. Score: 0.95 | MemOS architecture docs                   │
│ 2. Score: 0.89 | Memory types overview                     │
│ 3. Score: 0.87 | Installation guide                        │
│ ...                                                         │
│                                                             │
├────────────────────────────────────────────────────────────┤
│                                                             │
│ Vector Visualization: [PCA ▼] [t-SNE] [UMAP]              │
│ [2D scatter plot showing vectors colored by memory type]   │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

**Features:**
- **Vector Inspection:**
  - Raw vector display (truncated)
  - Vector statistics (norm, sparsity)
  - Download vector as numpy/json

- **Similarity Search:**
  - Find K nearest neighbors
  - Distance metric selection
  - Similarity threshold

- **Visualization:**
  - Dimensionality reduction (PCA, t-SNE, UMAP)
  - 2D/3D scatter plots
  - Color by memory type, tag, date
  - Interactive (hover for details)

#### View 3: Batch Testing & Evaluation

**Layout:**
```
┌────────────────────────────────────────────────────────────┐
│ Batch Search Evaluation                                     │
├────────────────────────────────────────────────────────────┤
│                                                             │
│ Test Suite: [MemOS Knowledge Base ▼] [Custom]             │
│                                                             │
│ Queries (6):                                                │
│ ✓ What is MemOS? (Avg: 0.73)                              │
│ ✓ Neo4j configuration (Avg: 0.61)                          │
│ ✓ Installation guide (Avg: 0.76)                           │
│ ✓ Memory types (Avg: 0.77)                                 │
│ ✓ API endpoints (Avg: 0.56)                                │
│ ✓ Chunking strategies (Avg: 0.34)                          │
│                                                             │
│ [Run Tests] [Add Query] [Export Results]                   │
│                                                             │
├────────────────────────────────────────────────────────────┤
│                                                             │
│ Results Summary:                                            │
│ • Total Queries: 6                                          │
│ • Avg Top-1 Score: 0.63                                    │
│ • Avg Top-5 Score: 0.58                                    │
│ • Queries with results: 6/6 (100%)                         │
│                                                             │
│ [View Detailed Report] [Compare with Baseline]             │
└────────────────────────────────────────────────────────────┘
```

**Features:**
- **Test Suites:**
  - Pre-defined query sets
  - Custom query upload (CSV)
  - Expected results (optional)

- **Metrics:**
  - Average relevance scores
  - Precision@K
  - Recall@K (if ground truth provided)
  - MRR (Mean Reciprocal Rank)

- **Reporting:**
  - Per-query results
  - Aggregate statistics
  - Export to CSV/JSON
  - Comparison with previous runs

---

### 3.3 Chat with Fact Tracking (Priority 3)

**Purpose:** Interactive chat showing how facts are extracted, preserved, and injected.

#### Main View: Chat Interface with Inspector

**Layout:**
```
┌────────────────────────────────────────────────────────────┐
│ MemOS Chat with Fact Tracking                              │
├─────────────────────────────┬──────────────────────────────┤
│ Chat (Left 60%)             │ Inspector (Right 40%)        │
│                             │                              │
│ ┌─────────────────────────┐ │ Phase: [Memory Retrieval ▼] │
│ │ Chat History            │ │                              │
│ │                         │ │ ─── Memory Retrieval ────   │
│ │ 👤 You:                 │ │ Query: "What is MemOS?"      │
│ │ What is MemOS?          │ │                              │
│ │                         │ │ Retrieved 8 memories:        │
│ │ 🤖 Assistant:           │ │ 1. MemOS Documentation (0.74)│
│ │ MemOS is a memory       │ │ 2. Core architecture (0.73)  │
│ │ orchestration system... │ │ 3. Introduction doc (0.71)   │
│ │                         │ │ ... [+5 more]                │
│ │ [View References]       │ │                              │
│ │                         │ │ ─── Fact Extraction ─────    │
│ │                         │ │ Extracted 3 facts:           │
│ │                         │ │ • MemOS is memory OS         │
│ │                         │ │ • 3 types: Working/Long/User │
│ │                         │ │ • Architecture details       │
│ │                         │ │                              │
│ │                         │ │ ─── Memory Injection ────    │
│ │                         │ │ Injected into LLM context:   │
│ │                         │ │ Context window: 2,048 tokens │
│ │                         │ │ Memory tokens: 485 tokens    │
│ │                         │ │ [View Full Context]          │
│ └─────────────────────────┘ │                              │
│                             │ ─── Response Generation ──   │
│ Message: [Type here...___] │ Model: gpt-4                 │
│ [Send] [Clear] [Export]    │ Tokens: 128 generated        │
│                             │ Time: 2.3s                   │
└─────────────────────────────┴──────────────────────────────┘
```

**Features:**

**Chat Panel:**
- Standard chat interface
- Message history
- Markdown rendering
- Code highlighting
- Copy messages
- Clear history

**Inspector Panel (Tabs):**

**Tab 1: Memory Retrieval**
- Query sent to Qdrant
- Retrieved memories list
- Relevance scores
- Filter applied (type, threshold)
- Retrieval time

**Tab 2: Fact Extraction**
- Extracted facts from response
- Fact type (user viewpoint, assistant viewpoint, etc.)
- Confidence scores
- What will be stored

**Tab 3: Memory Injection**
- Memories injected into context
- Token count breakdown
- Context window usage
- Truncation/summarization (if any)

**Tab 4: Response Generation**
- Model used
- Temperature/parameters
- Generation time
- Token usage
- Cost estimation

**Tab 5: Memory Storage**
- New memories created
- Memory IDs
- Neo4j node IDs
- Qdrant vector IDs
- Storage success/failure

**Additional Features:**
- **Conversation Export:** Save entire chat as JSON/MD
- **Memory Replay:** Show which memories were used for each message
- **Diff View:** Compare context before/after memory injection
- **Performance Metrics:** Response time, retrieval time, storage time

---

## 4. Technical Implementation

### 4.1 Project Structure

```
memos-ui/
├── Dockerfile                  # Container definition
├── docker-compose.yml         # Standalone deployment
├── requirements.txt           # Python dependencies
├── .env.example              # Configuration template
├── README.md                 # Setup instructions
│
├── app.py                    # Main Streamlit app entry point
├── config.py                 # Configuration loader
│
├── pages/                    # Streamlit pages (multi-page app)
│   ├── 1_🗂️_Memory_Explorer.py
│   ├── 2_🔍_Embeddings_Tester.py
│   └── 3_💬_Chat_Inspector.py
│
├── components/               # Reusable UI components
│   ├── __init__.py
│   ├── memory_card.py       # Memory display card
│   ├── timeline.py          # Timeline visualization
│   ├── filters.py           # Filter widgets
│   └── metrics.py           # Metrics displays
│
├── services/                # Backend services
│   ├── __init__.py
│   ├── neo4j_service.py     # Neo4j queries
│   ├── qdrant_service.py    # Qdrant queries
│   ├── memos_api.py         # MemOS API client
│   └── analytics.py         # Data analysis utilities
│
├── utils/                   # Helper utilities
│   ├── __init__.py
│   ├── formatting.py        # Data formatting
│   ├── visualization.py     # Chart helpers
│   └── export.py            # Export utilities
│
└── assets/                  # Static assets
    ├── styles.css           # Custom CSS
    └── images/              # Icons, logos
```

### 4.2 Key Dependencies

```txt
# Core
streamlit==1.31.0
python-dotenv==1.0.0

# Database clients
neo4j==5.14.0
qdrant-client==1.7.0

# API client
requests==2.31.0

# Data processing
pandas==2.1.4
numpy==1.26.2

# Visualization
plotly==5.18.0
altair==5.2.0

# NLP/ML (for vector visualization)
scikit-learn==1.3.2
umap-learn==0.5.5

# Utilities
python-dateutil==2.8.2
```

### 4.3 Configuration (Environment Variables)

**File: `.env.example`**
```bash
# MemOS UI Configuration

# UI Settings
UI_TITLE=MemOS Explorer
UI_PAGE_ICON=🧠
UI_LAYOUT=wide

# MemOS API Connection
MEMOS_API_URL=http://test1-memos-api:8000
MEMOS_USER_ID=test1_user

# Neo4j Connection
NEO4J_URI=bolt://test1-neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
NEO4J_DATABASE=neo4j

# Qdrant Connection
QDRANT_URL=http://test1-qdrant:6333
QDRANT_COLLECTION=neo4j_vec_db

# Optional: Authentication
# UI_USERNAME=admin
# UI_PASSWORD=secret

# Optional: Features
ENABLE_EXPORT=true
ENABLE_EDIT=false
ENABLE_DELETE=false
MAX_RESULTS=100
```

### 4.4 Docker Deployment

**File: `Dockerfile`**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run Streamlit
CMD ["streamlit", "run", "app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true"]
```

**File: `docker-compose.yml`**
```yaml
version: '3.8'

services:
  memos-ui:
    build: .
    container_name: memos-ui
    ports:
      - "8501:8501"
    environment:
      - MEMOS_API_URL=${MEMOS_API_URL}
      - NEO4J_URI=${NEO4J_URI}
      - NEO4J_USER=${NEO4J_USER}
      - NEO4J_PASSWORD=${NEO4J_PASSWORD}
      - QDRANT_URL=${QDRANT_URL}
      - QDRANT_COLLECTION=${QDRANT_COLLECTION}
    networks:
      - memos-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3

networks:
  memos-network:
    name: docker-test1_default
    external: true
```

**Usage:**
```bash
# Join existing docker-test1 network
cd memos-ui
cp .env.example .env
# Edit .env with your settings

# Start UI (connects to docker-test1 services)
docker-compose up -d

# Access UI
open http://localhost:8501

# Restart UI without touching MemOS services
docker-compose restart

# Stop UI
docker-compose down
```

---

## 5. Development Roadmap

### Phase 1: Foundation (Week 1) ✓ Priority 1
**Goal:** Basic Neo4j Memory Explorer

- [ ] Project setup (Docker, Streamlit, dependencies)
- [ ] Configuration system (load from .env)
- [ ] Neo4j service (connect, query memories)
- [ ] Basic UI layout (sidebar, main area)
- [ ] Memory table/list view
- [ ] Memory details panel
- [ ] Basic filters (type, date range)

**Deliverable:** Working UI showing all 319 memories in a table

### Phase 2: Visualization (Week 2) ✓ Priority 1
**Goal:** Timeline and Statistics

- [ ] Timeline view by creation date
- [ ] Time grouping (daily, hourly, weekly)
- [ ] Statistics dashboard
- [ ] Charts (memory distribution, tags, timeline)
- [ ] Export functionality (CSV, JSON)

**Deliverable:** Complete Memory Explorer with multiple views

### Phase 3: Embeddings (Week 3) → Priority 2
**Goal:** Qdrant Embeddings Tester

- [ ] Qdrant service (connect, search)
- [ ] Semantic search interface
- [ ] Search results display
- [ ] Vector space explorer
- [ ] Similarity visualization
- [ ] Batch testing framework

**Deliverable:** Working embeddings tester with search and visualization

### Phase 4: Chat (Week 4) → Priority 3
**Goal:** Chat with Fact Tracking

- [ ] MemOS API integration
- [ ] Chat interface
- [ ] SSE stream handling
- [ ] Inspector panel (tabs)
- [ ] Memory retrieval tracking
- [ ] Fact extraction display
- [ ] Context injection visualization
- [ ] Performance metrics

**Deliverable:** Full chat interface with complete fact tracking

### Phase 5: Polish (Week 5)
**Goal:** Production-ready UI

- [ ] Error handling
- [ ] Loading states
- [ ] Empty states
- [ ] Responsive design
- [ ] Custom CSS styling
- [ ] Documentation
- [ ] User guide
- [ ] Demo video

**Deliverable:** Polished, documented UI ready for demos

---

## 6. UI/UX Design Principles

### 6.1 Design Goals

1. **Clarity:** Data should be immediately understandable
2. **Speed:** Fast loading, responsive interactions
3. **Simplicity:** Minimal clicks to accomplish tasks
4. **Consistency:** Uniform patterns across all pages
5. **Feedback:** Clear indication of actions and states

### 6.2 Visual Design

**Color Scheme:**
- Primary: Blue (#1f77b4) - for actions, links
- Success: Green (#2ca02c) - for success states
- Warning: Orange (#ff7f0e) - for warnings
- Error: Red (#d62728) - for errors
- Neutral: Gray (#7f7f7f) - for disabled, secondary

**Memory Type Colors:**
- LongTermMemory: Blue (#1f77b4)
- WorkingMemory: Orange (#ff7f0e)
- UserMemory: Green (#2ca02c)

**Typography:**
- Headers: Inter or system font
- Body: System font (optimal for long reading)
- Code: JetBrains Mono or Fira Code

### 6.3 Interaction Patterns

**Loading States:**
- Spinner for quick operations (<3s)
- Progress bar for long operations (>3s)
- Skeleton screens for list views

**Empty States:**
- Helpful message
- Suggested actions
- Icon or illustration

**Error States:**
- Clear error message
- Suggested fix
- Retry action
- Link to docs/support

---

## 7. Sample Code Snippets

### 7.1 Main App Entry Point

**File: `app.py`**
```python
import streamlit as st
from config import load_config

# Page config
st.set_page_config(
    page_title="MemOS Explorer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load configuration
config = load_config()

# Sidebar
with st.sidebar:
    st.title("🧠 MemOS Explorer")
    st.markdown("---")

    # Connection status
    st.subheader("Connections")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Neo4j", "✓" if check_neo4j() else "✗")
    with col2:
        st.metric("Qdrant", "✓" if check_qdrant() else "✗")

    st.markdown("---")

    # User selection
    st.subheader("Settings")
    user_id = st.text_input("User ID", config.MEMOS_USER_ID)

    st.markdown("---")
    st.caption(f"Connected to: {config.MEMOS_API_URL}")

# Main content
st.title("Welcome to MemOS Explorer")
st.markdown("""
This UI allows you to explore and test your MemOS memory system:

- **📊 Memory Explorer:** Visualize your 319 loaded memories
- **🔍 Embeddings Tester:** Test semantic search and relevance
- **💬 Chat Inspector:** See how facts are extracted and injected
""")

# Quick stats
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Memories", get_memory_count())
with col2:
    st.metric("Total Vectors", get_vector_count())
with col3:
    st.metric("Sync Success", "100%")
```

### 7.2 Neo4j Service

**File: `services/neo4j_service.py`**
```python
from neo4j import GraphDatabase
from typing import List, Dict, Optional
import pandas as pd

class Neo4jService:
    def __init__(self, uri: str, user: str, password: str, database: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.database = database

    def get_all_memories(
        self,
        user_name: str,
        memory_type: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict]:
        """Get all memories with optional filters"""

        query = """
        MATCH (m:Memory {user_name: $user_name})
        WHERE $memory_type IS NULL OR m.memory_type = $memory_type
        RETURN m
        ORDER BY m.created_at DESC
        LIMIT $limit
        """

        with self.driver.session(database=self.database) as session:
            result = session.run(
                query,
                user_name=user_name,
                memory_type=memory_type,
                limit=limit
            )
            return [dict(record["m"]) for record in result]

    def get_memory_by_id(self, memory_id: str) -> Optional[Dict]:
        """Get a single memory by ID"""

        query = "MATCH (m:Memory {id: $id}) RETURN m"

        with self.driver.session(database=self.database) as session:
            result = session.run(query, id=memory_id)
            record = result.single()
            return dict(record["m"]) if record else None

    def get_statistics(self, user_name: str) -> Dict:
        """Get memory statistics"""

        query = """
        MATCH (m:Memory {user_name: $user_name})
        RETURN
            count(m) as total,
            collect(DISTINCT m.memory_type) as types,
            min(m.created_at) as earliest,
            max(m.created_at) as latest
        """

        with self.driver.session(database=self.database) as session:
            result = session.run(query, user_name=user_name)
            record = result.single()
            return dict(record) if record else {}

    def close(self):
        self.driver.close()
```

### 7.3 Memory Card Component

**File: `components/memory_card.py`**
```python
import streamlit as st
from datetime import datetime

def render_memory_card(memory: dict, expanded: bool = False):
    """Render a memory card with details"""

    # Memory type badge color
    type_colors = {
        "LongTermMemory": "blue",
        "WorkingMemory": "orange",
        "UserMemory": "green"
    }
    color = type_colors.get(memory.get("memory_type"), "gray")

    with st.container():
        col1, col2 = st.columns([4, 1])

        with col1:
            st.markdown(f"**{memory.get('key', 'Untitled')}**")
        with col2:
            st.markdown(f":{color}[{memory.get('memory_type')}]")

        # Preview or full content
        if expanded:
            st.markdown(memory.get("memory", "No content"))

            # Metadata
            with st.expander("📋 Metadata"):
                st.json({
                    "id": memory.get("id"),
                    "confidence": memory.get("confidence"),
                    "status": memory.get("status"),
                    "tags": memory.get("tags", []),
                    "created_at": str(memory.get("created_at")),
                    "vector_sync": memory.get("vector_sync")
                })
        else:
            preview = memory.get("memory", "")[:200] + "..."
            st.markdown(preview)

        # Actions
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Details", key=f"details_{memory['id']}"):
                st.session_state.selected_memory = memory["id"]
        with col2:
            if st.button("Copy ID", key=f"copy_{memory['id']}"):
                st.code(memory["id"])
        with col3:
            st.caption(f"Created: {format_date(memory.get('created_at'))}")
```

---

## 8. Testing Strategy

### 8.1 Development Testing

**Manual Testing Checklist:**
- [ ] All pages load without errors
- [ ] Neo4j connection works
- [ ] Qdrant connection works
- [ ] Memory list displays correctly
- [ ] Filters work as expected
- [ ] Timeline view renders correctly
- [ ] Search returns relevant results
- [ ] Chat interface sends/receives messages
- [ ] Export functions work

### 8.2 Integration Testing

**Test Scenarios:**
1. **Connect to docker-test1**
   - Verify all 319 memories load
   - Verify 612 vectors accessible
   - Test search with known queries

2. **Connect to production**
   - Handle large datasets (10K+ memories)
   - Performance with slow network
   - Timeout handling

3. **Handle edge cases**
   - Empty database
   - Network failures
   - Invalid credentials
   - Malformed data

---

## 9. Documentation Requirements

### 9.1 User Documentation

**README.md sections:**
1. Introduction (what is MemOS Explorer)
2. Features overview
3. Installation (Docker setup)
4. Configuration (environment variables)
5. Usage guide (screenshots)
6. Troubleshooting
7. FAQ

### 9.2 Developer Documentation

**DEVELOPMENT.md sections:**
1. Project structure
2. Development setup (local)
3. Adding new features
4. Code style guide
5. Testing guidelines
6. Deployment process

---

## 10. Future Enhancements

### Beyond MVP:

**Features:**
- [ ] Interactive graph visualization (force-directed)
- [ ] Memory editing/deletion (with confirmation)
- [ ] Bulk operations (export, delete, tag)
- [ ] Advanced analytics (clustering, trends)
- [ ] Real-time updates (WebSocket)
- [ ] Multi-user comparison
- [ ] Memory diff viewer
- [ ] API endpoint testing tool
- [ ] Performance profiling
- [ ] Memory consolidation/archival tools

**Technical:**
- [ ] Caching (Redis) for faster queries
- [ ] Pagination for large datasets
- [ ] Background task queue (Celery)
- [ ] User authentication (OAuth)
- [ ] Role-based access control
- [ ] Audit logging
- [ ] A/B testing framework

---

## 11. Success Metrics

**Launch Criteria:**
- [ ] All Phase 1 features complete
- [ ] Successfully connects to docker-test1
- [ ] Displays all 319 memories
- [ ] No critical bugs
- [ ] Documentation complete

**Adoption Metrics:**
- Number of active users
- Average session duration
- Most used features
- Feature request frequency

**Performance Metrics:**
- Page load time < 2s
- Search response time < 1s
- Memory list load time < 3s
- Zero crashes/errors

---

## 12. Budget & Resources

### Time Estimate:
- **Phase 1 (Foundation):** 20-30 hours
- **Phase 2 (Visualization):** 15-20 hours
- **Phase 3 (Embeddings):** 25-30 hours
- **Phase 4 (Chat):** 30-40 hours
- **Phase 5 (Polish):** 15-20 hours
- **Total:** 105-140 hours (~3-4 weeks full-time)

### Resources Needed:
- Python developer (Streamlit experience)
- UI/UX feedback (optional)
- Test data (already have 164 docs loaded)

---

## 13. Risks & Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Streamlit limitations | Medium | Low | Prototype first, pivot if needed |
| Performance with large data | High | Medium | Implement pagination, caching |
| Neo4j/Qdrant API changes | Medium | Low | Abstract with service layer |
| Complex graph visualization | Low | Medium | Start with simple views |
| User adoption | High | Medium | Focus on useful features first |

---

## Appendix A: Wireframes

*(Wireframes would be added here with tools like Figma, Excalidraw, or hand-drawn sketches)*

## Appendix B: API Integration Examples

**MemOS API Client:**
```python
import requests
from typing import List, Dict

class MemosAPIClient:
    def __init__(self, base_url: str, user_id: str):
        self.base_url = base_url
        self.user_id = user_id

    def search(self, query: str, top_k: int = 5) -> Dict:
        url = f"{self.base_url}/product/search"
        payload = {
            "user_id": self.user_id,
            "query": query,
            "top_k": top_k
        }
        response = requests.post(url, json=payload)
        return response.json()

    def chat(self, query: str, stream: bool = True):
        url = f"{self.base_url}/product/chat"
        payload = {
            "user_id": self.user_id,
            "query": query,
            "internet_search": False
        }

        if stream:
            return requests.post(url, json=payload, stream=True)
        else:
            return requests.post(url, json=payload)
```

---

**Document Status:** DRAFT
**Next Steps:** Review, feedback, then proceed to Phase 1 implementation
**Questions:** Contact development team
