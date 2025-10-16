---
source_url: https://arxiv.org/html/2507.03724v3
paper_id: 2507.03724v3
title: \titlefontMemOS: A Memory OS for AI System
scraped_date: 2025-10-16
has_images: yes
has_tables: yes
---

# \titlefontMemOS: A Memory OS for AI System

\ul1]MemTensor (Shanghai) Technology Co., Ltd.
2]Shanghai Jiao Tong University
3]Institute for Advanced Algorithms Research, Shanghai
4]Tongji University
5]Zhejiang University
6]University of Science and Technology of China
7]Peking University
8]Renmin University of China
9]Beihang University
10]Research Institute of China Telecom

# \titlefontMemOS: A Memory OS for AI System

###### Abstract

Large Language Models (LLMs) have become an essential infrastructure for Artificial General Intelligence (AGI), yet their lack of well-defined memory management systems hinders the development of long-context reasoning, continual personalization, and knowledge consistency.Existing models mainly rely on static parameters and short-lived contextual states, limiting their ability to track user preferences or update knowledge over extended periods.While Retrieval-Augmented Generation (RAG) introduces external knowledge in plain text, it remains a stateless workaround without lifecycle control or integration with persistent representations.Recent work has modeled the training and inference cost of LLMs from a memory hierarchy perspective, showing that introducing an explicit memory layer between parameter memory and external retrieval can substantially reduce these costs by externalizing specific knowledge[1]. Beyond computational efficiency, LLMs face broader challenges arising from how information is distributed over time and context, requiring systems capable of managing heterogeneous knowledge spanning different temporal scales and sources. To address this challenge, we proposeMemOS, a memory operating system that treats memory as a manageable system resource. It unifies the representation, scheduling, and evolution of plaintext, activation-based, and parameter-level memories, enabling cost-efficient storage and retrieval. As the basic unit, a MemCube encapsulates both memory content and metadata such as provenance and versioning. MemCubes can be composed, migrated, and fused over time, enabling flexible transitions between memory types and bridging retrieval with parameter-based learning.MemOSestablishes a memory-centric system framework that brings controllability, plasticity, and evolvability to LLMs, laying the foundation for continual learning and personalized modeling.

[Author Legend]†Correspondence\checkdata[Project Website]https://memos.openmem.net/\checkdata[Code]https://github.com/MemTensor/MemOS

## 1Introduction

With the advent of the Transformer architecture and the maturation of self-supervised pretraining, Large Language Models (LLMs) have become the cornerstone of modern NLP.
Trained on large-scale corpora, LLMs exhibit near-human performance in open-domain QA, text generation, and summarization tasks[2].
With increasing model size and compute, their capabilities have expanded to structured code generation[3], cross-modal reasoning[4], multi-turn dialogue, and complex planning—positioning LLMs as a leading paradigm toward Artificial General Intelligence (AGI).

Looking ahead, the presence of LLMs, or more generally, AGI systems, will expand vastly in both time and space.
Temporally, models will shift from stateless, session-based tools to persistent agents embedded in long-running workflows.
Much like humans, they will need to accumulate interaction histories, adapt internal states, and reason over extended contexts.
Spatially, LLMs are evolving into foundational intelligence layers across users, platforms, and ecosystems.
Whether deployed in cloud services or embedded in enterprise systems, they must support consistency, adaptability, and personalization across users, roles, and tasks.
As such omnipresence becomes the norm, a critical challenge emerges: how should knowledge be organized, stored, and retrieved?

With expanding interaction histories, models face a potentially unbounded context space.
We anticipate that future LLMs will seek to leverage as much of their accessible temporal and spatial context as possible, to support deeper reasoning, decision-making, and adaptation.
No longer reprocessing all past information per inference, they will decide what to retain, compress, discard, or prioritize.
In this always-on paradigm, memory becomes a necessity, not an add-on, for maintaining coherent behavior and identity over time.
This requires efficient management of large-scale, multi-source information and dynamic scheduling of memory conditioned on context.
This motivates a layered memory hierarchy, similar to how OSs manage memory, consisting of working memory, long-term storage, and cold archives, governed by recency, access frequency, and importance.
Sharing memory across users and agents requires scoping, permission control, and migratable, reusable representations.
These capabilities are vital not only for system efficiency, but for the long-term sustainability of model-based knowledge evolution.

The management of memory will become model-defined instead of human-defined.
Just as deep learning replaced feature engineering, the transition of memory management from hard-coded pipelines (e.g., RAG) to learnable strategies is natural and necessary.
Future agents will autonomously decide whether to retrieve memory, summarize interaction into reusable rules, abstract preferences, or transfer knowledge across contexts.
In essence, models must take on the responsibility of shaping their own memory architectures and strategies.
Yet, existing infrastructures fall short of enabling this shift.

Mainstream LLMs rely on implicitparameter memory, encoding knowledge in billions or trillions of model weights.
While this approach affords generalization, it suffers from high update cost, poor interpretability, and limited flexibility.
Retraining or fine-tuning requires significant computational resources and risks issues such as catastrophic forgetting.

To address this bottleneck, Retrieval-Augmented Generation (RAG) has emerged as a popular augmentation strategy.
By incorporating external retrieval modules, RAG allows models to dynamically access fresh information at inference time, enabling augmentation without parameter updates[5,6,7,8,9,10,11].
It is now widely deployed in systems such as Copilots[12]and enterprise search[13,14,15,16].
Nonetheless, RAG remains fundamentally an “on-the-fly retrieval and transient composition” pipeline, rather than an integrated memory management system.
It lacks core memory manageability features such as lifecycle tracking, versioning, and permission-aware scheduling, limiting its ability to support long-term, adaptive knowledge systems.
As a result, models continue to exhibit short-memory behavior in multi-turn dialogue, planning, and personalization tasks, struggling to maintain behavioral consistency or long-horizon adaptation.

Recent work has shown that the limitations of current memory mechanisms are not incidental, but stem from the architectural absence of explicit and hierarchical memory representations within LLMs.
For example,[1]argues that without an intermediate explicit memory layer bridging external retrieval and parametric storage, models become suboptimal in terms of read-write cost, and cannot balance storage cost against retrieval efficiency.
This distinction is illustrated in Figure2, which categorizes knowledge and memory formats and highlights the intermediate role of explicit memory.

From a systems perspective, neither parametric memory nor RAG treats memory as a schedulable and evolvable system resource.
This structural gap remains a core bottleneck preventing LLMs from becoming persistent and collaborative intelligent agents.
As application scenarios grow more complex, these limitations become particularly evident in the following four typical contexts.

- •Long-range Dependency Modeling: As tasks and dialogues grow in length, models must preserve instruction and state consistency across multiple turns or stages.
However, current Transformer architectures face three major obstacles: limited context windows constrain input capacity, quadratic attention cost leads to high compute overhead, and user instructions often detach from model behavior over long horizons.
For example, in complex tasks, user-defined code structures or writing styles are frequently forgotten, and model outputs revert to default modes.
As LLMs are deployed in multi-turn dialogue, long-form generation, and persistent workflows, long-context—and even infinite-context—will become a general requirement rather than a rare exception.
This limitation indicates the lack of mechanisms for persistent state maintenance and structured context retention.
- •Adapting to Knowledge Evolution: Real-world knowledge evolves continuously (e.g., legal updates, scientific discoveries, current events), but static parameters prevent timely reflection. RAG allows dynamic retrieval, yet remains a stateless patching mechanism lacking unified versioning, provenance, or temporal awareness. For instance, it may cite outdated and new regulations simultaneously without reconciliation. It cannot retire obsolete facts, prioritize reliable ones, or track knowledge evolution—limiting long-term consistency.
- •Personalization and Multi-role Support: LLMs lack durable “memory traces” across users, roles, or tasks. Each session resets to a blank state, ignoring accumulated preferences or styles. Although tools like ChatGPT and Claude now offer memory, issues persist: capacity limits, unstable access, opaque updates, and missing editability. Current systems emphasize passive recording over structured control, making them ill-suited for long-term personalization across diverse use cases.
- •Cross-platform Memory Migration and Ecosystem Diversity: As LLMs expand from single interfaces to multi-end deployments (web, mobile, enterprise), user memories (e.g., profiles, task history, preferences) should persist across contexts. Yet most systems trap memory within specific instances, forming “memory islands.” For example, ideas explored in ChatGPT[17]can’t carry over to Cursor[18], forcing context rebuilding. This impairs continuity and blocks memory reuse. Deeper yet, centralization vs. decentralization poses a systemic challenge: while monopolized platforms benefit from feedback loops, distributed models risk stagnation. Making memory portable and reusable is key to balancing evolution efficiency with ecosystem diversity.

Long-range Dependency Modeling: As tasks and dialogues grow in length, models must preserve instruction and state consistency across multiple turns or stages.
However, current Transformer architectures face three major obstacles: limited context windows constrain input capacity, quadratic attention cost leads to high compute overhead, and user instructions often detach from model behavior over long horizons.
For example, in complex tasks, user-defined code structures or writing styles are frequently forgotten, and model outputs revert to default modes.
As LLMs are deployed in multi-turn dialogue, long-form generation, and persistent workflows, long-context—and even infinite-context—will become a general requirement rather than a rare exception.
This limitation indicates the lack of mechanisms for persistent state maintenance and structured context retention.

Adapting to Knowledge Evolution: Real-world knowledge evolves continuously (e.g., legal updates, scientific discoveries, current events), but static parameters prevent timely reflection. RAG allows dynamic retrieval, yet remains a stateless patching mechanism lacking unified versioning, provenance, or temporal awareness. For instance, it may cite outdated and new regulations simultaneously without reconciliation. It cannot retire obsolete facts, prioritize reliable ones, or track knowledge evolution—limiting long-term consistency.

Personalization and Multi-role Support: LLMs lack durable “memory traces” across users, roles, or tasks. Each session resets to a blank state, ignoring accumulated preferences or styles. Although tools like ChatGPT and Claude now offer memory, issues persist: capacity limits, unstable access, opaque updates, and missing editability. Current systems emphasize passive recording over structured control, making them ill-suited for long-term personalization across diverse use cases.

Cross-platform Memory Migration and Ecosystem Diversity: As LLMs expand from single interfaces to multi-end deployments (web, mobile, enterprise), user memories (e.g., profiles, task history, preferences) should persist across contexts. Yet most systems trap memory within specific instances, forming “memory islands.” For example, ideas explored in ChatGPT[17]can’t carry over to Cursor[18], forcing context rebuilding. This impairs continuity and blocks memory reuse. Deeper yet, centralization vs. decentralization poses a systemic challenge: while monopolized platforms benefit from feedback loops, distributed models risk stagnation. Making memory portable and reusable is key to balancing evolution efficiency with ecosystem diversity.

A review of the four challenges reveals a shared pattern: models lack the ability to coherently manage and coordinate information distributed across time and space.
This is not due to any single failing module, but to the absence of a system-level mechanism for organizing and operating over memory.

Modern LLMs lack an intermediate layer between parametric storage and external retrieval, making it difficult to manage memory lifecycle, integrate evolving knowledge, or maintain behavioral continuity.
While RAG provides access to external information, its lack of unified structure and operational semantics prevents long-term, controllable use of knowledge.

Therefore, we argue that building future-capable language intelligence systems requires treating memory as a system-level resource that can be explicitly modeled and scheduled.
In modern operating systems, computational resources (CPU), storage (RAM/disks), and communication (I/O) are uniformly scheduled and managed across their lifecycle.
In contrast, memory in large model architectures exists as implicit parameters or temporary retrievals—neither schedulable nor traceable, and incapable of integration or transfer.
Therefore, the key to enhancing memory in LLMs is not simply “adding a cache" or “attaching an external retrieval module," but redefining the operational logic and resource management of memory from a systems-level perspective.

To address these challenges, we proposeMemOS(Memory Operating System), a dedicated memory operating system designed for large language models.
The core philosophy ofMemOSis that, in order to fully utilize temporally and spatially distributed information, models require a unified framework for organizing memory, maintaining internal state, and supporting long-term adaptation.

Inspired by recent work on memory hierarchy for improving model efficiency and adaptability[1],MemOSextends this idea into a system-level design by modeling memory as schedulable and evolvable resource units.
It builds a modular architecture around the memory lifecycle—including generation, activation, fusion, archiving, and expiration—supported by components such asMemReader,MemScheduler,MemLifecycle, andMemOperator, which together orchestrate memory flow, state transitions, and access control.

Much like traditional operating systems coordinate CPU, memory, and I/O,MemOSprovides an abstraction layer and unifiedMemory API, enabling consistent and auditable access to memory units across users, tasks, and sessions.
The system supports structured storage, provenance tagging, lifecycle tracking, and fine-grained permission enforcement, forming a scalable foundation for memory-driven reasoning.
More importantly,MemOSlays a cognitive foundation for the next generation of AGI systems with long-term memory and continual evolution, and provides efficient infrastructure for memory-centric architectural innovation.

The system provides three core capabilities:

- •Controllability:MemOSoffers full lifecycle management of memory units, enabling unified scheduling of memory creation, activation, fusion, and disposal. It implements multi-level permission control and context-aware activation strategies, ensuring safety and traceability in multi-task and multi-user environments through access control and operation auditing. For instance, user preference memories can be scoped to specific agent instances and automatically expire or archive after task completion.
- •Plasticity:MemOSsupports memory restructuring and migration across tasks and roles. It provides memory slicing, tagging, hierarchical mapping, and context binding capabilities, allowing developers or systems to construct highly adaptable memory structures based on inference objectives. This enables models to activate different memory views for different tasks or update memory associations dynamically during role transitions, facilitating rapid cognitive adaptation and behavior shaping.
- •Evolvability:MemOSenables dynamic transitions and unified scheduling among different memory types—including parameter memory (knowledge embedded in model weights), activation memory (contextual inference state), and plaintext memory (structured knowledge fragments). The system supports seamless transitions, such as converting user-defined rules from multiple dialogues into active memory, or compressing long-term structured knowledge into parametric form. This cross-memory adaptation provides a robust foundation for knowledge integration, autonomous learning, and model evolution.

Controllability:MemOSoffers full lifecycle management of memory units, enabling unified scheduling of memory creation, activation, fusion, and disposal. It implements multi-level permission control and context-aware activation strategies, ensuring safety and traceability in multi-task and multi-user environments through access control and operation auditing. For instance, user preference memories can be scoped to specific agent instances and automatically expire or archive after task completion.

Plasticity:MemOSsupports memory restructuring and migration across tasks and roles. It provides memory slicing, tagging, hierarchical mapping, and context binding capabilities, allowing developers or systems to construct highly adaptable memory structures based on inference objectives. This enables models to activate different memory views for different tasks or update memory associations dynamically during role transitions, facilitating rapid cognitive adaptation and behavior shaping.

Evolvability:MemOSenables dynamic transitions and unified scheduling among different memory types—including parameter memory (knowledge embedded in model weights), activation memory (contextual inference state), and plaintext memory (structured knowledge fragments). The system supports seamless transitions, such as converting user-defined rules from multiple dialogues into active memory, or compressing long-term structured knowledge into parametric form. This cross-memory adaptation provides a robust foundation for knowledge integration, autonomous learning, and model evolution.

Therefore, as a novel infrastructure for the continual evolution of LLMs,MemOSaims to reconstruct the representation, management, and scheduling of memory from a systems perspective. It addresses core limitations in structured memory, lifecycle management, and multi-source integration, while providing OS-level support for cross-task adaptation, cross-modal evolution, and cross-platform migration.
The introduction ofMemOSmarks a critical transition in the development of large models: from mere perception and generation to memory and evolution.

## 2Memory in Large Language Models

Research in memory capabilities in large language models has generally progressed through four key stages:(1) The stage of definition and exploration, which focuses on categorizing and analyzing LLM memory systems from multiple perspectives, while identifying effective optimization mechanisms applicable in real-world scenarios.(2) The stage of human-like memory development, which addresses performance gaps in complex tasks arising from discrepancies between LLM and human memory by introducing various forms of cognitively inspired memory mechanisms.(3) The stage of tool-based memory management, where modular interfaces for memory operations begin to emerge, yet are largely limited to basic insert, delete, and update functionalities over existing memory structures.
Our proposedMemOSintroduces operating system–inspired resource management mechanisms to LLM memory, offering standardized and unified interfaces for full-lifecycle memory management and scheduling. This paves the way toward(4) The stage of systematic memory governance, enabling structured evolution, abstraction, and secure control over memory resources.
In this subsection, we review existing research on memory in large models along this developmental trajectory.

### 2.1Stage 1: Memory Definition and Exploration

Several recent studies have proposed systematic classifications and analyses of memory in LLMs from various dimensions. For example,[19]categorizes memory into three types: parameter memory, unstructured contextual memory, and structured contextual memory.[20]classifies memory based on object (personal vs. system), form (parametric vs. non-parametric), and temporal aspects (short-term vs. long-term).[21]further divides memory into four types: parameter-based, key-value cache-based, hidden state-based, and text-based, and introduces retention duration as a standard to distinguish sensory memory, short-term memory, and long-term memory.

Building on these works, we propose that LLM memory can be characterized along two primary dimensions:implicitandexplicit. Implicit memory includes parameter memory, key-value cache, and hidden states, while explicit memory involves text- and context-based information storage.
Memory can be classified temporally as sensory, short-term, or long-term. Sensory memory captures fleeting impressions of perceptual input, with extremely short duration and no conscious processing. While traditionally treated as a separate stage, we include it under short-term memory for unified scheduling and handling of initial information. This work adopts this two-dimensional framework to analyze memory mechanisms in the first and second stages (see Figure3left, Table1).

