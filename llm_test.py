import os
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv(r"D:\WB01\2026-08-11-10-58-12\.env")
key = os.getenv("DASHSCOPE_API_KEY")

client = OpenAI(
    api_key = key,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# resp = client.chat.completions.create(
#     model="qwen-plus",
#     messages=[{"role":"user", "content":"用一句话介绍你自己"}],
# )

# print(resp.choices[0].message.content)


def ask(wenti):
    resp = client.chat.completions.create(
        model="qwen-plus",
        messages=[{"role": "user", "content": wenti}],     # ← 第 1 个空
    )
    return resp.choices[0].message.content                                            # ← 第 2 个空

print(ask("用一句话介绍云南"))
print(ask("1+1等于几"))
