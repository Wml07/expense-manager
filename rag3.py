# rag3.py —— 向量检索：不再"对字"，改比"意思像不像"
# ------------------------------------------------------------------
# 跟 rag1.py 结构完全一样：读 → 检索 → 拼 → 问。
# 只有"检索"那一段被换掉了 —— 换成了向量比对。
# ------------------------------------------------------------------

import json
from tools import client_embed, ask_zhishi

# ① 读回向量库（rag2.py 建好的） ------------------------------------
with open("xiangliang.json", encoding="utf-8") as f:
    ku = json.load(f)
kuai = ku["kuai"]           # 每一块的原文
vecs = ku["vecs"]           # 每一块对应的那串数字

# ② 把问题也变成一串数字 -------------------------------------------
wenti = "怎么防止 AI 乱说话？"

resp = client_embed.embeddings.create(
    model="BAAI/bge-m3",
    input=[wenti],          # 只有一条，也要用列表包起来
)
w_vec = resp.data[0].embedding


# ③ 比相似度 -------------------------------------------------------
def xiangsidu(a, b):
    """两串数字对位相乘，再全加起来。值越大 = 意思越接近。"""
    zong = 0
    for i in range(len(a)):
        zong = zong + a[i] * b[i]
    return zong


defen = []                                      # 记分表：[相似度, 第几块]
for i in range(len(vecs)):
    defen.append([xiangsidu(w_vec, vecs[i]), i])
defen.sort(reverse=True)                        # 最像的排最前

print("问题：", wenti)
print("【向量检索挑出来的】")
for d, i in defen[:3]:
    print("  相似度", round(d, 3), "→", kuai[i].split("\n")[0][:38])


# ④ 拼装 + 交给 AI（跟昨天一模一样） ------------------------------
ziliao = ""
for d, i in defen[:3]:
    ziliao = ziliao + kuai[i] + "\n\n"

prompt = "以下是我资料里的几个片段：\n\n" + ziliao + "\n\n我的问题是：" + wenti

print("【送出去的字数】", len(prompt), "字")

hua = ask_zhishi(prompt)
print("【AI 的回答】")
print(hua)
