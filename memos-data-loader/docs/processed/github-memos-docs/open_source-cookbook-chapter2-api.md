---
title: Linux API Version
---

## Scenario Design

**🎯 Problem Scenario:** You are an AI application developer who has learned the basic operations of MemOS and now wants to create a more structured memory system. You find that the basic `TextualMemoryMetadata` functionality is limited and cannot meet the needs of complex scenarios, such as distinguishing between working memory and long-term memory, tracking memory sources, and adding tags and entity information to memories.

**🔧 Solution:** Through this chapter, you will learn to use `TreeNodeTextualMemoryMetadata` to create structured memory, including memory lifecycle management, multi-source tracking, entity tagging and other features, giving your AI application a more intelligent memory system.

## Recipe 2.1: Understanding Core Concepts of TreeNodeTextualMemoryMetadata

**🎯 Problem Scenario:** You want to understand the differences between `TreeNodeTextualMemoryMetadata` and basic metadata, as well as its core functionality.

**🔧 Solution:** Through this recipe, you will master the core concepts and basic structure of `TreeNodeTextualMemoryMetadata`.

### Basic Imports

```python
from memos.memories.textual.item import TextualMemoryItem, TreeNodeTextualMemoryMetadata
```

### Core Concepts

#### 1. Memory Type (memory_type)

- `WorkingMemory`: Working memory, temporary storage
- `LongTermMemory`: Long-term memory, persistent storage  
- `UserMemory`: User memory, personalized storage

#### 2. Memory Status (status)

- `activated`: Activated state
- `archived`: Archived state
- `deleted`: Deleted state

#### 3. Memory Type (type)

- `fact`: Fact
- `event`: Event
- `opinion`: Opinion
- `topic`: Topic
- `reasoning`: Reasoning
- `procedure`: Procedure

## Recipe 2.2: Creating Basic Structured Memory

**🎯 Problem Scenario:** You want to create different types of memory, such as character information, project information, work tasks, etc., and need to set appropriate metadata for each type of memory.

**🔧 Solution:** Through this recipe, you will learn to create various types of structured memory.

### Example 1: Create Simple Character Memory

Create file `create_person_memory_api.py`:

```python
# create_person_memory_api.py
# 🎯 Example of creating character memory (API version)
import os
from dotenv import load_dotenv
from memos.memories.textual.item import TextualMemoryItem, TreeNodeTextualMemoryMetadata

def create_person_memory_api():
    """
    🎯 Example of creating character memory (API version)
    """
    
    print("🚀 Starting to create character memory (API version)...")
    
    # Load environment variables
    load_dotenv()
    
    # Check API configuration
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        raise ValueError("❌ OPENAI_API_KEY not configured. Please configure OpenAI API key in .env file.")
    
    print("✅ Detected OpenAI API mode")
    
    # Get user ID
    user_id = os.getenv("MOS_USER_ID", "default_user")
    
    # Create character memory metadata
    metadata = TreeNodeTextualMemoryMetadata(
        user_id=user_id,
        type="fact",
        source="conversation",
        confidence=90.0,
        memory_type="LongTermMemory",
        key="Zhang_San_Info",
        entities=["Zhang San", "Engineer"],
        tags=["Personnel", "Technical"]
    )

    # Create memory item
    memory_item = TextualMemoryItem(
        memory="Zhang San is a senior engineer in our company, specializing in Python and machine learning",
        metadata=metadata
    )

    print(f"Memory content: {memory_item.memory}")
    print(f"Memory key: {memory_item.metadata.key}")
    print(f"Memory type: {memory_item.metadata.memory_type}")
    print(f"Tags: {memory_item.metadata.tags}")
    print(f"🎯 Configuration mode: OPENAI API")
    
    return memory_item

if __name__ == "__main__":
    create_person_memory_api()
```

Run command:

```bash
cd test_cookbook/chapter2/API/2
python create_person_memory_api.py
```

### Example 2: Create Project Memory

Create file `create_project_memory_api.py`:

```python
# create_project_memory_api.py
# 🎯 Example of creating project memory (API version)
import os
from dotenv import load_dotenv
from memos.memories.textual.item import TextualMemoryItem, TreeNodeTextualMemoryMetadata

def create_project_memory_api():
    """
    🎯 Example of creating project memory (API version)
    """
    
    print("🚀 Starting to create project memory (API version)...")
    
    # Load environment variables
    load_dotenv()
    
    # Check API configuration
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        raise ValueError("❌ OPENAI_API_KEY not configured. Please configure OpenAI API key in .env file.")
    
    print("✅ Detected OpenAI API mode")
    
    # Get user ID
    user_id = os.getenv("MOS_USER_ID", "default_user")
    
    # Create project memory metadata
    project_metadata = TreeNodeTextualMemoryMetadata(
        user_id=user_id,
        type="fact",
        source="file",
        confidence=95.0,
        memory_type="LongTermMemory",
        key="AI_Project_Details",
        entities=["AI Project", "Machine Learning"],
        tags=["Project", "AI", "Important"],
        sources=["Project Documentation", "Meeting Records"]
    )

    # Create memory item
    project_memory = TextualMemoryItem(
        memory="AI Project is an intelligent customer service system using the latest NLP technology, expected to be completed in 6 months",
        metadata=project_metadata
    )

    print(f"Project memory: {project_memory.memory}")
    print(f"Sources: {project_memory.metadata.sources}")
    print(f"🎯 Configuration mode: OPENAI API")
    
    return project_memory

if __name__ == "__main__":
    create_project_memory_api() 
```

