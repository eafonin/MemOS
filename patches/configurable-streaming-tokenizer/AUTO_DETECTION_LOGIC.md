# Streaming Tokenizer Auto-Detection Logic

**Version**: 1.0.0
**Created**: 2025-10-21
**Part of**: Configurable Streaming Tokenizer Patch

---

## Table of Contents

1. [Overview](#overview)
2. [Auto-Detection Architecture](#auto-detection-architecture)
3. [Decision Flow](#decision-flow)
4. [Code Implementation](#code-implementation)
5. [Detection Rules](#detection-rules)
6. [Examples](#examples)
7. [Cache Loading Process](#cache-loading-process)
8. [Fallback Mechanisms](#fallback-mechanisms)
9. [Configuration Override](#configuration-override)

---

## Overview

The streaming tokenizer auto-detection system **intelligently selects** the appropriate tokenizer based on your LLM backend, ensuring correct token boundaries during chat response streaming.

### Why Auto-Detection?

Different LLM families use **different tokenization schemes**:

| LLM Family | Tokenizer Type | Vocabulary Size | Special Tokens |
|------------|----------------|-----------------|----------------|
| **GPT (OpenAI)** | BPE (Byte-Pair Encoding) | ~50,257 | `<|endoftext|>` |
| **Claude (Anthropic)** | Similar to GPT-2 | ~50,000 | Compatible with GPT-2 |
| **Qwen (Alibaba)** | tiktoken-based | ~151,646 | Custom Chinese/English |
| **BERT** | WordPiece | ~30,522 | `[CLS]`, `[SEP]`, `[MASK]` |

**Using the wrong tokenizer causes:**
- ❌ Incorrect token boundaries (words split mid-character)
- ❌ Token count mismatches with LLM expectations
- ❌ Encoding errors for non-ASCII text
- ❌ Poor streaming experience

---

## Auto-Detection Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    STARTUP SEQUENCE                             │
└─────────────────────────────────────────────────────────────────┘

Container Starts
    ↓
┌─────────────────────────────────────────────────────────────┐
│  1. Read Environment Variables                              │
├─────────────────────────────────────────────────────────────┤
│  • MOS_STREAMING_TOKENIZER (default: "auto")               │
│  • MOS_CHAT_MODEL (your LLM backend)                       │
│  • HF_ENDPOINT (HuggingFace mirror)                        │
└─────────────────────────────────────────────────────────────┘
    ↓
    ┌─────────────────────────────────────────────┐
    │ Is MOS_STREAMING_TOKENIZER = "auto"?       │
    └─────────────────┬───────────────────────────┘
                      │
         YES ◄────────┴────────► NO (explicit tokenizer set)
          │                          │
          ▼                          ▼
    ┌─────────────────────────┐  ┌──────────────────────────┐
    │  AUTO-DETECTION         │  │  USE CONFIGURED VALUE   │
    │                         │  │                          │
    │  Call:                  │  │  tokenizer_name =        │
    │  _detect_tokenizer_     │  │    MOS_STREAMING_        │
    │    for_model()          │  │    TOKENIZER             │
    │                         │  │                          │
    │  Input:                 │  └──────────┬───────────────┘
    │    MOS_CHAT_MODEL       │             │
    │                         │             │
    │  Output:                │             │
    │    tokenizer_name       │             │
    └────────────┬────────────┘             │
                 │                          │
                 └───────────┬──────────────┘
                             ↓
                ┌─────────────────────────────────────┐
                │  2. Temporarily Unset HF_ENDPOINT  │
                ├─────────────────────────────────────┤
                │  Why: Prevent connection attempts  │
                │       to hf-mirror.com in offline  │
                │       mode                         │
                └───────────────┬─────────────────────┘
                                ↓
                ┌─────────────────────────────────────┐
                │  3. Load from Cache                │
                ├─────────────────────────────────────┤
                │  AutoTokenizer.from_pretrained(    │
                │      tokenizer_name,               │
                │      local_files_only=True         │
                │  )                                 │
                └───────────────┬─────────────────────┘
                                │
                       ┌────────┴────────┐
                       │                 │
                  SUCCESS            FAILURE
                       │                 │
                       ▼                 ▼
            ┌──────────────────┐  ┌──────────────────┐
            │  Return          │  │  Return None     │
            │  Tokenizer       │  │  (fallback to    │
            │  Instance        │  │  character-based)│
            └──────────────────┘  └──────────────────┘
                       │
                       ▼
                ┌─────────────────────────────────────┐
                │  4. Restore HF_ENDPOINT            │
                ├─────────────────────────────────────┤
                │  Restore original value to avoid   │
                │  side effects                      │
                └─────────────────────────────────────┘
                       │
                       ▼
                ┌─────────────────────────────────────┐
                │  5. Ready for Streaming            │
                ├─────────────────────────────────────┤
                │  self.tokenizer = <instance>       │
                │  Used by _chunk_response_with_     │
                │         tiktoken()                 │
                └─────────────────────────────────────┘
```

---

## Decision Flow

### `_detect_tokenizer_for_model()` Function

```python
def _detect_tokenizer_for_model(self, model_name: str) -> str:
    """
    Detect appropriate tokenizer based on chat model name.

    Args:
        model_name: The LLM model name (e.g., from MOS_CHAT_MODEL)

    Returns:
        HuggingFace tokenizer model path
    """
    model_lower = model_name.lower()

    # Rule 1: Qwen family models
    if "qwen" in model_lower:
        return "Qwen/Qwen3-0.6B"

    # Rule 2: Claude, GPT, OpenAI models
    if any(x in model_lower for x in ["claude", "gpt", "openai", "chatgpt"]):
        return "gpt2"

    # Rule 3: General fallback
    return "bert-base-uncased"
```

### Decision Tree

```
Input: MOS_CHAT_MODEL value
    │
    ▼
┌─────────────────────────────────────────────┐
│ Does model name contain "qwen"?            │
│ (case-insensitive)                         │
└───────────┬─────────────────────────────────┘
            │
    YES ◄───┴───► NO
     │            │
     ▼            ▼
┌──────────┐  ┌────────────────────────────────────┐
│ Return:  │  │ Does model name contain:          │
│ "Qwen/   │  │  • "claude"                       │
│  Qwen3-  │  │  • "gpt"                          │
│  0.6B"   │  │  • "openai"                       │
└──────────┘  │  • "chatgpt"                      │
              │ (case-insensitive)                │
              └────────────┬───────────────────────┘
                           │
                   YES ◄───┴───► NO
                    │            │
                    ▼            ▼
              ┌──────────┐  ┌──────────────┐
              │ Return:  │  │ Return:      │
              │ "gpt2"   │  │ "bert-base-  │
              │          │  │  uncased"    │
              └──────────┘  └──────────────┘
```

---

## Code Implementation

### File: `src/memos/mem_os/product.py`

#### Location: Lines 164-184

```python
def _detect_tokenizer_for_model(self, model_name: str) -> str:
    """Detect appropriate tokenizer based on chat model name.

    Args:
        model_name: The LLM model name (e.g., from MOS_CHAT_MODEL)

    Returns:
        HuggingFace tokenizer model path
    """
    model_lower = model_name.lower()

    # Qwen family models
    if "qwen" in model_lower:
        return "Qwen/Qwen3-0.6B"

    # Claude, GPT, OpenAI models - use GPT-2 tokenizer (widely compatible)
    if any(x in model_lower for x in ["claude", "gpt", "openai", "chatgpt"]):
        return "gpt2"

    # General fallback
    return "bert-base-uncased"
```

#### Location: Lines 186-224

```python
def _initialize_streaming_tokenizer(self):
    """Initialize tokenizer for streaming responses with configurable model.

    Returns:
        AutoTokenizer instance or None if initialization fails
    """
    try:
        # Get tokenizer configuration from environment
        tokenizer_config = os.getenv("MOS_STREAMING_TOKENIZER", "auto")

        # Auto-detect based on chat model if set to "auto"
        if tokenizer_config == "auto":
            chat_model = os.getenv("MOS_CHAT_MODEL", "")
            tokenizer_name = self._detect_tokenizer_for_model(chat_model)
            logger.info(f"Auto-detected tokenizer '{tokenizer_name}' for model '{chat_model}'")
        else:
            tokenizer_name = tokenizer_config
            logger.info(f"Using configured tokenizer: {tokenizer_name}")

        # Temporarily unset HF_ENDPOINT to prevent connection attempts
        original_hf_endpoint = os.environ.get('HF_ENDPOINT')
        if original_hf_endpoint:
            os.environ.pop('HF_ENDPOINT', None)

        try:
            # Try to load from cache (for offline mode compatibility)
            tokenizer = AutoTokenizer.from_pretrained(tokenizer_name, local_files_only=True)
            logger.info(f"Successfully loaded tokenizer '{tokenizer_name}' from cache for streaming")
            return tokenizer
        finally:
            # Restore HF_ENDPOINT
            if original_hf_endpoint:
                os.environ['HF_ENDPOINT'] = original_hf_endpoint

    except Exception as e:
        logger.warning(
            f"Failed to initialize tokenizer, will use character-based chunking: {e}"
        )
        return None
```

---

## Detection Rules

### Rule 1: Qwen Models → `Qwen/Qwen3-0.6B`

**Trigger:** Model name contains `"qwen"` (case-insensitive)

**Why?**
- Qwen uses a **custom tiktoken-based tokenizer**
- Different vocabulary (151,646 tokens vs GPT-2's 50,257)
- Optimized for Chinese/English bilingual text
- Token IDs don't match GPT-2

**Matches:**
- `Qwen/Qwen3-1.7B`
- `Qwen/Qwen3-0.6B`
- `qwen-plus`
- `Qwen2.5-7B-Instruct`
- `deepseek-qwen-7b` ✅ (contains "qwen")

**Example:**
```python
model = "Qwen/Qwen3-1.7B"
# Auto-detects: Qwen/Qwen3-0.6B
```

---

### Rule 2: Claude/GPT/OpenAI → `gpt2`

**Trigger:** Model name contains any of:
- `"claude"` (Anthropic Claude)
- `"gpt"` (OpenAI GPT models)
- `"openai"` (OpenAI models)
- `"chatgpt"` (ChatGPT variants)

**Why?**
- GPT-2 tokenizer is **widely compatible** with modern LLMs
- Claude uses a **similar tokenization scheme** (BPE-based)
- OpenAI's GPT-3/GPT-4 are **backward compatible** with GPT-2 tokenizer
- Small (< 1MB), fast, universally cached

**Token Compatibility:**
```
GPT-2 tokenizer:
  • Used by: GPT-2, GPT-3, GPT-3.5, GPT-4 (with extensions)
  • Compatible with: Claude (close enough for streaming)
  • Vocabulary: 50,257 tokens
  • Encoding: Byte-Pair Encoding (BPE)
```

**Matches:**
- `anthropic/claude-3.5-sonnet` ✅ (your config)
- `anthropic/claude-3-opus`
- `openai/gpt-4`
- `openai/gpt-3.5-turbo`
- `chatgpt-4o-latest`
- `gpt2-medium`

**Example:**
```python
model = "anthropic/claude-3.5-sonnet"
# Auto-detects: gpt2
```

---

### Rule 3: Fallback → `bert-base-uncased`

**Trigger:** Model name doesn't match Rule 1 or Rule 2

**Why?**
- **Most universally compatible** tokenizer
- Works reasonably well for **multilingual** text
- Already cached in many MemOS deployments (used for document chunking)
- Prioritizes **availability** over perfect accuracy

**Matches:**
- `meta-llama/Llama-2-7b`
- `meta-llama/Llama-3-8b`
- `mistralai/Mistral-7B`
- `deepseek-ai/deepseek-coder`
- Any unknown model

**Example:**
```python
model = "meta-llama/Llama-2-7b"
# Auto-detects: bert-base-uncased
```

---

## Examples

### Example 1: Your Configuration (Claude)

```bash
# .env file
MOS_CHAT_MODEL=anthropic/claude-3.5-sonnet
MOS_STREAMING_TOKENIZER=auto
```

**Execution:**
```python
1. tokenizer_config = "auto"  # from MOS_STREAMING_TOKENIZER
2. chat_model = "anthropic/claude-3.5-sonnet"  # from MOS_CHAT_MODEL
3. _detect_tokenizer_for_model("anthropic/claude-3.5-sonnet")
   ├─ Check: "qwen" in "anthropic/claude-3.5-sonnet".lower() → False
   ├─ Check: "claude" in "anthropic/claude-3.5-sonnet".lower() → True ✓
   └─ Return: "gpt2"
4. Load from cache: /root/.cache/huggingface/hub/models--gpt2
5. Result: ✅ Tokenizer loaded successfully
```

**Logs:**
```
[INFO] Auto-detected tokenizer 'gpt2' for model 'anthropic/claude-3.5-sonnet'
[INFO] Successfully loaded tokenizer 'gpt2' from cache for streaming
```

---

### Example 2: Qwen Model

```bash
MOS_CHAT_MODEL=Qwen/Qwen3-1.7B
MOS_STREAMING_TOKENIZER=auto
```

**Execution:**
```python
1. tokenizer_config = "auto"
2. chat_model = "Qwen/Qwen3-1.7B"
3. _detect_tokenizer_for_model("Qwen/Qwen3-1.7B")
   ├─ Check: "qwen" in "qwen/qwen3-1.7b".lower() → True ✓
   └─ Return: "Qwen/Qwen3-0.6B"
4. Load from cache: /root/.cache/huggingface/hub/models--Qwen--Qwen3-0.6B
5. Result: ✅ Tokenizer loaded (if cached) or ❌ Falls back
```

**Why Qwen3-0.6B instead of Qwen3-1.7B?**
- Smaller model (1.2GB vs 3.4GB)
- **Tokenizer is identical** across Qwen3 family
- Faster to download and cache
- Sufficient for tokenization purposes

---

### Example 3: GPT-4

```bash
MOS_CHAT_MODEL=openai/gpt-4
MOS_STREAMING_TOKENIZER=auto
```

**Execution:**
```python
1. tokenizer_config = "auto"
2. chat_model = "openai/gpt-4"
3. _detect_tokenizer_for_model("openai/gpt-4")
   ├─ Check: "qwen" in "openai/gpt-4".lower() → False
   ├─ Check: "gpt" in "openai/gpt-4".lower() → True ✓
   └─ Return: "gpt2"
4. Load from cache: /root/.cache/huggingface/hub/models--gpt2
5. Result: ✅ Tokenizer loaded
```

**Note:** GPT-4 uses an extended tokenizer (cl100k_base), but GPT-2 is **close enough** for streaming purposes.

---

### Example 4: Llama (Fallback)

```bash
MOS_CHAT_MODEL=meta-llama/Llama-2-7b
MOS_STREAMING_TOKENIZER=auto
```

**Execution:**
```python
1. tokenizer_config = "auto"
2. chat_model = "meta-llama/Llama-2-7b"
3. _detect_tokenizer_for_model("meta-llama/Llama-2-7b")
   ├─ Check: "qwen" in "meta-llama/llama-2-7b".lower() → False
   ├─ Check: "claude"/"gpt"/"openai" in "meta-llama/llama-2-7b" → False
   └─ Return: "bert-base-uncased" (fallback)
4. Load from cache: /root/.cache/huggingface/hub/models--bert-base-uncased
5. Result: ✅ Tokenizer loaded (universal compatibility)
```

---

## Cache Loading Process

### Step-by-Step

```
┌─────────────────────────────────────────────────────────────┐
│  CACHE LOADING SEQUENCE                                     │
└─────────────────────────────────────────────────────────────┘

1. Determine tokenizer_name
   ├─ From auto-detection OR
   └─ From MOS_STREAMING_TOKENIZER

2. Save original HF_ENDPOINT
   ├─ original_hf_endpoint = os.environ.get('HF_ENDPOINT')
   └─ Why: May be set to hf-mirror.com

3. Temporarily unset HF_ENDPOINT
   ├─ os.environ.pop('HF_ENDPOINT', None)
   └─ Why: Prevents connection attempts in offline mode

4. Load tokenizer from cache
   ├─ AutoTokenizer.from_pretrained(
   │      tokenizer_name,
   │      local_files_only=True  ← Forces cache-only
   │  )
   │
   ├─ Searches in: /root/.cache/huggingface/hub/
   │               models--{tokenizer_name}/
   │
   ├─ Required files:
   │   • config.json
   │   • tokenizer.json
   │   • vocab.txt (for BERT) OR
   │   • vocab.json + merges.txt (for GPT-2/Qwen)
   │
   └─ If found → Load ✓
      If not found → Raise error → Caught by try/except

5. Restore HF_ENDPOINT (in finally block)
   ├─ if original_hf_endpoint:
   │      os.environ['HF_ENDPOINT'] = original_hf_endpoint
   └─ Ensures no side effects

6. Return tokenizer instance or None
```

### Cache Structure

```
/root/.cache/huggingface/hub/
├── .locks/
│   └── models--gpt2/
│       └── *.lock
├── models--gpt2/
│   ├── refs/
│   │   └── main
│   ├── snapshots/
│   │   └── e7da7f2/
│   │       ├── config.json
│   │       ├── tokenizer.json
│   │       ├── vocab.json
│   │       └── merges.txt
│   └── blobs/
│       └── *.blob
├── models--bert-base-uncased/
│   └── ... (similar structure)
└── models--Qwen--Qwen3-0.6B/
    └── ... (similar structure)
```

---

## Fallback Mechanisms

### 3-Level Fallback System

```
Level 1: Auto-Detection
   ↓ (on failure)
Level 2: Explicit Configuration
   ↓ (on failure)
Level 3: Character-Based Chunking
```

### Level 1: Auto-Detection

```python
if tokenizer_config == "auto":
    tokenizer_name = self._detect_tokenizer_for_model(chat_model)
    # Attempts to load from cache
```

**Failure Modes:**
- Tokenizer not in cache
- Corrupted cache files
- Permission issues

**Fallback:** Catch exception → Log warning → Return None

---

### Level 2: Explicit Configuration

User can override auto-detection:

```bash
# Force specific tokenizer
MOS_STREAMING_TOKENIZER=gpt2
```

**Bypasses auto-detection**, directly uses configured value.

---

### Level 3: Character-Based Chunking

If tokenizer loading fails:

```python
except Exception as e:
    logger.warning(f"Failed to initialize tokenizer: {e}")
    return None  # self.tokenizer = None
```

**Streaming function checks:**

```python
def _chunk_response_with_tiktoken(self, response: str, chunk_size: int):
    if self.tokenizer:
        # Token-based chunking (OPTIMAL)
        tokens = self.tokenizer.encode(response)
        for i in range(0, len(tokens), chunk_size):
            chunk = self.tokenizer.decode(tokens[i:i+chunk_size])
            yield chunk
    else:
        # Character-based chunking (FALLBACK)
        for i in range(0, len(response), chunk_size * 4):  # Approx. 4 chars/token
            yield response[i:i+chunk_size*4]
```

**Quality Comparison:**

| Aspect | Token-Based | Character-Based |
|--------|-------------|-----------------|
| **Word Boundaries** | ✅ Respects tokens | ❌ May split words |
| **Token Count Accuracy** | ✅ Exact | ❌ Approximate |
| **Speed** | ✅ Fast | 🟡 Slightly slower |
| **Quality** | ✅ High | 🟡 Medium |

---

## Configuration Override

### When to Use Explicit Configuration

```bash
# Scenario 1: Using a custom fine-tuned model
MOS_CHAT_MODEL=my-org/custom-llama-7b
MOS_STREAMING_TOKENIZER=meta-llama/Llama-2-7b-hf  # Explicit

# Scenario 2: Testing different tokenizers
MOS_STREAMING_TOKENIZER=gpt2  # Override auto-detection

# Scenario 3: Offline environment with specific cache
MOS_STREAMING_TOKENIZER=bert-base-uncased  # Known to be cached
```

### Override Priority

```
1. Explicit MOS_STREAMING_TOKENIZER value (highest)
   ↓ (if set to "auto")
2. Auto-detection based on MOS_CHAT_MODEL
   ↓ (if detection succeeds)
3. Use detected tokenizer
   ↓ (if loading fails)
4. Fall back to character-based chunking (lowest)
```

---

## Troubleshooting

### Issue: Auto-detection picks wrong tokenizer

**Symptom:** Streaming has encoding issues or token boundaries are incorrect.

**Solution:** Override with explicit tokenizer:

```bash
# Check what was auto-detected
docker logs test1-memos-api | grep "Auto-detected"
# Output: Auto-detected tokenizer 'gpt2' for model 'your-model'

# Override if needed
MOS_STREAMING_TOKENIZER=bert-base-uncased
```

---

### Issue: Tokenizer not in cache

**Symptom:** `Failed to initialize tokenizer, will use character-based chunking`

**Solution:** Download tokenizer to cache:

```bash
# Inside container (with offline mode disabled)
docker exec test1-memos-api bash -c "
  unset HF_HUB_OFFLINE
  python3 -c 'from transformers import AutoTokenizer; AutoTokenizer.from_pretrained(\"gpt2\")'
"

# Then copy to host cache for persistence
sudo docker cp test1-memos-api:/root/.cache/huggingface/hub/models--gpt2 \
               docker-test1/data/hf-cache/hub/
```

---

### Issue: Multiple tokenizers detected

**Symptom:** Model name matches multiple rules (edge case).

**Example:**
```bash
MOS_CHAT_MODEL=deepseek-qwen-gpt-7b
# Contains: "qwen" AND "gpt"
```

**Result:** First matching rule wins (Rule 1: Qwen)

**Solution:** Use explicit configuration:
```bash
MOS_STREAMING_TOKENIZER=gpt2  # Override
```

---

## Summary

### Key Points

✅ **Automatic Selection**: Detects based on `MOS_CHAT_MODEL`
✅ **Intelligent Rules**: Qwen → Qwen, Claude/GPT → GPT-2, Others → BERT
✅ **Cache-Only Loading**: Works in offline mode (`local_files_only=True`)
✅ **HF_ENDPOINT Handling**: Temporarily unsets to prevent connection attempts
✅ **Graceful Fallback**: Falls back to character-based if loading fails
✅ **Override Available**: Can set explicit tokenizer via `MOS_STREAMING_TOKENIZER`

### Your Current Setup

```yaml
Model: anthropic/claude-3.5-sonnet
Auto-Detected: gpt2
Loaded From: /root/.cache/huggingface/hub/models--gpt2
Status: ✅ Successfully loaded
Streaming: ✅ Token-based (optimal)
```

---

## See Also

- [Main README](README.md) - Complete patch documentation
- [Patch Installation](APPLY.sh) - Automated installation
- [Test Suite](TEST.sh) - Verification tests
- [Troubleshooting Guide](README.md#troubleshooting) - Common issues

---

**Document Version**: 1.0.0
**Last Updated**: 2025-10-21
**Maintainer**: MemOS Community
