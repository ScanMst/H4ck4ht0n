from openai import OpenAI
from config import OPENROUTER_API_KEY

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)

response = client.chat.completions.create(
    model="meta-llama/llama-3.1-8b-instruct",
    messages=[
        {
            "role": "system",
            "content": "Responde exactamente con la frase solicitada. No expliques nada."
        },
        {
            "role": "user",
            "content": "Di exactamente: OpenRouter conectado"
        }
    ],
    temperature=0
)

print(response.choices[0].message.content)