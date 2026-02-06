import time
import json
import requests
import os

# 从环境变量读取，避免硬编码
ANTIGRAVITY_API_KEY = os.getenv("ANTIGRAVITY_API_KEY")
ANTIGRAVITY_BASE_URL = "http://127.0.0.1:8045/v1/chat/completions"

if not ANTIGRAVITY_API_KEY:
    raise RuntimeError("ANTIGRAVITY_API_KEY is not set")

def call_llm(user_input: str) -> dict:
    # ⭐ 每次调用前限流，而不是 import 时
    time.sleep(1.5)

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

    payload = {
        "model": "gemini-3-flash",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    headers = {
        "Authorization": f"Bearer {ANTIGRAVITY_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        ANTIGRAVITY_BASE_URL,
        headers=headers,
        json=payload,
        timeout=60
    )

    # ⭐ 关键：把 429 作为“环境信号”抛给 Agent
    if response.status_code == 429:
        raise RuntimeError("RATE_LIMIT")

    # 其它错误仍然是真错误
    if response.status_code != 200:
        response.raise_for_status()

    data = response.json()
    text = data["choices"][0]["message"]["content"].strip()

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)


if __name__ == "__main__":
    print(call_llm("我想学习如何构建一个 AI Agent"))
