# MemOS Quick Start Guide

**Source:** https://memos-docs.openmem.net/overview/quick_start/overview
**Scraped:** 2025-10-16
**Type:** Official Documentation - Quick Start

---

## Overview

MemOS (Memory Operating System) is designed to give AI applications persistent memory capabilities. The platform offers two pathways:
1. **Cloud service** - requires only an API Key
2. **Open-source framework** - for local deployment

---

## Cloud Service Setup

### Step 1: API Key Acquisition

Register on the MemOS Cloud Platform to obtain your default API Key for authentication.

### Step 2: Message Storage (addMessage)

Submit conversation logs to the system, which automatically processes and stores them as retrievable memory:

```python
import os
import requests
import json

os.environ["MEMOS_API_KEY"] = "YOUR_API_KEY"
os.environ["MEMOS_BASE_URL"] = "https://memos.memtensor.cn/api/openmem/v1"

data = {
  "messages": [
    {"role": "user", "content": "I want to travel during summer vacation..."},
    {"role": "assistant", "content": "Sure! Are you traveling alone..."}
  ],
  "user_id": "memos_user_123",
  "conversation_id": "0610"
}

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Token {os.environ['MEMOS_API_KEY']}"
}

url = f"{os.environ['MEMOS_BASE_URL']}/add/message"
res = requests.post(url=url, headers=headers, data=json.dumps(data))
```

### Step 3: Memory Retrieval (searchMemory)

Query the system to recall relevant memories for contextual responses:

```python
data = {
  "user_id": "memos_user_123",
  "conversation_id": "0928",
  "query": "Where to go for National Day travel?",
  "memory_limit_number": 6
}

url = f"{os.environ['MEMOS_BASE_URL']}/search/memory"
res = requests.post(url=url, headers=headers, data=json.dumps(data))
```

---

## Open-Source Framework

For local deployment, developers directly manage memory extraction and operations through the MemOS Python framework.

---

## Key Patterns for Data Loading

### Pattern 1: Message-Based Import
- Endpoint: `/add/message`
- Format: Array of message objects with role/content
- Required: `user_id`, `conversation_id`
- Use case: **Chat session imports**

### Pattern 2: Memory Search
- Endpoint: `/search/memory`
- Required: `user_id`, `query`
- Optional: `conversation_id`, `memory_limit_number`
- Use case: Contextual retrieval

---

## Authentication

**Method:** Token-based authentication
**Header:** `Authorization: Token YOUR_API_KEY`
**Content-Type:** `application/json`

---

## Critical Insights for Data Loader

1. **User Association Required**: All operations require `user_id`
2. **Conversation Grouping**: Use `conversation_id` to group related messages
3. **Message Structure**: Array of `{"role": "...", "content": "..."}`
4. **Base URL**: Playground likely uses similar endpoint structure
5. **Token Auth**: Bearer token pattern for playground

---

## Next Steps

- Verify playground endpoint structure matches cloud service
- Identify additional endpoints for document/file import
- Test authentication with playground credentials
