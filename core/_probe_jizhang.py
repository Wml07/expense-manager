# 记账人设探针 —— 换人设 / 换模型后，跑它看还稳不稳
#   用法：cd core && python _probe_jizhang.py
#   看两件事：① 正常记账会不会被误挡  ② 越界题会不会被放进来
from tools import client_chat, SHEZHI

# 现在 tools.py 里用的（V5，带"先判断是不是记账"那条）
base_old = [{"role": "system", "content": SHEZHI}]

# 候选：记账专用（去掉"先判断"那条 —— 因为门已经判过了）
SHEZHI_JIZHANG = """你是一台记账机器。用户发给你的每一句话，都是一笔已经发生的花销。

【唯一工作】把用户说的这笔花销复述出来，再补一句口语化点评。
【说话方式】口语化、直接，不寒暄。每次不超过 2 句。
【不要做的事】不要确认、不要反问、不要拒绝。用户说的每一句都算账，没有"不是记账"这种情况。"""
base_new = [{"role": "system", "content": SHEZHI_JIZHANG}]


def talk(hist, say):
    h = hist + [{"role": "user", "content": say}]
    r = client_chat.chat.completions.create(model="glm-4-flash", messages=h)
    return r.choices[0].message.content.replace("\n", " / ")


def batch(title, hist, say, n):
    print(f"=== {title}（{n} 次）===")
    for i in range(n):
        print("   ", i + 1, "->", talk(hist, say))
    print()


batch("旧人设 · 早饭23", base_old, "早饭23", 3)
batch("旧人设 · 午饭60", base_old, "午饭60", 3)
batch("新人设 · 早饭23", base_new, "早饭23", 5)
batch("新人设 · 午饭60", base_new, "午饭60", 3)
batch("新人设 · 越界题「帮我写一首诗」", base_new, "帮我写一首诗", 3)
