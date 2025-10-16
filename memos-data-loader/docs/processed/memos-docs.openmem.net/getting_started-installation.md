---
source_url: https://memos-docs.openmem.net/open_source/getting_started/installation
section: Getting Started
scraped_date: 2025-10-16
title: Installation Guide
has_images: no
has_tables: yes
---

# Installation Guide
 [ Complete installation guide for MemOS. 
## Basic Installation
 
[The simplest way to install MemOS is using pip:]
 
```
pip install MemoryOS -U

```
 
[For detailed development environment setup, workflow guidelines, and contribution best practices, please see our [Contribution Guide](/open_source/contribution/overview).]
 
## Optional Dependencies
 
[MemOS provides several optional dependency groups for different features. You can install them based on your needs.]
 
<table><thead><tr><th>Feature</th><th>Package Name</th></tr></thead><tbody><tr><td>Tree Memory</td><td>MemoryOS[tree-mem]</td></tr><tr><td>Memory Reader</td><td>MemoryOS[mem-reader]</td></tr><tr><td>Memory Scheduler</td><td>MemoryOS[mem-scheduler]</td></tr></tbody></table>
 
[Example installation commands:]
 
```
pip install MemoryOS[tree-mem]
pip install MemoryOS[tree-mem,mem-reader]
pip install MemoryOS[mem-scheduler]
pip install MemoryOS[tree-mem,mem-reader,mem-scheduler]

```
 
## External Dependencies
 
### Ollama Support
 
[To use MemOS with [[Ollama](https://ollama.com/)], first install the Ollama CLI:]
 
```
curl -fsSL https://ollama.com/install.sh | sh

```
 
### Transformers Support
 
[To use functionalities based on the `transformers` library, ensure you have [[PyTorch](https://pytorch.org/get-started/locally/)] installed (CUDA version recommended for GPU acceleration).]
 
### Neo4j Support **Neo4j Desktop Requirement** 
 If you plan to use Neo4j for graph memory, install Neo4j Desktop (community edition support coming soon!) ### Download Examples
 
[To download example code, data and configurations, run the following command:]
 
```
memos download_examples

```
 
## Verification
 
[To verify your installation, run:]
 
```
pip show MemoryOS
python -c "import memos; print(memos.__version__)"

```
