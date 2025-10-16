---
source_url: https://memos-docs.openmem.net/overview/quick_start/mem_schedule
section: Overview
scraped_date: 2025-10-16
title: Memory Scheduling
has_images: yes
has_tables: yes
---

# Memory Scheduling
 [ Memory Scheduling is like the brain's attention mechanism, dynamically deciding which memory to call at the right moment. 
## 1. Capability Introduction
 
[In MemOS, **Memory Scheduling** improves efficiency and accuracy by dynamically coordinating memories of different usage efficiencies (Parameter > Activated > Working > Other Plaintext). During conversations and tasks, it predicts which memories will be needed and preloads high-efficiency types like activated and working memories, accelerating the reasoning chain.] **Why Scheduling Is Needed** [In complex interactions, if the system only relies on simple global search each time, it may:]
 
- [**Be too slow**: Waiting until after the user finishes asking to search causes high first-token latency.]
- [**Be inaccurate**: Too much history overwhelms key information, making retrieval difficult.]
 
 
[The role of scheduling is to give the system âinstant readiness and fast responseâ capabilities:]
 
- [**Preloading**: At the start of the conversation, load the userâs commonly used background.]
- [**Predictive invocation**: Before the user finishes typing, prepare the memories that may be needed.] **How Scheduling Works â Dynamically arrange memory invocation and storage based on task semantics, context, access frequency, and lifecycle.** <table><thead><tr><th>Dimension</th><th>Explanation</th></tr></thead><tbody><tr><td>What to schedule?</td><td>Parameter memory (long-term knowledge and skills)Activated memory (runtime KV cache and hidden states)Plaintext memory (externally editable facts, user preferences, retrieval snippets)Supports dynamic migration among Plaintext â Activated â Parameter; frequently used plaintext snippets can be compiled into KV cache in advance; stable templates can be deposited into parameters.</td></tr><tr><td>When to schedule?</td><td>When context and efficient memory are insufficient to support answering user queries, memory structures are optimized.Prepare memory content in advance according to the userâs intent and needs.During continuous queries, scheduling ensures high efficiency and accuracy in conversation scenarios.</td></tr><tr><td>Who to schedule for?</td><td>Current user, specific role agent, or shared cross-task context</td></tr><tr><td>What form to schedule into?</td><td>Memories are tagged with indicators such as heat, timeliness, and importance. The scheduler decides which to load first, which to cool down, and which to archive.</td></tr></tbody></table>
 
[When using MemOS cloud services, the role of scheduling can be observed through the performance of the `searchMemory` API:]
 
- [It quickly returns relevant memories, avoiding context breaks.]
- [Returned content is already optimized by the scheduler, ensuring results are relevant without overloading model input.]
 
 
## 2. Example: Memory Scheduling in a Household Assistant Scenario
 
- [Some time ago: the user was busy buying a house]
 [ 
[User often said:]
 [ 
- [âCheck the average second-hand housing price in XX community.â]
- [âRemind me to view the house on Saturday.â]
- [âRecord the latest change in mortgage rates.â]
 ] 
[MemOS System Operation]
 [ 
- [Initially, the system generated these items as **Plaintext Memories**.]
- [Since house-buying information was frequently mentioned, the scheduler judged it as a **core theme** and migrated these plaintexts into **Activated Memories**, making subsequent queries faster and more direct.] - [Recently: the user bought the house and started decorating]
 [ 
[User frequently mentioned:]
 [ 
- [âGoing to check tiles this weekend.â]
- [âRemind me to confirm water and electricity work with the renovation company.â]
- [âRecord next weekâs furniture delivery time.â]
 ] 
[MemOS System Operation]
 [ 
- [The system continued to generate new **Plaintext Memories**.]
- [The scheduler detected that ârenovationâ had become the new high-frequency theme and migrated these entries into **Activated Memories**.]
- [Meanwhile, previous âhouse-buyingâ activated memories were no longer frequently used and were automatically **downgraded back to plaintext**, reducing active memory usage.] - [**At the current moment: the user casually saysââI feel like too many things are piling up, help me organize them.â**]
 [ 
[Without scheduling, the system can only do a full-library retrieval, pulling out all possibly relevant memories:]
 [ 
- [Checking tiles (renovation)]
- [Confirming water/electricity work (renovation)]
- [Furniture delivery (renovation)]
- [Checking housing prices (house-buying, outdated)]
- [Viewing houses (house-buying, outdated)]
- [Grocery shopping (daily life)]
- [Watching a movie (daily life)]
 ] 
[With scheduling, the system can return more quickly]
 [ 
- [Checking tiles]
- [Confirming water/electricity work]
- [Furniture delivery]
 
 
[ð **User experience UP**]
 
- [Faster response (no need for full-library search).]
- [The listed items are exactly what they care about most â makes the assistant feel âvery understanding.â] ## 3. Advanced: Deep Customization
 
[Developers can **extend scheduling strategies** to customize system behavior, mainly including:]
 
<table><thead><tr><th>Extension Point</th><th>Configurable Content</th><th>Example Scenario</th></tr></thead><tbody><tr><td>Scheduling Strategy</td><td>Define memory selection logic for different tasks</td><td>Conversation systems prioritize activated memories; research systems prioritize retrieving the latest plaintexts</td></tr><tr><td>Transformation Rules</td><td>Set conditions for cross-type migration</td><td>High-frequency FAQs â KV cache; stable paradigms â parameter modules</td></tr><tr><td>Context Binding</td><td>Bind memories to roles/users</td><td>Student users automatically load learning preferences; enterprise users load project archives</td></tr><tr><td>Permissions &amp; Governance</td><td>Combine scheduling with access control and compliance checks</td><td>Medical records visible only to doctors; sensitive content not shareable across domains</td></tr><tr><td>Scheduling Metrics</td><td>Optimize scheduling based on access frequency and latency needs</td><td>High-frequency hot memories prioritized; low-frequency cold memories downgraded to archive</td></tr></tbody></table>
 
 
## 4. Next Steps
 
[Learn more about MemOS core capabilities:]
 
- [[Memory Recall and Instruction Completion](/overview/quick_start/mem_recall)]
- [[Memory Lifecycle Management](/overview/quick_start/mem_lifecycle)]
