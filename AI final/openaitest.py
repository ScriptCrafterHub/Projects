import os
import openai
from config import apikey

openai.api_key = apikey

response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant who writes professional emails."},
        {"role": "user", "content": "Write an email to my boss for resignation."}
    ],
    temperature=0.7
)

print(response.choices[0].message.content)
