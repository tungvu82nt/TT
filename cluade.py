from openai import OpenAI

client = OpenAI(
    base_url="https://ai.megallm.io/v1",
    api_key="sk-mega-a310c993795e12f73cd46269cbffd1ea771e7f73e12f52fc22e3bbd181964307"
)

response = client.chat.completions.create(
    model="moonshotai/kimi-k2-instruct-0905",
    messages=[{"role": "user", "content": "Analyze this data..."}]
)

print("AI Response:", response.choices[0].message.content)