Run command:

```bash
python create_project_memory_api.py
```

### Example 3: Create Work Memory

Create file `create_work_memory_api.py`:

```python
# create_work_memory_api.py
# 🎯 Example of creating work memory (API version)
import os
from dotenv import load_dotenv
from memos.memories.textual.item import TextualMemoryItem, TreeNodeTextualMemoryMetadata

def create_work_memory_api():
    """
    🎯 Example of creating work memory (API version)
    """
    
    print("🚀 Starting to create work memory (API version)...")
    
    # Load environment variables
    load_dotenv()
    
    # Check API configuration
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        raise ValueError("❌ OPENAI_API_KEY not configured. Please configure OpenAI API key in .env file.")
    
    print("✅ Detected OpenAI API mode")
    
    # Get user ID
    user_id = os.getenv("MOS_USER_ID", "default_user")
    
    # Create work memory metadata
    work_metadata = TreeNodeTextualMemoryMetadata(
        user_id=user_id,
        type="procedure",
        source="conversation",
        confidence=80.0,
        memory_type="WorkingMemory",  # Working memory
        key="Today_Tasks",
        tags=["Tasks", "Today"]
    )

    # Create memory item
    work_memory = TextualMemoryItem(
        memory="Today need to complete code review, team meeting, and prepare tomorrow's presentation",
        metadata=work_metadata
    )

    print(f"Work memory: {work_memory.memory}")
    print(f"Memory type: {work_memory.metadata.memory_type}")
    print(f"🎯 Configuration mode: OPENAI API")
    
    return work_memory

if __name__ == "__main__":
    create_work_memory_api() 
```

Run command:

```bash
python create_work_memory_api.py
```

## Recipe 2.3: Common Field Descriptions and Configuration

**🎯 Problem Scenario:** You need to understand all available fields of `TreeNodeTextualMemoryMetadata` and how to configure them correctly.

**🔧 Solution:** Through this recipe, you will master the meaning and configuration methods of all fields.

### Common Field Descriptions

| Field | Type | Description | Example |
| --- | --- | --- | --- |
| `user_id` | str | User ID | "user123" |
| `type` | str | Memory type | "fact", "event" |
| `source` | str | Source | "conversation", "file" |
| `confidence` | float | Confidence (0-100) | 90.0 |
| `memory_type` | str | Memory lifecycle type | "LongTermMemory" |
| `key` | str | Memory key/title | "Important Info" |
| `entities` | list | Entity list | ["Zhang San", "Project"] |
| `tags` | list | Tag list | ["Important", "Technical"] |
| `sources` | list | Multi-source list | ["Document", "Meeting"] |

## Recipe 2.4: Practical Application - Create Memory and Add to MemCube

**🎯 Problem Scenario:** You have learned to create structured memory and now want to add these memories to MemCube for querying and management.

**🔧 Solution:** Through this recipe, you will learn how to integrate structured memory into MemCube and implement complete memory management workflow.

Create file `memcube_with_structured_memories_api.py`:

