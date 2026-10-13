# -*- coding: utf-8 -*-
"""检索诊断探针：看「正确的那一节」在 top-N 里排第几。

【为什么写它】
C 项实测发现「问 global 被误杀（0.472）」的真因**不是阈值太低**，
而是【讲 global 的那一节压根没被召回到前 3 名】。
—— 那么问题来了：它到底排第几？把 top-k 从 3 扩到 5 或 8，救得回来吗？
   这个探针就是来量这个的：把 top-8 全部打出来，标出"目标节"的位置。

【怎么读结果】
- 目标节在前 3 名内 → 检索没问题，问题在阈值/生成
- 目标节排第 4~8      → 有救：扩大 top-k 就行
- 目标节压根不在前 8  → 向量检索这条路对它失效（要靠 rerank 或换切块方式）

用法：cd core && python _probe_retrieval.py
"""

import json
import os
import sys

_CORE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _CORE)

from tools import client_embed  # noqa: E402  （必须在 sys.path 补完之后 import）

with open(os.path.join(_CORE, "xiangliang.json"), encoding="utf-8") as f:
    ku = json.load(f)
kuai = ku["kuai"]
vecs = ku["vecs"]


def xiangsidu(a, b):
    """两串数字对位相乘再全加起来 —— 值越大越像。"""
    z = 0
    for i in range(len(a)):
        z = z + a[i] * b[i]
    return z


def biaoti(yi_jie):
    """取一节的标题（第一行）。"""
    return yi_jie.split("\n")[0].strip()


# (问题, 期望命中节里的关键词；None = 资料里本来就没有答案)
WENTI = [
    ("global 是用来干嘛的", "global"),
    ("向量检索的阈值是怎么定出来的", "阈值"),
    ("我学过的东西怎么才能不忘记", "抗遗忘"),
    ("怎么监控 AI 的回答有没有胡说", None),
    ("Python 的装饰器怎么用", None),
]


def main():
    print("向量库共 %d 节\n" % len(kuai))
    for wenti, guanjian in WENTI:
        resp = client_embed.embeddings.create(model="BAAI/bge-m3", input=[wenti])
        w = resp.data[0].embedding

        defen = []
        for i in range(len(vecs)):
            defen.append([xiangsidu(w, vecs[i]), i])
        defen.sort(reverse=True)

        print("=" * 74)
        print("问题：%s" % wenti)
        if guanjian:
            print("期望命中：含「%s」的那一节" % guanjian)
        else:
            print("期望：资料里本来没有 → 应该被闸门拦下")
        for mingci, (fen, i) in enumerate(defen[:8], 1):
            biao = biaoti(kuai[i])
            mark = "   <<< 目标节" if (guanjian and guanjian in kuai[i]) else ""
            print("  %d. %.4f  [下标%2d] %s%s" % (mingci, fen, i, biao, mark))
        print()


if __name__ == "__main__":
    main()