<table class="ltx_tabular ltx_centering ltx_align_middle">
<tr class="ltx_tr">
<td class="ltx_td ltx_align_justify ltx_align_middle ltx_border_t" style="width:34.7pt;padding-top:1.7pt;padding-bottom:1.7pt;">
<span class="ltx_inline-block ltx_align_top">
<span class="ltx_p"><span class="ltx_text ltx_font_bold" style="font-size:80%;">Timescale</span></span>
</span>
</td>
<td class="ltx_td ltx_align_justify ltx_align_middle ltx_border_t" style="width:52.0pt;padding-top:1.7pt;padding-bottom:1.7pt;">
<span class="ltx_inline-block ltx_align_top">
<span class="ltx_p"><span class="ltx_text ltx_font_bold" style="font-size:80%;">Consciousness</span></span>
</span>
</td>
<td class="ltx_td ltx_align_justify ltx_align_middle ltx_border_t" style="width:99.7pt;padding-top:1.7pt;padding-bottom:1.7pt;">
<span class="ltx_inline-block ltx_align_top">
<span class="ltx_p"><span class="ltx_text ltx_font_bold" style="font-size:80%;">Mechanism</span></span>
</span>
</td>
<td class="ltx_td ltx_align_justify ltx_align_middle ltx_border_t" style="width:199.5pt;padding-top:1.7pt;padding-bottom:1.7pt;">
<span class="ltx_inline-block ltx_align_top">
<span class="ltx_p"><span class="ltx_text ltx_font_bold" style="font-size:80%;">Example References</span></span>
</span>
</td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_align_justify ltx_align_middle ltx_border_t" rowspan="4" style="width:34.7pt;padding-top:1.7pt;padding-bottom:1.7pt;">
<span class="ltx_inline-block ltx_align_top">
<span class="ltx_p"><span class="ltx_text" style="font-size:80%;">
<span class="ltx_tabular ltx_align_middle">
<span class="ltx_tr">
<span class="ltx_td ltx_nopad_r ltx_align_left" style="padding-top:1.7pt;padding-bottom:1.7pt;">Short-term</span></span>
</span></span><span class="ltx_text" style="font-size:80%;"> </span></span>
</span>
</td>
<td class="ltx_td ltx_align_justify ltx_align_middle ltx_border_t" style="width:52.0pt;padding-top:1.7pt;padding-bottom:1.7pt;">
<span class="ltx_inline-block ltx_align_top">
<span class="ltx_p"><span class="ltx_text" style="font-size:80%;">
<span class="ltx_tabular ltx_align_middle">
<span class="ltx_tr">
<span class="ltx_td ltx_nopad_r ltx_align_left" style="padding-top:1.7pt;padding-bottom:1.7pt;">Explicit</span></span>
</span></span><span class="ltx_text" style="font-size:80%;"> </span></span>
</span>
</td>
<td class="ltx_td ltx_align_justify ltx_align_middle ltx_border_t" style="width:99.7pt;padding-top:1.7pt;padding-bottom:1.7pt;">
<span class="ltx_inline-block ltx_align_top">
<span class="ltx_p"><span class="ltx_text" style="font-size:80%;">Prompt-Based Context</span></span>
</span>
</td>
<td class="ltx_td ltx_align_justify ltx_align_middle ltx_border_t" style="width:199.5pt;padding-top:1.7pt;padding-bottom:1.7pt;">
<span class="ltx_inline-block ltx_align_top">
<span class="ltx_p"><span class="ltx_text" style="font-size:80%;">GPT-2 </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib22" title="">22</a><span class="ltx_text" style="font-size:80%;">]</span></cite><span class="ltx_text" style="font-size:80%;">, GPT-3 </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib23" title="">23</a><span class="ltx_text" style="font-size:80%;">]</span></cite><span class="ltx_text" style="font-size:80%;">, Prefix-Tuning </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib24" title="">24</a><span class="ltx_text" style="font-size:80%;">]</span></cite><span class="ltx_text" style="font-size:80%;">, Prompt-Tuning </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib25" title="">25</a><span class="ltx_text" style="font-size:80%;">]</span></cite><span class="ltx_text" style="font-size:80%;">, P-Tuning </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib26" title="">26</a>, <a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib27" title="">27</a><span class="ltx_text" style="font-size:80%;">]</span></cite><span class="ltx_text" style="font-size:80%;">, InstructGPT </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib28" title="">28</a><span class="ltx_text" style="font-size:80%;">]</span></cite></span>
</span>
</td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_align_justify ltx_align_middle ltx_border_t" rowspan="3" style="width:52.0pt;padding-top:1.7pt;padding-bottom:1.7pt;">
<span class="ltx_inline-block ltx_align_top">
<span class="ltx_p"><span class="ltx_text" style="font-size:80%;">
<span class="ltx_tabular ltx_align_middle">
<span class="ltx_tr">
<span class="ltx_td ltx_nopad_r ltx_align_left" style="padding-top:1.7pt;padding-bottom:1.7pt;">Implicit</span></span>
</span></span><span class="ltx_text" style="font-size:80%;"> </span></span>
</span>
</td>
<td class="ltx_td ltx_align_justify ltx_align_middle ltx_border_t" style="width:99.7pt;padding-top:1.7pt;padding-bottom:1.7pt;">
<span class="ltx_inline-block ltx_align_top">
<span class="ltx_p"><span class="ltx_text" style="font-size:80%;">Key-Value Cache Mechanism</span></span>
</span>
</td>
<td class="ltx_td ltx_align_justify ltx_align_middle ltx_border_t" style="width:199.5pt;padding-top:1.7pt;padding-bottom:1.7pt;">
<span class="ltx_inline-block ltx_align_top">
<span class="ltx_p"><span class="ltx_text" style="font-size:80%;">vLLM </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib29" title="">29</a><span class="ltx_text" style="font-size:80%;">]</span></cite><span class="ltx_text" style="font-size:80%;">, StreamingLLM</span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib30" title="">30</a><span class="ltx_text" style="font-size:80%;">]</span></cite><span class="ltx_text" style="font-size:80%;">, H2O</span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib31" title="">31</a><span class="ltx_text" style="font-size:80%;">]</span></cite><span class="ltx_text" style="font-size:80%;">, LESS </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib32" title="">32</a><span class="ltx_text" style="font-size:80%;">]</span></cite><span class="ltx_text" style="font-size:80%;">, KVQuant </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib33" title="">33</a><span class="ltx_text" style="font-size:80%;">]</span></cite><span class="ltx_text" style="font-size:80%;">, RetrievalAttention </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib34" title="">34</a><span class="ltx_text" style="font-size:80%;">]</span></cite><span class="ltx_text" style="font-size:80%;">, Memory</span><sup class="ltx_sup"><span class="ltx_text" style="font-size:80%;">3</span></sup><span class="ltx_text" style="font-size:80%;"> </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib1" title="">1</a><span class="ltx_text" style="font-size:80%;">]</span></cite></span>
</span>
</td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_align_justify ltx_align_middle ltx_border_t" style="width:99.7pt;padding-top:1.7pt;padding-bottom:1.7pt;">
<span class="ltx_inline-block ltx_align_top">
<span class="ltx_p"><span class="ltx_text" style="font-size:80%;">Hidden State Steering</span></span>
</span>
</td>
<td class="ltx_td ltx_align_justify ltx_align_middle ltx_border_t" style="width:199.5pt;padding-top:1.7pt;padding-bottom:1.7pt;">
<span class="ltx_inline-block ltx_align_top">
<span class="ltx_p"><span class="ltx_text" style="font-size:80%;">Steer </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib35" title="">35</a><span class="ltx_text" style="font-size:80%;">]</span></cite><span class="ltx_text" style="font-size:80%;">, ICV </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib36" title="">36</a><span class="ltx_text" style="font-size:80%;">]</span></cite><span class="ltx_text" style="font-size:80%;">, ActAdd </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib37" title="">37</a><span class="ltx_text" style="font-size:80%;">]</span></cite><span class="ltx_text" style="font-size:80%;">, StyleVec </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib38" title="">38</a><span class="ltx_text" style="font-size:80%;">]</span></cite><span class="ltx_text" style="font-size:80%;">, CAA </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib39" title="">39</a><span class="ltx_text" style="font-size:80%;">]</span></cite><span class="ltx_text" style="font-size:80%;">, FreeCtrl </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib40" title="">40</a><span class="ltx_text" style="font-size:80%;">]</span></cite><span class="ltx_text" style="font-size:80%;">, EasyEdit2 </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib41" title="">41</a><span class="ltx_text" style="font-size:80%;">]</span></cite></span>
</span>
</td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_align_justify ltx_align_middle ltx_border_t" style="width:99.7pt;padding-top:1.7pt;padding-bottom:1.7pt;">
<span class="ltx_inline-block ltx_align_top">
<span class="ltx_p"><span class="ltx_text" style="font-size:80%;">Activation Circuit Modulation</span></span>
</span>
</td>
<td class="ltx_td ltx_align_justify ltx_align_middle ltx_border_t" style="width:199.5pt;padding-top:1.7pt;padding-bottom:1.7pt;">
<span class="ltx_inline-block ltx_align_top">
<span class="ltx_p"><span class="ltx_text" style="font-size:80%;">SAC </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib42" title="">42</a><span class="ltx_text" style="font-size:80%;">]</span></cite><span class="ltx_text" style="font-size:80%;">, DESTEIN </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib43" title="">43</a><span class="ltx_text" style="font-size:80%;">]</span></cite><span class="ltx_text" style="font-size:80%;">, LM-Steer </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib44" title="">44</a><span class="ltx_text" style="font-size:80%;">]</span></cite></span>
</span>
</td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_align_justify ltx_align_middle ltx_border_b ltx_border_t" rowspan="4" style="width:34.7pt;padding-top:1.7pt;padding-bottom:1.7pt;">
<span class="ltx_inline-block ltx_align_top">
<span class="ltx_p"><span class="ltx_text" style="font-size:80%;">
<span class="ltx_tabular ltx_align_middle">
<span class="ltx_tr">
<span class="ltx_td ltx_nopad_r ltx_align_left" style="padding-top:1.7pt;padding-bottom:1.7pt;">Long-term</span></span>
</span></span><span class="ltx_text" style="font-size:80%;"> </span></span>
</span>
</td>
<td class="ltx_td ltx_align_justify ltx_align_middle ltx_border_t" style="width:52.0pt;padding-top:1.7pt;padding-bottom:1.7pt;">
<span class="ltx_inline-block ltx_align_top">
<span class="ltx_p"><span class="ltx_text" style="font-size:80%;">
<span class="ltx_tabular ltx_align_middle">
<span class="ltx_tr">
<span class="ltx_td ltx_nopad_r ltx_align_left" style="padding-top:1.7pt;padding-bottom:1.7pt;">Explicit</span></span>
</span></span><span class="ltx_text" style="font-size:80%;"> </span></span>
</span>
</td>
<td class="ltx_td ltx_align_justify ltx_align_middle ltx_border_t" style="width:99.7pt;padding-top:1.7pt;padding-bottom:1.7pt;">
<span class="ltx_inline-block ltx_align_top">
<span class="ltx_p"><span class="ltx_text" style="font-size:80%;">Non-parametric Retrieval-Augmented Generation</span></span>
</span>
</td>
<td class="ltx_td ltx_align_justify ltx_align_middle ltx_border_t" style="width:199.5pt;padding-top:1.7pt;padding-bottom:1.7pt;">
<span class="ltx_inline-block ltx_align_top">
<span class="ltx_p"><span class="ltx_text" style="font-size:80%;">kNN-LMs </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib45" title="">45</a>, <a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib46" title="">46</a><span class="ltx_text" style="font-size:80%;">]</span></cite><span class="ltx_text" style="font-size:80%;">, MEMWALKER </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib9" title="">9</a><span class="ltx_text" style="font-size:80%;">]</span></cite><span class="ltx_text" style="font-size:80%;">, Graph RAG </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib10" title="">10</a><span class="ltx_text" style="font-size:80%;">]</span></cite><span class="ltx_text" style="font-size:80%;">, LightRAG </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib11" title="">11</a><span class="ltx_text" style="font-size:80%;">]</span></cite><span class="ltx_text" style="font-size:80%;">, NodeRAG </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib47" title="">47</a>, <a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib48" title="">48</a><span class="ltx_text" style="font-size:80%;">]</span></cite><span class="ltx_text" style="font-size:80%;">, HyperGraphRAG </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib49" title="">49</a><span class="ltx_text" style="font-size:80%;">]</span></cite><span class="ltx_text" style="font-size:80%;">, HippoRAG </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib50" title="">50</a>, <a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib51" title="">51</a><span class="ltx_text" style="font-size:80%;">]</span></cite><span class="ltx_text" style="font-size:80%;">, PGRAG</span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib52" title="">52</a><span class="ltx_text" style="font-size:80%;">]</span></cite><span class="ltx_text" style="font-size:80%;">, Zep </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib53" title="">53</a><span class="ltx_text" style="font-size:80%;">]</span></cite><span class="ltx_text" style="font-size:80%;">, A-MEM </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib54" title="">54</a><span class="ltx_text" style="font-size:80%;">]</span></cite><span class="ltx_text" style="font-size:80%;">, Mem0</span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib55" title="">55</a><span class="ltx_text" style="font-size:80%;">]</span></cite></span>
</span>
</td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_align_justify ltx_align_middle ltx_border_b ltx_border_t" rowspan="3" style="width:52.0pt;padding-top:1.7pt;padding-bottom:1.7pt;">
<span class="ltx_inline-block ltx_align_top">
<span class="ltx_p"><span class="ltx_text" style="font-size:80%;">
<span class="ltx_tabular ltx_align_middle">
<span class="ltx_tr">
<span class="ltx_td ltx_nopad_r ltx_align_left" style="padding-top:1.7pt;padding-bottom:1.7pt;">Implicit</span></span>
</span></span><span class="ltx_text" style="font-size:80%;"> </span></span>
</span>
</td>
<td class="ltx_td ltx_align_justify ltx_align_middle ltx_border_t" style="width:99.7pt;padding-top:1.7pt;padding-bottom:1.7pt;">
<span class="ltx_inline-block ltx_align_top">
<span class="ltx_p"><span class="ltx_text" style="font-size:80%;">Parametric Knowledge</span></span>
</span>
</td>
<td class="ltx_td ltx_align_justify ltx_align_middle ltx_border_t" style="width:199.5pt;padding-top:1.7pt;padding-bottom:1.7pt;">
<span class="ltx_inline-block ltx_align_top">
<span class="ltx_p"><span class="ltx_text" style="font-size:80%;">BERT </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib56" title="">56</a><span class="ltx_text" style="font-size:80%;">]</span></cite><span class="ltx_text" style="font-size:80%;">, RLHF </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib57" title="">57</a><span class="ltx_text" style="font-size:80%;">]</span></cite><span class="ltx_text" style="font-size:80%;">, CTRL </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib58" title="">58</a><span class="ltx_text" style="font-size:80%;">]</span></cite><span class="ltx_text" style="font-size:80%;">, SLayer </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib59" title="">59</a><span class="ltx_text" style="font-size:80%;">]</span></cite></span>
</span>
</td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_align_justify ltx_align_middle ltx_border_t" style="width:99.7pt;padding-top:1.7pt;padding-bottom:1.7pt;">
<span class="ltx_inline-block ltx_align_top">
<span class="ltx_p"><span class="ltx_text" style="font-size:80%;">Modular Parameter Adaptation</span></span>
</span>
</td>
<td class="ltx_td ltx_align_justify ltx_align_middle ltx_border_t" style="width:199.5pt;padding-top:1.7pt;padding-bottom:1.7pt;">
<span class="ltx_inline-block ltx_align_top">
<span class="ltx_p"><span class="ltx_text" style="font-size:80%;">LoRA </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib60" title="">60</a><span class="ltx_text" style="font-size:80%;">]</span></cite><span class="ltx_text" style="font-size:80%;">, PRAG </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib61" title="">61</a><span class="ltx_text" style="font-size:80%;">]</span></cite><span class="ltx_text" style="font-size:80%;">, DyPRAG </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib62" title="">62</a><span class="ltx_text" style="font-size:80%;">]</span></cite><span class="ltx_text" style="font-size:80%;">, SERAC </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib63" title="">63</a><span class="ltx_text" style="font-size:80%;">]</span></cite><span class="ltx_text" style="font-size:80%;">, CaliNet </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib64" title="">64</a><span class="ltx_text" style="font-size:80%;">]</span></cite><span class="ltx_text" style="font-size:80%;">, DPM </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib65" title="">65</a><span class="ltx_text" style="font-size:80%;">]</span></cite><span class="ltx_text" style="font-size:80%;">, GRACE </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib66" title="">66</a><span class="ltx_text" style="font-size:80%;">]</span></cite></span>
</span>
</td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_align_justify ltx_align_middle ltx_border_b ltx_border_t" style="width:99.7pt;padding-top:1.7pt;padding-bottom:1.7pt;">
<span class="ltx_inline-block ltx_align_top">
<span class="ltx_p"><span class="ltx_text" style="font-size:80%;">Parametric Memory Editing</span></span>
</span>
</td>
<td class="ltx_td ltx_align_justify ltx_align_middle ltx_border_b ltx_border_t" style="width:199.5pt;padding-top:1.7pt;padding-bottom:1.7pt;">
<span class="ltx_inline-block ltx_align_top">
<span class="ltx_p"><span class="ltx_text" style="font-size:80%;">ROME </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib67" title="">67</a><span class="ltx_text" style="font-size:80%;">]</span></cite><span class="ltx_text" style="font-size:80%;">, MEMIT </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib68" title="">68</a><span class="ltx_text" style="font-size:80%;">]</span></cite><span class="ltx_text" style="font-size:80%;">, AlphaEdit </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib69" title="">69</a><span class="ltx_text" style="font-size:80%;">]</span></cite><span class="ltx_text" style="font-size:80%;">, AnyEdit </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib70" title="">70</a><span class="ltx_text" style="font-size:80%;">]</span></cite><span class="ltx_text" style="font-size:80%;">, EasyEdit </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib71" title="">71</a><span class="ltx_text" style="font-size:80%;">]</span></cite><span class="ltx_text" style="font-size:80%;">, AdaPLE </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib72" title="">72</a><span class="ltx_text" style="font-size:80%;">]</span></cite><span class="ltx_text" style="font-size:80%;">, MEMAT </span><cite class="ltx_cite ltx_citemacro_cite"><span class="ltx_text" style="font-size:80%;">[</span><a class="ltx_ref" href="https://arxiv.org/html/2507.03724v3#bib.bib73" title="">73</a><span class="ltx_text" style="font-size:80%;">]</span></cite></span>
</span>
</td>
</tr>
</table>

#### 2.1.1Implicit Memory in LLMs

##### Implicit Long-term Memory in LLMs

Through large-scale pretraining, LLMs encode syntactic structures, conceptual relationships, and language usage patterns from corpora into their weight matrices. These parameters serve as implicit long-term memory, internalized into the model’s inherent capabilities. Although they lack explicit expression, they continuously influence language generation behavior, knowledge expression, and even semantic generalization.

Training:In LLMs, training is the most fundamental and direct method for forming implicit long-term memory. For example, pretraining[56,23]and post-training[57,28]enable large-scale parameter updates, fundamentally reconstructing the internal knowledge distribution and behavioral structure of the model.
Some studies introduce memory explicitly during training. For instance, CTRL[58]includes control codes in training data to help models automatically associate contextual information during text generation. Memory&Reasoning[74]fine-tunes the model to decouple output into separate memory and reasoning components, fully leveraging memory for inference. SLayer[59]identifies memory-relevant layers in the model and locally fine-tunes them to enhance specific knowledge representation.
It is worth noting that relying solely on memorization of training data can be limited in real-world deployment due to distributional shifts between real-world and training data.
Titans[75]proposes a dynamic memory mechanism by encoding historical information into neural network parameters and training a pluggable online meta-model. This meta-model can adaptively decide retention or forgetting strategies for specific data during real usage, thereby improving generalization across distribution shifts.

Adaptor:Full-scale training or fine-tuning is costly and often impractical for rapid memory updates in real-world scenarios.
To address this, adapter-based methods freeze the core model parameters and introduce small, trainable modules that adapt quickly to new memory with minimal disruption to original capabilities.
LoRA[60]inserts low-rank adapters into the model, enabling lightweight parameter tuning without modifying the original parameter structure, supporting efficient loading and storage of implicit memory.
PRAG[61]treats LoRA adapter modules trained for specific documents or tasks as “memory units” and merges them into the main model as needed, enabling rapid access to specialized knowledge.
Furthermore, DyPRAG[62]introduces a neural generator that directly maps input documents to LoRA parameters, significantly reducing explicit memory storage cost.

Editing:Memory editing refers to targeted interventions on model parameters to induce new knowledge or behaviors for specific inputs while preserving existing capabilities as much as possible.
Most existing research focuses on editing objective factual knowledge, such as correcting answers to questions like “Who is the president of the United States?”
However, memory in LLMs also includes abstract competencies such as language style, semantic preferences, and reasoning modes, for which systematic editing methods are still lacking.
If not carefully controlled, local parameter edits can lead to undesirable global behavior shifts. Thus, edit precision and retention of existing capabilities are key evaluation metrics.
This paper follows[76]in categorizing knowledge editing techniques into three types:(1) Locate-then-edit intuitive methods[67,68,77]: These methods use causal tracing to locate where the target knowledge is stored, followed by targeted parameter updates.(2) Meta-learning-based methods[78,79,80]: These use hypernetworks to directly predict parameter changes. Another important direction is preserving prior knowledge and abilities during editing[69,70,72].(3) Adapter-based editing strategies[64,63,66,65]: These preserve the LLM backbone, offering a degree of edit controllability.

##### Implicit Short-term Memory in LLMs

Beyond the internalized parametric long-term memory, LLMs also depend on dynamically generated and transient intermediate representations during inference—such as KV-caches and hidden states. Although these representations lack explicit forms, they continually influence attention distributions and behavioral strategies in autoregressive generation, forming the implicit short-term memory of LLMs. They play a vital role in maintaining contextual coherence, enabling instant control, and facilitating behavior transition, and have become a crucial entry point for understanding and enhancing dynamic capabilities of language models.

KV-cache:KV-cache stores key-value representations of previously processed tokens, enabling persistent access to historical memory during autoregressive generation. Although users cannot directly manipulate these caches, they implicitly modulate attention and output behavior during inference[1].
Subsequent optimization work has focused primarily on improving compute and memory efficiency. Techniques such as low-rank compression and quantization are adopted by LESS[32]and KVQuant[33], while StreamingLLM[30]and H2O[31]dynamically prune less relevant KV pairs based on attention patterns.
More recent studies introduce retrieval-based memory activation[81,34], enabling selective access to cached content. Meanwhile, vLLM[29]draws from operating system design by implementing PagedAttention—using virtual memory-style page caching to reduce redundant storage and improve KV access.

