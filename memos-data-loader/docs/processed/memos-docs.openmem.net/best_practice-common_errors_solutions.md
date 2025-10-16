---
source_url: https://memos-docs.openmem.net/open_source/best_practice/common_errors_solutions
section: Best Practice
scraped_date: 2025-10-16
title: Common Errors and Solutions
has_images: no
has_tables: no
---

# Common Errors and Solutions
 [
## Configuration Errors

### Missing Required Fields

```
# â Always include required fields
llm_config = {
 "backend": "openai",
 "config": {
 "api_key": "your-api-key",
 "model_name_or_path": "gpt-4"
 }
}

```

### Backend Mismatch

```
# â KVCache requires HuggingFace backend
kv_config = {
 "backend": "kv_cache",
 "config": {
 "extractor_llm": {
 "backend": "huggingface",
 "config": {
 "model_name_or_path": "Qwen/Qwen3-1.7B"
 }
 }
 }
}

```

## Service Connection Issues

```
# Start required services as needed
docker run -p 6333:6333 qdrant/qdrant
ollama serve

```

### Memory Loading Failures

```
try:
 mem_cube.load("memory_dir")
except Exception:
 mem_cube = GeneralMemCube(config)
 mem_cube.dump("memory_dir")

```

### GPU Memory

```
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
# Use smaller models if GPU memory is limited: Qwen/Qwen3-0.6B

```

## User Management

```
# Register user first
mos.register_mem_cube(cube_path="path", user_id="user_id", cube_id="cube_id")

# Check if user exists
try:
 user_id = mos.create_user(user_name="john", role=UserRole.USER)
except ValueError:
 user = mos.user_manager.get_user_by_name("john")

```
