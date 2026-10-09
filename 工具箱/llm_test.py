import os
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv(r"D:\WB01\2026-08-11-10-58-12\.env")

# 这个文件最早的用途：9/19 第一次打通大模型 API。
# 现在换成「冒烟测试」—— 换服务商 / 换 key 之后，先跑它：能打印出两句话，就说明通了。
client = OpenAI(
    api_key = os.getenv("ZHIPU_API_KEY"),
    base_url="https://open.bigmodel.cn/api/paas/v4/",
)

def ask(wenti):
    resp = client.chat.completions.create(
        model="glm-4-flash",
        messages=[{"role": "user", "content": wenti}],     
    )
    return resp.choices[0].message.content                                            

print(ask("用一句话介绍云南"))
print(ask("1+1等于几"))