While most existing work focuses on optimizing KV-cache for inference efficiency, its capacity to represent structured and controllable knowledge remains underexplored. Memory3[1]takes a first step in this direction by encoding external knowledge bases as sparse key-value pairs, which are injected into the model’s self-attention layers. This enables dynamic, non-parametric retrieval of relevant information during inference, effectively externalizing knowledge and improving memory controllability—offering new directions for the structured use of short-term memory.
Building on the foundation laid by Memory3,MemOSadvances the notion of structured memory by proposing the first hierarchical memory architecture for LLMs that models and unifies three distinct substrates: plaintext memory, activation memory, and parameter memory. It introduces an integrated retrieval and scheduling framework that enables explicit control, efficient fusion, and dynamic activation. The MemCube module further organizes semantic fragments into a multi-dimensional structure, enabling query-based aggregation and multi-granularity activation—paving the way for more systematic and scalable memory utilization in LLMs.

Hidden States:Hidden states represent the layer-wise intermediate activations within LLMs during processing, encoding the model’s semantic understanding and generation trajectory. Compared to modifying model parameters, directly manipulating hidden states offers a more flexible, instantaneous, and efficient means of memory control.
Among the various mechanisms, steering vectors[35]stand out as a representative method. These vectors are derived by computing activation differences between inputs with contrasting semantic attributes, forming directionally meaningful control signals. Injecting such vectors into the intermediate activations of other inputs can steer generation toward specific semantic directions without altering the model architecture.
To avoid reliance on supervised corpora, methods like Self-Detoxifying[82], ActAdd[37], ICV[36], StyleVec[38], and CAA[39]propose unsupervised contrastive approaches. These construct semantically similar yet attribute-opposing input pairs (e.g., emotion, stance, politeness) to extract hidden state differences and generate steering vectors, enabling automated, lightweight signal derivation. This not only enhances the portability of steerable control but also lowers its entry barrier.
As an implicit short-term memory mechanism, hidden states have been validated in various practical tasks. For example, steering vectors have been employed in hallucination mitigation and factual consistency enhancement in ACT[83], ITI[84], and InferAligner[85]. IFS[86]extends their application to controlling low-level generation features such as text formatting and sentence length, indicating that hidden state interventions are effective not only for abstract semantics but also for structural behavior modulation.

#### 2.1.2Explicit Memory in LLMs

##### Explicit Short-term Memory in LLMs

LLMs’ explicit short-term memory primarily resides in their input context window—namely, the prompt and directly concatenated historical dialogues, including user task descriptions, interaction history, and reference documents. These explicitly injected elements are directly perceived and utilized during inference, forming the basis for understanding the current context and generating responses.
With the increasing scale and capabilities of LLMs, their ability to manage explicit short-term memory has significantly improved. From early general-purpose language models relying on static text input[22,23], to parameterized prompt techniques using learnable continuous vectors[24,25,26,27], to advanced instruction-following models[87,88,89], and the InstructGPT-style instruction tuning paradigm[28], mechanisms for expressing and managing explicit short-term memory have evolved from static configuration to dynamic interaction, becoming increasingly structured and flexible.
However, explicit short-term memory in LLMs is physically constrained by context window length. When handling lengthy texts or multi-turn dialogues, models often encounter truncation of early content and memory fading, leading to diminished semantic coherence or loss of key information[90,91]. Recent research has attempted to alleviate these bottlenecks through longer windows, external retrieval, or more efficient caching, yet the capacity of explicit short-term memory remains a key limiting factor in real-time comprehension and interaction.

##### Explicit Long-term Memory in LLMs

Unlike short-term memory dependent on context windows, LLMs’ explicit long-term memory emphasizes sustained access to external non-parametric knowledge, with a focus on optimizing memory organization structures and retrieval strategies.
Early research focused on identifying effective retrieval mechanisms for recalling relevant content from standalone external memory stores. Common approaches include off-the-shelf retrievers such as BM25[92], Dense Passage Retrieval (DPR)[93], and hybrid retrieval methods[94].
However, such retrieve-then-generate approaches impose an inherent bottleneck in integrating retrieved content into model reasoning. Thus, some studies have explored tighter coupling of retrieval with inference. Non-parametric language models (NPLMs) such as kNN-LMs[45,46]propose a linear fusion of neural language models (e.g., Transformers) with k-nearest-neighbor retrieval. At each prediction step, they retrieve top-matching context chunks from memory and blend their influence into the model’s output distribution to improve reference fidelity.

Due to the limited representational capacity of flat memory structures, optimizing retrieval alone often fails to surpass performance ceilings. As a result, research has increasingly shifted toward enhancing memory organization itself. Traditional key-value formats have gradually evolved into more hierarchical and relational structures, such as tree-based[9]and graph-based formats[10,11].
To further represent diverse memory relationships, researchers have introduced heterogeneous graphs[47,48]and hypergraph structures[49], enabling unified modeling and dynamic control of varied knowledge types and complex semantic links. These advances greatly enhance the expressive power and generalization of memory networks. To endow LLMs with structured, dynamic, and persistent memory, Zep[53]builds on GraphRAG[10]by adding timeline modeling to track memory evolution over time. A-MEM[54]draws from dynamic memory networks to support automatic memory linking and semantic updating, allowing LLM memory to evolve across multi-turn interactions.

### 2.2Stage 2: Development of Human-like Memory

To enhance the memory capabilities of LLMs in complex tasks, some studies have drawn inspiration from human memory mechanisms and knowledge management methods, proposing various forms of human-like memory.

In the early stages of human-like memory research, the focus was on simulating the structural and functional mechanisms of human memory.
One representative early work is the HippoRAG series of models[50,51], inspired by the "hippocampal indexing theory" in human long-term memory.
The model integrates LLMs, knowledge graphs, and the Personalized PageRank algorithm to emulate the roles of the neocortex and hippocampus in memory, achieving more efficient knowledge integration and retrieval.
Memory3[1], inspired by the hierarchical structure of human memory, makes the KV-cache in the attention mechanism explicit as a memory carrier for the model.
This approach offers a lower-cost alternative to parameter storage or traditional RAG, significantly reducing the resource consumption for training and inference.

As research advanced, system designs began emphasizing human-like behavior and function, simulating how humans actually use memory.
For instance, PGRAG[52]mimics the act of note-taking during reading, automatically generating mind maps as explicit long-term memory to enhance organization and durability.
Second-Me[95]proposes a multi-level architecture centered on human-like memory behaviors, emphasizing experience-driven personalized retrieval.
The system consists of three layers: L0 retains raw data for completeness; L1 enhances organization and retrievability through structured natural language; L2 internalizes user preferences via parameter tuning, enabling associative reasoning similar to humans.
AutoGen[96]introduces a multi-agent framework to simulate human group collaboration, forming a dialog ecosystem of interacting agents.
Each agent has distinct roles, and they collaborate through dialog to share information and accomplish complex tasks like mathematical reasoning, information retrieval, and code generation.

### 2.3Stage 3: Tool-based Memory Management

With the growing understanding of memory in LLMs, researchers have begun exploring explicit manipulation of knowledge, pushing memory management from implicit representations toward tool-based interfaces.

This stage witnessed the emergence of standardized frameworks for memory editing, enabling users to dynamically update the model’s semantic behavior through insert, modify, and delete operations. For example, early approaches like EasyEdit[71,41]offer unified interfaces to manipulate model parameters and hidden states for fine-grained control.
Another representative line of work is Mem0[97], which targets the context window bottleneck by introducing external memory modules maintained through extract-update workflows. Follow-ups to Mem0 even structure conversational memory into graphs to enable richer semantic modeling and long-term evolution.
Among these, Letta[98]stands out as a system-oriented attempt. It draws inspiration from traditional operating systems by modularizing context and introducing function-style paging for dynamic memory access.

However, most work in this stage remains limited to interface-level utilities. While tool-based management introduces basic CRUD operations, it lacks systematic modeling and governance of memory as a core resource—making it insufficient for tasks requiring memory evolution, coordination, or security.

### 2.4Stage 4: Systematic Memory Governance

Although tool-based management introduces explicit memory operation interfaces, it essentially patches implicit mechanisms.
CRUD capabilities alleviate short-term issues but fall short of addressing systemic challenges like memory evolution, access control, and version management.
Just as system calls alone cannot build a complete OS, "tooling" memory lacks a sustainable and scalable governance architecture.

To overcome the limitations of tool-based management, we proposeMemOS, a memory operating system purpose-built for LLMs, marking the entry into the stage of systematic memory governance.MemOStreats memory units as first-class resources and builds upon operating system design principles to introduce comprehensive governance mechanisms including scheduling, layering, API abstraction, permission control, and exception handling.
Unlike the tool-based phase,MemOSnot only enables operations but also emphasizes the evolution and integration of memory across tasks, sessions, and agent roles.
With core modules such as MemScheduler, Memory Layering, and Memory Governance,MemOSenables unified scheduling and behavior-driven evolution of heterogeneous memory types—building a long-term cognitive structure essential for AGI.
We envision the “memory-as-OS” paradigm pioneered byMemOSas the infrastructural backbone for future general-purpose agents, enabling sustainable knowledge accumulation and self-evolution.

## 3MemOSDesign Philosophy

### 3.1Vision ofMemOS

As AGI advances toward increasingly complex systems involving multiple tasks, roles, and modalities, LLMs must go beyond merely “understanding the world”—they must also “accumulate experience,” “retain memory,” and “continuously evolve.” However, current mainstream LLM architectures lack systematic support for memory as a core intelligence capability: knowledge is rigidly encoded in parameters, context cannot be preserved across sessions, personalization cannot be retained, and knowledge updates are prohibitively expensive. We argue that the next-generation LLM architecture must adopt a memory-centric design paradigm.

As shown in Figure4, model performance is approaching the upper limits predicted by traditional scaling laws. The prevailing research paradigm is transitioning from data- and parameter-centric pretraining to post-training, which emphasizes reinforcement alignment and instruction tuning[99]. Yet this shift faces two major challenges: diminishing returns and growing system complexity. To unlock the next leap in capability, we must transcend the current paradigm by incorporating continuous memory modeling and dynamic memory scheduling—thereby enabling long-term knowledge accumulation, task adaptation, and behavioural evolution.

Beyond the temporal benefits of continual learning, memory training also introduces a spatial scaling effect. Thousands of heterogeneously deployed model instances can gather experience in situ and exchange compact memory units—rather than expensive parameters or gradients—to build a collective knowledge base. This memory-parallel regime blurs the line between training and deployment, effectively extending data parallelism to a society-scale, distributed intelligence ecosystem.
Two technical challenges arise:
(1) efficient knowledge exchange across highly heterogeneous environments, and
(2) strict governance that protects private or sensitive data while maximising shared utility.

We therefore advocate a memory-centric training strategy—the Mem-training Paradigm. Instead of relying solely on sporadic parameter updates, Mem-training drives continuous evolution through explicit, controllable memory units. Unlike traditional workflows that modify the model only during pretraining or fine-tuning, Mem-training allows knowledge to be collected, re-structured, and propagated at runtime, enabling self-adaptation across tasks, time horizons, and deployment environments.

In this paradigm, "training" is no longer limited to large-scale corpora but extends to dynamic knowledge accumulation via continuous interaction with users and the environment. The focus shifts from how much knowledge the model learns once to whether it can transform experience into structured memory and repeatedly retrieve and reconstruct it.MemOSserves as the system-level foundation for this paradigm, enabling end-to-end capabilities in memory generation, scheduling, fusion, and updating.

Our vision is forMemOSto become the foundational memory infrastructure for next-generation intelligent agents, with its core mission expressed through the following three pillars:

- •Memory as a System Resource: Abstract memory from a latent, internal dependency into a first-class, schedulable, and manageable resource. Build memory pathways that span agents, users, applications, and sessions, breaking down "memory silos" across platforms, significantly reducing memory management complexity, and improving the effectiveness and efficiency of memory access.
- •Evolution as a Core Capability: Enable continuous learning, structural reorganization, and task transfer throughout long-term memory usage. Build a co-evolutionary infrastructure for models and memory, allowing LLMs to self-adapt and upgrade in response to changing tasks, environments, and feedback—achieving truly sustainable, evolving intelligence.
- •Governance as the Foundation for Safety: Provide lifecycle-wide memory governance mechanisms including access control, versioning, provenance auditing, and more. Ensure controllability, traceability, and explainability of memory, laying the groundwork for secure, trustworthy, and compliant intelligent agent systems.

Memory as a System Resource: Abstract memory from a latent, internal dependency into a first-class, schedulable, and manageable resource. Build memory pathways that span agents, users, applications, and sessions, breaking down "memory silos" across platforms, significantly reducing memory management complexity, and improving the effectiveness and efficiency of memory access.

Evolution as a Core Capability: Enable continuous learning, structural reorganization, and task transfer throughout long-term memory usage. Build a co-evolutionary infrastructure for models and memory, allowing LLMs to self-adapt and upgrade in response to changing tasks, environments, and feedback—achieving truly sustainable, evolving intelligence.

Governance as the Foundation for Safety: Provide lifecycle-wide memory governance mechanisms including access control, versioning, provenance auditing, and more. Ensure controllability, traceability, and explainability of memory, laying the groundwork for secure, trustworthy, and compliant intelligent agent systems.

We believe that just as traditional operating systems laid the foundation for modern computing by unifying computation and storage management,MemOSwill elevate memory to a core system resource, forming an indispensable foundation for both general-purpose and embodied intelligent agents. This will drive a paradigm shift from reactive, perception-based systems to memory-driven, evolving agents.

### 3.2From Computer OS to Memory OS

In traditional computing systems, the operating system (OS) centrally manages key hardware resources—such as the central processing unit (CPU), memory, storage devices, and peripherals—to support efficient execution and stable operation of applications. The OS’s abstraction of resources, unified scheduling, and lifecycle governance serve as the foundation for the scalability and reliability of modern computing infrastructures.

As large language models (LLMs) scale in inference and application complexity, both internal and external memory resources—ranging from static parameter memory to runtime activation memory and dynamically retrieved explicit memory modules—exhibit increasingly dynamic and heterogeneous behavior. These memory forms are not only foundational to inference but also continuously evolve with task shifts and knowledge updates. Therefore, LLMs similarly require a systematic resource management framework akin to traditional operating systems, enabling standardized abstraction, dynamic scheduling, and autonomous lifecycle governance of memory.

MemOSproposes a design philosophy for the unified and systematic management of memory resources in LLMs, drawing extensively on mature mechanisms from traditional OS domains such as resource scheduling, interface abstraction, access control, and fault handling. Table2illustrates the mapping between classical OS components andMemOSmodules:MemOScoordinates inference and memory block scheduling via the LLM Core and MemScheduler, manages hierarchical memory through Memory Layering and MemStore, offers standardized API abstraction through MemAPI and Backend Adapter, enforces security and access governance through Memory Governance, and supports monitoring and anomaly detection through the Memory Observability framework. These modules work in concert to adapt traditional resource management principles to the evolving demands of memory in LLMs.

<table class="ltx_tabular ltx_align_middle">
<tr class="ltx_tr">
<td class="ltx_td ltx_align_left ltx_border_tt"><span class="ltx_text" style="font-size:80%;">Layer</span></td>
<td class="ltx_td ltx_align_left ltx_border_tt"><span class="ltx_text" style="font-size:80%;">OS Component</span></td>
<td class="ltx_td ltx_align_left ltx_border_tt"><span class="ltx_text" style="font-size:80%;">MemOS Module</span></td>
<td class="ltx_td ltx_align_left ltx_border_tt"><span class="ltx_text" style="font-size:80%;">Role</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_align_center ltx_border_t" colspan="4"><span class="ltx_text ltx_font_italic" style="font-size:80%;">Core Operation Layer</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_align_left ltx_border_t"><span class="ltx_text" style="font-size:80%;">Parameter Memory</span></td>
<td class="ltx_td ltx_align_left ltx_border_t"><span class="ltx_text" style="font-size:80%;">Registers / Microcode</span></td>
<td class="ltx_td ltx_align_left ltx_border_t"><span class="ltx_text" style="font-size:80%;">Parameter Memory</span></td>
<td class="ltx_td ltx_align_left ltx_border_t"><span class="ltx_text" style="font-size:80%;">Long-term ability</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_align_left"><span class="ltx_text" style="font-size:80%;">Activation Memory</span></td>
<td class="ltx_td ltx_align_left"><span class="ltx_text" style="font-size:80%;">Cache</span></td>
<td class="ltx_td ltx_align_left"><span class="ltx_text" style="font-size:80%;">Activation Memory</span></td>
<td class="ltx_td ltx_align_left"><span class="ltx_text" style="font-size:80%;">Fast working state</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_align_left"><span class="ltx_text" style="font-size:80%;">Plaintext Memory</span></td>
<td class="ltx_td ltx_align_left"><span class="ltx_text" style="font-size:80%;">I/O Buffer</span></td>
<td class="ltx_td ltx_align_left"><span class="ltx_text" style="font-size:80%;">Plaintext Memory</span></td>
<td class="ltx_td ltx_align_left"><span class="ltx_text" style="font-size:80%;">External episodes</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_align_center ltx_border_t" colspan="4"><span class="ltx_text ltx_font_italic" style="font-size:80%;">Management Layer</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_align_left ltx_border_t"><span class="ltx_text" style="font-size:80%;">Scheduling</span></td>
<td class="ltx_td ltx_align_left ltx_border_t"><span class="ltx_text" style="font-size:80%;">Scheduler</span></td>
<td class="ltx_td ltx_align_left ltx_border_t"><span class="ltx_text" style="font-size:80%;">MemScheduler</span></td>
<td class="ltx_td ltx_align_left ltx_border_t"><span class="ltx_text" style="font-size:80%;">Prioritise ops</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_align_left"><span class="ltx_text" style="font-size:80%;">Persistent Store</span></td>
<td class="ltx_td ltx_align_left"><span class="ltx_text" style="font-size:80%;">File System</span></td>
<td class="ltx_td ltx_align_left"><span class="ltx_text" style="font-size:80%;">MemVault</span></td>
<td class="ltx_td ltx_align_left"><span class="ltx_text" style="font-size:80%;">Versioned store</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_align_left"><span class="ltx_text" style="font-size:80%;">System Interface</span></td>
<td class="ltx_td ltx_align_left"><span class="ltx_text" style="font-size:80%;">System Call</span></td>
<td class="ltx_td ltx_align_left"><span class="ltx_text" style="font-size:80%;">Memory API</span></td>
<td class="ltx_td ltx_align_left"><span class="ltx_text" style="font-size:80%;">Unified access</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_align_left"><span class="ltx_text" style="font-size:80%;">Backend Driver</span></td>
<td class="ltx_td ltx_align_left"><span class="ltx_text" style="font-size:80%;">Device Driver</span></td>
<td class="ltx_td ltx_align_left"><span class="ltx_text" style="font-size:80%;">MemLoader / Dumper</span></td>
<td class="ltx_td ltx_align_left"><span class="ltx_text" style="font-size:80%;">Move memories</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_align_left"><span class="ltx_text" style="font-size:80%;">Package Deploy</span></td>
<td class="ltx_td ltx_align_left"><span class="ltx_text" style="font-size:80%;">Package Manager</span></td>
<td class="ltx_td ltx_align_left"><span class="ltx_text" style="font-size:80%;">MemStore</span></td>
<td class="ltx_td ltx_align_left"><span class="ltx_text" style="font-size:80%;">Share bundles</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_align_center ltx_border_t" colspan="4"><span class="ltx_text ltx_font_italic" style="font-size:80%;">Governance &amp; Observability</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_align_left ltx_border_t"><span class="ltx_text" style="font-size:80%;">Auth / ACLs</span></td>
<td class="ltx_td ltx_align_left ltx_border_t"><span class="ltx_text" style="font-size:80%;">Auth Module, ACLs</span></td>
<td class="ltx_td ltx_align_left ltx_border_t"><span class="ltx_text" style="font-size:80%;">MemGovernance</span></td>
<td class="ltx_td ltx_align_left ltx_border_t"><span class="ltx_text" style="font-size:80%;">Access control</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_align_left"><span class="ltx_text" style="font-size:80%;">Logging</span></td>
<td class="ltx_td ltx_align_left"><span class="ltx_text" style="font-size:80%;">Syslog</span></td>
<td class="ltx_td ltx_align_left"><span class="ltx_text" style="font-size:80%;">Audit Log</span></td>
<td class="ltx_td ltx_align_left"><span class="ltx_text" style="font-size:80%;">Audit trail</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_align_left ltx_border_bb"><span class="ltx_text" style="font-size:80%;">Fault Handling</span></td>
<td class="ltx_td ltx_align_left ltx_border_bb"><span class="ltx_text" style="font-size:80%;">Excp. Handler</span></td>
<td class="ltx_td ltx_align_left ltx_border_bb"><span class="ltx_text" style="font-size:80%;">Error Recovery</span></td>
<td class="ltx_td ltx_align_left ltx_border_bb"><span class="ltx_text" style="font-size:80%;">Error recover</span></td>
</tr>
</table>

