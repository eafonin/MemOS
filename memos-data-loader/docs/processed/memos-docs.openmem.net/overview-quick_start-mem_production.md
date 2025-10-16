---
source_url: https://memos-docs.openmem.net/overview/quick_start/mem_production
section: Overview
scraped_date: 2025-10-16
title: Memory Production
has_images: yes
has_tables: yes
---

# Memory Production
 [ The Memory Production module transforms raw messages or events into storable and retrievable memory units, serving as the starting point of the entire MemOS workflow. 
## 1. Capability Introduction: Why Process Raw Messages into Memory
 
[In MemOS, what you submit is **raw information** (conversations between users and AI, user operation logs/action traces in the app, etc.), and the system will automatically complete the process of âmemorization.â] **Why process memory?** [If you simply save all the raw conversations and directly feed them to the large model, several problems will occur:]
 
- [**Overlong context**: Raw messages are often lengthy and repetitive. Feeding the entire context to the model is inefficient and wastes tokens.]
- [**Inaccurate retrieval**: Unprocessed raw text makes it difficult to quickly locate key information, and retrieval often recalls large amounts of noise.]
- [**High invocation cost**: Directly concatenating raw messages significantly increases model input length, leading to token costs and latency.] **Whatâs different after processing?** [MemOS transforms raw messages into structured memory units, automatically extracting:]
 
- [**Key facts**: e.g., âThe user usually travels with the whole family (children and parents).â]
- [**Task clues**: Extracting the userâs goal intent, such as âplanning a family trip,â rather than just âgoing out during summer vacation.â]
- [**User preferences**:
Not only explicit expressions (âI like traveling with my familyâ), but also implicit reasoning patterns.For example, if the user shows a preference for âclear logic in writingâ while asking AI to rate 10 articles, MemOS will preserve this preference pattern for the next 20 article rating tasks, guiding the model to remain consistent.]
 
 
[As a result:]
 
- [**Faster and more accurate retrieval**: Directly locate facts/preferences/tasks instead of parsing a whole raw conversation.]
- [**More efficient invocation**: Only concise memory needs to be passed to the model, reducing token consumption.]
- [**More stable experience**: The model can continuously maintain its understanding of user habits without drifting due to lost context.]
 
 
[**Example**:]
 
```
User: I want to go on a trip during the summer vacation. Can you recommend something?
AI: Sure! Will you be traveling alone or with family and friends?
User: Of course with kids. Our family always travels together.
AI: Got it. So, you travel with both kids and parents, right?
User: Yes, we usually bring the kids and eldersâtraveling as a whole family.
AI: Understood. Iâll recommend destinations suitable for family trips.

```
 
```
Memory: The user usually travels with the whole family (children and parents)
Metadata: timestamp=2025-06-10, source=Conversation Aâ¦

```
 
> For you, this means: as long as you store raw conversations, you donât need to write your own âkeyword extractionâ or âintent recognitionâ logicâyou can directly obtain reusable long-term user preferences.
 
 
## 2. Advanced: If You Want Deep Customization
 
[In MemOS, **memory production** is the full process of converting raw input into schedulable and retrievable memory units. The specific pipeline details (such as extraction methods, embedding models, storage backends) evolve with versions and community practicesâso this section does not provide a fixed unique workflow, but instead explains **extensible components** where you can make adjustments.]
 
<table><thead><tr><th>Extensible Component Examples</th><th>Default Behavior</th><th>Customizable Options</th></tr></thead><tbody><tr><td>Extraction &amp; Structuring</td><td>Generates MemoryItem (including content, timestamp, source)</td><td>Replace the extraction model or template, or add domain-specific fields to schema</td></tr><tr><td>Chunking &amp; Embedding</td><td>System chunks long text and feeds it into embedding models</td><td>Adjust chunking granularity, or replace with better-suited embedding models (e.g., bge, e5)</td></tr><tr><td>Storage Backend</td><td>Defaults to a vector database (e.g., Qdrant)</td><td>Switch to a graph database, or use a hybrid of both</td></tr><tr><td>Merging &amp; Governance</td><td>Automatically handles duplicates and conflicts</td><td>Add custom rules (e.g., time priority, source priority), or governance logic (deduplication, filtering, etc.)</td></tr></tbody></table>
 
 
## 3. Next Steps
 
[Learn more about MemOS core capabilities:]
 
- [[Memory Scheduling](/overview/quick_start/mem_schedule)]
- [[Memory Recall & Instruction Completion](/overview/quick_start/mem_recall)]
- [[Memory Lifecycle Management](/overview/quick_start/mem_lifecycle)]
