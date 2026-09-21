import os
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv(r"D:\WB01\2026-08-11-10-58-12\.env")
key = os.getenv("DASHSCOPE_API_KEY")

client = OpenAI(
    api_key = key,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)


# 记账助手的人设（system 用）：站最前面，先给 AI 立规矩
SHEZHI = """
请你只做一件事：用不超过 2 句话点评这份花销。硬性要求：
① 一个字都不许出现数字 —— 不要重复、不要重算、不要引入新的数字；
② 不列明细、不分条列举；
③ 先说一句观察，再说一句建议，口语化
"""


def ask(wenti):
    resp = client.chat.completions.create(
        model="qwen-plus",
        messages=[{"role": "system", "content": SHEZHI},
                  {"role":"user","content":wenti},
                  ],     
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

print("工具箱自检通过")