## 4Memory Modeling inMemOS

### 4.1Types of Memory inMemOS

The concept of hierarchical memory was originally introduced in our prior work Memory3[1], which proposed a distinction between explicit and implicit memory paths in LLMs and investigated their interaction mechanisms.

Building on this foundation,MemOSsystematizes the idea by delineating three core memory types—Plaintext Memory,Activation Memory, andParameter Memory—that together reflect a full semantic evolution trajectory from perception to consolidation.

To coordinate scheduling and evolution across heterogeneous memory types,MemOSintroduces theMemCube—a unified abstraction that standardizes memory representation, lifecycle management, cross-modal fusion, and dynamic memory state transitions.
Its design is inspired by the controllable externalization proposed in Memory3, while advancing it into a composable and schedulable memory substrate suitable for intelligent agent construction.
This design forms the semantic memory backbone ofMemOS, enabling seamless integration and transformation of multiple memory types during inference.

##### Plaintext Memory

Plaintext memory refers to explicit, dynamically retrieved knowledge modules accessed via external interfaces—editable, traceable, and storable independently.
Examples include retrieved passages, structured graphs, and prompt templates.
Injected into model input, it bypasses the limitations of parameter capacity and context window size.
It enables rapid knowledge updates, task customization, and user personalization.

MemOSencapsulates plaintext memory into tunableMemCubes, with lifecycle control, access policies, and version tracking.
It supports graph-structured and multimodal memory, contextual fingerprinting, and timestamp-based loading.
Plaintext memory is not merely an external plugin.MemOSdeeply integrates it into the inference loop, enabling interaction with activation memory.
High-frequency plaintext can be transformed into activation paths, achieving dynamic externalization and internalization of knowledge.
To enhance scheduling efficiency and long-term evolvability,MemOSmanages plaintext memory in a hierarchical graph structure organized by task–concept–fact paths.
Task parsing combined with semantic similarity and topic-aware strategies enables structured query routing and prioritized retrieval.
It supports conflict detection, deduplication, versioning, and forgetting policies to maintain memory quality and evolution.

Plaintext memory is particularly suited for fact-heavy, personalized, and multi-agent tasks—serving as a core enabler of transparent and collaborative intelligence.

##### Activation Memory

Activation memory consists of intermediate states generated during inference, with the KV-cache as the central structure.
It retains key-value representations of context, enabling efficient long-range dependency modeling and recursive reasoning.
It supports instant contextual response and reusable inference pathways through cache-stable behaviors.
Other elements include hidden states (hilh^{l}_{i}) and attention weights (αi​jl\alpha^{l}_{ij}), comprising the model’s runtime semantic perception.
These are characterized as short-term, dynamic, and implicitly activated.

MemOSoffers unified scheduling and lifecycle management for activation memory.
It enables lazy loading, selective freezing, and priority-driven adjustments.
Frequent KV patterns are cached to form low-latency “instant memory paths”.
Beyond KV patterns, strategic behaviors that are repeatedly triggered can also be abstracted into persistent memory structures, such as steering vectors or semantic templates.
KV memory proves valuable in multi-turn dialogue, code assistance, and runtime safety management.
For instance, in medical agent systems, stable and frequently accessed knowledge—such as patient histories, routine diagnostic procedures, or clinical commonsense—can be abstracted into cached KV segments, enabling rapid recall and minimizing redundant decoding.
It is essential for maintaining contextual continuity, stylistic coherence, and precise response control.

##### Parameter Memory

Parameter memory refers to knowledge and capabilities encoded in the model’s fixed weights. It serves as the primary repository of long-term semantic knowledge within the model.
It encodes deep representations of linguistic structure, commonsense knowledge, and general semantics—typically instantiated as feedforward weight matrices (e.g.,WMLPlW^{l}_{\text{MLP}}) and attention key/value matrices (e.g.,WKlW^{l}_{K},WVlW^{l}_{V}).
Unlike other memory types, parameter memory is activated implicitly without retrieval or explicit context, forming the foundation for zero-shot inference, general QA, and language generation.

InMemOS, parameter memory includes both pre-trained linguistic and world knowledge and can be modularly enhanced via lightweight fine-tuning methods such as LoRA or adapters.MemOSenables distilling domain-specific knowledge into parameter blocks, loadable as “capability modules" (e.g., summarization expert, legal assistant, style generator).
While offering strong expressivity and high efficiency, parameter memory suffers from high update costs, limited customizability, and poor interpretability.
To address this,MemOSlinks parameter memory with plaintext and activation memories.
For instance, frequently used and structurally stable plaintext may be distilled into parametric form for embedded efficiency.
Conversely, outdated or inconsistent parameter memory can be backpatched by reverting to plaintext.
Parameter memory is ideal for capability-centric agents, such as legal advisors, financial auditors, technical writers, or summarizers, or as composable “capability plugins”.
Compared with frequently updated plaintext or transient activation memory, it better supports long-term, structurally stable capabilities.

### 4.2Memory Cube (MemCube) as a Core Resource

InMemOS, the foundation of a unified and structured memory management system lies in the standardized abstraction and system-level governance of heterogeneous memory resources. To this end, we propose theMemory Cube (MemCube)as a universal encapsulation unit for memory resources (see Figure6).

Memory in LLMs is highly diverse, spanning long-term knowledge embedded in model parameters, intermediate activation states generated during inference, and externally injected structured knowledge fragments (e.g., retrieved passages, knowledge graph nodes). These resources differ significantly in origin, lifecycle, representation, and scheduling method, making unified control, evolution, and governance a systemic challenge.

The design ofMemCubeaims to encapsulate all memory types as unified scheduling units, each with standard interfaces, behavioral properties, and governance strategies. EachMemCubeinstance consists of two components: theMemory Payload, which contains the semantic content, and theMetadata, which encodes identity, control, and behavioral metrics. These metadata elements serve as foundational interfaces forMemOSscheduling and governance and as central anchors for long-term system evolution, task adaptation, and security control.

The metadata of eachMemCubeis categorized into three groups:descriptive identifiers,governance attributes, andbehavioral usage indicators. Together, these enable full-spectrum memory management across structural identification, access control, and behavioral evolution. We elaborate below on their motivations, components, and system-level implications.

##### Descriptive Identifiers

define each memory block’s identity, classification, and organization. Unified memory scheduling at scale relies on precise identification of these “semantic fingerprints.”MemCubeembeds key fields such as:Timestamp, indicating creation or last update for lifecycle modeling;Origin Signature, identifying whether the memory comes from inference extraction, user input, external retrieval, or parameter finetuning; andSemantic Type, specifying its use (e.g., task prompt, fact, user preference) to support semantic composition. These jointly enable layered memory structuring and contextual navigation.

##### Governance Attributes

provide systemic controls for memory access, security, and scheduling. In dynamic, multi-user, long-running systems, default model reasoning is insufficient for robust memory governance.MemOSdefines a comprehensive rule set per memory unit, including:Access Control(read/write/share scope),Lifespan Policy(TTL or decay rules),Priority Level(for scheduling), andCompliance & Traceability(e.g., sensitivity tags, watermarks, logs). Together, they form the memory governance kernel—critical for system stability, transparency, and accountability.

##### Behavioral Usage Indicators

reflect real-time memory usage during inference, enabling “value-driven” scheduling and cross-type transformation. Unlike static labels, these runtime metrics empower adaptive orchestration of memory.

Access Patterns, such as frequency and recency, inform whether a memory is “hot” or “cold” during inference.MemOSuses this to adjust caching priority—for example, promoting high-frequency plaintext memory into fast-access layers to reduce latency.

These indicators also supportCross-Modality Memory Transformation, allowing dynamic transitions across memory types:

- •Plaintext⇒\RightarrowActivation:Frequently used plaintext memory can be pre-transformed into activation vectors or attention templates for faster decoding.
- •Plaintext/Activation⇒\RightarrowParameter:Stable knowledge across tasks can be distilled into parameter modules, internalized as efficient capability plugins.
- •Parameter⇒\RightarrowPlaintext:Cold or outdated parameters can be offloaded into external plaintext storage to increase flexibility and reduce structural overhead.

Plaintext⇒\RightarrowActivation:Frequently used plaintext memory can be pre-transformed into activation vectors or attention templates for faster decoding.

Plaintext/Activation⇒\RightarrowParameter:Stable knowledge across tasks can be distilled into parameter modules, internalized as efficient capability plugins.

Parameter⇒\RightarrowPlaintext:Cold or outdated parameters can be offloaded into external plaintext storage to increase flexibility and reduce structural overhead.

To support such transformations,MemOSintroducesPolicy-Aware Scheduling: the system dynamically adjusts a memory block’s tier and format based on usage frequency, contextual dependency, and task fit—enabling layered memory evolution.
Additionally, each memory is associated with aContextual Fingerprint, a lightweight semantic signature for fast retrieval and task alignment.
AVersion Chainlogs each memory’s modification history and derivation lineage, enabling version control, conflict resolution, and rollback.
These behavioral metrics allowMemOSto perceive the “value” of memory, forming the basis for adaptive scheduling, memory transformation, and knowledge evolution. As a result, memory becomes a self-regulating and self-evolving intelligent resource unit.
Through the coordinated design of these three metadata types,MemCubeenables structured abstraction, permissioned control, and behavior-driven evolution of heterogeneous memory resources.

## 5Architecture ofMemOS

### 5.1Overview: Three-layer Architecture ofMemOS

MemOSadopts a modular three-layer architecture to support efficient invocation, dynamic scheduling, and compliant governance of complex memory tasks (see Figure7). It consists of the Interface Layer, Operation Layer, and Infrastructure Layer, each with distinct responsibilities and collaborative interfaces—together building a unified execution and governance framework for heterogeneous memory types that enables robust intelligent agent performance across complex tasks.

##### Memory Interface Layer

The interface layer interacts with users or upstream systems and serves as the entry point for all memory operations.
It provides a standardizedMemory APIsuite that supports querying, writing, updating, transferring, and composing memory units.
All user requests are parsed by the interface layer into specific memory manipulation commands.
The built-inMemReadermodule plays a central role in this process.
It converts natural language inputs into structured memory operation chains, extracting time expressions, task intents, contextual anchors, and memory scopes.
For instance, given a request like “Summarize my meeting notes from last month,”MemReaderextracts the time range (last month), memory type (meeting notes), and output target (summary), and formulates a labeledMemoryQuerywith proper window parameters.
In multi-turn conversations,MemReaderuses context to infer omitted details, ensuring consistency in memory invocation.
This layer also performs permission checks, parameter encapsulation, and call sequence management. It coordinates withMemGovernanceto validate the compliance and traceability of every operation.

##### Memory Operation Layer

The operation layer serves as the control center ofMemOS, organizing, planning, and scheduling memory resources during inference.
Its core components includeMemOperator, which builds tag systems, semantic indexes, and graph-based topologies across heterogeneous memory types and contexts, facilitating efficient retrieval and contextual adaptation.MemSchedulerselects appropriate memory types (e.g., Plaintext, activation, parameter ) based on task intent and context, and dynamically plans invocation order and integration strategy to optimize for low latency and task relevance.MemLifecycletracks the lifecycle transitions of each memory unit—creation, activation, expiration, and reclamation—to ensure memory resource controllability and freshness.
In a multi-turn QA or complex dialogue, the operation layer first retrieves relevant memory (e.g., user preferences, past conversations, external structured documents) viaMemOperator, determines the optimal invocation path viaMemScheduler, and updates memory states usingMemLifecycle.
Thanks to this design, memory becomes a dynamic, context-aware resource rather than a static data fragment.

##### Memory Infrastructure Layer

The infrastructure layer handles storage, security, migration, and flow of memory data, serving as the foundation for reliable system execution.MemGovernanceenforces access control, retention policies, audit logging, and sensitive content handling.MemVaultmanages multiple memory repositories (e.g., user-specific, domain knowledge, shared pipelines) and provides standardized access interfaces.MemLoaderandMemDumperenable memory import/export and cross-platform synchronization.MemStoreprovides a publish-subscribe mechanism for open memory sharing among multiple agents.
In organizational QA systems, for instance, a locally updated memory entry can be validated and synchronized to a central memory hub, becoming available to authorized users.

Together, these three layers form the complete memory operation loop inMemOS—from task input to execution scheduling to governance and archival. The standard interface decoupling allows rapid iteration and extensibility, laying the foundation for multi-model, multi-task, and cross-platform memory sharing in future intelligent systems.

### 5.2Execution Path and Interaction Flow ofMemOS

The execution ofMemOSis triggered by either user interaction or automated tasks. It follows a closed-loop process through input parsing, memory scheduling, state management, and storage archiving(Figure8).

##### Prompt Input and Memory API Packaging

System execution begins with a user-issued natural language prompt or an automatically triggered task. The interface layer processes the input through the built-inMemReadermodule, which identifies task intent, time scope, topic entities, and contextual anchors to determine if memory access is involved. If so,MemReaderconverts the prompt into a structuredMemoryCall, including the caller ID, context scope, memory type, access intent, and time window. This is encapsulated into a standardizedMemory APIrequest and passed to the operation layer for execution.
For example, in a healthcare scenario, when a patient inputs, “Please retrieve my inpatient records from last year,”MemReaderidentifies the time range (last year), topic tag (diagnostic records), contextual anchor (hospitalization period), and intent (historical query), and generates a structuredMemoryCall, which proceeds to the memory retrieval and scheduling pipeline.

##### Memory Retrieval and Organization

TheMemOperatorin the operation layer uses intent and context info from theMemory APIto perform semantic matching and organize memory units. It constructs task-specific indexes (user preferences, anchors, keyword vectors) and memory graphs (temporal chains, entity relations, dependencies) to filter relevant candidates.
For instance, if a patient asks the system to reference past cases for diagnosis, the operator retrieves memory blocks with symptom keywords, treatment periods, and associated physician notes to construct a structured retrieval path.

##### Memory Scheduling and Activation

After the candidate set is identified,MemScheduleroptimizes memory selection using metrics like contextual similarity, access frequency, temporal decay, and priority tags. It dynamically computes the optimal injection strategy.
In a follow-up appointment, the system injects recent consultation summaries (activation memory), diagnosis templates (parameter memory), and lifestyle advice (plaintext memory), ensuring integrated, semantically coherent support.

##### Lifecycle Modeling and State Transitions

Scheduled memory units are passed toMemLifecyclefor state management. Each memory item transitions through five states—Generated, Activated, Merged, Archived, and Expired—based on access patterns, time decay, and task labels.
For example, in medical use, generated medication advice starts in "Generated" state. If frequently accessed, it becomes "Activated"; after repeated user confirmations, it is "Merged" into frequent-use suggestions; and eventually archived or expired if unused.

##### Storage Archiving and Access Governance

Evolved memories are archived inMemVaultand organized by user, task, or context. Archiving may be triggered by policy, user command, or scheduling, keeping frequently accessed data active and less-used data cold or long-term stored.
The archiving phase also invokesMemGovernancefor permission encapsulation and compliance checks. Each memory unit is assigned a set of access control strategies—such as Access Control List (ACL), Time-To-Live (TTL), and conditional activation policies—that determine its availability based on user roles and task context.
For example, a treatment summary may be fully visible to the care team but partially visible to the patient. After redaction and watermarking, it can be registered inMemStorefor sharing across institutions.

The full governance and archiving pipeline ensures that all memory units—across diverse modalities and agents—are handled in a structured, transparent, and traceable manner, maintaining compliance and efficiency across collaborative healthcare environments.

### 5.3Interface Layer

#### 5.3.1MemReader

InMemOS, the first step of any memory operation is interpreting natural language inputs from users or system tasks. This responsibility is handled by theMemReader, which serves as the semantic abstraction module for memory-level reasoning. It parses incoming prompts to extract key memory-related features—such as task intent, temporal scope, entity focus, memory type, and contextual anchors—and outputs a structured intermediate representation.
For example, a prompt like "Remind me what the doctor said about my medication during last year’s hospitalization" would be parsed byMemReaderinto a structured memory access plan: task intent (retrieval), time scope (last year), topic (medication guidance), and context anchor (hospitalization period). This plan is passed downstream as aMemoryCallto be processed by the memory operation layer.MemReaderalso supports prompt rewriting, coreference resolution, and dialogue memory slot filling across multi-turn interactions. It functions as both an intent recognizer and memory orchestrator, ensuring the system issues precise and traceable calls to the underlying memory infrastructure.

#### 5.3.2Memory API

The interface layer ofMemOSis built around a unified and composableMemory API, which bridges upper-level tasks with backend memory operations. All memory-related actions—including creation, updates, retrieval, and auditing—are performed via standardized APIs that ensure extensibility, composability, and governance.Provenance APIenables provenance tracking by embedding metadata into memory objects at creation or modification time. This includes event triggers, contextual state, model identifiers, and external links. Each memory is tagged with a unique provenance ID that persists throughout its lifecycle. Provenance metadata supports explainability, debugging, access control, and memory lineage tracing.Update APIsupports mutation operations such as append, merge, or overwrite. It is version-aware, allowing snapshots and label-based differential writes. Typical use cases include task result logging, user correction, and fine-grained memory consolidation. When paired withMemLifecycle, update operations can trigger state transitions and index refreshes.LogQuery APIallows structured access to memory access logs and execution traces. It supports filtering by timestamp, caller identity, memory type, and operation kind. It is essential for debugging, hotspot analysis, auditing, and governance enforcement. For instance, developers can investigate memory usage that led to faulty responses, or validate whether specific memories were invoked.
AllMemory APIcalls useMemoryCubeas their parameter carrier and response format. They support transactional safety, structured status reporting, and are governed byMemGovernance, which enforces access control based on users, roles, models, and tasks.

#### 5.3.3Memory Pipeline

To support complex workflows in enterprise and multi-agent settings,MemOSoffers a pipeline-style composition mechanism for chaining memory operations. Developers or agent systems can define a sequence of memory actions—e.g., retrieve → augment → update → archive—and execute them as a cohesive pipeline.
Each pipeline step operates on a sharedMemoryCubeobject, which carries input-output state, metadata, and intermediate artifacts. For example, a medical assistant might define a pipeline that (1) retrieves past medication notes viaLogQuery, (2) adds doctor’s latest instructions viaUpdate, (3) tags the memory with a new provenance entry, and (4) archives it post-consultation.
Pipelines support transactional consistency, rollback, and fault isolation. They can be defined declaratively through a domain-specific language (DSL), or constructed programmatically. For agent orchestration,MemSchedulerinterprets dependencies across steps and coordinates scheduling. Pipeline templates can be reused across agents—e.g., for follow-up generation in customer support, or for diagnosis tracking in clinical triage.

By enabling compositional memory flows,MemOSempowers developers to model higher-level cognition patterns, task-specific knowledge shaping, and auditable memory workflows.

### 5.4Operation Layer

#### 5.4.1MemOperator

InMemOS, efficient memory organization and accurate retrieval are fundamental to enabling intelligent behavior generation, contextual reasoning, and knowledge reuse. TheMemOperatormodule fulfills this role by structuring memory content both logically and semantically. It incorporates tag-based annotation, graph-based linking, and hierarchical abstraction to support multi-perspective memory modeling. Simultaneously, it provides unified interfaces for hybrid retrieval, serving diverse agents across tasks, models, and user contexts.

##### Multi-perspective Memory Structuring

MemOSemploys three complementary mechanisms for organizing memory. First, a flexible tagging system allows each memory unit to be annotated with metadata such as topic, source, credibility, and sentiment, supporting both user-defined and model-predicted labels. Second, a knowledge-graph structure treats memory as nodes connected via semantic edges, enabling traversable relations across memory items. Third, a semantic layering scheme segments memory into private, shared, and global layers, facilitating memory isolation and coordinated access across tasks and roles.

##### Hybrid Retrieval and Dynamic Dispatch

