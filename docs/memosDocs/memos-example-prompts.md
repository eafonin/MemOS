# Example Prompts for MemOS Development

## 🐍 Python Code Development Prompts

### Prompt 1: Building a Domain-Specific Knowledge Assistant
```
Using the MemOS documentation, specifically referencing:
- "memos Building an Intelligent Novel Analysis System with MemOS.pdf"
- "memos Using MemOS to Build a ProductionGrade Knowledge QA System.pdf" 
- "memos TreeTextMemory_ Structured Hierarchical Textual Memory.pdf"

Please generate a complete Python implementation for a medical knowledge assistant that:
1. Uses TreeTextMemory with Neo4j backend for hierarchical medical knowledge storage
2. Implements concept graph augmentation for medical terminology relationships
3. Includes a MemReader configuration optimized for processing medical literature (PDFs, research papers)
4. Provides semantic search with multi-hop reasoning for differential diagnosis support
5. Implements the production-grade API client pattern from the QA system example
6. Uses embeddings optimized for medical text (suggest best model from documentation)

Include error handling, memory lifecycle management, and the scheduling configuration for managing working memory (recent consultations) vs long-term memory (medical knowledge base).
```

### Prompt 2: Multi-Agent Memory Coordination System
```
Based on the MemOS architecture documentation:
- "2507.03724v3_MEMEOS.pdf" (Section 5.3: Memory Pipeline and Multi-agent coordination)
- "memos MemOS Examples.pdf" (Example 5: Multi-Memory Scheduling)
- "memos Memory Scheduling.pdf"
- "memos Linux API Version.pdf" (Recipe 1.3: MemCube lifecycle management)

Create a Python implementation for a multi-agent customer service system where:
1. Multiple agents share a common knowledge base (TreeTextMemory) but maintain individual conversation contexts (GeneralTextMemory)
2. Implement the MemCube lifecycle manager from Linux API examples
3. Use the Memory Pipeline pattern for chaining operations: retrieve → augment → update → archive
4. Include dynamic scheduling that prioritizes based on customer priority and query complexity
5. Implement proper multi-tenant isolation using the patterns from NebulaGraph backend
6. Add KVCache memory for frequently accessed responses (FAQ optimization)

Show how agents hand off conversations while preserving context, and how the system learns from resolved tickets to improve the knowledge base.
```

### Prompt 3: Real-time Personalization Engine
```
Referencing these MemOS documents:
- "memos Let the Financial Assistant Understand Customer Preferences Behind Behaviors.pdf"
- "memos Memory Production.pdf"
- "memos Memory Recall and Instruction Completion.pdf"

Develop a Python real-time personalization engine that:
1. Transforms user clickstream and behavior data into semantic memories using MemReader
2. Implements the behavior → memory abstraction pattern from the financial assistant example
3. Creates user preference profiles that evolve based on interactions
4. Uses both working memory (current session) and long-term memory (historical preferences)
5. Implements the instruction completion chain to generate personalized recommendations
6. Includes confidence scoring and memory decay for outdated preferences

The code should handle high-throughput events (1000+ events/second), batch memory updates efficiently, and provide sub-100ms retrieval for personalization decisions.
```

---

## 📋 System Requirements Prompts

### Prompt 4: Enterprise MemOS Deployment Requirements
```
Using the comprehensive MemOS documentation, particularly:
- "memos MemOS Configuration Guide.pdf" (all configuration requirements)
- "memos Using MemOS to Build a ProductionGrade Knowledge QA System.pdf"
- "memos REST API Server.pdf" and all API Reference documents (1-12)
- "memos Security Configuration Memos.pdf"
- "Database Configuration Memos.pdf"

Generate a complete System Requirements Document (SRD) for an enterprise deployment of MemOS that will:
1. Support 10,000 concurrent users with individual MemCubes
2. Handle 1 million memories per day with real-time indexing
3. Integrate with existing corporate SSO (OAuth 2.0)
4. Provide 99.9% availability with disaster recovery

Include:
- Functional requirements (from API references and use cases)
- Non-functional requirements (performance, security, scalability)
- Hardware specifications for Neo4j cluster, vector databases, and application servers
- Network architecture with rate limiting and load balancing
- Storage requirements for different memory types and retention policies
- Security requirements including encryption, authentication, and audit logging
- Integration requirements for existing enterprise systems
- Monitoring and observability requirements
- Backup and recovery specifications
- Compliance considerations (GDPR, HIPAA if medical data)
```

