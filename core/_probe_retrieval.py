# -*- coding: utf-8 -*-
"""检索诊断探针 V2：量「正确答案排第几」，并统计 top-k 命中率。

【为什么写它】
C 项实测发现「问 global 被误杀（0.472）」时，我判断真因是"检索没召回"。
但这个判断是**基于错误的期望标注**得出来的 —— 我把两道「资料里其实有答案」的题
（监控 AI 胡说 / 我学过的东西怎么才能不忘记）误标成了"资料里没有"。
所以先修标注，再重新量。

【怎么读结果】
- 每题打印 top-8，标出"目标节"（= 含期望关键词的节）排第几。
- 末尾统计三件事：
  ① 目标节落在 top-1 / top-3 / top-5 / top-8 的命中率 → 决定「扩大 top-k 值不值」
  ② 卷首块（第 0 块）的排名 → 它是否在当"噪声霸榜"
  ③ "资料里没有"的题，其最高分 vs 有答案题的最高分 → 决定「阈值能不能用」

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


# (问题, 期望关键词列表 —— 列表里任一关键词出现在某节正文里，那节就算"正确答案"；
#  空列表 [] = 这个问题资料里【本来就没有答案】)
WENTI = [
    ("global 是用来干嘛的", ["作用域与"]),
    ("向量检索的阈值是怎么定出来的", ["分数不够，门直接焊死", "向量检索：不比"]),
    ("怎么监控 AI 的回答有没有胡说", ["出处校验"]),
    ("我学过的东西怎么才能不忘记", []),          # 修订：笔记里没有讲"学习方法"的节
    ("Python 的装饰器怎么用", []),               # 真的没有
]


def main():
    print("向量库共 %d 块（含卷首第 0 块）\n" % len(kuai))

    you_paiming = []        # 有答案的题：最优命中排名
    wu_zuigao = []          # 没答案的题：最高分
    you_zuigao = []         # 有答案的题：最高分
    juanhou_paiming = []    # 每题里卷首块（下标 0）排第几

    for wenti, guanjian in WENTI:
        resp = client_embed.embeddings.create(model="BAAI/bge-m3", input=[wenti])
        w = resp.data[0].embedding

        defen = []
        for i in range(len(vecs)):
            defen.append([xiangsidu(w, vecs[i]), i])
        defen.sort(reverse=True)
        cixing = {i: n for n, (_, i) in enumerate(defen, 1)}   # 下标 -> 排名

        print("=" * 74)
        print("问题：%s" % wenti)
        if guanjian:
            print("期望命中：正文含 %s 的节" % guanjian)
        else:
            print("期望：资料里【本来没有】→ 理想结果是答「没有」，或检索不出相关节")
        for mingci, (fen, i) in enumerate(defen[:8], 1):
            biao = biaoti(kuai[i])
            shi_mubiao = guanjian and any(g in kuai[i] for g in guanjian)
            mark = "   <<< 目标节" if shi_mubiao else ""
            print("  %d. %.4f  [下标%2d] %s%s" % (mingci, fen, i, biao, mark))

        f0 = defen[0][0]
        juanhou_paiming.append(cixing.get(0, -1))
        if guanjian:
            you_zuigao.append(f0)
            paiming = [cixing[i] for i, k in enumerate(kuai)
                       if any(g in k for g in guanjian)]
            zui_hao = min(paiming) if paiming else -1
            you_paiming.append(zui_hao)
            print("  → 目标节最优排名：第 %d 名" % zui_hao)
        else:
            wu_zuigao.append(f0)
        print()

    # ── ① top-k 命中率 ──────────────────────────────────────────────
    print("=" * 74)
    print("【结论 1】目标节落在 top-k 里的比例（%d 道「资料里有」的题）" % len(you_paiming))
    for k in (1, 3, 5, 8):
        cheng = sum(1 for p in you_paiming if 0 < p <= k)
        print("  top-%-2d ： %d/%d 命中（%d%%）" % (k, cheng, len(you_paiming),
                                             round(cheng * 100 / len(you_paiming))))

    # ── ② 卷首块是不是噪声 ─────────────────────────────────────────
    print()
    print("【结论 2】卷首块（第 0 块，只有 4 行的「目录」）在每题的排名")
    for (wenti, _), p in zip(WENTI, juanhou_paiming):
        if p == -1:
            print("  %-28s → 前 8 名之外" % wenti)
        else:
            print("  %-28s → 第 %d 名" % (wenti, p))

    # ── ③ 分数能不能分开两类 ───────────────────────────────────────
    print()
    print("【结论 3】最高分对比（看两堆数字有没有「分界线」）")
    print("  资料里【有】答案： %s" % " ".join("%.4f" % x for x in sorted(you_zuigao, reverse=True)))
    print("  资料里【没有】答案：%s" % " ".join("%.4f" % x for x in sorted(wu_zuigao, reverse=True)))
    allf = sorted(you_zuigao + wu_zuigao, reverse=True)
    print("  全部混在一起排：   %s" % " ".join("%.4f" % x for x in allf))
    print("  → 若两类数字【交错出现】，说明任何一条阈值线都无法分开它们。")


if __name__ == "__main__":
    main()
