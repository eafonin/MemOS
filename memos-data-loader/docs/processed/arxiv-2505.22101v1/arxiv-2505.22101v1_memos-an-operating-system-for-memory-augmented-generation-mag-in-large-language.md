---
source_url: https://arxiv.org/html/2505.22101v1
paper_id: 2505.22101v1
title: MemOS: An Operating System for Memory-Augmented Generation (MAG) in Large Language Models (Short Version)
scraped_date: 2025-10-16
has_images: yes
has_tables: yes
---

# MemOS: An Operating System for Memory-Augmented Generation (MAG) in Large Language Models (Short Version)

###### Abstract

Large Language Models (LLMs) have emerged as foundational infrastructure in the pursuit of Artificial General Intelligence (AGI). Despite their remarkable capabilities in language perception and generation, current LLMs fundamentally lack a unified and structured architecture for handling memory. They primarily rely on parametric memory (knowledge encoded in model weights) and ephemeral activation memory (context-limited runtime states). While emerging methods like Retrieval-Augmented Generation (RAG) incorporate plaintext memory, they lack lifecycle management and multi-modal integration, limiting their capacity for long-term knowledge evolution. To address this, we introduce —a memory operating system designed for LLMs that, for the first time, elevates memory to a first-class operational resource. It builds unified mechanisms for representation, organization, and governance across three core memory types: parametric, activation, and plaintext. At its core is theMemCube, a standardized memory abstraction that enables tracking, fusion, and migration of heterogeneous memory, while offering structured, traceable access across tasks and contexts.MemOSestablishes a memory-centric execution framework with strong controllability, adaptability, and evolvability. It fills a critical gap in current LLM infrastructure and lays the groundwork for continual adaptation, personalized intelligence, and cross-platform coordination in next-generation intelligent systems.

[Author Legend]*Co-equal primary author, †Correspondence