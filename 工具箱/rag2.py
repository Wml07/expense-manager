# rag2.py —— 建"向量库"：把资料每一块，变成一串数字
# ------------------------------------------------------------------
# 为什么要变数字？
#   昨天的逐字匹配只会"对字"，不懂意思（问"怎么防止AI胡说"找不到"编账"）。
#   换成数字之后，就能比"意思像不像" —— 这就是语义检索。
#
# 这个脚本只需要跑一次：把 30 块资料全部变成向量，存进 xiangliang.json。
# 以后每次提问直接读这个文件，不用重算。
# ------------------------------------------------------------------

import json
from tools import client_embed

# 路径挂在"文件自己"身上，不靠"当前在哪个文件夹"——
# 否则换个地方运行，会把向量库写到别的文件夹去（这种事不报错，最难发现）。
import os
_工具箱目录 = os.path.dirname(os.path.abspath(__file__))
_笔记路径   = os.path.join(os.path.dirname(_工具箱目录), "..", "学习笔记.md")
_向量库路径 = os.path.join(_工具箱目录, "xiangliang.json")

# ① 读资料 + 切块（跟昨天一模一样） --------------------------------
with open(_笔记路径, encoding="utf-8") as f:
    quanwen = f.read()

kuai = quanwen.split("\n## ")       # 还是砍在二级标题上
print("切成了", len(kuai), "块")


# ② 把每一块变成向量 ------------------------------------------------
# embedding 接口一次最多收 10 条，所以要一批一批送
vecs = []                           # 装所有向量，一个块一个
for k in range(0, len(kuai), 10):   # 0, 10, 20 … 每次跳 10
    pi = kuai[k:k + 10]             # 切出这一批（最多 10 条）

    resp = client_embed.embeddings.create(
        model="BAAI/bge-m3",        # 硅基流动的免费向量模型（1024 维，跟 text-embedding-v3 一样宽）
        input=pi,                   # 这一批文本
    )

    for d in resp.data:             # 一条一条取出来
        vecs.append(d.embedding)    # d.embedding 就是一串数字

    print("已完成", len(vecs), "块")

print("第一条向量有几个数字：", len(vecs[0]))


# ③ 存盘 ------------------------------------------------------------
# 把"块"和"向量"一起存起来，下次直接用
with open(_向量库路径, "w", encoding="utf-8") as f:
    json.dump({"kuai": kuai, "vecs": vecs}, f, ensure_ascii=False)

print("向量库已存好 → xiangliang.json")
