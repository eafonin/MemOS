---
source_url: https://memos-docs.openmem.net/open_source/best_practice/performance_tuning
section: Best Practice
scraped_date: 2025-10-16
title: Performance Tuning
has_images: no
has_tables: no
---

# Performance Tuning
 [
## Embedding Optimization

```
fast_embedder = {
 "backend": "ollama",
 "config": {
 "model_name_or_path": "nomic-embed-text:latest"
 }
}

slow_embedder = {
 "backend": "sentence_transformer",
 "config": {
 "model_name_or_path": "nomic-ai/nomic-embed-text-v1.5"
 }
}

```

## Inference Speed

```
generation_config = {
 "max_new_tokens": 256, # Limit response length
 "temperature": 0.7,
 "do_sample": True
}

```

## System Resource Optimization

### Memory Capacity Limits

```
scheduler_config = {
 "memory_capacities": {
 "working_memory_capacity": 20, # Active context
 "user_memory_capacity": 500, # User storage
 "long_term_memory_capacity": 2000, # Domain knowledge
 "transformed_act_memory_capacity": 50 # KV cache items
 }
}

```

### Batch Processing

```
def batch_memory_operations(operations, batch_size=10):
 for i in range(0, len(operations), batch_size):
 batch = operations[i:i + batch_size]
 yield batch # Process in batches

```
