# MEMOS Data Loader - Implementation Plan

**Project Goal:** Create a Python CLI tool to load data into MEMOS playground instance (https://memos-playground.openmem.net/)

**Status:** Planning Phase
**Last Updated:** 2025-10-16

---

## Project Overview

### Objectives
- Build a standalone, autonomous data loading script for MEMOS system
- Support three primary use cases (from documentation):
  1. CLI tool stdout ingestion
  2. Chat session imports
  3. [TBD - from scraped documentation]
- Work specifically with MEMOS playground instance
- Generate LLM-optimized documentation for future development reference

### Technical Requirements
- **Language:** Python 3.x
- **Environment:** Debian Linux, isolated venv
- **Interface:** CLI (framework for Claude integration)
- **Logging:** JSON-LN format
- **Scale:** Development/testing phase, dozens of records
- **Mode:** Ongoing/repeated data loading capability
- **Data transformations:** Optional/as-needed
- **No validation/deduplication** in initial version

### Authentication Details

#### Playground Environment
- **Playground URL:** https://memos-playground.openmem.net/
- **Auth Method:** Email + OTP
- **Email:** afonin.es@gmail.com
- **Token:** Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxOTcwODkwNDkzNzQ1MzY5MDkwIiwiZW1haWwiOiJhZm9uaW4uZXNAZ21haWwuY29tIiwiaWF0IjoxNzYwNjA4MDExLCJleHAiOjE3NjMyMDAwMTF9.QTWg4a1g_kcup3KNJzXERUNSJ_3BQlJB4LfMI54OOUo
- **Token Expiry:** 2025-11-15 (30 days from issue)
- **Note:** Playground is a Vue/Nuxt web application, not a direct REST API

#### Dashboard Sandbox Environment (PRIMARY DEVELOPMENT TARGET)
- **Dashboard URL:** https://memos-dashboard.openmem.net/
- **Auth Method:** API Key
- **Token:** mpg-sBTVnDI9930OZa/sXWJ2iK9zICwB++x0A0aQZpKT
- **Token Type:** Dashboard API Key
- **Created:** 2025-10-16
- **Status:** Active
- **API Examples:** See [DASHBOARD_SANDBOX_API.md](./DASHBOARD_SANDBOX_API.md) and API_python*.md files

### Repository Context
- **Working Repository:** MemOS fork at eafonin/MemOS
- **Upstream:** MemTensor/MemOS
- **Current Branch:** main
- **Project Root:** /home/memos/Development/MemOS/

---

## Project Structure

```
/home/memos/Development/MemOS/
└── memos-data-loader/
    ├── PLAN.md                    # This file - master plan
    ├── DASHBOARD_SANDBOX_API.md   # Dashboard sandbox API reference
    ├── PROGRESS.md                # Implementation progress tracking
    ├── docs/                      # LLM-optimized documentation
    │   ├── scraped/              # Raw scraped content
    │   │   └── sections/         # 56 scraped pages + IMAGES/
    │   │       ├── API_pythonHTTP.md   # Dashboard HTTP examples
    │   │       ├── API_pythonSDK.md    # Dashboard SDK examples
    │   │       └── API_pythonCURL.md   # Dashboard cURL examples
    │   ├── processed/            # Converted to markdown, annotated
    │   ├── indexes/              # Topic indexes, cross-references
    │   └── api-reference/        # Technical API documentation
    ├── src/                       # Python source code
    │   ├── __init__.py
    │   ├── cli.py                # Main CLI entry point
    │   ├── auth.py               # Authentication handling
    │   ├── loader.py             # Data loading engine
    │   ├── transformers.py       # Data transformation pipeline
    │   └── logger.py             # JSON-LN logging utilities
    ├── config/                    # Configuration files
    │   ├── config.template.json  # Configuration template
    │   └── .env.example          # Environment variables example
    ├── logs/                      # JSON-LN log files
    ├── tests/                     # Test data and scripts
    ├── venv/                      # Python virtual environment
    ├── requirements.txt           # Python dependencies
    └── README.md                  # Usage documentation
```

---

## Implementation Phases

### PHASE 1: Documentation Intelligence Gathering
**Status:** Pending
**Goal:** Scrape and process MEMOS documentation into LLM-optimized formats

#### 1.1 Source Identification & Scraping
**Input Sources:**
- Official MEMOS documentation: https://memos-docs.openmem.net/
- User-provided PDFs (awaiting delivery)
- User-provided URLs (awaiting delivery)
- MemOS GitHub repository code analysis

**Tasks:**
- [ ] 1.1.1 Receive and catalog PDFs from user
- [ ] 1.1.2 Receive and catalog URLs from user
- [ ] 1.1.3 Scrape official MEMOS documentation site
- [ ] 1.1.4 Extract relevant sections from MemOS repository
- [ ] 1.1.5 Store raw content in `docs/scraped/`

**Deliverable:** Complete raw documentation corpus in `docs/scraped/`

#### 1.2 Documentation Processing & Optimization
**Tasks:**
- [ ] 1.2.1 Convert all content to markdown format
- [ ] 1.2.2 Add metadata annotations (source, date, topic, relevance)
- [ ] 1.2.3 Organize by topic areas (API, data models, use cases, architecture)
- [ ] 1.2.4 Create topic-based index files
- [ ] 1.2.5 Generate cross-reference maps
- [ ] 1.2.6 Extract three primary use cases from documentation

**Deliverable:** LLM-optimized documentation in `docs/processed/` and `docs/indexes/`

---

### PHASE 2: API & Architecture Analysis
**Status:** Pending
**Goal:** Understand how data flows into MEMOS playground

#### 2.1 Playground Instance Exploration
**Tasks:**
- [ ] 2.1.1 Use browser automation/inspection to examine web UI
- [ ] 2.1.2 Capture network requests (API endpoints, payloads)
- [ ] 2.1.3 Document authentication flow
- [ ] 2.1.4 Identify data loading endpoints
- [ ] 2.1.5 Capture request/response formats
- [ ] 2.1.6 Document data model/schema

**Tools:** Browser DevTools, Network inspector, potentially Playwright/Selenium

**Deliverable:** Technical API documentation in `docs/api-reference/playground-api.md`

#### 2.2 Repository Code Analysis
**Tasks:**
- [ ] 2.2.1 Analyze MemOS repository for data import functionality
- [ ] 2.2.2 Review API endpoint implementations
- [ ] 2.2.3 Extract database schema information
- [ ] 2.2.4 Document error handling patterns
- [ ] 2.2.5 Identify relevant code examples for reference

**Focus Areas:**
- `/memos/mem_os/` - Memory OS implementation
- `/memos/mem_cube/` - MemCube data structures
- API routes and handlers
- Data validation and transformation logic

**Deliverable:** Code reference documentation in `docs/api-reference/code-reference.md`

---

### PHASE 3: Script Development
**Status:** Pending
**Goal:** Build the Python CLI data loading tool

#### 3.1 Project Setup
**Tasks:**
- [ ] 3.1.1 Create Python virtual environment
- [ ] 3.1.2 Define dependencies (requests, click/typer, pydantic, etc.)
- [ ] 3.1.3 Set up project structure
- [ ] 3.1.4 Create configuration templates
- [ ] 3.1.5 Initialize git tracking for the subdirectory

**Deliverable:** Working development environment

#### 3.2 Core Infrastructure
**Tasks:**
- [ ] 3.2.1 Implement JSON-LN logging system (`src/logger.py`)
- [ ] 3.2.2 Build configuration management (`config/`)
- [ ] 3.2.3 Create authentication handler (`src/auth.py`)
- [ ] 3.2.4 Set up CLI framework (`src/cli.py`)

**Technologies:**
- Logging: Custom JSON-LN formatter
- Config: JSON + environment variables
- CLI: Click or Typer framework
- Auth: Requests with Bearer token

**Deliverable:** Core utilities and CLI skeleton

#### 3.3 Data Loading Engine
**Tasks:**
- [ ] 3.3.1 Implement Use Case 1: CLI stdout ingestion
- [ ] 3.3.2 Implement Use Case 2: Chat session imports
- [ ] 3.3.3 Implement Use Case 3: [TBD from docs]
- [ ] 3.3.4 Build data transformation pipeline (`src/transformers.py`)
- [ ] 3.3.5 Create main loader orchestrator (`src/loader.py`)
- [ ] 3.3.6 Add error handling and retry logic

**Deliverable:** Working data loader with three use cases

---

### PHASE 4: Testing & Validation
**Status:** Pending
**Goal:** Validate functionality against playground instance

#### 4.1 Integration Testing
**Tasks:**
- [ ] 4.1.1 Test authentication with playground
- [ ] 4.1.2 Test each use case with sample data
- [ ] 4.1.3 Verify data appears correctly in playground
- [ ] 4.1.4 Test error scenarios (network, auth, malformed data)
- [ ] 4.1.5 Validate logging output

**Deliverable:** Test results and bug fixes

#### 4.2 Documentation & Examples
**Tasks:**
- [ ] 4.2.1 Create usage guide (`README.md`)
- [ ] 4.2.2 Document CLI commands and options
- [ ] 4.2.3 Provide example data files
- [ ] 4.2.4 Document configuration options
- [ ] 4.2.5 Add troubleshooting guide

**Deliverable:** Complete user documentation

---

## Success Criteria

### Phase 1 Complete When:
- [x] All documentation sources scraped and organized
- [x] LLM-optimized markdown documentation generated
- [x] Three use cases clearly identified and documented
- [x] Topic indexes and cross-references created

### Phase 2 Complete When:
- [x] Playground API endpoints documented
- [x] Authentication flow understood and documented
- [x] Data schemas and payloads documented
- [x] Relevant code examples extracted and annotated

### Phase 3 Complete When:
- [x] Python venv configured with all dependencies
- [x] CLI tool accepts commands and configuration
- [x] All three use cases implemented
- [x] Authentication works with playground
- [x] JSON-LN logging operational

### Phase 4 Complete When:
- [x] All use cases tested successfully against playground
- [x] Documentation complete and accurate
- [x] Example data provided
- [x] Known issues documented

---

## Dependencies & Blockers

### External Dependencies
- User to provide PDFs for documentation
- User to provide URLs for documentation
- Playground instance must remain accessible
- Auth token valid until 2025-11-15

### Technical Dependencies
- Python 3.8+ available on Debian system
- Network access to playground instance
- Sufficient disk space for documentation corpus

### Potential Blockers
- Token expiration (need re-authentication process)
- API changes in playground
- Rate limiting or access restrictions
- Undocumented API behavior

---

## Design Principles

1. **Autonomous Operation:** Minimize user intervention after initial setup
2. **Fresh Implementation:** No code reuse from existing MemOS - build from requirements
3. **Documentation First:** Understand before building
4. **Iterative Development:** Work step-by-step with checkpoints
5. **Defensive Coding:** Assume failures, handle gracefully
6. **Clear Logging:** Every operation logged in structured format
7. **Configuration Over Code:** Externalize settings for flexibility

---

## Next Steps

### Immediate Actions (Awaiting User Input)
1. **Receive PDFs** - User to provide PDF documentation sources
2. **Receive URLs** - User to provide URL documentation sources
3. **Plan Approval** - User to review and approve this plan

### After User Input
1. Begin Phase 1.1.1 - Catalog received documentation
2. Start parallel documentation scraping tasks
3. Move to Phase 1.2 - Process and optimize documentation

---

## Change Log

| Date | Phase | Change | Reason |
|------|-------|--------|--------|
| 2025-10-16 | Planning | Initial plan created | Project kickoff |

---

## Notes & Decisions

- **Decision:** Use dedicated subdirectory `memos-data-loader/` for clean separation
- **Decision:** No data validation/deduplication in v1 - focus on core loading
- **Decision:** JSON-LN logging format for structured, parseable logs
- **Decision:** Python + venv for portability and dependency isolation
- **Decision:** CLI interface for flexibility and automation
- **Note:** Token expires in 30 days - may need re-auth mechanism for long-term use
- **Note:** Documentation will be reusable for other MemOS development activities
