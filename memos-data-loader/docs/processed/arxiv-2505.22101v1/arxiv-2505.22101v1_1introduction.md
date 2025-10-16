---
source_url: https://arxiv.org/html/2505.22101v1
paper_id: 2505.22101v1
title: MemOS: An Operating System for Memory-Augmented Generation (MAG) in Large Language Models (Short Version)
scraped_date: 2025-10-16
has_images: yes
has_tables: yes
---

## 1Introduction

Large Language Models (LLMs) are emerging as a foundational pathway toward Artificial General Intelligence (AGI)[39], yet they remain fundamentally limited in supporting robust memory capabilities. Most current architectures rely on implicit parametric memory—knowledge embedded within massive model weights—which is difficult to interpret[37], update[20], or transfer[13]. Although Retrieval-Augmented Generation (RAG) incorporates external knowledge sources[38,10,3,8,11], it effectively serves as an ad hoc textual patch and lacks a structured, unified mechanism for memory management. These architectural shortcomings lead to four critical issues in real-world applications: inability to model long-term and multi-turn conversational states; poor adaptability to evolving knowledge; lack of persistent modeling for user preferences and multi-agent workflows; and the emergence of “memory silos” across platforms, hindering the reuse and migration of prior interactions. At the root of these challenges lies a fundamental oversight: current LLMs do not treat memory as an explicit, schedulable, and governable resource.

To address this, we propose —a memory operating system designed for large language models.MemOScenters memory units as operational resources and establishes a full lifecycle encompassing memory generation, organization, utilization, and evolution. It offers structured representations, unified interfaces, version control, and access governance to overcome systemic limitations in memory handling. Rather than merely extending the RAG paradigm,MemOSintroduces a controllable, adaptable, and evolvable memory infrastructure that empowers LLMs to track knowledge updates, internalize user preferences, and maintain behavioral consistency across platforms. This represents a fundamental shift in language model architecture: from systems that merely perceive and generate to those thatremember, adapt, and grow over time.