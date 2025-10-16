

##Environment##
import os
import requests
import json

os.environ["MEMOS_API_KEY"] = "YOUR_API_KEY"
os.environ["MEMOS_BASE_URL"] = "https://memos.memtensor.cn/api/openmem/v1"

##Store Raw Conversations##
As shown in the example below, let’s assume it happened on June 10 of a certain year. You only need to store the user’s original conversation records into MemOS. MemOS will automatically abstract, process, and save them as memories.

data = {
    "user_id": "memos_user_123",
    "conversation_id": "0610",
    "messages": [
      {"role": "user", "content": "I want to travel during summer vacation, can you recommend something?"},
      {"role": "assistant", "content": "Sure! Are you traveling alone, with family or with friends?"},
      {"role": "user", "content": "I'm bringing my kid. My family always travels together."},
      {"role": "assistant", "content": "Got it, so you're traveling with your children as a family, right?"},
      {"role": "user", "content": "Yes, with both kids and elderly, we usually travel as a whole family."},
      {"role": "assistant", "content": "Understood, I'll recommend destinations suitable for family trips."}
    ]
  }
headers = {
  "Content-Type": "application/json",
  "Authorization": f"Token {os.environ['MEMOS_API_KEY']}"
}
url = f"{os.environ['MEMOS_BASE_URL']}/add/message"

res = requests.post(url=url, headers=headers, data=json.dumps(data))

print(f"result: {res.json()}")

##Retrieve Related Memories##
As shown in the example below, let’s assume it happened on September 28 of a certain year. In a new session, the user asks the AI to recommend a National Day holiday travel plan. MemOS will automatically recall the relevant memories for the AI to reference, thereby providing a more personalized travel plan.


data = {
  "query": "Any suggestions for where to go during National Day?",
  "user_id": "memos_user_123",
  "conversation_id": "0928"
}
headers = {
  "Content-Type": "application/json",
  "Authorization": f"Token {os.environ['MEMOS_API_KEY']}"
}
url = f"{os.environ['MEMOS_BASE_URL']}/search/memory"

res = requests.post(url=url, headers=headers, data=json.dumps(data))

print(f"result: {res.json()}")