TheMemOperatormodule supports hybrid retrieval mechanisms that combine symbolic and semantic strategies. Structured retrieval applies rule-based filtering over tags, time spans, Boolean conditions, and access control policies. Semantic retrieval uses embedding-based vector representations to identify contextually relevant memory units via similarity search. These two mechanisms can be composed into complex query expressions—such as tag filters combined with semantic ranking—to serve applications like multi-turn dialogue, question answering, or knowledge integration.

##### Pipeline Coupling and Caching Strategy

Retrieved memory units are passed downstream as inputs to execution pipelines, tightly coupled with theMemory APIandMemoryCubemodules. To minimize latency,MemOSimplements a local index caching strategy whereby frequently accessed memory is automatically migrated to high-speed intermediate storage. Cache invalidation is managed by heuristics based on usage frequency and contextual drift, with theMemSchedulermodule overseeing refresh operations in a dynamic, workload-aware manner.

##### Task-Aligned Memory Routing

To address the complexity of real-world tasks,MemOSemploys a task-aligned routing mechanism that resolves memory navigation paths based on hierarchical semantic goals. User inputs are decomposed into a topic–concept–fact structure, forming a three-layered task schema. TheMemoryPathResolvercomponent then formulates a retrieval strategy that answers three key questions: what to search, where to search, and in what order. This structured approach enhances interpretability, scheduling relevance, and alignment between memory selection and task intent.

#### 5.4.2MemScheduler

MemScheduleris the central memory dispatcher of theMemOSoperation layer. Its purpose goes beyond simply "retrieving" stored memories; it dynamically transforms and loads them into the runtime context based on task semantics, call frequency, and content stability.
Relying on the three memory types defined inMemCube—Activation Memory (KV-Cache), Plaintext Memory, and Parameter Memory—MemSchedulersupports classification, transformation, and hierarchical dispatch to deliver adaptive, high-performance memory operations.

##### Type-Aware Transformation and Loading Mechanism

During memory scheduling,MemScheduleranalyzes task semantics, window size, and resource constraints to determine the best-fit memory type.
Stable, frequently accessed content is transformed intoActivation Memoryfor KV caching, minimizing prefill latency.
Abstract rules and reusable patterns are encoded asParameter Memory—e.g., via distillation or adapters embedded into model weights.
Time-sensitive or session-specific knowledge is preserved asPlaintext Memory, inserted into the prompt as raw text.
Adaptive triggers guide the loading process.
For coherence-heavy tasks like multi-turn dialogue, the scheduler favors KV-cache recall.
For procedural or expert-driven flows, parametric modules take precedence.
For on-demand factual queries, plain memory is retrieved and contextualized.
All decisions are logged toMemCubeand coordinated withMemOperator’s memory structure to maintain traceability and interpretability.

##### Cross-Type Conversion and Migration

To maintain long-term performance and adaptive memory utilization,MemSchedulersupports cross-type memory migration.
For example, plain memories frequently recalled across sessions may be promoted to Activation Memory (KV cache).
Stable templates used repeatedly can be distilled into parameter Memory.
Conversely, underutilized KV entries may be downgraded to Plain Memory and archived to cold storage.
This type-shifting mechanism ensures memory units evolve toward their optimal invocation form while conserving system resources.

##### Execution Path Integration and Governance

MemSchedulerintegrates upstream withMemReaderand theMemory APIto parse structured calls and semantic goals.
Downstream, it collaborates with model execution paths to determine how and where to inject memory.
Scheduling logic is optimized in real time, guided by task type, model load, cache hit rates, and access history.
All dispatch actions are governed byMemGovernance, which enforces user-role boundaries, rate limits, and lifecycle policies.
This ensures proper memory isolation and secure usage across users, models, and tasks, while maintaining an auditable record of every memory interaction.

#### 5.4.3MemLifecycle

InMemOS, each memory object is treated as a dynamic entity with evolving states, managed centrally by theMemLifecyclemodule.
The system models memory as a finite state machine, cycling through four key states: Generated, Activated, Merged, and Archived.
This framework supports semantic evolution, dynamic memory management, and stable, controlled resource scheduling at the storage layer.

##### State Modeling and Evolution Logic

State transitions are triggered by a combination of system policies and user actions.
For instance, in a smart meeting assistant, an auto-generated summary is initially labeled as “Generated”.
If that summary is later referenced in a follow-up task—like agenda tracking or meeting comparison—it transitions into the “Activated” state.
When the user adds supplementary data, or the system detects semantic overlap with historical memory, these entries are consolidated into a new version and marked as “Merged”.
If a memory is no longer accessed for a prolonged period, it is demoted to the “Archived” state and moved to cold storage.
Transitions can be explicitly initiated by user actions, or implicitly driven by system heuristics such as recency, contextual salience, or successful merge events.

##### Time Machine and Freezing Mechanism

To ensure long-term consistency and recovery,MemOSoffers a “Time Machine” capability that snapshots memory states and supports historical rollbacks.
Users or developers can invoke this feature to restore an archived or merged memory back to a specific version, re-enabling its use in inference and context injection.
This is critical for scenarios such as detecting model forgetting, handling user retractions, or conducting counterfactual simulations.
In a policy collaboration platform, a user might unarchive an old clause to perform “what-if” simulations, without impacting the canonical frozen version and its audit trail.MemOSalso supports a “Frozen” state for critical memories—like legal agreements or standard guidelines—where updates are disabled and full modification histories are retained for auditing, compliance, or education.

##### Scheduling and Storage Integration Strategy

Lifecycle states directly influence scheduling priority and storage allocation strategies.
“Activated” memories are preferentially cached in local memory or fast-accessMemoryCubeinstances for low-latency retrieval.
“Archived” or “Frozen” memories are offloaded toMemVault, a cold storage layer optimized for durability over speed.
Based on lifecycle rules, the system can batch-trigger operations like cleanup, compression, or migration to balance call availability with efficient resource usage.

### 5.5Infrastructure Layer

#### 5.5.1MemGovernance

MemGovernanceis the core module inMemOSresponsible for memory access control, compliance enforcement, and auditability.
As memory systems evolve toward multi-user collaboration and long-horizon task reasoning,MemGovernanceensures that memory remains secure, interpretable, and controllable throughout its sharing, transfer, and inference processes.

It establishes a ternary permission model involving the user identity, the memory object, and the calling context, supporting private, shared, and read-only access policies.
Each memory request undergoes identity authentication and contextual validation to prevent unauthorized access.
For example, in clinical settings, only physicians may access a patient’s diagnostic records; in enterprise systems, only authorized managers can retrieve archived policy documents.

It manages memory lifecycle policies such as time-to-live (TTL) enforcement and access-frequency-based garbage collection or archiving of inactive items.
It also tracks memory usage heat to monitor high-traffic memory segments.
Its privacy control subsystem includes sensitive content detection, automatic redaction, and access logging to ensure personal and behavioral data remain secure.

All memory objects carry full provenance metadata, including creation source, invocation lineage, and mutation logs.
Generated content can be watermarked semantically and tagged with behavioral fingerprints, allowing attribution and copyright tracking in multi-platform scenarios.

The module also exposes audit interfaces for integration with enterprise compliance systems, supporting export of access logs and permission revision reports.
These features support regulatory compliance in high-stakes environments such as healthcare and finance.

#### 5.5.2MemVault

MemVaultis the central memory storage and routing infrastructure inMemOS, responsible for managing and serving diverse categories of memory.
Memory is organized into namespaces such as user-private stores, expert knowledge bases, industry-shared repositories, contextual memory pools, and pipeline-aligned caches.
Each is assigned a dedicated namespace and path structure to support efficient lookup and access control.

To support heterogeneous backends,MemVaultinterfaces with vector stores, relational databases, and blob storage through a unifiedMemoryAdapterabstraction.
This allows API-level consistency for querying, writing, and syncing memory regardless of backend heterogeneity.
Stores may be configured as read-only caches or write-enabled repositories, depending on latency or learning objectives.

At runtime,MemVaultworks in concert withMemSchedulerandMemLifecycleto dynamically load memory based on access history, contextual relevance, and memory state.
It supports tag-based, semantic, and full-text loading patterns, and triggers migration for hot memory to fast storage or cold data to archival zones.
This architecture is vital for multi-model collaboration, domain-level knowledge fusion, and consistency in multi-turn dialogue—forming the knowledge backbone for scalable intelligent systems.

#### 5.5.3MemLoader & MemDumper

MemLoaderandMemDumperform a bi-directional channel for memory migration across platforms inMemOS.
They support injection, export, and synchronization of structured units likeMemoryCube.
This capability is essential for system handover, edge-cloud integration, and knowledge continuity across distributed agents.

During ingestion,MemLoaderaccepts memory from local caches, third-party systems, or archives and maps it to target stores.
It auto-fills provenance metadata, tagging, and lifecycle status to ensure governance readiness.

MemDumperexports selected memory in portable formats with permission metadata, redacted fields, and access logs.
Both components support periodic and event-driven updates, such as automatic export upon tag activation.
The migration process is governed byMemGovernanceto validate policies, trace operations, and isolate sensitive data.
For instance, a mobile device may export patient interaction logs to the cloud, which remote agents later load to preserve task context.

#### 5.5.4MemStore

MemStoreis the open-access interface inMemOSthat enables controlled publishing, subscription, and distribution of memory units.
It supports memory exchange between models, institutions, and even industry-wide networks.

Users may declare memory as publishable and define visibility, usage conditions, and access control rules.
Each shared unit carries unique IDs and provenance metadata;MemGovernanceensures masking, watermarking, and policy validation during dissemination.

MemStoreenables both push and pull models of memory exchange.
Consumers can define subscriptions using tags or semantic filters, and the system delivers matched updates proactively.
Licensed memory assets can enforce contract-bound access frequencies and expiry policies.
All access is logged with invocation traces to support audit and accountability.

For example, a hospital may publish de-identified diagnostic records for remote triage agents, with every call validated for context and provenance.

## 6Evaluation

To systematically evaluate the capabilities ofMemOS, we conduct both holistic and component-level experiments.
We begin by benchmarking the full system on the LOCOMO benchmark suite to assess its performance in memory-intensive reasoning tasks, comparing against several state-of-the-art baselines.
In addition, we present targeted evaluations of key architectural subsystems, including multi-perspective memory organization, hybrid semantic retrieval, task-aligned scheduling, and KV-based activation memory injection. These experiments assess the individual effectiveness of each component and its contribution to overall system performance.

### 6.1End-to-End Evaluation on LOCOMO

<table class="ltx_tabular ltx_align_middle">
<tr class="ltx_tr">
<td class="ltx_td ltx_align_left ltx_border_r ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">Category</span></td>
<td class="ltx_td ltx_align_left ltx_border_r ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">Method</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;">
<table class="ltx_tabular ltx_align_middle">
<tr class="ltx_tr">
<td class="ltx_td ltx_nopad_r ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">Chunk /</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_nopad_r ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">Mem Tok</span></td>
</tr>
</table>
</td>
<td class="ltx_td ltx_align_center ltx_border_r ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">Top-K</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">LLMJudge Score</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">F1</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">RL</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">B1</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">B2</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">METEOR</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">BERT-F1</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">Sim</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"></td>
<td class="ltx_td ltx_align_left ltx_border_r ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">langmem</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">165</span></td>
<td class="ltx_td ltx_align_center ltx_border_r ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">-</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">68.21±0.06</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">41.72</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">44.80</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">35.61</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">24.73</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">36.42</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">43.77</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;">
<span class="ltx_ERROR undefined">\ul</span><span class="ltx_text" style="font-size:70%;">76.25</span>
</td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"></td>
<td class="ltx_td ltx_align_left ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">zep</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">2320</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">20</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">50.42±0.29</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">32.49</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">35.07</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">27.38</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">18.81</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">28.49</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">35.26</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">66.95</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"></td>
<td class="ltx_td ltx_align_left ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">openai</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">4141</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">-</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">61.83±0.10</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">36.96</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">41.45</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">30.72</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">22.02</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">35.39</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">40.56</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">69.84</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"></td>
<td class="ltx_td ltx_align_left ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">mem0</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">1176</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">20</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;">
<span class="ltx_ERROR undefined">\ul</span><span class="ltx_text" style="font-size:70%;">73.33±0.20</span>
</td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text ltx_font_bold" style="font-size:70%;">47.26</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text ltx_font_bold" style="font-size:70%;">51.44</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text ltx_font_bold" style="font-size:70%;">40.34</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text ltx_font_bold" style="font-size:70%;">30.02</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;">
<span class="ltx_ERROR undefined">\ul</span><span class="ltx_text" style="font-size:70%;">43.96</span>
</td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text ltx_font_bold" style="font-size:70%;">48.53</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text ltx_font_bold" style="font-size:70%;">76.56</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_align_left ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">
<span class="ltx_tabular ltx_align_middle">
<span class="ltx_tr">
<span class="ltx_td ltx_nopad_r ltx_align_left" style="padding-top:1.2pt;padding-bottom:1.2pt;">single</span></span>
<span class="ltx_tr">
<span class="ltx_td ltx_nopad_r ltx_align_left" style="padding-top:1.2pt;padding-bottom:1.2pt;">hop</span></span>
</span></span></td>
<td class="ltx_td ltx_align_left ltx_border_r" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">memos-0630</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">1600</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">20</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text ltx_font_bold" style="font-size:70%;background-color:#EFEFEF;">78.44±0.11</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;">
<span class="ltx_ERROR undefined">\ul</span><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">45.55</span>
</td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;">
<span class="ltx_ERROR undefined">\ul</span><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">51.00</span>
</td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;">
<span class="ltx_ERROR undefined">\ul</span><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">38.32</span>
</td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;">
<span class="ltx_ERROR undefined">\ul</span><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">28.32</span>
</td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text ltx_font_bold" style="font-size:70%;background-color:#EFEFEF;">44.46</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;">
<span class="ltx_ERROR undefined">\ul</span><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">47.53</span>
</td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">74.70</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"></td>
<td class="ltx_td ltx_align_left ltx_border_r ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">langmem</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">185</span></td>
<td class="ltx_td ltx_align_center ltx_border_r ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">-</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">56.74±0.29</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text ltx_font_bold" style="font-size:70%;">36.03</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text ltx_font_bold" style="font-size:70%;">36.32</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text ltx_font_bold" style="font-size:70%;">27.22</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text ltx_font_bold" style="font-size:70%;">17.03</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;">
<span class="ltx_ERROR undefined">\ul</span><span class="ltx_text" style="font-size:70%;">29.14</span>
</td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;">
<span class="ltx_ERROR undefined">\ul</span><span class="ltx_text" style="font-size:70%;">33.03</span>
</td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text ltx_font_bold" style="font-size:70%;">73.05</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"></td>
<td class="ltx_td ltx_align_left ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">zep</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">2351</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">20</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">42.20±0.77</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">23.14</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">24.63</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">14.96</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">8.49</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">17.38</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">25.15</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">64.26</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"></td>
<td class="ltx_td ltx_align_left ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">openai</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">3924</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">-</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;">
<span class="ltx_ERROR undefined">\ul</span><span class="ltx_text" style="font-size:70%;">60.28±0.00</span>
</td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">33.10</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">35.36</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">23.84</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">15.36</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">27.25</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">32.36</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">68.82</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"></td>
<td class="ltx_td ltx_align_left ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">mem0</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">1163</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">20</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">58.75±0.44</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">35.24</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">34.87</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">25.91</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">16.55</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">27.90</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">32.65</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;">
<span class="ltx_ERROR undefined">\ul</span><span class="ltx_text" style="font-size:70%;">70.71</span>
</td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_align_left ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">
<span class="ltx_tabular ltx_align_middle">
<span class="ltx_tr">
<span class="ltx_td ltx_nopad_r ltx_align_left" style="padding-top:1.2pt;padding-bottom:1.2pt;">multi</span></span>
<span class="ltx_tr">
<span class="ltx_td ltx_nopad_r ltx_align_left" style="padding-top:1.2pt;padding-bottom:1.2pt;">hop</span></span>
</span></span></td>
<td class="ltx_td ltx_align_left ltx_border_r" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">memos-0630</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">1528</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">20</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text ltx_font_bold" style="font-size:70%;background-color:#EFEFEF;">64.30±0.44</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;">
<span class="ltx_ERROR undefined">\ul</span><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">35.57</span>
</td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;">
<span class="ltx_ERROR undefined">\ul</span><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">36.25</span>
</td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;">
<span class="ltx_ERROR undefined">\ul</span><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">26.71</span>
</td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;">
<span class="ltx_ERROR undefined">\ul</span><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">16.59</span>
</td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text ltx_font_bold" style="font-size:70%;background-color:#EFEFEF;">29.42</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text ltx_font_bold" style="font-size:70%;background-color:#EFEFEF;">33.85</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">69.60</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"></td>
<td class="ltx_td ltx_align_left ltx_border_r ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">langmem</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">209</span></td>
<td class="ltx_td ltx_align_center ltx_border_r ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">-</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;">
<span class="ltx_ERROR undefined">\ul</span><span class="ltx_text" style="font-size:70%;">49.65±1.30</span>
</td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text ltx_font_bold" style="font-size:70%;">29.79</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;">
<span class="ltx_ERROR undefined">\ul</span><span class="ltx_text" style="font-size:70%;">30.54</span>
</td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text ltx_font_bold" style="font-size:70%;">23.17</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;">
<span class="ltx_ERROR undefined">\ul</span><span class="ltx_text" style="font-size:70%;">11.72</span>
</td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;">
<span class="ltx_ERROR undefined">\ul</span><span class="ltx_text" style="font-size:70%;">21.03</span>
</td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text ltx_font_bold" style="font-size:70%;">32.27</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text ltx_font_bold" style="font-size:70%;">67.34</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"></td>
<td class="ltx_td ltx_align_left ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">zep</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">2276</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">20</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">38.19±0.49</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">19.76</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">20.62</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">13.17</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">6.18</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">14.20</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">21.07</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">58.59</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"></td>
<td class="ltx_td ltx_align_left ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">openai</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">4071</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">-</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">32.99±1.30</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">17.19</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">15.88</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">11.04</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">5.23</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">12.05</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">19.37</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">57.53</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"></td>
<td class="ltx_td ltx_align_left ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">mem0</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">1141</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">20</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">45.83±0.00</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">27.80</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">28.67</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">20.01</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">10.59</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">20.33</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">28.38</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;">
<span class="ltx_ERROR undefined">\ul</span><span class="ltx_text" style="font-size:70%;">63.74</span>
</td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_align_left ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">
<span class="ltx_tabular ltx_align_middle">
<span class="ltx_tr">
<span class="ltx_td ltx_nopad_r ltx_align_left" style="padding-top:1.2pt;padding-bottom:1.2pt;">open</span></span>
<span class="ltx_tr">
<span class="ltx_td ltx_nopad_r ltx_align_left" style="padding-top:1.2pt;padding-bottom:1.2pt;">domain</span></span>
</span></span></td>
<td class="ltx_td ltx_align_left ltx_border_r" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">memos-0630</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">1511</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">20</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text ltx_font_bold" style="font-size:70%;background-color:#EFEFEF;">55.21±0.00</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;">
<span class="ltx_ERROR undefined">\ul</span><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">29.64</span>
</td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text ltx_font_bold" style="font-size:70%;background-color:#EFEFEF;">31.54</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;">
<span class="ltx_ERROR undefined">\ul</span><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">22.40</span>
</td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text ltx_font_bold" style="font-size:70%;background-color:#EFEFEF;">11.78</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text ltx_font_bold" style="font-size:70%;background-color:#EFEFEF;">23.74</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;">
<span class="ltx_ERROR undefined">\ul</span><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">30.36</span>
</td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">63.06</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"></td>
<td class="ltx_td ltx_align_left ltx_border_r ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">langmem</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">134</span></td>
<td class="ltx_td ltx_align_center ltx_border_r ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">-</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">24.09±0.39</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">38.10</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">38.33</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">32.23</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">18.81</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">27.55</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;">
<span class="ltx_ERROR undefined">\ul</span><span class="ltx_text" style="font-size:70%;">48.30</span>
</td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">74.57</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"></td>
<td class="ltx_td ltx_align_left ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">zep</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">2295</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">20</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">19.11±0.29</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">17.59</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">19.03</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">14.57</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">8.11</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">13.81</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">17.59</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">59.38</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"></td>
<td class="ltx_td ltx_align_left ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">openai</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">4048</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">-</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">28.25±0.59</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">23.90</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">24.47</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">18.25</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">11.87</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">19.35</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">23.11</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">59.53</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"></td>
<td class="ltx_td ltx_align_left ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">mem0</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">1173</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">20</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;">
<span class="ltx_ERROR undefined">\ul</span><span class="ltx_text" style="font-size:70%;">52.34±0.25</span>
</td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;">
<span class="ltx_ERROR undefined">\ul</span><span class="ltx_text" style="font-size:70%;">45.40</span>
</td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;">
<span class="ltx_ERROR undefined">\ul</span><span class="ltx_text" style="font-size:70%;">46.90</span>
</td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;">
<span class="ltx_ERROR undefined">\ul</span><span class="ltx_text" style="font-size:70%;">38.15</span>
</td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;">
<span class="ltx_ERROR undefined">\ul</span><span class="ltx_text" style="font-size:70%;">22.27</span>
</td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;">
<span class="ltx_ERROR undefined">\ul</span><span class="ltx_text" style="font-size:70%;">34.60</span>
</td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">44.59</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;">
<span class="ltx_ERROR undefined">\ul</span><span class="ltx_text" style="font-size:70%;">76.15</span>
</td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_align_left ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">
<span class="ltx_tabular ltx_align_middle">
<span class="ltx_tr">
<span class="ltx_td ltx_nopad_r ltx_align_left" style="padding-top:1.2pt;padding-bottom:1.2pt;">temporal</span></span>
<span class="ltx_tr">
<span class="ltx_td ltx_nopad_r ltx_align_left" style="padding-top:1.2pt;padding-bottom:1.2pt;">reasoning</span></span>
</span></span></td>
<td class="ltx_td ltx_align_left ltx_border_r" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">memos-0630</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">1655</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">20</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text ltx_font_bold" style="font-size:70%;background-color:#EFEFEF;">73.21±0.25</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text ltx_font_bold" style="font-size:70%;background-color:#EFEFEF;">53.67</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text ltx_font_bold" style="font-size:70%;background-color:#EFEFEF;">53.69</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text ltx_font_bold" style="font-size:70%;background-color:#EFEFEF;">46.37</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text ltx_font_bold" style="font-size:70%;background-color:#EFEFEF;">29.69</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text ltx_font_bold" style="font-size:70%;background-color:#EFEFEF;">43.45</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text ltx_font_bold" style="font-size:70%;background-color:#EFEFEF;">48.48</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text ltx_font_bold" style="font-size:70%;background-color:#EFEFEF;">76.97</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"></td>
<td class="ltx_td ltx_align_left ltx_border_r ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">langmem</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">165</span></td>
<td class="ltx_td ltx_align_center ltx_border_r ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">-</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">55.76±0.16</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">39.18</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">41.01</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">32.59</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">21.27</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">32.28</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">42.03</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text ltx_font_bold" style="font-size:70%;">74.76</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"></td>
<td class="ltx_td ltx_align_left ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">zep</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">2318</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">20</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">41.62±0.21</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">26.88</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">28.91</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">21.55</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">13.90</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">22.51</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">28.84</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">64.36</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"></td>
<td class="ltx_td ltx_align_left ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">openai</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">4077</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">-</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">52.75±0.08</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">32.30</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">35.20</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">25.64</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">17.64</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">29.10</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">34.10</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">66.74</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"></td>
<td class="ltx_td ltx_align_left ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">mem0</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">1171</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">20</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;">
<span class="ltx_ERROR undefined">\ul</span><span class="ltx_text" style="font-size:70%;">64.57±0.06</span>
</td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;">
<span class="ltx_ERROR undefined">\ul</span><span class="ltx_text" style="font-size:70%;">43.46</span>
</td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;">
<span class="ltx_ERROR undefined">\ul</span><span class="ltx_text" style="font-size:70%;">46.04</span>
</td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;">
<span class="ltx_ERROR undefined">\ul</span><span class="ltx_text" style="font-size:70%;">35.97</span>
</td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;">
<span class="ltx_ERROR undefined">\ul</span><span class="ltx_text" style="font-size:70%;">24.72</span>
</td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;">
<span class="ltx_ERROR undefined">\ul</span><span class="ltx_text" style="font-size:70%;">37.60</span>
</td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;">
<span class="ltx_ERROR undefined">\ul</span><span class="ltx_text" style="font-size:70%;">43.54</span>
</td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;">
<span class="ltx_ERROR undefined">\ul</span><span class="ltx_text" style="font-size:70%;">74.61</span>
</td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_align_left ltx_border_b ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">overall</span></td>
<td class="ltx_td ltx_align_left ltx_border_b ltx_border_r" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">memos-0630</span></td>
<td class="ltx_td ltx_align_center ltx_border_b" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">1593</span></td>
<td class="ltx_td ltx_align_center ltx_border_b ltx_border_r" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">20</span></td>
<td class="ltx_td ltx_align_center ltx_border_b" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text ltx_font_bold" style="font-size:70%;background-color:#EFEFEF;">73.31±0.05</span></td>
<td class="ltx_td ltx_align_center ltx_border_b" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text ltx_font_bold" style="font-size:70%;background-color:#EFEFEF;">44.42</span></td>
<td class="ltx_td ltx_align_center ltx_border_b" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text ltx_font_bold" style="font-size:70%;background-color:#EFEFEF;">47.65</span></td>
<td class="ltx_td ltx_align_center ltx_border_b" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text ltx_font_bold" style="font-size:70%;background-color:#EFEFEF;">36.88</span></td>
<td class="ltx_td ltx_align_center ltx_border_b" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text ltx_font_bold" style="font-size:70%;background-color:#EFEFEF;">25.43</span></td>
<td class="ltx_td ltx_align_center ltx_border_b" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text ltx_font_bold" style="font-size:70%;background-color:#EFEFEF;">40.20</span></td>
<td class="ltx_td ltx_align_center ltx_border_b" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text ltx_font_bold" style="font-size:70%;background-color:#EFEFEF;">44.15</span></td>
<td class="ltx_td ltx_align_center ltx_border_b" style="background-color:#EFEFEF;padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">73.51</span></td>
</tr>
</table>

