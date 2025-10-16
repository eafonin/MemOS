# MemOS Documentation - Introduction

**Source:** https://memos-docs.openmem.net/overview/introduction
**Scraped:** 2025-10-16
**Type:** Official Documentation

---

# MemOS (Memory Operating System)

**MemOS (Memory Operating System)** is a memory management system for AI applications designed to provide long-term memory capabilities similar to human cognition. Rather than relying solely on native model context, it enables AI systems to remember, invoke, update, and schedule memories proactively.

## Why MemOS is Needed

Native large language models face inherent limitations:
- **Limited context:** No matter how large the token window is, it cannot carry long-term knowledge
- **Severe forgetting:** Preferences mentioned by the user last week may disappear in the next conversation
- **Difficult to manage:** As interactions increase, memories become chaotic

The system abstracts the memory layer, eliminating complex workarounds and enabling memory reuse across different agents.

## Core Capabilities

- **Personalized conversations** with automatic preference supplementation
- **Team knowledge base conversion** from fragmented interactions
- **Task continuity** across sessions and applications
- **Multi-layer memory scheduling** for optimized retrieval
- **Open extensibility** as standalone API or framework integration

## Technical Architecture

The documentation references several memory types and modules:
- **KV Cache Memory**
- **Plaintext Memory** (General Textual, Tree Textual)
- **Graph databases** (Neo4j, Nebula)
- **Parametric Memory**

## Documentation Structure

The documentation includes sections on:
- Quick Start guides
- Cloud platform API reference
- Use cases (financial, life, writing assistants)
- Open source implementation
- Best practices and contribution guidelines

## Key Links

- **GitHub repository:** https://github.com/MemTensor/MemOS
- **Quick Start:** `/overview/quick_start/overview`
- **API Reference:** `/api-reference/configure-memos`

---

## Notes for Data Loading

This documentation indicates MemOS supports multiple memory types and scheduling. Key implications for data loading:
1. Need to understand memory type differentiation (KV Cache vs Plaintext vs Graph)
2. Data import likely requires specifying memory type
3. May need user/agent association for personalized memories
4. Multi-layer scheduling suggests importance of memory metadata
