from ollama import chat, pull
from ollama import ChatResponse

pull(model='llama3.2:1b')

response: ChatResponse = chat(model='llama3.2:1b', messages=[
  {
        "role": "user",
        "content": "Porque o céu é azul?",
    },
])
print(response['message']['content'])
# or access fields directly from the response object
print(response.message.content)