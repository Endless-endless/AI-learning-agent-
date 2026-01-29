import os
import json
from openai import OpenAI

# Groq 是 OpenAI-compatible
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

def call_llm(user_input: str) -> dict:
    prompt = f"""
你是一个结构化输出助手。
请【只输出 JSON】，不要输出任何多余文本。

JSON 格式：
{{
  "summary": "一句话总结",
  "confidence": 0.0
}}

输入：
{user_input}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # ✅ Groq 官方可用模型
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )

    text = response.choices[0].message.content.strip()

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)


if __name__ == "__main__":
    print("Calling Groq...")
    result = call_llm("我想学习如何构建一个 AI Agent")
    print(result)
