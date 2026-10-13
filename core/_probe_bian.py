# _probe_bian.py —— 抓"编造"的探针
# ------------------------------------------------------------------
# 目的：闸门只拦得住"分数低的问题"。分数够高、但资料里其实没写的时候，
#       AI 会不会顺着往下编？这个脚本把【分数 + 拿到的片段 + AI 的答案】
#       三样一起打出来，让人肉眼判断"这段答案有没有出处"。
#
# 用法：cd core && python _probe_bian.py
# ------------------------------------------------------------------

import json
import os
import sys

# 跟 gongneng.py 一样：先把 core（自己这一层）报给 Python，才能 import tools
_这里 = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _这里)

from tools import client_embed, ask_zhishi      # noqa: E402  (报完地址才 import)


# ── ① 读向量库（跟 gongneng.py 一模一样的读法）──────────────────────
with open(os.path.join(_这里, "xiangliang.json"), encoding="utf-8") as f:
    ku = json.load(f)
    kuai = ku["kuai"]
    vecs = ku["vecs"]


def xiangsidu(a, b):
    """两串数字对位相乘再全加：值越大 = 意思越接近。"""
    zong = 0
    for i in range(len(a)):
        zong = zong + a[i] * b[i]
    return zong


def cha(wenti):
    """对一个提问跑完整流程：算分 → 取前 3 段 → 问 AI。返回(最高分, 片段标题, 答案)。"""
    resp = client_embed.embeddings.create(model="BAAI/bge-m3", input=[wenti])
    w_vec = resp.data[0].embedding

    defen = []
    for i in range(len(vecs)):
        defen.append([xiangsidu(w_vec, vecs[i]), i])
    defen.sort(reverse=True)

    ziliao = ""
    biaoti = []
    for _, i in defen[:3]:                       # 只取前 3 段（跟作品里一致）
        ziliao = ziliao + kuai[i] + "\n\n"
        biaoti.append(kuai[i].split("\n")[0][:38])   # 片段标题，方便肉眼看出处

    zui_gao = defen[0][0]
    if zui_gao < 0.5:                            # 闸门（阈值 0.5）
        return zui_gao, biaoti, "【闸门拦下】资料里没写"

    prompt = "以下是我资料里的几个片段：\n\n" + ziliao + "\n\n我的问题是：" + wenti
    return zui_gao, biaoti, ask_zhishi(prompt)


# ── ② 测试问题集 ────────────────────────────────────────────────────
# 分两组：一组"资料里确实有"，一组"资料里没有但沾边"——后者才是陷阱。
WENTI = [
    ("资料里有", "向量检索的阈值是怎么定出来的？"),
    ("资料里有", "global 是用来干嘛的？"),
    ("资料里没有", "怎么监控 AI 的回答有没有胡说？"),
    ("资料里没有", "Python 的装饰器怎么用？"),
    ("资料里没有", "怎么给这个项目写单元测试？"),
]

for zu, w in WENTI:
    fenshu, biaoti, daan = cha(w)
    print("=" * 70)
    print(f"【{zu}】{w}")
    print(f"最高分：{fenshu:.3f}    闸门线：0.500")
    print("拿到的片段：")
    for t in biaoti:
        print("   -", t)
    print("AI 的回答：")
    print("  ", daan.replace("\n", "\n   "))
