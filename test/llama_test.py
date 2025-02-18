# You can use this to ensure LLama runs on your setup
from ollama import chat
from ollama import ChatResponse

response: ChatResponse = chat(
    model="llama3.1:8b",
    messages=[
        {
            "role": "user",
            "content": "Why is the sky blue?",
        },
    ],
)

# or access fields directly from the response object
print(response.message.content)
