---
source_url: https://memos-docs.openmem.net/usecase/financial_assistant
section: Usecase
scraped_date: 2025-10-16
title: Let the Financial Assistant Understand Customer Preferences Behind Behaviors
has_images: no
has_tables: yes
---

# Let the Financial Assistant Understand Customer Preferences Behind Behaviors
 [ With MemOS, user operations and conversational behaviors are abstracted into "memories," enabling the identification and extraction of underlying investment preferences to deliver more personalized services. 
## 1. Overview
 
[In intelligent investment advisory products, users leave behind a large number of **behavioral traces**:]
 
- [**Traffic Source**: Which ad or post did the user click? (e.g., clicked the âRetirement Financeâ ad)]
- [**In-App Operations**: Which fund products did they browse? Which financial products did they bookmark?]
- [**Communication Records**: Conversations with financial advisors and interactions with the AI financial assistant.]
 
[These are just raw behaviors. If stored directly as logs, they are of limited help to large models. **The key is how to abstract behaviors into "memories."**]
 
 
### 1.1 How are behaviors abstracted into memories?
 
<table><thead><tr><th>User Behavior (Raw Trace)</th><th>Corresponding Memory (Semantic Abstraction)</th></tr></thead><tbody><tr><td>Clicked âRetirement Financeâ ad to enter the app</td><td>Memory: âUser has potential interest in retirement financeâ</td></tr><tr><td>Frequently browsed low-risk fund detail pages</td><td>Memory: âUserâs risk preference is conservativeâ</td></tr><tr><td>Bookmarked âlow-risk financial productsâ</td><td>Memory: âUser tends to choose low-risk financial productsâ</td></tr><tr><td>Said in conversation: âI donât want to take too much riskâ</td><td>Memory: âExplicitly expressed low-risk demandâ</td></tr></tbody></table>
 
[When the user later asks, âWhat kind of investment suits me?â, the financial assistant does not need to scan through a pile of logs but instead directly uses these semantic memories to drive the model to generate personalized answers.]
 
 
### 1.2 Why not traditional RAG?
 
[RAG is more suitable for knowledge Q&A, such as explaining âWhat is a bond.â But it does not summarize preferences from user behaviors:]
 
<table><thead><tr><th>Traditional RAG</th><th>MemOS</th></tr></thead><tbody><tr><td>Returns static financial knowledge snippets</td><td>Abstracts user behaviors into semantic memories (interests, preferences, profiles)</td></tr><tr><td>Cannot answer âWhat kind of investment suits me?â</td><td>Can combine memories to generate personalized advice</td></tr></tbody></table>
 
 
### 1.3 Why not build it yourself?
 
[Of course, developers can store behaviors themselves, but they will face three challenges:]
 
- [**Lack of abstraction**: Simply storing âclicked Fund Aâ is not useful; it needs to be transformed into ârisk preference = low risk.â]
- [**Integration complexity**: Before calling the model, developers must manually build prompts by abstracting scattered behaviors into semantic information.]
- [**Poor scalability**: As more channels, products, and communication scenarios are added, the code quickly becomes unmanageable.]
 
 
### 1.4 Why use MemOS?
 
[When making a technology selection, you can directly compare three approaches:]
 
<table><thead><tr><th>Approach</th><th>Characteristics</th><th>Limitations</th><th>Advantages of MemOS</th></tr></thead><tbody><tr><td>Traditional RAG</td><td>Retrieves knowledge base documents</td><td>Does not process user behaviors, cannot build profiles</td><td>Suitable for FAQ, but not for personalized financial advisory</td></tr><tr><td>Self-Built Storage</td><td>Directly stores behavior logs</td><td>Requires manual abstraction from behavior â memory; high prompt engineering cost</td><td>Requires developingå¤§é glue code</td></tr><tr><td>MemOS</td><td>Two interfaces: addMessage for writing, searchMemory for retrieval</td><td>ââ</td><td>Automatically abstracts behavior traces into memories for direct use by the model</td></tr></tbody></table>
 
 
### 1.5 What will this case demonstrate?
 
[This case demonstrates how to use MemOS cloud services to quickly build an intelligent financial assistant that âturns user behaviors into memories.â]
 
[In the demo:]
 
- [**D1 Traffic Behavior**: Clicking the âRetirement Financeâ ad â generates memory âInterest in retirement finance.â]
- [**D2 In-App Behavior**: Browsing and bookmarking low-risk funds â generates memory âRisk preference = low risk.â]
- [**D3 Conversational Behavior**: Saying âI donât want to take risksâ â generates memory âExplicit low-risk demand.â]
 
[When the user asks, âWhat kind of investment suits me?â:]
 
- [`searchMemory` retrieves the above memories]
- [The large model generates an answer that combines these profiles â outputs âMore suitable for low-risk fixed income products.â]
 
[When running this case script, developers will see in the console:]
 
- [Each `addMessage` request/response (behaviors stored)]
- [Each `searchMemory` request/response (semantic memories retrieved)]
- [The modelâs final personalized investment recommendation]
 
 
## 2. Example
 
### 2.1 Environment Setup
 
[Use pip to install required dependencies:]
 
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

class FinancialManagementAssistant:
 """AI financial management assistant with memory capability"""
 
 def __init__(self):
 self.memos_client = MemOSClient(api_key=os.getenv("MEMOS_API_KEY"))
 self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
 
 def search_memory(self, query, user_id, conversation_id):
 """Search relevant memories based on query"""
 response = self.memos_client.search_memory(query, user_id, conversation_id)

 return [memory_detail.memory_value for memory_detail in response.data.memory_detail_list]

 def build_system_prompt(self, memories):
 """Construct a system prompt including formatted memories"""
 base_prompt = """
 You are a knowledgeable and professional financial management assistant.
 You can access conversational memories to help you provide more personalized answers.
 Use memories to understand the userâs background, preferences, and past interactions.
 If memories are provided, naturally reference them when relevant, but do not explicitly mention having memories.
 """

 if memories:
 # Format memories as a numbered list
 formatted_memories = "## Memories:\n"
 for i, memory in enumerate(memories, 1):
 formatted_memories += f"{i}. {memory}\n"
 
 return f"{base_prompt}\n\n{formatted_memories}"
 else:
 return base_prompt
 

 def add_message(self, messages, user_id, conversation_id):
 """Add messages to MemOS so they can be processed into memories"""
 self.memos_client.add_message(messages, user_id, conversation_id)

 def get_message(self, user_id, conversation_id):
 """Retrieve the raw messages stored in MemOS (for debugging/inspection)"""
 response = self.memos_client.get_message(user_id, conversation_id)
 return response.data.message_detail_list

 def chat(self, query, user_id, conversation_id):
 """Main chat function for handling conversations with memory integration"""
 # 1) Search relevant memories
 memories = self.search_memory(query, user_id, conversation_id)
 
 # Build system prompt with memories
 system_prompt = self.build_system_prompt(memories)
 
 # 2) Use OpenAI to generate an answer
 response = self.openai_client.chat.completions.create(
 model="gpt-4o",
 messages=[
 {"role": "system", "content": system_prompt},
 {"role": "user", "content": query}

 )
 answer = response.choices[0].message.content

 # 3) Save the interaction back to MemOS
 messages = [
 {"role": "user", "content": query},
 {"role": "assistant", "content": answer}

 self.memos_client.add_message(messages, user_id, conversation_id)
 
 return answer

ai_assistant = FinancialManagementAssistant()
user_id = "memos_financial_management_user_123"

def demo_questions():
 return [
 "What is my risk preference?",
 "Recommend some investments suitable for me"

def preset_user_behaviors():
 """Show preset user behavior memories"""
 conversation_id = generate_conversation_id()
 print(f"\nð Preset user behavior memoriesï¼conversation_id={conversation_id}ï¼:")
 print("=" * 60)

 behaviors = [{
 "role": "user",
 "content": "Clicked 'Retirement Finance' ad to enter app"
 }, {
 "role": "user",
 "content": "Browsed and bookmarked low-risk funds"
 }]
 
 for i, behavior in enumerate(behaviors, 1):
 print(f"{i}. {behavior['content']}")
 ai_assistant.add_message(behaviors, user_id, conversation_id)
 
 print("=" * 60)
 print("ð¡ The above behavioral memories have been recorded by MemOS. The assistant will provide personalized recommendations based on them.")

def main():
 print("ð° Welcome to see how MemOS is used in a financial management assistant!")
 print("ð¡ With MemOS, your financial assistant becomes smarter and more caring! ð \n")
 
 # Ask whether to preload user behavior memories (consumes 1 add quota)
 while True:
 pre_chat = input("ð¤ Do you want to preload user behavior memories? This will consume 1 add quota. Proceed? (y/n): ").strip().lower()
 
 if pre_chat in ['y', 'yes']:
 preset_user_behaviors()
 break
 elif pre_chat in ['n', 'no']:
 print("ð Starting a new conversation...")
 break
 else:
 print("â ï¸ Please enter 'y' for yes or 'n' for no")

 print("\nâ¡ï¸ Each question you enter next will take place in a brand-new conversation (with a new conversation ID). MemOS will automatically recall your historical behavioral memories across conversations to provide you with continuous and personalized service.") 
 print("\nð¯ Here are some example questions you can continue to ask the assistant:")
 for i, question in enumerate(demo_questions(), 1):
 print(f" {i}. {question}")

 while True:
 user_query = input("\nð¤ Please enter your question (or type 'exit' to quit): ").strip()
 
 if user_query.lower() in ['quit', 'exit', 'q']:
 print("ð Thanks for using the financial management assistant!")
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
 
1. [Set your MemOS API key and OpenAI API key in environment variables]
2. [Instantiate **FinancialManagementAssistant**]
3. [Choose whether to execute preset conversations, which will consume 1 add and 2 search quotas]
4. [Use the `main()` function to interact with the assistant through a conversation loop]
5. [The assistant will call `chat`, first performing a `search` to retrieve memories, then calling OpenAI for conversation, and finally performing an `add` to store memories]
