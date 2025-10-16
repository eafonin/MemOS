# MEMOS Data Loader

A Python CLI tool for loading data into MEMOS playground instance.

## Status

🚧 **In Development** - Currently in planning phase

## Quick Links

- **Master Plan:** [PLAN.md](./PLAN.md) - Comprehensive implementation plan
- **Dashboard Sandbox:** https://memos-dashboard.openmem.net/ (PRIMARY TARGET)
- **Dashboard API Reference:** [DASHBOARD_SANDBOX_API.md](./DASHBOARD_SANDBOX_API.md)
- **Playground:** https://memos-playground.openmem.net/ (Web UI)
- **Documentation:** [docs/](./docs/) - LLM-optimized MEMOS documentation
- **API Examples:** [docs/scraped/sections/](./docs/scraped/sections/) - API_python*.md files

## Project Structure

```
memos-data-loader/
├── PLAN.md              # Master implementation plan
├── README.md            # This file
├── docs/                # LLM-optimized documentation
│   ├── scraped/        # Raw scraped content
│   ├── processed/      # Processed markdown docs
│   ├── indexes/        # Topic indexes
│   └── api-reference/  # API documentation
├── src/                 # Python source code
├── config/              # Configuration files
├── logs/                # JSON-LN logs
└── venv/                # Python virtual environment
```

## Development Phases

1. **Phase 1:** Documentation Intelligence Gathering
2. **Phase 2:** API & Architecture Analysis
3. **Phase 3:** Script Development
4. **Phase 4:** Testing & Validation

## Requirements

- Python 3.8+
- Debian Linux
- Network access to MEMOS playground

## Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies (coming soon)
pip install -r requirements.txt
```

## Usage

Documentation coming after development phase.

## Design Principles

- Autonomous operation
- Fresh implementation (no code reuse)
- Documentation-first approach
- Iterative development
- Defensive coding
- Structured logging (JSON-LN)

## Support

For questions or issues, refer to the master plan in [PLAN.md](./PLAN.md).