We evaluateMemOSagainst a diverse set of strong baselines, each representing a distinct memory system design paradigm. Specifically,LangMemapplies hierarchical semantic retrieval over flat textual history;Zepintegrates time-aware knowledge graphs with structured query resolution;OpenAI-Memoryrepresents a commercial, closed-source memory module with opaque internal logic; andMem0implements slot-based long-term memory with top-k semantic search. To ensure architectural parity, all methods are implemented over the same LLM backbone (GPT-4o-mini).

All experiments are conducted on an 80GB H800 GPU under identical hardware and software configurations. For memory-augmented systems, we vary the number of retrieved items (Top-K) and chunk granularity (Chunk / Mem Tok), which controls the length of each retrieved memory segment. The configuration for each method is selected based on its best validation performance, ensuring a fair and optimized comparison across all metrics.

We report LLM-judge scores as the primary evaluation metric (Table3), supported by standard generation quality indicators including F1, ROUGE-L (RL), BLEU-1/2 (B1/B2), METEOR, and BERTScore-F1 (BERT-F1), as well as cosine similarity (Sim) computed over semantic embeddings.

Overall,MemOSachieves the best average performance across all task categories, consistently outperforming strong baselines such as mem0, openai-memory, and zep.
Across all sub-tasks in the LOCOMO benchmark, MemOS ranks among the top performers, maintaining first or second place in nearly every category. It demonstrates clear advantages in multi-hop and temporal reasoning, where long-range memory and contextual integration are especially critical. Beyond LLM-judge scores, MemOS also delivers strong generation quality across F1, ROUGE-L, and BLEU, particularly in long-form completeness and stylistic consistency. At the representation level, it maintains tight semantic alignment with reference answers, as indicated by consistently high cosine similarity in semantic embeddings across tasks.

To better understand the impact of memory configuration, we conduct an ablation study by varying chunk sizes and Top-K retrieval depth.
As shown in Figure9,MemOSdemonstrates stable and strong performance across all LOCOMO sub-tasks, with performance steadily improving as memory capacity increases—particularly for multi-hop and temporal reasoning tasks that demand long-range retrieval and contextual integration.
In addition to higher LLM-Judge scores, generation metrics such as F1, ROUGE-L, and BLEU also benefit from memory expansion. Cosine similarity remains consistently high, indicating stable semantic alignment even with deeper retrieval.

These results collectively validate the effectiveness ofMemOS’s architectural innovations—particularly its hybrid semantic retrieval and memory-centric design—which enable accurate, fluent, and contextually aligned responses under long-horizon constraints.

<table class="ltx_tabular ltx_align_middle">
<tr class="ltx_tr">
<td class="ltx_td ltx_align_left ltx_border_r ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">Method</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;">
<table class="ltx_tabular ltx_align_middle">
<tr class="ltx_tr">
<td class="ltx_td ltx_nopad_r ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">Chunk /</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_nopad_r ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">Mem Tok</span></td>
</tr>
</table>
</td>
<td class="ltx_td ltx_align_center ltx_border_r ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">Top-K</span></td>
<td class="ltx_td ltx_align_center ltx_border_r ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">LLMJudge Scores</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" colspan="2" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">search duration (ms)</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" colspan="2" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">total duration (ms)</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"></td>
<td class="ltx_td" style="padding-top:1.2pt;padding-bottom:1.2pt;"></td>
<td class="ltx_td ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"></td>
<td class="ltx_td ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">P50</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">P95</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">P50</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">P95</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"></td>
<td class="ltx_td ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"></td>
<td class="ltx_td ltx_align_center ltx_border_r ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">1</span></td>
<td class="ltx_td ltx_align_center ltx_border_r ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">44.61±0.05</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">516</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">800</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">1306</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">1963</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">128</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">2</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">55.71±0.05</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">523</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">850</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">1325</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">2040</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"></td>
<td class="ltx_td ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"></td>
<td class="ltx_td ltx_align_center ltx_border_r ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">1</span></td>
<td class="ltx_td ltx_align_center ltx_border_r ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">45.13±0.19</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">553</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">1288</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">1438</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">2606</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">256</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">2</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">56.54±0.25</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">575</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">1371</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">1496</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">2843</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"></td>
<td class="ltx_td ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"></td>
<td class="ltx_td ltx_align_center ltx_border_r ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">1</span></td>
<td class="ltx_td ltx_align_center ltx_border_r ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">41.36±0.24</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">481</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">1979</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">1331</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">4129</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">512</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">2</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">54.29±0.19</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">482</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">2070</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">1351</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">4252</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"></td>
<td class="ltx_td ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"></td>
<td class="ltx_td ltx_align_center ltx_border_r ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">1</span></td>
<td class="ltx_td ltx_align_center ltx_border_r ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">36.04±0.09</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">1008</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">2436</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">2061</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">4443</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">1024</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">2</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">46.97±0.03</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">468</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">808</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">1466</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">2193</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"></td>
<td class="ltx_td ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"></td>
<td class="ltx_td ltx_align_center ltx_border_r ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">1</span></td>
<td class="ltx_td ltx_align_center ltx_border_r ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">33.70±0.05</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">460</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">986</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">1387</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">2311</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">2048</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">2</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">44.81±0.05</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">456</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">903</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">1476</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">2479</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"></td>
<td class="ltx_td ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"></td>
<td class="ltx_td ltx_align_center ltx_border_r ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">1</span></td>
<td class="ltx_td ltx_align_center ltx_border_r ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">33.9±0.05</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">449</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">715</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">1432</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">2324</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">4096</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">2</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">48.53±0.13</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">459</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">1055</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">1606</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">3324</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"></td>
<td class="ltx_td ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"></td>
<td class="ltx_td ltx_align_center ltx_border_r ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">1</span></td>
<td class="ltx_td ltx_align_center ltx_border_r ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">41.45±0.17</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">692</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">1733</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">2016</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">5037</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_align_left ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">RAG</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">8192</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">2</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">58.20±0.08</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">688</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">1773</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">2335</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">6008</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_align_left ltx_border_r ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">Full-Context</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">22636</span></td>
<td class="ltx_td ltx_align_center ltx_border_r ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">-</span></td>
<td class="ltx_td ltx_align_center ltx_border_r ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">71.58±0.08</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">-</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">-</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">2339</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">7016</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_align_left ltx_border_r ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">langmem</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">165</span></td>
<td class="ltx_td ltx_align_center ltx_border_r ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">-</span></td>
<td class="ltx_td ltx_align_center ltx_border_r ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">55.76±0.16</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">17226</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">29344</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">18025</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">30139</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_align_left ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">zep</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">2318</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">20</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">41.62±0.21</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">1364</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">1901</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">9777</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">20197</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_align_left ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">openai</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">4077</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">-</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">52.75±0.08</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">-</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">-</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">1184</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">2240</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_align_left ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">mem0</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">1171</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">20</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">64.57±0.06</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">1297</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">1416</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">4906</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;">5962</span></td>
</tr>
<tr class="ltx_tr" style="background-color:#EFEFEF;">
<td class="ltx_td ltx_align_left ltx_border_b ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">memos-0630</span></td>
<td class="ltx_td ltx_align_center ltx_border_b" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">1593</span></td>
<td class="ltx_td ltx_align_center ltx_border_b ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">20</span></td>
<td class="ltx_td ltx_align_center ltx_border_b ltx_border_r" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text ltx_font_bold" style="font-size:70%;background-color:#EFEFEF;">73.31±0.05</span></td>
<td class="ltx_td ltx_align_center ltx_border_b" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">1758</span></td>
<td class="ltx_td ltx_align_center ltx_border_b" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">1969</span></td>
<td class="ltx_td ltx_align_center ltx_border_b" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">4942</span></td>
<td class="ltx_td ltx_align_center ltx_border_b" style="padding-top:1.2pt;padding-bottom:1.2pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">7937</span></td>
</tr>
</table>

### 6.2Evaluation of Memory Retrieval

We conduct a focused evaluation to analyze the efficiency and effectiveness of memory retrieval across representative system designs. As shown in Table4, we compare latency and generation quality under different memory configurations, including standard RAG pipelines, memory-augmented models, and our proposedMemOS.

To test RAG-style retrieval systems, we systematically vary chunk sizes (from 128 to 8192 tokens) and Top-K values (1 or 2) to observe the trade-offs between context size, search latency, and LLM output quality. Larger chunk sizes reduce retrieval depth but increase encoding and integration cost, while smaller chunks allow finer granularity at the expense of retrieval breadth.

In addition to standard retrieval, we include full-context and commercial memory systems to establish upper and lower bounds. Notably, the full-context baseline—where the entire dialogue history is loaded into the model—achieves strong LLMJudge scores but suffers from prohibitively high latency due to extreme context length. LangMem and Zep incur substantial retrieval delays from graph traversal or multi-level indexing. OpenAI-Memory offers low latency but only moderate output quality, likely limited by opaque memory heuristics.

Remarkably,MemOSnot only matches but surpasses the full-context baseline in LLMJudge scores—while operating at significantly lower latency. Despite managing over 1500 memory tokens, its retrieval time remains close to smaller baselines such as mem0. This demonstrates thatMemOS’s hybrid semantic organization and activation-based memory loading can achieve superior performance without the cost of full-context inference.

### 6.3Evaluation of KV-Based Memory Acceleration

To evaluate the effectiveness of KV-form memory acceleration withinMemOS, we design a controlled experiment simulating realistic memory reuse scenarios.

During typical usage, theMemSchedulermodule inMemOScontinuously monitors model interactions and automatically identifies the most frequently accessed and semantically stable plaintext memory entries. These entries are then converted intoactivation memory—a KV-format structure injected into the model’s attention cache and proactively transferred to GPU memory for low-latency reuse.

Our evaluation assumes this realistic deployment: memory has already been preprocessed and cached on GPU in KV format, avoiding the need for repeated prompt encoding.

We compare two memory usage strategies: prompt-based memory injection, where memory entries are prepended to the input sequence, and KV-cache injection, where memory is injected directly as key-value pairs into the model’s attention mechanism.

To simulate realistic inference conditions, we evaluate across three context lengths—short (583 tokens), medium (2773 tokens), and long (6064 tokens)—as well as three query types of increasing length and complexity: short (167 tokens), medium (302.7 tokens), and long (952.7 tokens).
All experiments are conducted using the HuggingFacetransformerslibrary, running on a single NVIDIA H800 GPU with 80GB of memory under consistent system settings.

We report four metrics as shown in Table5. “Build” time refers to the preprocessing duration needed to convert memory into KV format. “KV TTFT” denotes the first-token latency under KV-based memory injection, while “Dir TTFT” indicates the latency under prompt-based injection. “Speedup” reflects the relative latency reduction achieved by KV injection compared to direct prompt injection.

<table class="ltx_tabular ltx_align_middle">
<tr class="ltx_tr">
<td class="ltx_td ltx_align_left ltx_border_r ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">Model</span></td>
<td class="ltx_td ltx_align_left ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">Ctx</span></td>
<td class="ltx_td ltx_align_center ltx_border_r ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">CtxTok</span></td>
<td class="ltx_td ltx_align_left ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">Qry</span></td>
<td class="ltx_td ltx_align_center ltx_border_r ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">QryTok</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">Build (s)</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">KV TTFT (s)</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">Dir TTFT (s)</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">Speedup (%)</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_border_r ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_align_left ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">long</span></td>
<td class="ltx_td ltx_align_center ltx_border_r ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">952.7</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">0.92</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">0.50</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">2.37</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">79.1</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_align_left" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">medium</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">302.7</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">0.93</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">0.19</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">2.16</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">91.1</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_align_left" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">long</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">6064</span></td>
<td class="ltx_td ltx_align_left" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">short</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">167</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">0.93</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">0.12</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">2.04</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">94.2</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_border_r ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_align_left ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">long</span></td>
<td class="ltx_td ltx_align_center ltx_border_r ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">952.7</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">0.41</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">0.43</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">1.22</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">64.6</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_align_left" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">medium</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">302.7</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">0.41</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">0.16</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">1.08</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">85.1</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_align_left" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">medium</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">2773</span></td>
<td class="ltx_td ltx_align_left" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">short</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">167</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">0.43</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">0.10</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">0.95</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">89.7</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_border_r ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_align_left ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">long</span></td>
<td class="ltx_td ltx_align_center ltx_border_r ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">952.7</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">0.12</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">0.39</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">0.51</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">23.0</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_align_left" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">medium</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">302.7</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">0.12</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">0.14</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">0.32</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">55.6</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_align_left ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">Qwen3-8B</span></td>
<td class="ltx_td ltx_align_left" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">short</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">583</span></td>
<td class="ltx_td ltx_align_left" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">short</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">167</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">0.12</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">0.08</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">0.29</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">71.3</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_border_r ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_align_left ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">long</span></td>
<td class="ltx_td ltx_align_center ltx_border_r ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">952.7</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">0.71</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">0.31</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">1.09</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">71.4</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_align_left" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">medium</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">302.7</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">0.71</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">0.15</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">0.98</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">84.3</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_align_left" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">long</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">6064</span></td>
<td class="ltx_td ltx_align_left" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">short</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">167</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">0.71</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">0.11</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">0.96</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">88.8</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_border_r ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_align_left ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">long</span></td>
<td class="ltx_td ltx_align_center ltx_border_r ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">952.7</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">0.31</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">0.24</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">0.56</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">56.9</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_align_left" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">medium</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">302.7</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">0.31</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">0.12</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">0.47</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">75.1</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_align_left" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">medium</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">2773</span></td>
<td class="ltx_td ltx_align_left" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">short</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">167</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">0.31</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">0.08</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">0.44</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">81.2</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_border_r ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_align_left ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">long</span></td>
<td class="ltx_td ltx_align_center ltx_border_r ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">952.7</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">0.09</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">0.20</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">0.24</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">18.6</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_align_left" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">medium</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">302.7</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">0.09</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">0.09</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">0.15</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">39.6</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_align_left ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">Qwen3-32B</span></td>
<td class="ltx_td ltx_align_left" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">short</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">583</span></td>
<td class="ltx_td ltx_align_left" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">short</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">167</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">0.09</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">0.07</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">0.14</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">53.5</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_border_r ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_align_left ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">long</span></td>
<td class="ltx_td ltx_align_center ltx_border_r ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">952.7</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">1.26</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">0.48</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">2.04</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">76.4</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_align_left" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">medium</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">302.7</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">1.26</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">0.23</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">1.82</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">87.2</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_align_left" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">long</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">6064</span></td>
<td class="ltx_td ltx_align_left" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">short</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">167</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">1.27</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">0.15</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">1.79</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">91.4</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_border_r ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_align_left ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">long</span></td>
<td class="ltx_td ltx_align_center ltx_border_r ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">952.7</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">0.58</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">0.39</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">1.05</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">62.7</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_align_left" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">medium</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">302.7</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">0.58</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">0.18</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">0.89</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">79.2</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_align_left" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">medium</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">2773</span></td>
<td class="ltx_td ltx_align_left" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">short</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">167</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">0.71</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">0.23</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">0.82</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">71.6</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_border_r ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_align_left ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">long</span></td>
<td class="ltx_td ltx_align_center ltx_border_r ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">952.7</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">0.16</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">0.33</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">0.43</span></td>
<td class="ltx_td ltx_align_center ltx_border_t" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">23.8</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"></td>
<td class="ltx_td ltx_align_left" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">medium</span></td>
<td class="ltx_td ltx_align_center ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">302.7</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">0.16</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">0.15</span></td>
<td class="ltx_td ltx_align_center" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">0.27</span></td>
<td class="ltx_td ltx_align_center" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">43.2</span></td>
</tr>
<tr class="ltx_tr">
<td class="ltx_td ltx_align_left ltx_border_b ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">Qwen2.5-72B</span></td>
<td class="ltx_td ltx_align_left ltx_border_b" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">short</span></td>
<td class="ltx_td ltx_align_center ltx_border_b ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">583</span></td>
<td class="ltx_td ltx_align_left ltx_border_b" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">short</span></td>
<td class="ltx_td ltx_align_center ltx_border_b ltx_border_r" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">167</span></td>
<td class="ltx_td ltx_align_center ltx_border_b" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">0.16</span></td>
<td class="ltx_td ltx_align_center ltx_border_b" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">0.10</span></td>
<td class="ltx_td ltx_align_center ltx_border_b" style="padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;">0.25</span></td>
<td class="ltx_td ltx_align_center ltx_border_b" style="background-color:#EFEFEF;padding-top:0.4pt;padding-bottom:0.4pt;"><span class="ltx_text" style="font-size:70%;background-color:#EFEFEF;">60.5</span></td>
</tr>
</table>

