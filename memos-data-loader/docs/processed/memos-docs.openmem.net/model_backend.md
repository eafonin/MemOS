---
source_url: https://memos-docs.openmem.net/open_source/modules/model_backend
section: Mos
scraped_date: 2025-10-16
title: LLMs and Embeddings
has_images: no
has_tables: yes
---

# LLMs and Embeddings
 [ A practical guide to configuring and using Large Language Models (LLM) and Embedders in **MemOS** . 
## Overview
 
[MemOS decouples **model logic** from **runtime config** via two Pydantic factories:]
 
<table><thead><tr><th>Factory</th><th>Produces</th><th>Typical backends</th></tr></thead><tbody><tr><td>LLMFactory</td><td>Chatâcompletion model</td><td>ollama, openai, qwen, deepseek, huggingface</td></tr><tr><td>EmbedderFactory</td><td>Textâtoâvector encoder</td><td>ollama, sentence_transformer, universal_api</td></tr></tbody></table>
 
[Both factories accept a `*_ConfigFactory(model_validate(...))` blob, so you can switch provider with a single `backend=` swap.]
 
## LLM Module
 
### SupportedÂ LLMÂ Backends
 
<table><thead><tr><th>Backend</th><th>Notes</th><th>Example Model Id</th></tr></thead><tbody><tr><td>ollama</td><td>Local llamaâcpp runner</td><td>qwen3:0.6b etc.</td></tr><tr><td>openai</td><td>Official or proxy</td><td>gpt-4o-mini, gpt-3.5-turbo etc.</td></tr><tr><td>qwen</td><td>DashScopeâcompatible</td><td>qwen-plus, qwen-max-2025-01-25 etc.</td></tr><tr><td>deepseek</td><td>DeepSeek REST API</td><td>deepseek-chat, deepseek-reasoner etc.</td></tr><tr><td>huggingface</td><td>Transformers pipeline</td><td>Qwen/Qwen3-1.7B etc.</td></tr></tbody></table>
 
### LLMÂ Config Schema
 
[Common fields:]
 
<table><thead><tr><th>Field</th><th>Type</th><th>Default</th><th>Description</th></tr></thead><tbody><tr><td>model_name_or_path</td><td>str</td><td>â</td><td>Model id or local tag</td></tr><tr><td>temperature</td><td>float</td><td>0.8</td><td></td></tr><tr><td>max_tokens</td><td>int</td><td>1024</td><td></td></tr><tr><td>top_p / top_k</td><td>float / int</td><td>0.9 /Â 50</td><td></td></tr><tr><td>APIâspecific</td><td>e.g.Â api_key, api_base</td><td>â</td><td>OpenAIâcompatible creds</td></tr><tr><td>remove_think_prefix</td><td>bool</td><td>True</td><td>Strip /think role content</td></tr></tbody></table>
 
### FactoryÂ Usage
 
```
from memos.configs.llm import LLMConfigFactory
from memos.llms.factory import LLMFactory

cfg = LLMConfigFactory.model_validate({
 "backend": "ollama",
 "config": {"model_name_or_path": "qwen3:0.6b"}
})
llm = LLMFactory.from_config(cfg)

```
 
### LLMÂ CoreÂ APIs
 
<table><thead><tr><th>Method</th><th>Purpose</th></tr></thead><tbody><tr><td>generate(messages: list)</td><td>Return full string response</td></tr><tr><td>generate_stream(messages)</td><td>Yield streaming chunks</td></tr></tbody></table>
 
### StreamingÂ &Â CoT
 
```
messages = [{"role": "user", "content": "Letâs think step by step: â¦"}]
for chunk in llm.generate_stream(messages):
 print(chunk, end="")

``` **Full code** 
 Find all scenarios in `examples/basic_modules/llm.py` . ### PerformanceÂ Tips
 
- [Use `qwen3:0.6b` for <thead><tr><th>Backend</th><th>Example Model</th><th>Vector Dim</th></tr></thead><tbody><tr><td>ollama</td><td>nomic-embed-text:latest</td><td>768</td></tr><tr><td>sentence_transformer</td><td>nomic-ai/nomic-embed-text-v1.5</td><td>768</td></tr><tr><td>universal_api</td><td>text-embedding-3-large</td><td>3072</td></tr></tbody></table>
 
### EmbedderÂ Config Schema
 
[Shared keys: `model_name_or_path`, optional API creds (`api_key`, `base_url`), etc.]
 
### FactoryÂ Usage
 
```
cfg = EmbedderConfigFactory.model_validate({
 "backend": "ollama",
 "config": {"model_name_or_path": "nomic-embed-text:latest"}
})
embedder = EmbedderFactory.from_config(cfg)

```
