# p16.py —— 多轮对话：让 AI "记住"前面说过的话
#
# 一句话机制：AI 自己【没有记忆】。
# 它之所以"记得"，是因为你每一轮都把整份历史又发过去给它看了一遍。
# 列表里装了什么，它就知道什么 —— 一条一条对得上，不多也不少。
#
# 运行：D:\python3.11.8\python.exe p16.py

from tools import client, SHEZHI, ask   # ask 拿来做对照组（它每轮都是全新的，不带历史）

# ① 开局先摆好一个列表。system 永远站第一格，而且只放一次 —— 摆在开头，管全局。
xiaoxi = [
    {"role": "system", "content": SHEZHI},
]


def shuo(wo_de_hua):
    """带历史地说一句：我塞进去 → 整份发过去 → 它的话也塞回去"""

    # ② 我说的这句，追加进列表
    xiaoxi.append({"role": "user", "content": wo_de_hua})

    # ③ 把【整份列表】发过去 —— 注意是整份，前面聊过的全在里面
    resp = client.chat.completions.create(model="qwen-plus", messages=xiaoxi)
    ta_de_hua = resp.choices[0].message.content

    # ④ 它说的话也塞回列表。
    #    这行管的是"它自己说过的话"能不能被追问 —— 比如它反问你"是早饭那笔吗？"，
    #    你回"是"，要是列表里没有它那句话，这个"是"就没有指代对象。
    xiaoxi.append({"role": "assistant", "content": ta_de_hua})

    return ta_de_hua


print("========== 第一组：带历史（用 shuo）==========")
print(shuo("今天早饭23，午饭60，晚饭25"))
print("【本轮之后，列表里有", len(xiaoxi), "条】")

print("----- 分隔线：下面这句话里，一个数字都没有 -----")
print(shuo("把刚才那三笔再说一遍"))
print("【本轮之后，列表里有", len(xiaoxi), "条】")


print("========== 第二组：对照组，不带历史（用 ask）==========")
print(ask("今天早饭23，午饭60，晚饭25"))
print("----- 同样一句，一个数字都没有 -----")
print(ask("把刚才那三笔再说一遍"))