```python
# memcube_with_structured_memories_api.py
# 🎯 Complete example of adding structured memory to MemCube (API version)
import os
from dotenv import load_dotenv
from memos.mem_cube.general import GeneralMemCube
from memos.configs.mem_cube import GeneralMemCubeConfig
from memos.memories.textual.item import TextualMemoryItem, TreeNodeTextualMemoryMetadata

def create_memcube_config_api():
    """
    🎯 Create MemCube configuration (API version)
    """
    
    print("🔧 Creating MemCube configuration (API version)...")
    
    # Load environment variables
    load_dotenv()
    
    # Check API configuration
    openai_key = os.getenv("OPENAI_API_KEY")
    openai_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
    
    if not openai_key:
        raise ValueError("❌ OPENAI_API_KEY not configured. Please configure OpenAI API key in .env file.")
    
    print("✅ Detected OpenAI API mode")
    
    # Get configuration
    user_id = os.getenv("MOS_USER_ID", "default_user")
    top_k = int(os.getenv("MOS_TOP_K", "5"))
    
    # OpenAI mode configuration
    config = GeneralMemCubeConfig(
        user_id=user_id,
        cube_id=f"{user_id}_structured_memories_cube",
        text_mem={
            "backend": "general_text",
            "config": {
                "extractor_llm": {
                    "backend": "openai",
                    "config": {
                        "model_name_or_path": "gpt-3.5-turbo",
                        "api_key": openai_key,
                        "api_base": openai_base,
                        "temperature": 0.1,
                        "max_tokens": 1024,
                    }
                },
                "embedder": {
                    "backend": "universal_api",
                    "config": {
                        "provider": "openai",
                        "api_key": openai_key,
                        "model_name_or_path": "text-embedding-ada-002",
                        "base_url": openai_base,
                    }
                },
                "vector_db": {
                    "backend": "qdrant",
                    "config": {
                        "collection_name": f"{user_id}_structured_memories",
                        "vector_dimension": 1536,
                        "distance_metric": "cosine"
                    }
                }
            }
        },
        act_mem={"backend": "uninitialized"},
        para_mem={"backend": "uninitialized"}
    )
    
    return config

def create_structured_memories_api():
    """
    🎯 Complete example of adding structured memory to MemCube (API version)
    """
    
    print("🚀 Starting to create structured memory MemCube (API version)...")
    
    # Create MemCube configuration
    config = create_memcube_config_api()
    
    # Create MemCube
    mem_cube = GeneralMemCube(config)
    
    print("✅ MemCube created successfully!")
    print(f"  📊 User ID: {mem_cube.config.user_id}")
    print(f"  📊 MemCube ID: {mem_cube.config.cube_id}")
    print(f"  📊 Text memory backend: {mem_cube.config.text_mem.backend}")
    print(f"  🔍 Embedding model: text-embedding-ada-002 (OpenAI)")
    print(f"  🎯 Configuration mode: OPENAI API")
    
    # Create multiple memory items
    memories = []

    # Memory 1: Character information
    person_metadata = TreeNodeTextualMemoryMetadata(
        user_id=mem_cube.config.user_id,
        type="fact",
        source="conversation",
        confidence=90.0,
        memory_type="LongTermMemory",
        key="Li_Si_Info",
        entities=["Li Si", "Designer"],
        tags=["Personnel", "Design"]
    )

    memories.append({
        "memory": "Li Si is our UI designer with 5 years of experience, specializing in user interface design",
        "metadata": person_metadata
    })

    # Memory 2: Project information
    project_metadata = TreeNodeTextualMemoryMetadata(
        user_id=mem_cube.config.user_id,
        type="fact",
        source="file",
        confidence=95.0,
        memory_type="LongTermMemory",
        key="Mobile_App_Project",
        entities=["Mobile App", "Development"],
        tags=["Project", "Mobile", "Important"]
    )

    memories.append({
        "memory": "Mobile app project is in progress, expected to be completed in 3 months, team has 8 people",
        "metadata": project_metadata
    })

    # Memory 3: Work memory
    work_metadata = TreeNodeTextualMemoryMetadata(
        user_id=mem_cube.config.user_id,
        type="procedure",
        source="conversation",
        confidence=85.0,
        memory_type="WorkingMemory",
        key="This_Week_Tasks",
        tags=["Tasks", "This Week"]
    )

    memories.append({
        "memory": "This week need to complete requirements analysis, prototype design, and technology selection",
        "metadata": work_metadata
    })

    # Add to MemCube
    mem_cube.text_mem.add(memories)

    print("✅ Successfully added 3 memory items to MemCube")

    # Query memories
    print("\n🔍 Query all memories:")
    all_memories = mem_cube.text_mem.get_all()
    for i, memory in enumerate(all_memories, 1):
        print(f"{i}. {memory.memory}")
        print(f"   Key: {memory.metadata.key}")
        print(f"   Type: {memory.metadata.memory_type}")
        print(f"   Tags: {memory.metadata.tags}")
        print()

    # Search specific memories
    print("🔍 Search memories containing 'Li Si':")
    search_results = mem_cube.text_mem.search("Li Si", top_k=2)
    for result in search_results:
        print(f"- {result.memory}")
    
    return mem_cube

if __name__ == "__main__":
    create_structured_memories_api() 
```

Run command:

```bash
cd test_cookbook/chapter2/API/4
python memcube_with_structured_memories_api.py
```

## Common Problems and Solutions

**Q1: How to choose appropriate memory_type?**

```python
# 🔧 Choose based on memory importance
if is_important:
    memory_type = "LongTermMemory"  # Long-term storage
elif is_temporary:
    memory_type = "WorkingMemory"   # Temporary storage
else:
    memory_type = "UserMemory"      # Personalized storage
```

**Q2: How to set appropriate confidence value?**

```python
# 🔧 Set based on information source reliability
if source == "verified_document":
    confidence = 95.0
elif source == "conversation":
    confidence = 80.0
elif source == "web_search":
    confidence = 70.0
```

**Q3: How to effectively use tags and entities?**

```python
# 🔧 Use meaningful tags and entities
tags = ["Project", "Technical", "Important"]  # Easy for categorization and retrieval
entities = ["Zhang San", "AI Project"]    # Easy for entity recognition and association
``` 