# MemOS Data Loader - Quick Start Guide

## 🎯 Purpose
Load security scan outputs (nmap, SSH checks, etc.) into MemOS Dashboard for testing and exploration.

## ⚡ Quick Setup

```bash
# 1. Create virtual environment
cd memos-data-loader
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure API (already done - using Dashboard sandbox)
# API key is in .env file
```

## 🔧 Usage

### Test Mode (NO API CALLS - Budget Safe!)
```bash
# Always start with dry-run to verify!
python src/simple_loader.py --file test-samples/sample-ssh-scan.txt --dry-run
```

### Load from File
```bash
# After dry-run looks good, remove --dry-run
python src/simple_loader.py --file test-samples/sample-ssh-scan.txt
```

### Load from Stdin (Pipe Command Output)
```bash
# Dry-run first
echo "Test output" | python src/simple_loader.py --stdin --source "test" --dry-run

# Real command examples (use sparingly!):
nmap -sV 192.168.1.1 | python src/simple_loader.py --stdin --source "nmap"
ssh-keyscan example.com | python src/simple_loader.py --stdin --source "ssh-scan"
```

### Search Memories
```bash
# Dry-run
python src/simple_loader.py --search "SSH ports" --dry-run

# Real search
python src/simple_loader.py --search "SSH ports"
```

## 📊 Budget Conservation Strategy

**IMPORTANT: We have limited API calls!**

1. **Always test with `--dry-run` first** ✓
2. **Use sample files** (test-samples/) for testing ✓
3. **Start with 1-2 real API calls** to validate
4. **Check Dashboard UI** before loading more
5. **Once validated:** use for real command outputs

## 📁 Sample Data

Three representative samples created:
- `test-samples/sample-ssh-scan.txt` - SSH service check
- `test-samples/sample-port-scan.txt` - Port scanning results
- `test-samples/sample-api-discovery.txt` - Web API enumeration

## 🔄 Workflow

```
1. Run security tool → 2. Dry-run load → 3. Verify output → 4. Real load → 5. Check Dashboard
```

## 🌐 Dashboard Access

- **URL**: https://memos-dashboard.openmem.net/
- **API Key**: Configured in .env
- **User ID**: security_scanner_001

## ⚙️ Configuration

Edit `.env` file:
```bash
MEMOS_API_KEY=your_key_here
MEMOS_BASE_URL=https://memos.memtensor.cn/api/openmem/v1
MEMOS_USER_ID=your_user_id
```

## 🐛 Troubleshooting

**Import error?**
```bash
source venv/bin/activate  # Must activate venv first
```

**API error?**
```bash
# Check .env file exists and has correct API key
cat .env
```

**Want to see what's being sent?**
```bash
# Use --dry-run - it shows the full payload
python src/simple_loader.py --file yourfile.txt --dry-run
```

## 📝 Next Steps

1. ✅ Test with dry-run (DONE)
2. ⏳ **Make 1 real API call to test**
3. ⏳ **Verify data appears in Dashboard UI**
4. ⏳ Test search functionality
5. ⏳ Load actual scan results from loadDataSource
6. ⏳ Apply learnings to local MemOS setup
