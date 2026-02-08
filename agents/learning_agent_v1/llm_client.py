import json
from zhipuai import ZhipuAI

# ⚠️ 这里直接填写你刚购买的 GLM API Key
# 后面等稳定了，再改成环境变量
GLM_API_KEY = "99ef2849c8f44a25a76dbc68746800d1.rUkT4NupSF5p3de7"

client = ZhipuAI(api_key=GLM_API_KEY)

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
        model="glm-4.7",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )

    text = response.choices[0].message.content.strip()

    # 处理可能的 ```json 包裹
    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)


# 用于单独测试 LLM 是否可用
if __name__ == "__main__":
    print(call_llm("我想学习如何构建一个 AI Agent"))
