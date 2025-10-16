---
source_url: https://memos-docs.openmem.net/dashboard/quick_start
section: Dashboard
scraped_date: 2025-10-16
title: Quick Start
has_images: yes
has_tables: no
---

# Quick Start
 [ Welcome to the MemOS Cloud Platform. Refer to this quick start guide to easily integrate memory capabilities. Youâll need to complete the following steps. 
## 1. Get Your API Key
 
[Register and log in to the [[MemOS Cloud Platform](https://memos-dashboard.openmem.net/quickstart)]. A default project will be created for you automatically. Copy the default API Key from the console.] ![image](./IMAGES/dashboard-quick_start-fa6579bf-8915-49e6-a63c-b4b6f8f6e944-1) ## 2. Core Memory Operations
 
### 2.1 Add Original Messages
 
[**Conversation A: Occurred on 2025-06-10**
Simply provide the **raw conversation records** to MemOS. MemOS will `automatically abstract, process, and save them as memory`.] [ Python (HTTP) Python (SDK) Curl [ 
```
import os
import requests
import json

# Replace with your API Key
os.environ["MEMOS_API_KEY"] = "YOUR_API_KEY"
os.environ["MEMOS_BASE_URL"] = "https://memos.memtensor.cn/api/openmem/v1"

data = {
 "messages": [
 {"role": "user", "content": "I want to travel during summer vacation, can you recommend something?"},
 {"role": "assistant", "content": "Sure! Are you traveling alone, with family or with friends?"},
 {"role": "user", "content": "Iâm bringing my kid. My family always travels together."},
 {"role": "assistant", "content": "Got it, so youâre traveling with your children as a family, right?"},
 {"role": "user", "content": "Yes, with both kids and elderly, we usually travel as a whole family."},
 {"role": "assistant", "content": "Understood, Iâll recommend destinations suitable for family trips."}
 ],
 "user_id": "memos_user_123",
 "conversation_id": "0610"
}
headers = {
 "Content-Type": "application/json",
 "Authorization": f"Token {os.environ['MEMOS_API_KEY']}"
}
url = f"{os.environ['MEMOS_BASE_URL']}/add/message"

res = requests.post(url=url, headers=headers, data=json.dumps(data))

print(f"result: {res.json()}")

```
 
```
# Please ensure that MemOS has been installed (pip install MemoryOS -U)
from memos.api.client import MemOSClient

# Initialize MemOS client with API Key to start sending requests
client = MemOSClient(api_key="YOUR_API_KEY")

messages = [
 {"role": "user", "content": "I want to travel during summer vacation, can you recommend something?"},
 {"role": "assistant", "content": "Sure! Are you traveling alone, with family or with friends?"},
 {"role": "user", "content": "Iâm bringing my kid. My family always travels together."},
 {"role": "assistant", "content": "Got it, so youâre traveling with your children as a family, right?"},
 {"role": "user", "content": "Yes, with both kids and elderly, we usually travel as a whole family."},
 {"role": "assistant", "content": "Understood, Iâll recommend destinations suitable for family trips."}
]
user_id = "memos_user_123"
conversation_id = "0610"

res = client.add_message(messages=messages, user_id=user_id, conversation_id=conversation_id)

print(f"result: {res}")

```
 
```
curl --request POST \
 --url https://memos.memtensor.cn/api/openmem/v1/add/message \
 --header 'Authorization: Token YOUR_API_KEY' \
 --header 'Content-Type: application/json' \
 --data '{
 "user_id": "memos_user_123",
 "conversation_id": "0610",
 "messages": [
 {"role":"user","content":"I want to travel during summer vacation, can you recommend something?"},
 {"role":"assistant","content":"Sure! Are you traveling alone, with family or with friends?"},
 {"role":"user","content":"I'\''m bringing my kid. My family always travels together."},
 {"role":"assistant","content":"Got it, so you'\''re traveling with your children as a family, right?"},
 {"role":"user","content":"Yes, with both kids and elderly, we usually travel as a whole family."},
 {"role":"assistant","content":"Understood, I'\''ll recommend destinations suitable for family trips."}

 }'

```
```
{
 "code": 0,
 "data": {
 "success": true
 },
 "message": "ok"
}

```
 
 
 
### 2.2 Search Memory
 
[**Conversation A: Occurred on 2025-09-28**
Use the user's utterance to search memory, and MemOS will automatically retrieve the most relevant memories for the AI to reference.]
 
> MemOS supports returningmatches,instruction(coming soon), andfull_instruction(coming soon). In practice, you only need to choose one according to your business needs.
 
> Need full controlâ usematches, which only returns memory entries, and developers manually stitch them into instructions.Want to save stitching work but still need to apply business rulesâ useinstruction, where the system has already combined memories with the userâs query into a semi-finished instruction, which developers can further refine.Pursue one-click direct connectionâ usefull_instruction, where the system generates a complete terminal instruction that can be directly sent to the LLM.
 
> Why this design: Most memory systems stop at ârecalling facts,â but facts do not equal an executable Prompt. MemOSâs unique instruction completion workflow saves you from complex stitching and fine-tuning, turning memories into prompts that the model can directly understand and execute. [ Python (HTTP) Python (SDK) Curl [ 
```
import os
import requests
import json

# Replace with your API Key
os.environ["MEMOS_API_KEY"] = "YOUR_API_KEY"
os.environ["MEMOS_BASE_URL"] = "https://memos.memtensor.cn/api/openmem/v1"

data = {
 "query": "Any suggestions for where to go during National Day?",
 "user_id": "memos_user_123",
 "conversation_id": "0928"
}

# MemOS will support returning matches, instruction, and full_instruction in the future:
# "return_matches": true
# "return_instruction": true
# "return_full_instruction": true

headers = {
 "Content-Type": "application/json",
 "Authorization": f"Token {os.environ['MEMOS_API_KEY']}"
}
url = f"{os.environ['MEMOS_BASE_URL']}/search/memory"

res = requests.post(url=url, headers=headers, data=json.dumps(data))

print(f"result: {res.json()}")

```
 
```
# Please ensure that MemOS has been installed (pip install MemoryOS -U)
from memos.api.client import MemOSClient

# Initialize MemOS client with API Key to start sending requests
client = MemOSClient(api_key="YOUR_API_KEY")

query = "Any suggestions for where to go during National Day?"
user_id = "memos_user_123"
conversation_id ="0928"

# MemOS will support returning matches, instruction, and full_instruction in the future:
# return_matches = True
# return_instruction = True
# return_full_instruction = True

res = client.search_memory(query=query, user_id=user_id, conversation_id=conversation_id)

print(f"result: {res}")

```
 
```
curl --request POST \
 --url https://memos.memtensor.cn/api/openmem/v1/search/memory \
 --header 'Authorization: Token YOUR_API_KEY' \
 --header 'Content-Type: application/json' \
 --data '{
 "query": "Any suggestions for where to go during National Day?",
 "user_id": "memos_user_123",
 "conversation_id": "0928"
 }'

```
```
{
 "code": 0,
 "data": {
 "memory_detail_list": [
 {
 "id": "0a89db3a-2061-4c97-a1b8-45700f8745bc",
 "memory_key": "Summer Family Trip Plan",
 "memory_value": "[user perspective] The user plans a family trip during the summer vacation, bringing along children and elderly family members, traveling together as a whole family.",
 "memory_type": "WorkingMemory",
 "memory_time": null,
 "conversation_id": "0610",
 "status": "activated",
 "confidence": 0.0,
 "tags": [
 "summer vacation",
 "family trip",
 "plan"
 ],
 "update_time": 1758095885922,
 "relativity": 0.007873535
 },
 {
 "id": "c8b41a89-83b3-4512-b4f7-1dfca3570107",
 "memory_key": "Family Trip Requirements",
 "memory_value": "[assistant perspective] The assistant understands that the user will travel with family, including children and elderly, and plans to recommend destinations suitable for family trips.",
 "memory_type": "WorkingMemory",
 "memory_time": null,
 "conversation_id": "0610",
 "status": "activated",
 "confidence": 0.0,
 "tags": [
 "family trip",
 "recommendation"
 ],
 "update_time": 1758095885923,
 "relativity": 0.0019950867
 }
 ],
 "message_detail_list": null
 },
 "message": "ok"
}

```
 
 
### 2.3 Get Original Messages
 
[Retrieve the **original conversation messages** for a specified user and conversati] [ Python (HTTP) Python (SDK) Curl [ 
```
import os
import requests
import json

# Replace with your API Key
os.environ["MEMOS_API_KEY"] = "YOUR_API_KEY"
os.environ["MEMOS_BASE_URL"] = "https://memos.memtensor.cn/api/openmem/v1"

data = {
 "user_id": "memos_user_123",
 "conversation_id": "0610"
}
headers = {
 "Content-Type": "application/json",
 "Authorization": f"Token {os.environ['MEMOS_API_KEY']}"
}
url = f"{os.environ['MEMOS_BASE_URL']}/get/message"

res = requests.post(url=url, headers=headers, data=json.dumps(data))

print(f"result: {res.json()}")

```
 
```
# Please ensure that MemoS has been installed (pip install MemoryOS -U).
from memos.api.client import MemOSClient

# Initialize MemOS client with API Key to start sending requests
client = MemOSClient(api_key="YOUR_API_KEY")

user_id = "memos_user_123"
conversation_id = "0610"

res = client.get_message(user_id=user_id, conversation_id=conversation_id)

print(f"result: {res}")

```
 
```
curl --request POST \
 --url https://memos.memtensor.cn/api/openmem/v1/get/message \
 --header 'Authorization: Token YOUR_API_KEY' \
 --header 'Content-Type: application/json' \
 --data '{
 "user_id": "memos_user_123",
 "conversation_id": "0610"
 }'

```
```
{
 "code": 0,
 "data": {
 "message_detail_list": [
 {
 "role": "user",
 "content": "I want to travel during summer vacation, can you recommend something?",
 "create_time": "2025-06-10 09:30:00",
 "update_time": "2025-06-10 09:30:00"
 },
 {
 "role": "assistant",
 "content": "Sure! Are you traveling alone, with family or with friends?",
 "create_time": "2025-06-10 09:30:00",
 "update_time": "2025-06-10 09:30:00"
 },
 {
 "role": "user",
 "content": "Iâm bringing my kid. My family always travels together.",
 "create_time": "2025-06-10 09:30:00",
 "update_time": "2025-06-10 09:30:00"
 },
 {
 "role": "assistant",
 "content": "Understood, Iâll recommend destinations suitable for family trips.",
 "create_time": "2025-06-10 09:30:00",
 "update_time": "2025-06-10 09:30:00"
 }

 },
 "message": ""
}

```
 
 
 
## 4. Next Steps
 
[ð You can now run MemOS and check out the full [API Docs](/api) to explore more features!]
