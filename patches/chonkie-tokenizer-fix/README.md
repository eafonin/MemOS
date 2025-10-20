# Chonkie Tokenizer Fix - Patch Package

**Date:** 2025-10-20
**Author:** Claude (Anthropic)
**Status:** ✅ Tested and verified in docker-test1

---

## Overview

This patch package fixes the issue where Chonkie text chunker was falling back to character-based chunking instead of using proper tokenization from HuggingFace cache.

## Problem Summary

**Symptoms:**
- Chonkie logs: "Could not load tokenizer with 'tokenizers'. Falling back to 'tiktoken'."
- MemOS logs: "Failed to initialize tokenizer, will use character-based chunking"
- Poor chunking quality due to character-based fallback

**Root Causes:**
1. Missing `tiktoken` package (ValueError: Tokenizer not found)
2. HF_ENDPOINT environment variable preventing cache access
3. Default tokenizer "gpt2" not available in HuggingFace cache
4. Tokenizer string passed to Chonkie instead of loaded object

## Patches Included

### 0001-fix-chonkie-tokenizer-loading-from-cache.patch

**Primary fix** - Modifies 4 source files to properly load tokenizers from cache:

1. **src/memos/chunkers/sentence_chunker.py**
   - Adds logic to load tokenizer from cache with HF_ENDPOINT workaround
   - Passes loaded tokenizer object (not string) to Chonkie
   - Handles errors gracefully with fallback

2. **src/memos/configs/chunker.py**
   - Changes default tokenizer from "gpt2" to "sentence-transformers/all-mpnet-base-v2"

3. **src/memos/api/config.py**
   - Updates 3 hardcoded "gpt2" references to sentence-transformers model

4. **src/memos/mem_os/utils/default_config.py**
   - Updates 1 hardcoded "gpt2" reference to sentence-transformers model

### 0002-add-tiktoken-dependency.patch

**Dependency fix** - Adds tiktoken to requirements.txt:

- Adds `tiktoken==0.8.0` after `threadpoolctl==3.6.0`
- Provides fallback tokenizer for Chonkie when transformers unavailable
- Prevents ValueError during Chonkie initialization

## How to Apply

### Option 1: Apply All Patches at Once

```bash
cd /home/memos/Development/MemOS

# Apply both patches in order
git apply patches/chonkie-tokenizer-fix/*.patch

# Or use 'patch' command
cat patches/chonkie-tokenizer-fix/*.patch | patch -p1

# Verify changes
git diff
```

### Option 2: Apply Patches Individually

```bash
cd /home/memos/Development/MemOS

# Apply tokenizer loading fix
git apply patches/chonkie-tokenizer-fix/0001-fix-chonkie-tokenizer-loading-from-cache.patch

# Apply tiktoken dependency
git apply patches/chonkie-tokenizer-fix/0002-add-tiktoken-dependency.patch
```

### Option 3: Cherry-Pick (if patches are git commits)

```bash
# If patches are converted to commits:
git cherry-pick <commit-hash-0001>
git cherry-pick <commit-hash-0002>
```

## Verification

After applying patches, verify the fix works:

```bash
# 1. Rebuild Docker image
cd docker-test1
docker-compose build memos-api

# 2. Start services
docker-compose up -d

# 3. Test tokenizer loading
docker exec test1-memos-api python3 -c "
from memos.chunkers.sentence_chunker import SentenceChunker
from memos.configs.chunker import SentenceChunkerConfig

config = SentenceChunkerConfig()
chunker = SentenceChunker(config)
chunks = chunker.chunk('This is a test sentence. And another one.')
print(f'✅ Success! Chunks: {len(chunks)}, Tokens: {chunks[0].token_count}')
"

# Expected output:
# Loading tokenizer 'sentence-transformers/all-mpnet-base-v2' from local cache...
# Successfully loaded tokenizer from cache: MPNetTokenizerFast
# ✅ Success! Chunks: 1, Tokens: 11
```

## Requirements

**Before applying:**
- Ensure HuggingFace cache contains `sentence-transformers/all-mpnet-base-v2`
- If using docker, mount cache at `/root/.cache/huggingface`
- Or download model before applying patch

**Download model (if needed):**
```bash
python3 -c "
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-mpnet-base-v2')
print('Model downloaded to cache')
"
```

## Files Modified

### Source Code (4 files)
- `src/memos/chunkers/sentence_chunker.py` (+27 lines, -1 line)
- `src/memos/configs/chunker.py` (+1 line, -1 line)
- `src/memos/api/config.py` (+3 lines, -3 lines)
- `src/memos/mem_os/utils/default_config.py` (+1 line, -1 line)

### Dependencies (1 file)
- `docker/requirements.txt` (+1 line) - if using patch 0002
- Or manually add to your requirements file

**Total:** 5 files modified, 33 insertions(+), 6 deletions(-)

## Compatibility

**Tested with:**
- Python: 3.11
- Chonkie: 1.1.1
- transformers: 4.53.2
- tokenizers: 0.21.2
- tiktoken: 0.8.0
- sentence-transformers: 4.1.0

**Docker images:**
- python:3.11-slim (Debian 12 bookworm)

**Environment:**
- Offline mode (HF_HUB_OFFLINE=1, TRANSFORMERS_OFFLINE=1)
- HF_ENDPOINT=https://hf-mirror.com (workaround applied)

## Known Issues

**Non-Critical:**
- `product.py` still shows tokenizer warning for "Qwen/Qwen3-0.6B" streaming feature
- This is separate from Chonkie and doesn't affect chunking functionality
- Streaming feature falls back to character-based counting (acceptable)

**If you need streaming tokenizer:**
- Download Qwen/Qwen3-0.6B to cache
- Or change product.py to use sentence-transformers model

## Rollback

To revert these changes:

```bash
cd /home/memos/Development/MemOS

# Revert all patches
git apply -R patches/chonkie-tokenizer-fix/*.patch

# Or revert individually
git apply -R patches/chonkie-tokenizer-fix/0002-add-tiktoken-dependency.patch
git apply -R patches/chonkie-tokenizer-fix/0001-fix-chonkie-tokenizer-loading-from-cache.patch
```

## Additional Documentation

See also:
- `docker-test1/CHONKIE_FIX_SUMMARY.md` - Detailed technical analysis
- `docker-test1/SOLUTION_SUMMARY.md` - Initial troubleshooting notes

## Support

**Questions or Issues:**
1. Check logs: `docker-compose logs memos-api | grep tokenizer`
2. Verify cache: `docker exec <container> ls /root/.cache/huggingface/hub/`
3. Test transformers directly: `AutoTokenizer.from_pretrained('sentence-transformers/all-mpnet-base-v2', local_files_only=True)`

**Common Issues:**
- "Model not found": Download sentence-transformers/all-mpnet-base-v2 to cache
- "Connection refused": Check HF_ENDPOINT env var is set in Dockerfile
- "Character-based chunking": Verify tokenizer loaded (check logs for "Successfully loaded")

## License

These patches maintain the same license as the MemOS project.

---

**Status:** ✅ Ready for production
**Priority:** Medium (improves chunking quality)
**Breaking Changes:** None (backward compatible)
