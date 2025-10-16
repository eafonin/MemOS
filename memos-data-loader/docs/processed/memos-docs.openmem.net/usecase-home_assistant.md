---
source_url: https://memos-docs.openmem.net/usecase/home_assistant
section: Usecase
scraped_date: 2025-10-16
title: Building a Home Life Assistant with Memory
has_images: no
has_tables: yes
---

# Building a Home Life Assistant with Memory
 [ With the support of MemOS, a home assistant can connect daily chores and long-term plans, quickly understanding and responding to the userâs real needs. 
## 1. Overview
 
[When developing a home life assistant product, developers often encounter a problem: **once the dialogue context ends, user information is lost**.]
 
- [User casually assigns a to-do (âTake the kids to the zoo on Saturdayâ)]
- [User expresses a habit (âWhen reminding, first list the key points, then give one action suggestionâ)]
- [User introduces family information (âMy wife is Xiaoyun, the child is 6 years oldâ)]
 
[If the assistant cannot remember this information, it will appear âheartlessâ: the next day when the user asks, âWhat plans do I have for the weekend?â, the assistant will have no idea what they are referring to.]
 
 
### 1.1 Why not traditional RAG?
 
[Many peopleâs first thought is: can we use RAG (Retrieval-Augmented Generation)?
But the characteristics of traditional RAG determine that it is not suitable for this kind of âpersonalized assistantâ scenario:]
 
<table><thead><tr><th>Traditional RAG</th><th>MemOS</th></tr></thead><tbody><tr><td>Relies on static knowledge bases, requiring manual document maintenance</td><td>Information generated during dialogue can be directly written in, no extra maintenance needed</td></tr><tr><td>Can only mechanically return fragments, does not learn preferences</td><td>Automatically forms to-do items, preferences, and profiles from conversations</td></tr><tr><td>Focuses on âcommon knowledgeâ, unsuitable for personal information</td><td>Designed for individualized scenarios, supports long-term tracking and invocation</td></tr></tbody></table>
 
 
### 1.2 Why not build your own solution?
 
[Of course, you could try to store this information yourself, but this brings several challenges:]
 
- [**Complex storage and retrieval logic**: must distinguish dialogue content, long-term memory, preferences, and facts, and ensure they can be retrieved as needed.]
- [**Troublesome integration with LLMs**: not only storing data, but also embedding relevant information into the prompt before generating responses.]
- [**Poor scalability**: as features increase (to-dos, preferences, profiles), the code becomes increasingly hard to maintain.]
 
 
### 1.3 Why use MemOS?
 
[When making a technical choice, you can intuitively compare three approaches:]
 
<table><thead><tr><th>Approach</th><th>Characteristics</th><th>Limitations</th><th>Advantages of MemOS</th></tr></thead><tbody><tr><td>Traditional RAG</td><td>Retrieves documents from a vector database and appends them into the prompt</td><td>Requires manual static document maintenance; cannot store personal to-dos/preferences; only mechanically returns fragments</td><td>Automatically captures key information from dialogues, supports personalization and dynamic updates</td></tr><tr><td>Self-built storage solution</td><td>Custom tables/cache to save dialogue information</td><td>Complex logic: must distinguish dialogues/long-term memory/preferences/profiles; still need to manually build prompt before model calls; poor scalability</td><td>MemOS encapsulates storage + retrieval + prompt injection, reducing developer burden</td></tr><tr><td>MemOS</td><td>Only two interfaces: addMessage for writing, searchMemory for retrieval</td><td>ââ</td><td>Supports long-term tracking, preference retention, and profile integration; ready-to-use and easily extendable</td></tr></tbody></table>
 
[Only two API calls are needed:]
 
- [`addMessage`: writes user or assistant messages into the system]
- [`searchMemory`: retrieves relevant memories before model response and injects them into the prompt]
 
[With this, the assistant can truly appear âwith memoryâ:]
 
- [**Track to-dos**User says âTake the kids to the zoo on SaturdayâA few days later asks âWhat plans do I have for the weekend?â â Assistant can answer accurately]
- [**Maintain preferences** (future versions will support more fine-grained instruction completion)User says âWhen reminding, first list three key points + one short suggestionâLater asks âHelp me plan next weekâs housework distributionâ â Assistant outputs in the preferred style]
- [**Incorporate profiles**User says âMy wife is Xiaoyun, the child is 6 years oldâLater asks âArrange a weekend activity for the family?â â Suggests a family-friendly activity plan]
 
 
### 1.4 What does this case demonstrate?
 
[We will use MemOS cloud service to quickly implement a home life assistant âthat remembers the user.â
When running the example script, developers will see complete logs:]
 
- [Requests/responses for each `addMessage` and `searchMemory` call]
- [Matched memory entries]
- [Concatenated and full instructions â TODO: coming soon]
- [Model responses (if LLM is not connected, a message will indicate LLM not connected)]
 
 
## 2. Example
 
### 2.1 Environment Setup
 
[Install required dependencies with pip:]
 
```
pip install MemoryOS -U

```
 
 
### 2.2 Full Code
 
```
import os
import uuid
from openai import OpenAI
from memos.api.client import MemOSClient

os.environ["MEMOS_API_KEY"] = "mpg-xx" # Get MemOS_API_KEY from cloud service console
os.environ["OPENAI_API_KEY"] = "sk-xx" # Replace with your own API_KEY

conversation_counter = 0

def generate_conversation_id():
 global conversation_counter
 conversation_counter += 1
 return f"conversation_{conversation_counter:03d}"

class HomeAssistant: 
 def __init__(self):
 self.memos_client = MemOSClient(api_key=os.getenv("MEMOS_API_KEY"))
 self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
 
 def search_memory(self, query, user_id, conversation_id):
 """Search relevant memories based on query"""
 response = self.memos_client.search_memory(query, user_id, conversation_id)

 return [memory_detail.memory_value for memory_detail in response.data.memory_detail_list]

 def add_message(self, messages, user_id, conversation_id):
 """Add messages to MemOS so they can be processed into memories"""
 self.memos_client.add_message(messages, user_id, conversation_id)

 def get_message(self, user_id, conversation_id):
 """Retrieve the raw messages stored in MemOS (for debugging/inspection)"""
 response = self.memos_client.get_message(user_id, conversation_id)
 
 return response.data.message_detail_list

 def build_system_prompt(self, memories):
 """Builds a system prompt containing formatted memories"""
 base_prompt = """
 You are a knowledgeable and considerate home life assistant.
 You can leverage conversation memories to provide more personalized responses.
 Use these memories to understand the userâs context, preferences, and past interactions.
 If memory content is provided, naturally reference it when relevant, but do not explicitly state you have memory functions.
 """

 if memories:
 # Format memories as a numbered list
 formatted_memories = "## Memories:\n"
 for i, memory in enumerate(memories, 1):
 formatted_memories += f"{i}. {memory}\n"
 
 return f"{base_prompt}\n\n{formatted_memories}"
 else:
 return base_prompt
 

 def chat(self, query, user_id, conversation_id):
 """Main chat function handling memory-integrated conversation"""
 # 1. Search relevant memories
 memories = self.search_memory(query, user_id, conversation_id)
 
 # Build system prompt including memories
 system_prompt = self.build_system_prompt(memories)
 
 # 2. Use OpenAI to generate response
 response = self.openai_client.chat.completions.create(
 model="gpt-4o",
 messages=[
 {"role": "system", "content": system_prompt},
 {"role": "user", "content": query}

 )
 answer = response.choices[0].message.content

 # 3. Save dialogue into memory
 messages = [
 {"role": "user", "content": query},
 {"role": "assistant", "content": answer}

 self.memos_client.add_message(messages, user_id, conversation_id)
 
 return answer

ai_assistant = HomeAssistant()
user_id = "memos_home_management_user_123"

def demo_questions():
 return [
 "What plans do I have for the weekend?",
 "Help me plan next weekâs housework distribution"

def pre_configured_conversations():
 """Return pre-configured dialogue pairs"""
 return [
 {
 "user": "Take the kids to the zoo on Saturday, please remember it.",
 },
 {
 "user": "For future reminders or plans, please first list three key points, then add one short suggestion.",
 }

def execute_pre_conversations():
 """Execute pre-configured dialogues"""
 conversations = pre_configured_conversations()
 conversation_id = generate_conversation_id()

 print(f"\nð Executing pre-configured dialoguesï¼conversation_id={conversation_id}ï¼...")
 print("=" * 60)
 
 for i, conv in enumerate(conversations, 1):
 print(f"\nð¬ Dialogue {i}")
 print(f"ð¤ User: {conv['user']}")
 
 # Execute dialogue
 answer = ai_assistant.chat(conv['user'], user_id, conversation_id)
 print(f"ð¤ Assistant: {answer}")
 print("-" * 40)
 
 print("\nâ Pre-configured dialogues completed!")
 print("=" * 60)

def main(): 
 print("ð  Welcome to the example of MemOS applied in a home assistant!")
 print("ð¡ With the power of MemOS, your product can deliver a real butler-like experience! ð \n")
 
 # Ask whether to execute pre-configured dialogues first
 while True:
 pre_chat = input("ð¤ Would you like to execute the pre-configured dialogues first? This will consume 2 add calls and 2 search calls. Proceed? (y/n): ").strip().lower()
 
 if pre_chat in ['y', 'yes']:
 execute_pre_conversations()
 break
 elif pre_chat in ['n', 'no']:
 print("ð Starting a new dialogue...")
 break
 else:
 print("â ï¸ Please enter 'y' for yes or 'n' for no")

 print("\nâ¡ï¸ Each question you enter next will take place in a brand-new conversation (with a new conversation ID). MemOS will automatically recall your historical behavioral memories across conversations to provide you with continuous and personalized service.")
 print("\nð¯ Here are some sample questions you can continue to ask the assistant:")
 for i, question in enumerate(demo_questions(), 1):
 print(f" {i}. {question}")

 while True:
 user_query = input("\nð¤ Please enter your question (or type 'exit' to quit): ").strip()
 
 if user_query.lower() in ['quit', 'exit', 'q']:
 print("ð Thank you for using the home assistant!")
 break
 
 if not user_query:
 continue
 
 print("ð¤ Processing...")
 conversation_id = generate_conversation_id()
 answer = ai_assistant.chat(user_query, user_id, conversation_id)
 print(f"\nð¬ conversation_id: {conversation_id}\nð¡ [Assistant]: {answer}\n")
 print("-" * 60)

if __name__ == "__main__":
 main()

```
 
 
### 2.3 Code Explanation
 
1. [Set your MemOS API key and OpenAI key in environment variables]
2. [Instantiate `HomeAssistant`]
3. [Choose whether to run pre-configured dialogues (consumes 2 add calls and 2 search calls)]
4. [Use the `main()` function to interact with the assistant in a dialogue loop]
5. [The assistant calls `chat`, first performing `search` to retrieve memories, then using OpenAI for conversation, and finally performing `add` to store the memory]
