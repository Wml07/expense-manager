# _probe_threshold.py —— 一次性探针（用完可删）
# 目的：量一量「资料里有答案」和「资料里没答案」两组问题，各自的最高分落在哪
# 为什么：阈值（那条线）不能拍脑袋定，得先看两边的分数长什么样

import json
from tools import client_embed

with open("xiangliang.json", encoding="utf-8") as f:
    ku = json.load(f)
    kuai = ku["kuai"]
    vecs = ku["vecs"]


def xiangsidu(a, b):
    """两串数字对位相乘再全加 —— 值越大越像"""
    zong = 0
    for i in range(len(a)):
        zong = zong + a[i] * b[i]
    return zong


# 两组问题：A 组笔记里确实讲过；B 组笔记里压根没这回事
wenti_list = [
    ("有答案", "怎么让它别瞎编？"),
    ("有答案", "什么是向量检索？"),
    ("有答案", "为什么说代码管数、AI 管话？"),
    ("没答案", "今天昆明天气怎么样？"),
    ("没答案", "帮我写一个爬虫"),
    ("没答案", "拉祜语的你好怎么说？"),
]

for biaoqian, wenti in wenti_list:
    resp = client_embed.embeddings.create(model="BAAI/bge-m3", input=[wenti])
    w_vec = resp.data[0].embedding

    defen = []
    for i in range(len(vecs)):
        defen.append([xiangsidu(w_vec, vecs[i]), i])
    defen.sort(reverse=True)

    # 只打最高分那一条 —— 我们将来要判的就是它
    print(f"[{biaoqian}] {wenti}")
    print(f"      最高分 {round(defen[0][0], 3)} → 第 {defen[0][1]+1} 块: {kuai[defen[0][1]].split(chr(10))[0][:30]}")