---

## 🏗️ Architecture Document Prompts

### Prompt 5: Comprehensive MemOS Architecture Design
```
Based on the complete MemOS documentation set, especially:
- "2507.03724v3_MEMEOS.pdf" (complete technical architecture)
- "memos Architecture.pdf" (system design patterns)
- "memos Graph Memory Backend.pdf" and "memos NebulaGraphBased Plaintext Memory Backend.pdf"
- "memos Memory Lifecycle Management.pdf"
- "memos MCP Model Context Protocol Setup Guide.pdf"
- All memory type documents (GeneralTextMemory, TreeTextMemory)

Create a detailed Software Architecture Document (SAD) that includes:

1. EXECUTIVE SUMMARY
   - Vision and goals from the MemOS overview
   - Key architectural decisions and trade-offs

2. SYSTEM ARCHITECTURE
   - 4+1 architectural views (Logical, Process, Development, Physical, Scenarios)
   - Component diagrams showing MemCube, MemReader, MOS, and Memory Pipeline relationships
   - Deployment architecture for distributed setup with Neo4j/NebulaGraph clusters
   - Data flow diagrams for memory production, scheduling, and recall

3. TECHNICAL ARCHITECTURE
   - Memory hierarchy (Plaintext, Activation, Parameter) with storage strategies
   - API gateway pattern using the REST API Server
   - Microservices breakdown if applicable
   - Message queue integration for async memory processing
   - Cache layers (Redis for KVCache, CDN for static content)

4. HARDWARE REQUIREMENTS
   Based on the production QA system example, specify:
   - Compute: CPU/GPU requirements for LLM inference and embedding generation
   - Memory: RAM requirements for different scales (startup/SMB/enterprise)
   - Storage: SSD/HDD mix for hot/warm/cold memory tiers
   - Network: Bandwidth for model serving and API traffic
   - Example configurations for 100/1,000/10,000 user deployments

5. INTEGRATION ARCHITECTURE
   - MCP protocol integration for AI assistants
   - Webhook patterns for external systems
   - Database choices (when to use SQLite vs PostgreSQL vs MySQL)
   - Graph database selection (Neo4j vs NebulaGraph trade-offs)
   - Vector database options and embedding strategies

6. SCALABILITY & PERFORMANCE
   - Horizontal scaling strategies for each component
   - Memory scheduling optimizations from best practices
   - Benchmark data from the academic paper
   - Bottleneck analysis and mitigation strategies

7. SECURITY ARCHITECTURE
   - Zero-trust security model implementation
   - Multi-tenant isolation patterns
   - Encryption in transit and at rest
   - API security with rate limiting and authentication
   - Audit logging and compliance tracking

8. OPERATIONAL ARCHITECTURE
   - CI/CD pipeline for MemOS deployments
   - Monitoring stack (metrics, logs, traces)
   - Disaster recovery and backup strategies
   - Blue-green deployment for zero-downtime updates

Include architecture decision records (ADRs) for key choices like:
- Why TreeTextMemory vs GeneralTextMemory for different use cases
- Graph database selection criteria
- Synchronous vs asynchronous memory processing
- Monolithic MOS vs distributed microservices
```

---

## 💡 Tips for Using These Prompts

1. **Combine with Specific Files**: Always reference 2-3 specific PDF files to ground the response in actual documentation
2. **Layer Complexity**: Start with simpler implementations and add complexity based on the comprehensive examples
3. **Cross-Reference**: Use the MD index hierarchy to find related documents that provide additional context
4. **Version-Specific**: Reference "memos Linux API Version.pdf" for Linux-specific implementations
5. **Production Patterns**: Always include references to production guides and best practices documents
6. **Error Handling**: Include "memos Common Errors and Solutions.pdf" to ensure robust implementations

## 🎯 Expected Outputs

These prompts should generate:
- **Code**: 500-1000 lines of production-ready Python with comments
- **Requirements**: 15-25 page detailed requirements documents
- **Architecture**: 30-40 page comprehensive architecture documents with diagrams
- **All outputs** should be immediately actionable and reference specific sections from the MemOS documentation