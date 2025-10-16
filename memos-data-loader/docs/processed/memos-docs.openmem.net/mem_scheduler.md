---
source_url: https://memos-docs.openmem.net/open_source/modules/mem_scheduler
section: Mos
scraped_date: 2025-10-16
title: MemScheduler: The Scheduler for Memory Organization
has_images: no
has_tables: yes
---

# MemScheduler: The Scheduler for Memory Organization
 [ `MemScheduler` is a concurrent memory management system parallel running with the MemOS system, which coordinates memory operations between working memory, long-term memory, and activation memory in AI systems. It handles memory retrieval, updates, and compaction through event-driven scheduling. 
 This system is particularly suited for conversational agents and reasoning systems requiring dynamic memory management. 
## Key Features
 
- [ð **Concurrent operation** with MemOS system]
- [ð§  **Multi-memory coordination** (Working/Long-Term/User memory)]
- [â¡ **Event-driven scheduling** for memory operations]
- [ð **Efficient retrieval** of relevant memory items]
- [ð **Comprehensive monitoring** of memory usage]
- [ð **Detailed logging** for debugging and analysis]
- []
 
## Memory Scheduler Architecture
 
[The `MemScheduler` system is structured around several key components:]
 
1. [**Message Handling**: Processes incoming messages through a dispatcher with labeled handlers]
2. [**Memory Management**: Manages different memory types (Working, Long-Term, User)]
3. [**Retrieval System**: Efficiently retrieves relevant memory items based on context]
4. [**Monitoring**: Tracks memory usage, frequencies, and triggers updates]
5. [**Dispatcher (Router)**: Trigger different memory reorganization strategies by checking messages from MemOS systems.]
6. [**Logging**: Maintains logs of memory operations for debugging and analysis]
 
## Message Processing
 
[The scheduler processes messages through a dispatcher with dedicated handlers:]
 
### Message Types
 
<table><thead><tr><th>Message Type</th><th>Handler Method</th><th>Description</th></tr></thead><tbody><tr><td>QUERY_LABEL</td><td>_query_message_consume</td><td>Handles user queries and triggers retrieval</td></tr><tr><td>ANSWER_LABEL</td><td>_answer_message_consume</td><td>Processes answers and updates memory usage</td></tr></tbody></table>
 
### Schedule Message Structure
 
[The scheduler processes messages from its queue using the following format:]
 
[ScheduleMessageItem:]
 
<table><thead><tr><th>Field</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td>item_id</td><td>str</td><td>UUID (auto-generated) for unique identification</td></tr><tr><td>user_id</td><td>str</td><td>Identifier for the associated user</td></tr><tr><td>mem_cube_id</td><td>str</td><td>Identifier for the memory cube</td></tr><tr><td>label</td><td>str</td><td>Message label (e.g., QUERY_LABEL, ANSWER_LABEL)</td></tr><tr><td>mem_cube</td><td>GeneralMemCubeï½str</td><td>Memory cube object or reference</td></tr><tr><td>content</td><td>str</td><td>Message content</td></tr><tr><td>timestamp</td><td>datetime</td><td>Time when the message was submitted</td></tr></tbody></table>
 
[Meanwhile the scheduler will send the scheduling messages by following structures.]
 
[ScheduleLogForWebItem:]
 
<table><thead><tr><th>Field</th><th>Type</th><th>Description</th><th>Default Value</th></tr></thead><tbody><tr><td>item_id</td><td>str</td><td>Unique log entry identifier (UUIDv4)</td><td>Auto-generated (uuid4())</td></tr><tr><td>user_id</td><td>str</td><td>Associated user identifier</td><td>(Required)</td></tr><tr><td>mem_cube_id</td><td>str</td><td>Linked memory cube ID</td><td>(Required)</td></tr><tr><td>label</td><td>str</td><td>Log category identifier</td><td>(Required)</td></tr><tr><td>from_memory_type</td><td>str</td><td>Source memory partitionPossible values:- "LongTermMemory"- "UserMemory"- "WorkingMemory"</td><td>(Required)</td></tr><tr><td>to_memory_type</td><td>str</td><td>Destination memory partition</td><td>(Required)</td></tr><tr><td>log_content</td><td>str</td><td>Detailed log message</td><td>(Required)</td></tr><tr><td>current_memory_sizes</td><td>MemorySizes</td><td>Current memory utilization</td><td>DEFAULT_MEMORY_SIZES = { "long_term_memory_size": -1, "user_memory_size": -1, "working_memory_size": -1, "transformed_act_memory_size": -1}</td></tr><tr><td>memory_capacities</td><td>MemoryCapacities</td><td>Memory partition limits</td><td>DEFAULT_MEMORY_CAPACITIES = { "long_term_memory_capacity": 10000, "user_memory_capacity": 10000, "working_memory_capacity": 20, "transformed_act_memory_capacity": -1}</td></tr><tr><td>timestamp</td><td>datetime</td><td>Log creation time</td><td>Auto-set (datetime.now)</td></tr></tbody></table>
 
## Execution Example
 
[`examples/mem_scheduler/schedule_w_memos.py` is a demonstration script showcasing how to utilize the `MemScheduler` module. It illustrates memory management and retrieval within conversational contexts.]
 
### Code Functionality Overview
 
[This script demonstrates two methods for initializing and using the memory scheduler:]
 
1. [**Automatic Initialization**: Configures the scheduler via configuration files]
2. [**Manual Initialization**: Explicitly creates and configures scheduler components]
 
[The script simulates a pet-related conversation between a user and an assistant, demonstrating how memory scheduler manages conversation history and retrieves relevant information.]
