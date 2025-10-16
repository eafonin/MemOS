---
source_url: https://memos-docs.openmem.net/open_source/modules/memories/parametric_memory
section: Memories
scraped_date: 2025-10-16
title: Parametric Memory *(Coming Soon)*
has_images: no
has_tables: no
---

# Parametric Memory *(Coming Soon)* [ **Coming Soon** This feature is still under active development. Stay tuned for updates! [`Parametric Memory` is the core **long-term knowledge and capability store** inside MemOS.
Unlike plaintext or activation memories, parametric memory is embedded directly within a modelâs weights â encoding deep representations of language structure, world knowledge, and general reasoning abilities.]
 
[In the MemOS architecture, parametric memory does not just refer to static pre-trained weights. It also includes modular weight components such as **LoRA adapters** and plug-in expert modules. These allow you to incrementally expand or specialize your LLMâs capabilities without retraining the entire model.]
 
[For example, you could distill structured or stable knowledge into parametric form, save it as a **capability block**, and dynamically load or unload it during inference. This makes it easy to create âexpert sub-modelsâ for tasks like legal reasoning, financial analysis, or domain-specific summarization â all managed by MemOS.]
 
## Design Goals
 Controllabilityâ Generate, load, swap, or compose parametric modules
on demand.Plasticityâ Evolve alongside plaintext and activation memories; support knowledge distillation and rollback.Traceability(Coming Soon)â Versioning and governance for parametric blocks. 
## Current Status
 
[`Parametric Memory` is currently under design and prototyping.
APIs for generating, compressing, and hot-swapping parametric modules will be released in future versions â supporting multi-task, multi-role, and multi-agent architectures.]
 
[Stay tuned!]
 
## Related Modules
 
[While parametric memory is under development, try out these today:]
 
- [**GeneralTextMemory**: Flexible vector-based semantic storage.]
- [**TreeTextMemory**: Structured, hierarchical knowledge graphs.]
- [**Activation Memory**: Efficient runtime state caching.]
 
## Developer Note
 
[Parametric Memory will complete MemOSâs vision of a unified **MemoryÂ³** architecture:]
 
- [**Parametric**: Embedded knowledge]
- [**Activation**: Ephemeral runtime states]
- [**Plaintext**: Structured, traceable external memories]
 
[Bringing all three together enables adaptable, evolvable, and explainable intelligent systems.]