The results (Table5and Figure10) confirm that KV-based memory injection yields substantial TTFT reduction across all models and configurations. The output sequences remain identical under both methods, validating their semantic equivalence. Acceleration is especially significant for larger models and longer contexts—for instance, Qwen2.5-72B achieves a 91.4% reduction in TTFT under long-context, short-query conditions. These findings highlight KV memory as a practical and effective technique for low-latency execution in memory-augmented language models.

## 7MemOSfor Architecture Innovation and Applications

### 7.1Architectural Innovations Enabled byMemOS

MemOStreats memory as a first-class system resource, enabling unified lifecycle management and orchestration of memory in multiple forms.
This abstraction supports architectural innovations that focus on memory-driven modules and services, facilitating the modularization and reusability of knowledge assets.

#### 7.1.1Paid Memory as Modular Installables (User-Facing Paradigm)

MemOSis designed around a memory-centric architecture, offering modularized and assetized memory interfaces that allow knowledge to be uploaded, mounted, and invoked like a digital resource.
Under this paradigm, memory is no longer bound to training pipelines or development workflows but becomes a composable and user-controllable intelligence unit.

Concretely, domain experts can publish structured experiential memories viaMemStore, akin to publishing a knowledge plugin or an expert tip.
Consumers—students, enterprise agents, or assistant models—can install these memories using a standardized loading interface, subject to permission control.
This entire flow abstracts away the need for understanding the underlying model architecture or performing manual alignment.
It drastically reduces the barrier to memory usage and makes memory-driven intelligence available beyond developers and platform operators.

For instance, a medical student in clinical rotation may wish to study how to manage a rare autoimmune condition.
An experienced physician can encapsulate diagnostic heuristics, questioning paths, and typical case patterns into a structured memory and upload it toMemStore.
The student can then search, install, and invoke this memory locally via their assistant model.
This bypasses the need for building formal ontologies or coordinating structured knowledge base design, as is common in traditional clinical AI.

MemOSencapsulates this process as a standardized "Memory-as-a-Service" capability, greatly expanding the accessibility and reusability of expert knowledge.
Furthermore,MemGovernance, the dedicated control module inMemOS, offers full-spectrum privacy and access control for memory assets.
It enables memory providers to define custom access conditions over their published content.
For example, a medical expert may restrict installation rights to users who have completed a micropayment, enabling a form of licensed intelligence delivery.

#### 7.1.2Painless Memory Management (Task-Oriented Paradigm)

MemOSabstracts memory as a universal, long-lived, and shareable infrastructure resource, architecturally analogous to storage subsystems in traditional operating systems.
This design elevates memory from a model-embedded utility to a first-class system-level asset with its own lifecycle and invocation semantics.

Unlike conventional transient memory techniques limited to context windows or parameter embeddings,MemOSoffers standardized memory interfaces, a unified access protocol, and structured persistence formats.
This enables runtime tasks to flexibly read, write, mount, fuse, or replace memory blocks on demand,
without requiring manual state tracking or architectural alignment.

Neither users nor developers need to handle low-level vector indexing, KV-caching, or context orchestration logic.
Instead, they can access and update memory seamlessly through task-levelMemory APIcalls.
This infrastructure-level abstraction proves especially valuable in multi-stage, long-horizon, and evolving tasks.

For example, in an intelligent legal assistant system, a user may complete a corporate contract review task in distinct phases:
the first phase may focus on structural layout and terminological consistency;
the second phase may highlight risky clauses and compare precedent cases;
and the final phase may involve checking compliance against current regulations.MemOSdynamically loads the appropriate memory sets at each stage (e.g., “Contract Template Memory”, “Risk Clause Case Logs”, “Recent Regulation Digest”),
and performs hot-swapping and cache eviction as task contexts evolve.
Throughout the task lifecycle, the user need not explicitly manage memory policies;
the system automatically schedules the relevant memory assets based on context semantics,
delivering a “memory-as-resource, use-on-demand” intelligent task execution experience.

### 7.2MemOSApplication Scenarios

#### 7.2.1Supporting Multi-Turn Dialogue and Cross-Task Continuity

Real-world interactions rarely reveal user intent in a single turn; instead, goals are refined progressively over multiple exchanges. However, traditional LLMs rely on static context windows, making it difficult to retain key semantic states across turns, resulting in “memory loss” between dialogue rounds.

For instance, in a procurement negotiation task, a user might set a budget cap of ¥300,000 in round 5, later revise product preferences in round 12 to prioritize domestic alternatives, yet by round 15, the model reverts to recommending high-priced imports based on earlier defaults.

MemOSaddresses this at the system level by extracting salient elements (e.g., budget, preferences, delivery constraints) after each user input and encoding them into structured “conversation memory units.” These are linked to the ongoing task’s long-term memory path viaMemLink.

During inference,MemSchedulerretrieves relevant historical fragments based on current context and integrates them into the active reasoning path. This ensures continuity of semantic state and prevents logic drift due to “context sliding.”

Furthermore,MemOSsupports cross-task memory reuse to enable dialogue continuity and state persistence. For example, after completing an auto-form-filling task, the system retains memory of ID details or user habits. When the user later initiates a “visa application” task,MemOSrecalls the previously stored data (e.g., from “passport issuance”), enabling seamless state transition across tasks.

#### 7.2.2Supporting Knowledge Evolution and Continuous Update

Modern knowledge is dynamic, yet LLMs are generally trained once with static datasets. Updating their internal knowledge either requires expensive fine-tuning or introduces risks like catastrophic forgetting. Even RAG approaches lack lifecycle, version, or governance mechanisms—leading to fragmented, unverifiable external knowledge.

MemOSredefines knowledge as dynamic, lifecycle-governed memory. Each memory unit evolves independently, with defined stages for generation, replacement, fusion, and deprecation. The system schedules updates based on usage frequency, contextual alignment, and semantic overlap.

For example, when updated clinical guidelines are published, medical authorities can release them as explicit memory blocks viaMemStore.MemOStags them as “trusted sources,” compares them with older versions, and suggests updates to users.

At inference time,MemSchedulerprioritizes trusted and active versions, while obsolete entries are archived. This allows the model to remain up-to-date without retraining or harming prior knowledge structures.

MemOSalso supports personalized knowledge development. For instance, a cancer specialist may iteratively add interpretations and heuristics to drug usage. Over time, these refinements are integrated into their personal memory path, coexisting with official guidelines and selected based on task context.

#### 7.2.3Enabling Personalization and Multi-Role Modeling

LLMs today often operate statelessly across users and roles, unable to remember stylistic preferences or distinguish between user roles in complex settings. As a result, users must re-specify information every time, and models struggle to maintain consistent identity or behavior.

MemOSprovides system-level support for identity-aware memory and role-based behavior. Each user identity is associated with dedicated memory spaces, and multiple roles can coexist under one account.

For example, a user may interact as both a “parent” managing home tasks and a “manager” handling contracts.MemOSkeeps memory streams separate and dynamically loads the appropriate persona during inference.

In addition, long-term interaction patterns are encoded into “personal memory units” capturing language tone, response preferences, or value leanings. These units are incorporated into inference, yielding a personalized and coherent AI behavior.

In enterprise contexts,MemOSallows deployment of predefined role templates with task scopes, permission controls, and memory sync strategies. For example, an organization may define roles for analysts, assistants, and project leads, each with distinct memory access and agent behavior.

#### 7.2.4Enabling Cross-Platform Memory Migration

In a world of multi-device, multi-agent environments, valuable user-model memories often become locked within individual platforms, creating “memory silos” that break continuity and fragment knowledge accumulation.

MemOSresolves this through standardized memory representations, encryption, and platform-agnostic mount protocols. All memory blocks are portable across environments—from mobile to cloud to enterprise infrastructure.

For example, a user’s “family travel preference” memory built via mobile assistant—including flight timing, hotel type, and budget—can be selectively migrated to a corporate travel planning agent on desktop, enabling consistent and efficient decision-making.

By breaking the memory silo,MemOStransforms memory from a private asset embedded in a single model to a distributed, governable, and reusable intelligence layer across platforms.

## 8Conclusion

In this work, we introduce a memory operating system designed for Large Language Models, aimed at collaboratively building foundational memory infrastructure for next-generation LLM applications.

MemOSprovides a unified abstraction and integrated management framework for heterogeneous memory types, including parameter memory, activation memory, and explicit plaintext memory. We propose a standardized memory unit,MemCube, and implement key modules for scheduling, lifecycle management, structured storage, and transparent augmentation. These components collectively enhance reasoning coherence, adaptability, and system scalability in LLMs.

Building on this foundation, we envision a future intelligent ecosystem centered on modular memory resources and supported by a decentralized memory marketplace. This paradigm shift enables the creation of next-generation AI systems capable of continual learning and long-term evolution.

Looking ahead, we plan to explore the following directions:

- •Cross-LLM Memory Sharing: Enable interoperability and module reuse across different foundation models by sharing parametric and activation memories. To support consistent semantics and secure exchange, we plan to extend theMemory Interchange Protocol (MIP)to define standard formats, compatibility rules, and trust mechanisms for cross-model/app memory transmission—facilitating collaborative knowledge transfer among agents.
- •Self-Evolving MemBlocks: Develop memory units capable of self-optimization, reconstruction, and evolution based on usage feedback, reducing the need for manual maintenance and supervision.
- •Scalable Memory Marketplace: Establish decentralized mechanisms for memory exchange, supporting asset-level transactions, collaborative updates, and distributed evolution to foster a sustainable AI ecosystem.

Cross-LLM Memory Sharing: Enable interoperability and module reuse across different foundation models by sharing parametric and activation memories. To support consistent semantics and secure exchange, we plan to extend theMemory Interchange Protocol (MIP)to define standard formats, compatibility rules, and trust mechanisms for cross-model/app memory transmission—facilitating collaborative knowledge transfer among agents.

Self-Evolving MemBlocks: Develop memory units capable of self-optimization, reconstruction, and evolution based on usage feedback, reducing the need for manual maintenance and supervision.

Scalable Memory Marketplace: Establish decentralized mechanisms for memory exchange, supporting asset-level transactions, collaborative updates, and distributed evolution to foster a sustainable AI ecosystem.

Overall, with the introduction ofMemOS, we aim to transform LLMs from closed, static generation systems to continuously evolving intelligent agents equipped with long-term memory, integrated knowledge, and behavioral plasticity.MemOSnot only addresses critical architectural limitations in current models but also lays the groundwork for cross-task, cross-platform, and multi-agent collaborative intelligence. Building on prior work demonstrating the potential of explicit memory and hierarchical memory representations in LLMs[1], we look forward to advancing the frontiers ofMemOSin collaboration with the community, making memory a first-class computational resource in the age of general-purpose AI.

## References

