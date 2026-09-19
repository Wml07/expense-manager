import os
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


prompt = "这是我这周的消费账本:\n" + text + "请帮我分析一下，并给出省钱建议"
print(ask(prompt))


