import os
import json
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv(r"D:\WB01\2026-08-11-10-58-12\.env")
key = os.getenv("DASHSCOPE_API_KEY")

client = OpenAI(
    api_key = key,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

def ask(wenti):
    resp = client.chat.completions.create(
        model="qwen-plus",
        messages=[{"role": "user", "content": wenti}],     
    )
    return resp.choices[0].message.content

def Rc_02(wenjian):
    Lt = []
    if os.path.exists(wenjian):
        with open(wenjian,encoding="utf-8") as f:
            for lines in f:
                lines = lines.strip()
                try:
                    lineser = lines.split(",")
                    Lt.append([lineser[0],int(lineser[1])])
                except:
                    continue
    return Lt


text = ""
for r,v in Rc_02("ZB.txt"):
    text = text + f"{r},{v}元\n"


prompt = ("这是我这周的消费账本：\n" + text +
          "\n请按类别汇总金额，只返回 JSON，格式：{\"类别\": 金额}。不要任何其他文字、解释或代码块标记。")

answer = ask(prompt)          # ① 先原样看它回了什么
# print("AI 原话：", answer)

data = json.loads(answer)                     # ② 把它变回字典 ← 你来填
print(data)                    #    看看它长什么样
# print(type(data))

with open("AI分析结果.json","w",encoding="utf-8") as f:
    a = json.dumps(data,ensure_ascii=False)
    f.write(a)


with open("AI分析结果.json",encoding="utf-8") as f:
    neirong = f.read()

huilai = json.loads(neirong)
print(huilai["午饭"])