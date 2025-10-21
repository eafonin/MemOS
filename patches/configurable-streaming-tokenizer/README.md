# Configurable Streaming Tokenizer Patch

**Version**: 1.0.0
**Created**: 2025-10-21
**Status**: ✅ Tested and Verified
**Applies to**: MemOS v1.1.2+

## Table of Contents

1. [Overview](#overview)
2. [Problem Statement](#problem-statement)
3. [Solution](#solution)
4. [Configuration](#configuration)
5. [Auto-Detection Logic](#auto-detection-logic)
6. [Supported Tokenizers](#supported-tokenizers)
7. [Offline Mode Support](#offline-mode-support)
8. [Installation](#installation)
9. [Testing](#testing)
10. [Troubleshooting](#troubleshooting)
11. [Technical Details](#technical-details)

---

## Overview

This patch makes the streaming tokenizer **configurable** via environment variables, enabling MemOS to work seamlessly with different LLM backends while maintaining proper token boundaries during chat response streaming.

### What This Patch Does

- ✅ Makes streaming tokenizer **configurable** via `MOS_STREAMING_TOKENIZER` environment variable
- ✅ Adds **intelligent auto-detection** based on your chat model (`MOS_CHAT_MODEL`)
- ✅ Provides **graceful fallback** to character-based chunking if tokenizer fails
- ✅ Supports **offline deployments** with HuggingFace cache
- ✅ Works with **any LLM backend** (Qwen, Claude, GPT, etc.)

### What This Patch Does NOT Affect

- ❌ **Document chunking tokenizer** - This remains `bert-base-uncased` (configured in sentence_chunker.py)
- ❌ **LLM selection** - Your chat model configuration stays the same
- ❌ **Memory storage or retrieval** - No changes to core MemOS functionality

---

## Problem Statement

### Background

MemOS uses tokenizers in **two separate contexts**:

1. **Document Chunking** (`sentence_chunker.py`): Splits documents into semantic chunks for storage
   - Uses `bert-base-uncased` (universal, works offline)
   - ✅ Already configurable and working

2. **Chat Streaming** (`product.py`): Chunks chat responses for real-time streaming to users
   - Was **hardcoded** to `Qwen/Qwen3-0.6B`
   - ❌ **Problem**: Incompatible with non-Qwen LLMs and offline deployments

### Issues with Hardcoded Tokenizer

| Issue | Impact | Severity |
|-------|--------|----------|
| **Wrong tokenizer family** | Incorrect token boundaries for Claude/GPT responses | 🟡 Medium |
| **Missing from cache** | Fails in offline mode with `HF_HUB_OFFLINE=1` | 🔴 High |
| **Not configurable** | Cannot adapt to different deployment scenarios | 🟡 Medium |
| **Error messages** | Confusing warnings during startup | 🟢 Low |

### Example Error (Before Patch)

```
[WARNING] Failed to initialize tokenizer, will use character-based chunking:
We couldn't connect to 'https://hf-mirror.com' to load the files, and couldn't find them in the cached files.
```

**Result**: Streaming falls back to character-based chunking (functional but suboptimal).

---

## Solution

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  MOS_STREAMING_TOKENIZER                    │
│                  Environment Variable                        │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ├─ "auto" ──────┐
                  │                │
                  │         ┌──────▼──────────────────────┐
                  │         │  Auto-Detection Logic       │
                  │         │  Based on MOS_CHAT_MODEL    │
                  │         └──────┬──────────────────────┘
                  │                │
                  │                ├─ "qwen" → Qwen/Qwen3-0.6B
                  │                ├─ "claude" → gpt2
                  │                ├─ "gpt" → gpt2
                  │                └─ default → bert-base-uncased
                  │
                  └─ "Qwen/Qwen3-0.6B" (explicit) ────┐
                  └─ "gpt2" (explicit) ────────────────┤
                  └─ "bert-base-uncased" (explicit) ───┘
                                                        │
                                      ┌─────────────────▼───────────────────┐
                                      │  Load from HuggingFace Cache        │
                                      │  (local_files_only=True)            │
                                      └─────────────────┬───────────────────┘
                                                        │
                                                        ├─ Success → Use tokenizer
                                                        └─ Fail → Character-based chunking
```

### Key Improvements

1. **Configurability**: Set tokenizer via environment variable
2. **Auto-Detection**: Automatically selects appropriate tokenizer for your LLM
3. **Offline Support**: Uses `local_files_only=True` for cache-only loading
4. **Graceful Degradation**: Falls back to character-based chunking if needed
5. **Clear Logging**: Informative messages about tokenizer selection

---

## Configuration

### Environment Variable

Add to your `.env` file:

```bash
# Streaming Tokenizer Configuration
# The tokenizer used for chunking chat responses during streaming.
# IMPORTANT: Should match your LLM family for accurate token boundaries.
#
# Supported values:
#   - "auto" (recommended): Automatically selects based on MOS_CHAT_MODEL
#   - HuggingFace model path (e.g., "Qwen/Qwen3-0.6B", "bert-base-uncased", "gpt2")
#
# Auto-detection logic:
#   - Qwen models → "Qwen/Qwen3-0.6B"
#   - Claude/GPT/OpenAI → "gpt2" (GPT-2 tokenizer is compatible)
#   - Other models → "bert-base-uncased" (general fallback)
#
# If tokenizer fails to load, falls back to character-based chunking (functional but suboptimal).
# For offline deployments, ensure the tokenizer model is cached in HF_HOME.
MOS_STREAMING_TOKENIZER=auto
```

### Configuration Options

| Value | Description | Use Case |
|-------|-------------|----------|
| `auto` | Auto-detect from `MOS_CHAT_MODEL` | **Recommended** - Works with any LLM |
| `Qwen/Qwen3-0.6B` | Qwen tokenizer | Qwen LLMs (Qwen3-1.7B, Qwen-Plus, etc.) |
| `gpt2` | GPT-2 tokenizer | Claude, GPT, OpenAI-compatible models |
| `bert-base-uncased` | BERT tokenizer | Universal fallback, works offline |
| Any HF model | Custom tokenizer | Advanced use cases |

---

## Auto-Detection Logic

### Detection Rules

The `_detect_tokenizer_for_model()` function analyzes `MOS_CHAT_MODEL` and selects the appropriate tokenizer:

```python
def _detect_tokenizer_for_model(model_name: str) -> str:
    model_lower = model_name.lower()

    # Qwen family models
    if "qwen" in model_lower:
        return "Qwen/Qwen3-0.6B"

    # Claude, GPT, OpenAI models
    if any(x in model_lower for x in ["claude", "gpt", "openai", "chatgpt"]):
        return "gpt2"

    # General fallback
    return "bert-base-uncased"
```

### Examples

| MOS_CHAT_MODEL | Auto-Detected Tokenizer | Reason |
|----------------|-------------------------|--------|
| `anthropic/claude-3.5-sonnet` | `gpt2` | Contains "claude" |
| `openai/gpt-4` | `gpt2` | Contains "gpt" |
| `Qwen/Qwen3-1.7B` | `Qwen/Qwen3-0.6B` | Contains "qwen" |
| `meta-llama/Llama-2-7b` | `bert-base-uncased` | Fallback |
| `deepseek-ai/deepseek-coder` | `bert-base-uncased` | Fallback |

### Why These Choices?

**Qwen Models** → `Qwen/Qwen3-0.6B`
- Qwen uses a **custom tokenizer** based on tiktoken
- Token boundaries differ from GPT/BERT
- Must use Qwen tokenizer for accurate chunking
- 0.6B variant is lightweight and compatible

**Claude/GPT/OpenAI** → `gpt2`
- GPT-2 tokenizer is **widely compatible** with modern LLMs
- Claude uses a similar tokenization scheme
- OpenAI models use GPT-family tokenizers
- Small (< 1MB), fast, universally cached

**Fallback** → `bert-base-uncased`
- **Most compatible** tokenizer across different models
- Works reasonably well for most languages
- Already cached in many MemOS deployments (used for chunking)
- Prioritizes availability over perfect accuracy

---

## Supported Tokenizers

### Recommended Tokenizers

| Tokenizer | Size | Languages | Use Case |
|-----------|------|-----------|----------|
| `gpt2` | ~1 MB | English-optimized | Claude, GPT, general use |
| `bert-base-uncased` | ~440 MB | Multilingual | Universal fallback, offline |
| `Qwen/Qwen3-0.6B` | ~1.2 GB | Chinese/English | Qwen models |

### Download Instructions

For offline deployments, pre-download tokenizers:

```bash
# Download GPT-2 tokenizer
python3 -c "from transformers import AutoTokenizer; AutoTokenizer.from_pretrained('gpt2')"

# Download BERT tokenizer (already cached if using chunking)
python3 -c "from transformers import AutoTokenizer; AutoTokenizer.from_pretrained('bert-base-uncased')"

# Download Qwen tokenizer (for Qwen LLMs)
python3 -c "from transformers import AutoTokenizer; AutoTokenizer.from_pretrained('Qwen/Qwen3-0.6B')"
```

These will be cached in `~/.cache/huggingface/` by default.

---

## Offline Mode Support

### HuggingFace Cache

The patch uses `local_files_only=True` to load tokenizers from cache:

```python
tokenizer = AutoTokenizer.from_pretrained(tokenizer_name, local_files_only=True)
```

### Docker Deployment

For Docker containers with `HF_HUB_OFFLINE=1`:

1. **Download tokenizer to host**:
   ```bash
   python3 -c "from transformers import AutoTokenizer; AutoTokenizer.from_pretrained('gpt2')"
   ```

2. **Mount cache into container**:
   ```yaml
   volumes:
     - ~/.cache/huggingface:/root/.cache/huggingface:ro
   ```

3. **Set environment variables**:
   ```bash
   HF_HUB_OFFLINE=1
   TRANSFORMERS_OFFLINE=1
   MOS_STREAMING_TOKENIZER=gpt2  # or "auto"
   ```

### Verification

Check if tokenizer is in cache:

```bash
ls ~/.cache/huggingface/hub/models--gpt2
ls ~/.cache/huggingface/hub/models--bert-base-uncased
```

---

## Installation

### Prerequisites

- MemOS v1.1.2 or later
- Git working directory clean (or stash changes)
- Backup recommended for production deployments

### Quick Install

```bash
cd /path/to/MemOS
bash patches/configurable-streaming-tokenizer/APPLY.sh
```

### Manual Installation

1. **Apply the patch**:
   ```bash
   cd /path/to/MemOS
   git apply patches/configurable-streaming-tokenizer/0001-add-configurable-streaming-tokenizer.patch
   ```

2. **Add environment variable** to `.env`:
   ```bash
   echo "MOS_STREAMING_TOKENIZER=auto" >> .env
   ```

3. **Download tokenizer** (for offline mode):
   ```bash
   python3 -c "from transformers import AutoTokenizer; AutoTokenizer.from_pretrained('gpt2')"
   ```

4. **Restart MemOS**:
   ```bash
   # Docker
   docker-compose restart memos-api

   # Direct
   systemctl restart memos
   ```

### Verification

Check logs for successful initialization:

```bash
docker logs memos-api 2>&1 | grep -i tokenizer
```

**Expected output**:
```
[INFO] Auto-detected tokenizer 'gpt2' for model 'anthropic/claude-3.5-sonnet'
[INFO] Successfully loaded tokenizer 'gpt2' from cache for streaming
```

---

## Testing

### Quick Test

Run the included test script:

```bash
bash patches/configurable-streaming-tokenizer/TEST.sh
```

### Manual Testing

1. **Test auto-detection**:
   ```bash
   export MOS_STREAMING_TOKENIZER=auto
   export MOS_CHAT_MODEL=anthropic/claude-3.5-sonnet

   docker exec memos-api python3 -c "
   import os
   os.environ['MOS_STREAMING_TOKENIZER'] = 'auto'
   os.environ['MOS_CHAT_MODEL'] = 'anthropic/claude-3.5-sonnet'
   from memos.mem_os.product import MOSProductService
   # Check logs
   "
   ```

2. **Test explicit configuration**:
   ```bash
   export MOS_STREAMING_TOKENIZER=gpt2
   # Restart and check logs
   ```

3. **Test fallback**:
   ```bash
   export MOS_STREAMING_TOKENIZER=nonexistent-tokenizer
   # Should fall back to character-based chunking with warning
   ```

### Test Cases

| Test | MOS_STREAMING_TOKENIZER | MOS_CHAT_MODEL | Expected Tokenizer |
|------|-------------------------|----------------|-------------------|
| Auto-detect Claude | `auto` | `anthropic/claude-3.5-sonnet` | `gpt2` |
| Auto-detect Qwen | `auto` | `Qwen/Qwen3-1.7B` | `Qwen/Qwen3-0.6B` |
| Explicit GPT-2 | `gpt2` | (any) | `gpt2` |
| Explicit BERT | `bert-base-uncased` | (any) | `bert-base-uncased` |
| Missing tokenizer | `auto` | (any) | Fallback to character |

---

## Troubleshooting

### Issue: "Failed to initialize tokenizer"

**Symptoms**:
```
[WARNING] Failed to initialize tokenizer, will use character-based chunking: ...
```

**Causes & Solutions**:

1. **Tokenizer not in cache (offline mode)**:
   ```bash
   # Download to cache
   python3 -c "from transformers import AutoTokenizer; AutoTokenizer.from_pretrained('gpt2')"
   ```

2. **Wrong tokenizer name**:
   ```bash
   # Check configuration
   echo $MOS_STREAMING_TOKENIZER

   # Use auto-detection instead
   export MOS_STREAMING_TOKENIZER=auto
   ```

3. **Cache mount issue (Docker)**:
   ```bash
   # Check if cache is mounted
   docker exec memos-api ls /root/.cache/huggingface/hub/

   # Fix docker-compose.yml volume mount
   ```

### Issue: "Incorrect token boundaries"

**Symptoms**: Chat responses have weird word splits, encoding issues

**Solution**: Ensure tokenizer matches LLM family:

```bash
# For Claude/GPT models
MOS_STREAMING_TOKENIZER=gpt2

# For Qwen models
MOS_STREAMING_TOKENIZER=Qwen/Qwen3-0.6B

# Or use auto-detection
MOS_STREAMING_TOKENIZER=auto
```

### Issue: "Character-based chunking is slow"

**Symptoms**: Slower streaming responses

**Solution**: This is expected behavior when tokenizer fails. Ensure tokenizer loads correctly (see above).

### Debug Mode

Enable detailed logging:

```bash
export MOS_LOG_LEVEL=DEBUG
docker-compose restart memos-api
docker logs -f memos-api | grep -i tokenizer
```

---

## Technical Details

### Code Changes

**File Modified**: `src/memos/mem_os/product.py`

**Functions Added**:
1. `_detect_tokenizer_for_model(model_name: str) -> str`
   - Auto-detects appropriate tokenizer based on model name
   - Returns HuggingFace model path

2. `_initialize_streaming_tokenizer() -> AutoTokenizer | None`
   - Reads `MOS_STREAMING_TOKENIZER` from environment
   - Handles auto-detection logic
   - Loads from cache with `local_files_only=True`
   - Returns tokenizer instance or None on failure

**Functions Modified**:
- `__init__()`: Calls `_initialize_streaming_tokenizer()` instead of hardcoded load

### Token Chunking Flow

```
Chat Response (Full Text)
         │
         ▼
┌──────────────────────┐
│ _chunk_response_with │
│     tiktoken()       │
└─────────┬────────────┘
          │
          ├─ self.tokenizer exists?
          │
          ├─ YES → Token-based chunking
          │         1. Encode to tokens
          │         2. Split by chunk_size (e.g., 5 tokens)
          │         3. Decode each chunk
          │         4. Yield chunk text
          │
          └─ NO → Character-based chunking
                    1. Split by character count
                    2. Yield chunks
```

### Performance Impact

| Metric | Token-based | Character-based |
|--------|-------------|-----------------|
| **Streaming Quality** | ✅ High (proper boundaries) | 🟡 Medium (may split words) |
| **Speed** | ✅ Fast (native encoding) | 🟡 Slower (string operations) |
| **Memory** | ✅ Low (< 10MB tokenizer) | ✅ Low (no overhead) |
| **Accuracy** | ✅ Exact token counts | ❌ Approximate |

### Backward Compatibility

✅ **Fully backward compatible**:
- If `MOS_STREAMING_TOKENIZER` is not set, defaults to `"auto"`
- Auto-detection tries to match original behavior (Qwen for Qwen models)
- Falls back gracefully if tokenizer unavailable
- Existing deployments continue to work

### Security Considerations

- ✅ Only loads from **local cache** (`local_files_only=True`)
- ✅ No network requests during tokenizer loading
- ✅ Environment variable validation (falls back on invalid values)
- ✅ Graceful failure (doesn't crash service)

---

## See Also

- **[Auto-Detection Logic](AUTO_DETECTION_LOGIC.md)** - Deep dive into how tokenizer selection works
- [Chonkie Tokenizer Fix Patch](../chonkie-tokenizer-fix/README.md) - For document chunking tokenizer
- [Neo4j Complex Object Serialization Fix](../neo4j-complex-object-serialization/README.md)
- [MemOS Documentation](https://github.com/MemOS-ai/MemOS)

---

## Changelog

### v1.0.0 (2025-10-21)
- ✅ Initial release
- ✅ Added `MOS_STREAMING_TOKENIZER` environment variable
- ✅ Implemented auto-detection logic
- ✅ Added offline mode support with `local_files_only=True`
- ✅ Comprehensive documentation
- ✅ Test scripts included

---

## License

This patch follows the same license as MemOS.

## Support

For issues or questions:
1. Check [Troubleshooting](#troubleshooting) section
2. Review MemOS logs: `docker logs memos-api | grep -i tokenizer`
3. Open an issue at [MemOS GitHub](https://github.com/MemOS-ai/MemOS/issues)
