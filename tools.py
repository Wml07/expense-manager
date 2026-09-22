import os
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv(r"D:\WB01\2026-08-11-10-58-12\.env")
key = os.getenv("DASHSCOPE_API_KEY")

client = OpenAI(
    api_key = key,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)


# 人设②：点评专用 —— 只点评花销、一个字都不许出现数字 → 配下面的 ask_dianping()
SHEZHI_DIANPING = """
请你只做一件事：用不超过 2 句话点评这份花销。硬性要求：
① 一个字都不许出现数字 —— 不要重复、不要重算、不要引入新的数字；
② 不列明细、不分条列举；
③ 先说一句观察，再说一句建议，口语化
"""


# 点评专用的调用：跟 ask() 长得一样，只改一处 —— 换了人设（SHEZHI_DIANPING）
def ask_dianping(wenti):
    resp = client.chat.completions.create(
        model="qwen-plus",
        messages = [{"role":"system","content":SHEZHI_DIANPING},  # ← 人设：点评版
                    {"role":"user","content":wenti},              # ← 用户的话（变量，不加引号）
                    ],
    )
    return resp.choices[0].message.content



# 人设①：记账助手（通用物）—— 管身份、口吻、边界
SHEZHI = """
你是「开销管家」的记账助手。

【职责】只做两件事：① 记录用户报的花销；② 汇总并点评用户的开销情况。其他一概不管。

【说话方式】口语化、直接。不寒暄、不客套。每次回复不超过 2 句：先给总额，再给一句点评。

【越界处理】除了记账和开销，其他问题一律只回这一句："这不是我负责的项目"。不要解释、不要反问、不要举例，说完就结束。
"""


def ask(wenti):
    resp = client.chat.completions.create(
        model="qwen-plus",
        messages=[{"role": "system", "content": SHEZHI},
                  {"role":"user","content":wenti},
                  ],     
    )
    return resp.choices[0].message.content


# 人设③：资料问答 —— 只根据给的资料回答，资料里没写就直说 → 配下面的 ask_zhishi()
# ⭐ 这是"一个用途一个函数"的第二次使用：新用途 → 新函数，老的 ask / ask_dianping 一个字不动
SHEZHI_ZHISHI = """
你是「资料问答助手」。用户会给你几段资料，然后提一个问题。

【铁律】只能根据这些资料回答：
① 资料里能查到的，照着资料答；
② 资料里没写的，直接回"资料里没写"，一个字都不要编；
③ 不许引入资料之外的任何知识，不许自己推测。
"""


def ask_zhishi(wenti):
    resp = client.chat.completions.create(
        model="qwen-plus",
        messages=[{"role":"system","content":SHEZHI_ZHISHI},   # ← 人设：资料问答版
                  {"role":"user","content":wenti},              # ← 用户的话（变量，不加引号）
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