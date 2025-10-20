# Virtual Environment Guide for Debug Agents

**Problem:** Python 3.11+ uses PEP 668 to prevent system-wide package installations. Agents trying to `pip install` packages will fail with "externally-managed-environment" errors.

**Solution:** Each debug agent has its own isolated virtual environment (venv) with the required dependencies.

---

## Quick Start

### For Users

**Option 1: Use the run script (Recommended)**
```bash
cd debug-agents/neo4j-agent
./setup.sh      # First time only
./run.sh --test # Automatically activates venv
```

**Option 2: Manual activation**
```bash
cd debug-agents/neo4j-agent
source venv/bin/activate  # Activate venv
python scripts/neo4j_utils.py --test
deactivate  # When done
```

### For Claude Code Agents

When an agent needs to run Python scripts for Neo4j or Qdrant:

**ALWAYS use the venv-aware commands:**

```bash
# ❌ WRONG - Will fail with PEP 668 error
cd /home/memos/Development/MemOS/debug-agents/neo4j-agent
python scripts/neo4j_utils.py

# ✅ CORRECT - Option 1: Use run.sh wrapper
cd /home/memos/Development/MemOS/debug-agents/neo4j-agent
./run.sh --test

# ✅ CORRECT - Option 2: Activate venv first
cd /home/memos/Development/MemOS/debug-agents/neo4j-agent
source venv/bin/activate && python scripts/neo4j_utils.py --test

# ✅ CORRECT - Option 3: Use venv python directly
cd /home/memos/Development/MemOS/debug-agents/neo4j-agent
venv/bin/python scripts/neo4j_utils.py --test
```

---

## Setup Instructions

### Initial Setup (First Time)

Each agent directory has a `setup.sh` script that:
1. Creates a virtual environment (`venv/` directory)
2. Installs required dependencies from `requirements.txt`
3. Configures the environment

**Neo4j Agent:**
```bash
cd /home/memos/Development/MemOS/debug-agents/neo4j-agent
./setup.sh
```

**Qdrant Agent:**
```bash
cd /home/memos/Development/MemOS/debug-agents/qdrant-agent
./setup.sh
```

### Verify Setup

```bash
# Check venv exists
ls -la debug-agents/neo4j-agent/venv

# Check packages installed
source debug-agents/neo4j-agent/venv/bin/activate
pip list
```

---

## Agent Directory Structure

```
debug-agents/
├── neo4j-agent/
│   ├── venv/                  # Virtual environment (gitignored)
│   ├── requirements.txt       # Python dependencies
│   ├── setup.sh              # Setup script (creates venv)
│   ├── run.sh                # Run script (auto-activates venv)
│   ├── config.env            # Environment configuration
│   └── scripts/
│       └── neo4j_utils.py    # Agent scripts
│
├── qdrant-agent/
│   ├── venv/                  # Virtual environment (gitignored)
│   ├── requirements.txt       # Python dependencies
│   ├── setup.sh              # Setup script
│   ├── run.sh                # Run script
│   ├── config.env            # Environment configuration
│   └── scripts/
│       └── qdrant_utils.py   # Agent scripts
│
└── VENV_GUIDE.md             # This file
```

---

## Troubleshooting

### Error: "externally-managed-environment"

**Problem:**
```
× This environment is externally managed
╰─> To install Python packages system-wide, try apt install...
```

**Cause:** Trying to install packages without using venv.

**Solution:** Run `./setup.sh` to create the venv, then use `./run.sh` or activate the venv manually.

### Error: "No module named 'neo4j'"

**Problem:** Python can't find the required package.

**Solution:**
```bash
# Make sure venv is activated
cd debug-agents/neo4j-agent
source venv/bin/activate

# Verify package is installed
pip list | grep neo4j

# If not installed, reinstall
pip install -r requirements.txt
```

### Error: "venv: command not found"

**Problem:** Python venv module not available.

**Solution:**
```bash
# Install python3-venv
sudo apt install python3-venv

# Then retry setup
./setup.sh
```

### Venv exists but packages missing

**Solution:** Recreate the venv
```bash
rm -rf venv
./setup.sh
```

### Permission denied: ./setup.sh

**Solution:** Make script executable
```bash
chmod +x setup.sh run.sh
./setup.sh
```

---

## For Developers: Adding New Agents

When creating a new debug agent:

1. **Create agent directory**
```bash
mkdir debug-agents/new-agent
cd debug-agents/new-agent
```

2. **Create requirements.txt**
```txt
# Add your dependencies
some-package==1.0.0
python-dotenv==1.0.0
```

3. **Copy setup template**
```bash
# Copy from existing agent and modify
cp ../neo4j-agent/setup.sh .
cp ../neo4j-agent/run.sh .
# Edit to match your agent name and requirements
```

4. **Create scripts directory**
```bash
mkdir scripts
# Add your Python scripts
```

5. **Test**
```bash
./setup.sh
./run.sh
```

---

## Agent Prompts (For Claude Code Agent Development)

When configuring agents that need Python dependencies, include this in the agent prompt:

```markdown
## Environment Setup

This agent requires Python packages. Use the virtual environment:

**Setup (first time):**
```bash
cd /home/memos/Development/MemOS/debug-agents/AGENT_NAME
./setup.sh
```

**Running scripts:**
```bash
# Option 1: Use run.sh wrapper (recommended)
./run.sh [arguments]

# Option 2: Activate venv manually
source venv/bin/activate
python scripts/your_script.py
deactivate

# Option 3: Use venv python directly
venv/bin/python scripts/your_script.py
```

**Important:** Never use system Python (`python3` or `pip` directly) - always use the venv.
```

---

## Maintenance

### Updating Dependencies

**Update a single package:**
```bash
source venv/bin/activate
pip install --upgrade package-name
pip freeze | grep package-name >> requirements.txt
```

**Update all packages:**
```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
pip freeze > requirements.txt
```

### Checking Package Versions

```bash
source venv/bin/activate
pip list
pip show neo4j  # Detailed info
```

### Cleaning Up

**Remove venv (will be recreated on next setup):**
```bash
rm -rf venv/
```

**Full reset:**
```bash
rm -rf venv/
./setup.sh
```

---

## Why Separate Venvs per Agent?

**Pros:**
- ✅ Complete isolation (no dependency conflicts)
- ✅ Different package versions per agent if needed
- ✅ Can delete/recreate individual agent without affecting others
- ✅ Clear ownership (each agent owns its dependencies)

**Cons:**
- ⚠️ More disk space (~50MB per venv)
- ⚠️ Duplicate packages if agents share dependencies

**Decision:** We use separate venvs because isolation is more important than disk space for debug agents.

---

## FAQ

**Q: Can I use a shared venv for all agents?**
A: Yes, but not recommended. Separate venvs provide better isolation and avoid version conflicts.

**Q: Do I need to commit the venv directory?**
A: No, venv/ is gitignored. Only commit requirements.txt, setup.sh, and run.sh.

**Q: Can I use pipenv or poetry instead?**
A: Yes, but venv is simpler and has no external dependencies.

**Q: What if I need different Python versions?**
A: Use `python3.11 -m venv venv` or specify the version you need.

**Q: Can I install packages with --break-system-packages?**
A: **No!** This is dangerous and can break your system Python. Always use venv.

---

## Reference

- **PEP 668:** https://peps.python.org/pep-0668/ (externally-managed-environments)
- **Python venv:** https://docs.python.org/3/library/venv.html
- **pip in venv:** https://pip.pypa.io/en/stable/user_guide/#using-pip-from-your-program

---

**Last Updated:** 2025-10-20
**Maintainer:** Development Team