- [1]Hongkang Yang, Zehao Lin, Wenjin Wang, Hao Wu, Zhiyu Li, Bo Tang, Wenqiang Wei, Jinbo Wang, Zeyun Tang, Shichao Song, Chenyang Xi, Yu Yu, Kai Chen, Feiyu Xiong, Linpeng Tang, and Weinan E.Memory3: Language modeling with explicit memory.Journal of Machine Learning, 3(3):300–346, January 2024.
- [2]Wayne Xin Zhao, Kun Zhou, Junyi Li, Tianyi Tang, Xiaolei Wang, Yupeng Hou, Yingqian Min, Beichen Zhang, Junjie Zhang, Zican Dong, et al.A survey of large language models.arXiv preprint arXiv:2303.18223, 1(2), 2023.
- [3]Yue Wang, Hung Le, Akhilesh Deepak Gotmare, Nghi DQ Bui, Junnan Li, and Steven CH Hoi.Codet5+: Open code large language models for code understanding and generation.arXiv preprint arXiv:2305.07922, 2023.
- [4]Shengsheng Qian, Zuyi Zhou, Dizhan Xue, Bing Wang, and Changsheng Xu.From linguistic giants to sensory maestros: A survey on cross-modal reasoning with large language models.arXiv preprint arXiv:2409.18996, 2024.
- [5]Penghao Zhao, Hailin Zhang, Qinhan Yu, Zhengren Wang, Yunteng Geng, Fangcheng Fu, Ling Yang, Wentao Zhang, and Bin Cui.Retrieval-augmented generation for ai-generated content: A survey.CoRR, abs/2402.19473, 2024.
- [6]Yunfan Gao, Yun Xiong, Xinyu Gao, Kangxiang Jia, Jinliu Pan, Yuxi Bi, Yi Dai, Jiawei Sun, Qianyu Guo, Meng Wang, and Haofen Wang.Retrieval-augmented generation for large language models: A survey.CoRR, abs/2312.10997, 2023.
- [7]Qinggang Zhang, Shengyuan Chen, Yuanchen Bei, Zheng Yuan, Huachi Zhou, Zijin Hong, Junnan Dong, Hao Chen, Yi Chang, and Xiao Huang.A survey of graph retrieval-augmented generation for customized large language models.CoRR, abs/2501.13958, 2025.
- [8]Bo Ni, Zheyuan Liu, Leyao Wang, Yongjia Lei, Yuying Zhao, Xueqi Cheng, Qingkai Zeng, Luna Dong, Yinglong Xia, Krishnaram Kenthapadi, Ryan A. Rossi, Franck Dernoncourt, Md. Mehrab Tanjim, Nesreen K. Ahmed, Xiaorui Liu, Wenqi Fan, Erik Blasch, Yu Wang, Meng Jiang, and Tyler Derr.Towards trustworthy retrieval augmented generation for large language models: A survey.CoRR, abs/2502.06872, 2025.
- [9]Howard Chen, Ramakanth Pasunuru, Jason Weston, and Asli Celikyilmaz.Walking down the memory maze: Beyond context limit through interactive reading.CoRR, abs/2310.05029, 2023.
- [10]Darren Edge, Ha Trinh, Newman Cheng, Joshua Bradley, Alex Chao, Apurva Mody, Steven Truitt, and Jonathan Larson.From local to global: A graph RAG approach to query-focused summarization.CoRR, abs/2404.16130, 2024.
- [11]Zirui Guo, Lianghao Xia, Yanhua Yu, Tu Ao, and Chao Huang.Lightrag: Simple and fast retrieval-augmented generation.CoRR, abs/2410.05779, 2024.
- [12]Microsoft.Retrieval augmented generation (rag) in azure ai search, 2025.
- [13]Google.Vertex ai search, 2025.
- [14]Elastic.Build innovative ai search experiences, 2025.
- [15]Nuclia.Agentic rag-as-a-service company, 2025.
- [16]Tu Vu, Mohit Iyyer, Xuezhi Wang, Noah Constant, Jerry Wei, Jason Wei, Chris Tar, Yun-Hsuan Sung, Denny Zhou, Quoc Le, and Thang Luong.Freshllms: Refreshing large language models with search engine augmentation, 2023.
- [17]Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al.Gpt-4 technical report.arXiv preprint arXiv:2303.08774, 2023.
- [18]Cursor - The AI Code Editor.
- [19]Yiming Du, Wenyu Huang, Danna Zheng, Zhaowei Wang, Sebastien Montella, Mirella Lapata, Kam-Fai Wong, and Jeff Z. Pan.Rethinking Memory in AI: Taxonomy, Operations, Topics, and Future Directions, May 2025.arXiv:2505.00675 [cs].
- [20]Yaxiong Wu, Sheng Liang, Chen Zhang, Yichao Wang, Yongyue Zhang, Huifeng Guo, Ruiming Tang, and Yong Liu.From Human Memory to AI Memory: A Survey on Memory Mechanisms in the Era of LLMs, April 2025.arXiv:2504.15965 [cs].
- [21]Lianlei Shan, Shixian Luo, Zezhou Zhu, Yu Yuan, and Yong Wu.Cognitive Memory in Large Language Models, April 2025.arXiv:2504.02441 [cs].
- [22]Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei, and Ilya Sutskever.Language Models are Unsupervised Multitask Learners.
- [23]Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon Child, Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu, Clemens Winter, Christopher Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya Sutskever, and Dario Amodei.Language Models are Few-Shot Learners, July 2020.arXiv:2005.14165 [cs].
- [24]Xiang Lisa Li and Percy Liang.Prefix-Tuning: Optimizing Continuous Prompts for Generation.InProceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (Volume 1: Long Papers), pages 4582–4597, Online, 2021. Association for Computational Linguistics.
- [25]Brian Lester, Rami Al-Rfou, and Noah Constant.The Power of Scale for Parameter-Efficient Prompt Tuning.InProceedings of the 2021 Conference on Empirical Methods in Natural Language Processing, pages 3045–3059, Online and Punta Cana, Dominican Republic, 2021. Association for Computational Linguistics.
- [26]Xiao Liu, Yanan Zheng, Zhengxiao Du, Ming Ding, Yujie Qian, Zhilin Yang, and Jie Tang.GPT Understands, Too, October 2023.arXiv:2103.10385 [cs].
- [27]Xiao Liu, Kaixuan Ji, Yicheng Fu, Weng Tam, Zhengxiao Du, Zhilin Yang, and Jie Tang.P-Tuning: Prompt Tuning Can Be Comparable to Fine-tuning Across Scales and Tasks.InProceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers), pages 61–68, Dublin, Ireland, 2022. Association for Computational Linguistics.
- [28]Long Ouyang, Jeff Wu, Xu Jiang, Diogo Almeida, Carroll L. Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, John Schulman, Jacob Hilton, Fraser Kelton, Luke Miller, Maddie Simens, Amanda Askell, Peter Welinder, Paul Christiano, Jan Leike, and Ryan Lowe.Training language models to follow instructions with human feedback, March 2022.arXiv:2203.02155 [cs].
- [29]Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng, Cody Hao Yu, Joseph Gonzalez, Hao Zhang, and Ion Stoica.Efficient Memory Management for Large Language Model Serving with PagedAttention.InProceedings of the 29th Symposium on Operating Systems Principles, pages 611–626, Koblenz Germany, October 2023. ACM.
- [30]Guangxuan Xiao, Yuandong Tian, Beidi Chen, Song Han, and Mike Lewis.Efficient Streaming Language Models with Attention Sinks.October 2023.
- [31]Zhenyu Zhang, Ying Sheng, Tianyi Zhou, Tianlong Chen, Lianmin Zheng, Ruisi Cai, Zhao Song, Yuandong Tian, Christopher Ré, Clark Barrett, Zhangyang "Atlas" Wang, and Beidi Chen.H2O: Heavy-Hitter Oracle for Efficient Generative Inference of Large Language Models.Advances in Neural Information Processing Systems, 36:34661–34710, December 2023.
- [32]Harry Dong, Xinyu Yang, Zhenyu Zhang, Zhangyang Wang, Yuejie Chi, and Beidi Chen.Get More with LESS: Synthesizing Recurrence with KV Cache Compression for Efficient LLM Inference.June 2024.
- [33]Coleman Hooper, Sehoon Kim, Hiva Mohammadzadeh, Michael W. Mahoney, Yakun S. Shao, Kurt Keutzer, and Amir Gholami.KVQuant: Towards 10 Million Context Length LLM Inference with KV Cache Quantization.Advances in Neural Information Processing Systems, 37:1270–1303, December 2024.
- [34]Di Liu, Meng Chen, Baotong Lu, Huiqiang Jiang, Zhenhua Han, Qianxi Zhang, Qi Chen, Chengruidong Zhang, Bailu Ding, Kai Zhang, Chen Chen, Fan Yang, Yuqing Yang, and Lili Qiu.RetrievalAttention: Accelerating Long-Context LLM Inference via Vector Retrieval, December 2024.arXiv:2409.10516 [cs].
- [35]Nishant Subramani, Nivedita Suresh, and Matthew Peters.Extracting Latent Steering Vectors from Pretrained Language Models.InFindings of the Association for Computational Linguistics: ACL 2022, pages 566–581, Dublin, Ireland, 2022. Association for Computational Linguistics.
- [36]Sheng Liu, Haotian Ye, Lei Xing, and James Zou.In-context Vectors: Making In Context Learning More Effective and Controllable Through Latent Space Steering, February 2024.arXiv:2311.06668 [cs].
- [37]Alexander Matt Turner, Lisa Thiergart, Gavin Leech, David Udell, Juan J. Vazquez, Ulisse Mini, and Monte MacDiarmid.Steering Language Models With Activation Engineering, October 2024.arXiv:2308.10248 [cs].
- [38]Kai Konen, Sophie Jentzsch, Diaoulé Diallo, Peer Schütt, Oliver Bensch, Roxanne El Baff, Dominik Opitz, and Tobias Hecking.Style vectors for steering generative large language models.In Yvette Graham and Matthew Purver, editors,Findings of the Association for Computational Linguistics: EACL 2024, pages 782–802, St. Julian’s, Malta, March 2024. Association for Computational Linguistics.
- [39]Nina Rimsky, Nick Gabrieli, Julian Schulz, Meg Tong, Evan Hubinger, and Alexander Turner.Steering Llama 2 via Contrastive Activation Addition.In Lun-Wei Ku, Andre Martins, and Vivek Srikumar, editors,Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 15504–15522, Bangkok, Thailand, August 2024. Association for Computational Linguistics.
- [40]Zijian Feng, Hanzhang Zhou, Kezhi Mao, and Zixiao Zhu.FreeCtrl: Constructing Control Centers with Feedforward Layers for Learning-Free Controllable Text Generation.InProceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 7627–7640, Bangkok, Thailand, 2024. Association for Computational Linguistics.
- [41]Ziwen Xu, Shuxun Wang, Kewei Xu, Haoming Xu, Mengru Wang, Xinle Deng, Yunzhi Yao, Guozhou Zheng, Huajun Chen, and Ningyu Zhang.EasyEdit2: An Easy-to-use Steering Framework for Editing Large Language Models, April 2025.arXiv:2504.15133 [cs].
- [42]Yuxin Xiao, Chaoqun Wan, Yonggang Zhang, Wenxiao Wang, Binbin Lin, Xiaofei He, Xu Shen, and Jieping Ye.Enhancing Multiple Dimensions of Trustworthiness in LLMs via Sparse Activation Control.November 2024.
- [43]Yu Li, Han Jiang, Chuanyang Gong, and Zhihua Wei.DESTEIN: Navigating Detoxification of Language Models via Universal Steering Pairs and Head-wise Activation Fusion, August 2024.arXiv:2404.10464 [cs].
- [44]Chi Han, Jialiang Xu, Manling Li, Yi Fung, Chenkai Sun, Nan Jiang, Tarek Abdelzaher, and Heng Ji.Word Embeddings Are Steers for Language Models.In Lun-Wei Ku, Andre Martins, and Vivek Srikumar, editors,Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 16410–16430, Bangkok, Thailand, August 2024. Association for Computational Linguistics.
- [45]Urvashi Khandelwal, Omer Levy, Dan Jurafsky, Luke Zettlemoyer, and Mike Lewis.Generalization through Memorization: Nearest Neighbor Language Models.September 2019.
- [46]Luiza Pozzobon, Beyza Ermis, Patrick Lewis, and Sara Hooker.Goodtriever: Adaptive Toxicity Mitigation with Retrieval-augmented Models.InFindings of the Association for Computational Linguistics: EMNLP 2023, pages 5108–5125, Singapore, 2023. Association for Computational Linguistics.
- [47]Tianyang Xu, Haojie Zheng, Chengze Li, Haoxiang Chen, Yixin Liu, Ruoxi Chen, and Lichao Sun.Noderag: Structuring graph-based rag with heterogeneous nodes, 2025.
- [48]Peiru Yang, Xintian Li, Zhiyang Hu, Jiapeng Wang, Jinhua Yin, Huili Wang, Lizhi He, Shuai Yang, Shangguang Wang, Yongfeng Huang, and Tao Qi.Heterag: A heterogeneous retrieval-augmented generation framework with decoupled knowledge representations, 2025.
- [49]Haoran Luo, Haihong E, Guanting Chen, Yandan Zheng, Xiaobao Wu, Yikai Guo, Qika Lin, Yu Feng, Ze-min Kuang, Meina Song, Yifan Zhu, and Luu Anh Tuan.Hypergraphrag: Retrieval-augmented generation with hypergraph-structured knowledge representation.CoRR, abs/2503.21322, 2025.
- [50]Bernal Jimenez Gutierrez, Yiheng Shu, Yu Gu, Michihiro Yasunaga, and Yu Su.Hipporag: Neurobiologically inspired long-term memory for large language models.In Amir Globersons, Lester Mackey, Danielle Belgrave, Angela Fan, Ulrich Paquet, Jakub M. Tomczak, and Cheng Zhang, editors,Advances in Neural Information Processing Systems 38: Annual Conference on Neural Information Processing Systems 2024, NeurIPS 2024, Vancouver, BC, Canada, December 10 - 15, 2024, 2024.
- [51]Bernal Jiménez Gutiérrez, Yiheng Shu, Weijian Qi, Sizhe Zhou, and Yu Su.From RAG to memory: Non-parametric continual learning for large language models.CoRR, abs/2502.14802, 2025.
- [52]Xiang Liang, Simin Niu, Zhiyu Li, Sensen Zhang, Shichao Song, Hanyu Wang, Jiawei Yang, Feiyu Xiong, Bo Tang, and Chenyang Xi.Empowering large language models to set up a knowledge retrieval indexer via self-learning.CoRR, abs/2405.16933, 2024.
- [53]Preston Rasmussen, Pavlo Paliychuk, Travis Beauvais, Jack Ryan, and Daniel Chalef.Zep: A temporal knowledge graph architecture for agent memory.CoRR, abs/2501.13956, 2025.
- [54]Wujiang Xu, Zujie Liang, Kai Mei, Hang Gao, Juntao Tan, and Yongfeng Zhang.A-MEM: agentic memory for LLM agents.CoRR, abs/2502.12110, 2025.
- [55]Prateek Chhikara, Dev Khant, Saket Aryan, Taranjeet Singh, and Deshraj Yadav.Mem0: Building production-ready ai agents with scalable long-term memory, 2025.
- [56]Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova.BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding.In Jill Burstein, Christy Doran, and Thamar Solorio, editors,Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers), pages 4171–4186, Minneapolis, Minnesota, June 2019. Association for Computational Linguistics.
- [57]Yuntao Bai, Andy Jones, Kamal Ndousse, Amanda Askell, Anna Chen, Nova DasSarma, Dawn Drain, Stanislav Fort, Deep Ganguli, Tom Henighan, Nicholas Joseph, Saurav Kadavath, Jackson Kernion, Tom Conerly, Sheer El-Showk, Nelson Elhage, Zac Hatfield-Dodds, Danny Hernandez, Tristan Hume, Scott Johnston, Shauna Kravec, Liane Lovitt, Neel Nanda, Catherine Olsson, Dario Amodei, Tom Brown, Jack Clark, Sam McCandlish, Chris Olah, Ben Mann, and Jared Kaplan.Training a Helpful and Harmless Assistant with Reinforcement Learning from Human Feedback, April 2022.arXiv:2204.05862 [cs].
- [58]Nitish Shirish Keskar, Bryan McCann, Lav R. Varshney, Caiming Xiong, and Richard Socher.CTRL: A Conditional Transformer Language Model for Controllable Generation, September 2019.arXiv:1909.05858 [cs].
- [59]Tianxiang Chen, Zhentao Tan, Tao Gong, Yue Wu, Qi Chu, Bin Liu, Jieping Ye, and Nenghai Yu.Llama SLayer 8B: Shallow Layers Hold the Key to Knowledge Injection.InFindings of the Association for Computational Linguistics: EMNLP 2024, pages 5991–6002, Miami, Florida, USA, 2024. Association for Computational Linguistics.
- [60]Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen.LoRA: Low-Rank Adaptation of Large Language Models, October 2021.arXiv:2106.09685 [cs].
- [61]Weihang Su, Yichen Tang, Qingyao Ai, Junxi Yan, Changyue Wang, Hongning Wang, Ziyi Ye, Yujia Zhou, and Yiqun Liu.Parametric Retrieval Augmented Generation, January 2025.arXiv:2501.15915 [cs].
- [62]Yuqiao Tan, Shizhu He, Huanxuan Liao, Jun Zhao, and Kang Liu.Better wit than wealth: Dynamic Parametric Retrieval Augmented Generation for Test-time Knowledge Enhancement, March 2025.arXiv:2503.23895 [cs].
- [63]Eric Mitchell, Charles Lin, Antoine Bosselut, Christopher D. Manning, and Chelsea Finn.Memory-Based Model Editing at Scale.InProceedings of the 39th International Conference on Machine Learning, pages 15817–15831. PMLR, June 2022.ISSN: 2640-3498.
- [64]Qingxiu Dong, Damai Dai, Yifan Song, Jingjing Xu, Zhifang Sui, and Lei Li.Calibrating Factual Knowledge in Pretrained Language Models.InFindings of the Association for Computational Linguistics: EMNLP 2022, pages 5937–5947, Abu Dhabi, United Arab Emirates, 2022. Association for Computational Linguistics.
- [65]Xin Cheng, Yankai Lin, Xiuying Chen, Dongyan Zhao, and Rui Yan.Decouple knowledge from paramters for plug-and-play language modeling.InFindings of the Association for Computational Linguistics: ACL 2023, pages 14288–14308, Toronto, Canada, 2023. Association for Computational Linguistics.
- [66]Thomas Hartvigsen, Swami Sankaranarayanan, Hamid Palangi, Yoon Kim, and Marzyeh Ghassemi.Aging with GRACE: Lifelong Model Editing with Discrete Key-Value Adaptors, October 2023.arXiv:2211.11031 [cs].
- [67]Kevin Meng, David Bau, Alex Andonian, and Yonatan Belinkov.Locating and Editing Factual Associations in GPT, January 2023.arXiv:2202.05262 [cs].
- [68]Kevin Meng, Arnab Sen Sharma, Alex Andonian, Yonatan Belinkov, and David Bau.Mass-Editing Memory in a Transformer, August 2023.arXiv:2210.07229 [cs].
- [69]Junfeng Fang, Houcheng Jiang, Kun Wang, Yunshan Ma, Shi Jie, Xiang Wang, Xiangnan He, and Tat-seng Chua.AlphaEdit: Null-Space Constrained Knowledge Editing for Language Models, March 2025.arXiv:2410.02355 [cs].
- [70]Houcheng Jiang, Junfeng Fang, Ningyu Zhang, Guojun Ma, Mingyang Wan, Xiang Wang, Xiangnan He, and Tat-seng Chua.AnyEdit: Edit Any Knowledge Encoded in Language Models, February 2025.arXiv:2502.05628 [cs].
- [71]Ningyu Zhang, Yunzhi Yao, Bozhong Tian, Peng Wang, Shumin Deng, Mengru Wang, Zekun Xi, Shengyu Mao, Jintian Zhang, Yuansheng Ni, Siyuan Cheng, Ziwen Xu, Xin Xu, Jia-Chen Gu, Yong Jiang, Pengjun Xie, Fei Huang, Lei Liang, Zhiqiang Zhang, Xiaowei Zhu, Jun Zhou, and Huajun Chen.A Comprehensive Study of Knowledge Editing for Large Language Models, November 2024.arXiv:2401.01286 [cs].
- [72]Qi Li and Xiaowen Chu.Can We Continually Edit Language Models? On the Knowledge Attenuation in Sequential Model Editing.In Lun-Wei Ku, Andre Martins, and Vivek Srikumar, editors,Findings of the Association for Computational Linguistics: ACL 2024, pages 5438–5455, Bangkok, Thailand, August 2024. Association for Computational Linguistics.
- [73]Daniel Tamayo, Aitor Gonzalez-Agirre, Javier Hernando, and Marta Villegas.Mass-Editing Memory with Attention in Transformers: A cross-lingual exploration of knowledge.InFindings of the Association for Computational Linguistics ACL 2024, pages 5831–5847, 2024.arXiv:2502.02173 [cs].
- [74]Mingyu Jin, Weidi Luo, Sitao Cheng, Xinyi Wang, Wenyue Hua, Ruixiang Tang, William Yang Wang, and Yongfeng Zhang.Disentangling Memory and Reasoning Ability in Large Language Models, November 2024.arXiv:2411.13504 [cs].
- [75]Ali Behrouz, Peilin Zhong, and Vahab Mirrokni.Titans: Learning to memorize at test time.CoRR, abs/2501.00663, 2025.
- [76]Yunzhi Yao, Peng Wang, Bozhong Tian, Siyuan Cheng, Zhoubo Li, Shumin Deng, Huajun Chen, and Ningyu Zhang.Editing Large Language Models: Problems, Methods, and Opportunities, November 2023.arXiv:2305.13172 [cs].
- [77]Xin Xu, Wei Xu, Ningyu Zhang, and Julian McAuley.BiasEdit: Debiasing Stereotyped Language Models via Model Editing, March 2025.arXiv:2503.08588 [cs].
- [78]Nicola De Cao, Wilker Aziz, and Ivan Titov.Editing Factual Knowledge in Language Models, September 2021.arXiv:2104.08164 [cs].
- [79]Eric Mitchell, Charles Lin, Antoine Bosselut, Chelsea Finn, and Christopher D. Manning.Fast Model Editing at Scale.October 2021.
- [80]Chenmien Tan, Ge Zhang, and Jie Fu.Massive Editing for Large Language Models via Meta Learning.October 2023.
- [81]Jiaming Tang, Yilong Zhao, Kan Zhu, Guangxuan Xiao, Baris Kasikci, and Song Han.QUEST: Query-Aware Sparsity for Efficient Long-Context LLM Inference.June 2024.
- [82]Chak Leong, Yi Cheng, Jiashuo Wang, Jian Wang, and Wenjie Li.Self-Detoxifying Language Models via Toxification Reversal.InProceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, pages 4433–4449, Singapore, 2023. Association for Computational Linguistics.
- [83]Tianlong Wang, Xianfeng Jiao, Yinghao Zhu, Zhongzhi Chen, Yifan He, Xu Chu, Junyi Gao, Yasha Wang, and Liantao Ma.Adaptive Activation Steering: A Tuning-Free LLM Truthfulness Improvement Method for Diverse Hallucinations Categories.InProceedings of the ACM on Web Conference 2025, WWW ’25, pages 2562–2578, New York, NY, USA, April 2025. Association for Computing Machinery.
- [84]Kenneth Li, Oam Patel, Fernanda Viégas, Hanspeter Pfister, and Martin Wattenberg.Inference-Time Intervention: Eliciting Truthful Answers from a Language Model.Advances in Neural Information Processing Systems, 36:41451–41530, December 2023.
- [85]Pengyu Wang, Dong Zhang, Linyang Li, Chenkun Tan, Xinghao Wang, Mozhi Zhang, Ke Ren, Botian Jiang, and Xipeng Qiu.InferAligner: Inference-Time Alignment for Harmlessness through Cross-Model Guidance.pages 10460–10479, November 2024.
- [86]Alessandro Stolfo, Vidhisha Balachandran, Safoora Yousefi, Eric Horvitz, and Besmira Nushi.Improving Instruction-Following in Language Models through Activation Steering, April 2025.arXiv:2410.12877 [cs].
- [87]Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timothée Lacroix, Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal Azhar, Aurelien Rodriguez, Armand Joulin, Edouard Grave, and Guillaume Lample.LLaMA: Open and Efficient Foundation Language Models, February 2023.arXiv:2302.13971 [cs].
- [88]Hugo Touvron, Louis Martin, Kevin Stone, et al.Llama 2: Open Foundation and Fine-Tuned Chat Models, July 2023.arXiv:2307.09288 [cs].
- [89]Junjie Ye, Xuanting Chen, Nuo Xu, Can Zu, Zekai Shao, Shichun Liu, Yuhan Cui, Zeyang Zhou, Chao Gong, Yang Shen, Jie Zhou, Siming Chen, Tao Gui, Qi Zhang, and Xuanjing Huang.A Comprehensive Capability Analysis of GPT-3 and GPT-3.5 Series Models, December 2023.arXiv:2303.10420 [cs].
- [90]Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, and Percy Liang.Lost in the Middle: How Language Models Use Long Contexts.Transactions of the Association for Computational Linguistics, 12:157–173, 2024.Place: Cambridge, MA Publisher: MIT Press.
- [91]Qingxiu Dong, Lei Li, Damai Dai, Ce Zheng, Jingyuan Ma, Rui Li, Heming Xia, Jingjing Xu, Zhiyong Wu, Baobao Chang, Xu Sun, Lei Li, and Zhifang Sui.A Survey on In-context Learning.In Yaser Al-Onaizan, Mohit Bansal, and Yun-Nung Chen, editors,Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing, pages 1107–1128, Miami, Florida, USA, November 2024. Association for Computational Linguistics.
- [92]Stephen E. Robertson and Hugo Zaragoza.The probabilistic relevance framework: BM25 and beyond.Found. Trends Inf. Retr., 3(4):333–389, 2009.
- [93]Nils Reimers and Iryna Gurevych.Sentence-bert: Sentence embeddings using siamese bert-networks.InProceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing, pages 3980–3990, 2019.
- [94]Langchaln.Ensemble retriever.https://python.langchain.com/v0.1/docs/modules/data_connection/retrievers/ensemble.
- [95]Jiale Wei, Xiang Ying, Tao Gao, Fangyi Bao, Felix Tao, and Jingbo Shang.Ai-native memory 2.0: Second me, 2025.
- [96]Qingyun Wu, Gagan Bansal, Jieyu Zhang, Yiran Wu, Shaokun Zhang, Erkang Zhu, Beibin Li, Li Jiang, Xiaoyun Zhang, and Chi Wang.Autogen: Enabling next-gen LLM applications via multi-agent conversation framework.CoRR, abs/2308.08155, 2023.
- [97]Prateek Chhikara, Dev Khant, Saket Aryan, Taranjeet Singh, and Deshraj Yadav.Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory, April 2025.arXiv:2504.19413 [cs].
- [98]Charles Packer, Sarah Wooders, Kevin Lin, Vivian Fang, Shishir G. Patil, Ion Stoica, and Joseph E. Gonzalez.MemGPT: Towards LLMs as Operating Systems, February 2024.arXiv:2310.08560 [cs].
- [99]Chunting Zhou, Pengfei Liu, Puxin Xu, Srini Iyer, Jiao Sun, Yuning Mao, Xuezhe Ma, Avia Efrat, Ping Yu, Lili Yu, Susan Zhang, Gargi Ghosh, Mike Lewis, Luke Zettlemoyer, and Omer Levy.Lima: Less is more for alignment, 2023.
