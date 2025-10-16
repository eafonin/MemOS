---
source_url: https://memos-docs.openmem.net/overview/quick_start/mem_lifecycle
section: Overview
scraped_date: 2025-10-16
title: Memory Lifecycle Management
has_images: yes
has_tables: yes
---

# Memory Lifecycle Management
 [ In MemOS, memories are not stored statically; they continuously evolve over time and through usage. 
## 1. Capability Overview
 
[A memory, once generated, may gradually consolidate into a stable long-term preference, or be removed if it becomes outdated or invalid.] **Tip** 
 This evolutionary process is called **Memory Lifecycle Management** , and its goal is to keep the memory base âclean and organized.â 
 
- [**Recently useful entries** remain active for easy retrieval;]
- [**Long-term stable facts** are consolidated to reduce duplication and noise;]
- [**Outdated or conflicting information** is archived or deleted to ensure consistency and compliance.] > Note that lifecycle management focuses onthe evolution of memory entries at the storage layer; whether a specific memory is invoked during reasoning is still determined by the scheduling mechanism. **Lifecycle Stage Overview** <table><thead><tr><th>Stage</th><th>Description</th><th>System Behavior</th></tr></thead><tbody><tr><td>Generated</td><td>Newly created memory object, with metadata such as source, timestamp, and confidence</td><td>Initially stored in the storage layer, awaiting future use</td></tr><tr><td>Activated</td><td>Referenced during reasoning or tasks, entering a high-frequency active state</td><td>More likely to be selected by the scheduling mechanism</td></tr><tr><td>Merged</td><td>Semantically overlaps with historical memories or user-provided data, integrated into a new version</td><td>Multiple records are compressed and merged into an updated stable entry</td></tr><tr><td>Archived</td><td>Not accessed for a long period, downgraded to cold storage</td><td>Only enabled during special retrievals or backtracking</td></tr><tr><td>Expired (optional)</td><td>After archiving, further timeout or policy judgment marks it invalid</td><td>Removed from the index, no longer used in reasoning, only minimal logs retained</td></tr><tr><td>Frozen (special state)</td><td>Critical or compliance-related memories are locked and cannot be modified</td><td>Full historical versions are preserved for audit and compliance tracking</td></tr></tbody></table>
 
 
## 2. Example: Memory Lifecycle of an Online Education Assistant Suppose you are building an **online education assistant** with MemOS to help students solve math problems. [**Generated**]
 
- [A student says for the first time: âI always confuse quadratic functions with linear functions.â]
- [The system extracts the memory:]
 
```
{"value": "The student often confuses quadratic and linear functions", "confidence": 0.8, "timestamp": "2025-09-11"}

```
 
- [Status: **Generated**]
- [Behavior: Stored into the memory base, awaiting future use.]
 
[**Activated**]
 
- [In the following problem-solving sessions, the system frequently calls this memory to assist with answers.]
- [Status: **Activated**]
- [Behavior: Prioritized by the scheduling mechanism and cached into the MemoryCube to improve retrieval speed.]
 
[**Merged**]
 
- [With more interactions, the system discovers that the student not only confuses linear and quadratic functions, but also struggles with exponential functions.]
- [The system merges multiple similar memories into:]
 
```
{"value": "This student is confused about function concepts, especially linear, quadratic, and exponential functions", "confidence": 0.95}

```
 
- [Status: **Merged**]
- [Behavior: Old entries are compressed to form a new version, reducing redundancy.]
 
[**Archived**]
 
- [Three months later, the student has mastered function-related concepts, and this memory hasnât been scheduled for a long time.]
- [Status: **Archived**]
- [Behavior: Migrated into MemVault (cold storage), excluded from reasoning by default, but available in âlearning trajectory backtracking.â]
 
[**Expired**]
 
- [A year later, the student advances to a new grade level. The old âjunior high function confusionâ memory is judged invalid by policy.]
- [Status: **Expired**]
- [Behavior: Fully removed from the index, retaining only minimal audit info:]
 
```
{"deleted_memory_id": "12345", "deleted_at": "2026-09-11"}

```
 
[**Frozen (special state)**]
 
- [Meanwhile, the studentâs âfinal exam evaluation reportâ is a compliance-related file that must not be modified.]
- [Status: **Frozen**]
- [Behavior: Locked against updates, retaining full history for audit and compliance inspection.]
 
 
## 3. Advanced: Deep Customization Options
 
<table><thead><tr><th>Extension Point</th><th>Description</th><th>Example</th></tr></thead><tbody><tr><td>State transition conditions</td><td>Control the triggers for each state</td><td>âIf unused for 7 days â Archiveâ</td></tr><tr><td>Merge and compression</td><td>Define how similar memories are handled</td><td>Multiple âlikes sci-fi moviesâ entries merged into one with higher confidence</td></tr><tr><td>Conflict resolution</td><td>Handle memory conflicts in timestamps or sources</td><td>Choose âlatest entry overridesâ or âpreserve in parallelâ</td></tr><tr><td>Cleanup mechanism</td><td>Set deletion rules to control index size</td><td>Remove low-confidence or user-retracted memories</td></tr><tr><td>Audit trail</td><td>Decide whether to retain minimal metadata of deleted items</td><td>Enable âtrace logsâ under compliance requirements</td></tr></tbody></table>
 
 
## 4. Next Steps
 
[Still have questions? Check out [FAQs](/overview/faq) to see if they can help.]
