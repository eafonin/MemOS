##Store Raw Conversations##
As shown in the example below, let’s assume it happened on June 10 of a certain year. You only need to store the user’s original conversation records into MemOS. MemOS will automatically abstract, process, and save them as memories.

curl --request POST \
  --url https://memos.memtensor.cn/api/openmem/v1/add/message \
  --header 'Authorization: Token YOUR_API_KEY'  \
  --header 'Content-Type: application/json' \
  --data '{
    "user_id": "memos_user_123",
    "conversation_id": "0610",
    "messages": [
      {"role": "user", "content": "I want to travel during summer vacation, can you recommend something?"},
      {"role": "assistant", "content": "Sure! Are you traveling alone, with family or with friends?"},
      {"role": "user", "content": "I'\''m bringing my kid. My family always travels together."},
      {"role": "assistant", "content": "Got it, so you'\''re traveling with your children as a family, right?"},
      {"role": "user", "content": "Yes, with both kids and elderly, we usually travel as a whole family."},
      {"role": "assistant", "content": "Understood, I'\''ll recommend destinations suitable for family trips."}
    ]
  }'

##Retrieve Related Memories##
As shown in the example below, let’s assume it happened on September 28 of a certain year. In a new session, the user asks the AI to recommend a National Day holiday travel plan. MemOS will automatically recall the relevant memories for the AI to reference, thereby providing a more personalized travel plan.

curl --request POST \
  --url https://memos.memtensor.cn/api/openmem/v1/search/memory \
  --header 'Authorization: Token YOUR_API_KEY' \
  --header 'Content-Type: application/json' \
  --data '{
    "query": "Any suggestions for where to go during National Day?",
    "user_id": "memos_user_123",
    "conversation_id": "0928"
  }'
