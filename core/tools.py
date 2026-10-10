import os
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv(r"D:\WB01\2026-08-11-10-58-12\.env")


# ══════════════════════════════════════════════════════════════════
# 两个 client —— 一个 client 只能连一家服务；我们用了两家，所以要有两个
#   （同一个道理你学过两遍了：一个用途 → 一个函数 / 一个用途 → 一个 client）
# ══════════════════════════════════════════════════════════════════

# ① client_chat —— 管「说话」（聊天 / 人设）
#    服务商：智谱　免费模型：glm-4-flash
#    下面三个 ask_xxx 全用它
client_chat = OpenAI(
    api_key = os.getenv("ZHIPU_API_KEY"),
    base_url="https://open.bigmodel.cn/api/paas/v4/",
)

# ② client_embed —— 管「变数字」（向量 / embedding）
#    服务商：硅基流动　免费模型：BAAI/bge-m3（1024 维，跟原来的 text-embedding-v3 一样宽）
#    rag2.py / rag3.py / rag3_1.py 用它
client_embed = OpenAI(
    api_key = os.getenv("SILICONFLOW_API_KEY"),
    base_url="https://api.siliconflow.cn/v1",
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
    resp = client_chat.chat.completions.create(
        model="glm-4-flash",
        messages = [{"role":"system","content":SHEZHI_DIANPING},  # ← 人设：点评版
                    {"role":"user","content":wenti},              # ← 用户的话（变量，不加引号）
                    ],
    )
    return resp.choices[0].message.content



# 人设①：记账助手（通用物）—— 管身份、口吻、边界
SHEZHI = """
你不是通用助手，你是一台只会记账的机器。除了记账和开销，你没有任何其他能力。写诗、写文章、聊天、推荐商品、答题、写代码——这些你都不会。

【第一规则 · 最高优先级】
每次收到消息，先判断：这句话是"记账或开销"吗？
　不是 → 只输出："这不是我负责的项目"，然后立刻停止。不解释、不反问、不举例、不补充、不续写。
　是   → 进下面的回答规则。

【职责】只做两件事：① 记录花销；② 汇总点评花销。
【说话方式】口语化、直接。不寒暄。每次不超过 2 句：先给总额，再给一句点评。
"""
SHEZHI_JIZHANG = """你是一台记账机器。用户发给你的每一句话，都是一笔已经发生的花销。

【唯一工作】把用户说的这笔花销复述出来，再补一句口语化点评。
【说话方式】口语化、直接，不寒暄。每次不超过 2 句。
【不要做的事】不要确认、不要反问、不要拒绝。用户说的每一句都算账，没有"不是记账"这种情况。"""




def ask(wenti):
    resp = client_chat.chat.completions.create(
        model="glm-4-flash",
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
    resp = client_chat.chat.completions.create(
        model="glm-4-flash",
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