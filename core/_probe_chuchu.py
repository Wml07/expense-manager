# _probe_chuchu.py —— 带「出处」的探针（C 项第 ② 步 · 第 2 版）
# ------------------------------------------------------------------
# 第 1 版教训：把 AI 抄的"依据"只在【检索到的 3 段】里找 → 真话也被判成假话。
# 这一版修三处：
#   ① 对照范围改成【全库】（AI 抄的原句可能来自资料别处）
#   ② 打印 AI 的【原始返回】，看清它到底回了什么（不再猜）
#   ③ 每题跑【两轮】，看这个免费小模型的输出稳不稳
#
# 用法：cd core && python _probe_chuchu.py
# ------------------------------------------------------------------

import json
import os
import sys

_这里 = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _这里)

from tools import client_embed, client_chat, SHEZHI_ZHISHI      # noqa: E402


# ── ① 读向量库 ──────────────────────────────────────────────────────
with open(os.path.join(_这里, "xiangliang.json"), encoding="utf-8") as f:
    ku = json.load(f)
    kuai = ku["kuai"]
    vecs = ku["vecs"]
quanku = "".join(kuai)          # 全库一大串 = 出处校验的对照范围


def xiangsidu(a, b):
    """两串数字对位相乘再全加：值越大 = 意思越接近。"""
    zong = 0
    for i in range(len(a)):
        zong = zong + a[i] * b[i]
    return zong


def qu_json(hua):
    """从 AI 回的文字里抠出 JSON。抠不出来 → None。"""
    t = hua.strip()
    if t.startswith("```"):
        t = t.strip("`")
        if t.lower().startswith("json"):
            t = t[4:]
        t = t.strip()
    zuo = t.find("{")
    you = t.rfind("}")
    if zuo == -1 or you == -1:
        return None
    try:
        return json.loads(t[zuo:you + 1])
    except ValueError:
        return None


def yan(yiju):
    """依据在全库里'像不像真话'？返回 (4字滑窗命中率, 结论)。
       为什么切片算命中率、而不是整段比对：
       实测证明 AI 抄原文时必然有细微改写（引号、破折号、空格、加编号），
       整段 100% 比对必然失败 —— 那是判据太严，不是 AI 在编。"""
    if not yiju:
        return 0.0, "无依据"
    zi = "".join(quanku.split())
    suo = "".join(yiju.split())
    if not suo:
        return 0.0, "无依据"
    n = 4
    if len(suo) <= n:
        hit = 1.0 if suo in zi else 0.0
        return hit, ("✅ 短句命中" if hit else "❌ 短句也没有")
    ws = [suo[i:i + n] for i in range(len(suo) - n + 1)]
    lv = sum(1 for w in ws if w in zi) / len(ws)
    return lv, ("✅ 像真话" if lv >= 0.8 else ("⚠ 半真" if lv >= 0.4 else "❌ 纯编"))


def cha(wenti):
    """算分 → 取前 3 段 → 问 AI。返回 (最高分, 片段标题, AI原始返回 或 闸门说明)"""
    resp = client_embed.embeddings.create(model="BAAI/bge-m3", input=[wenti])
    w_vec = resp.data[0].embedding

    defen = []
    for i in range(len(vecs)):
        defen.append([xiangsidu(w_vec, vecs[i]), i])
    defen.sort(reverse=True)

    ziliao = ""
    biaoti = []
    for _, i in defen[:3]:
        ziliao = ziliao + kuai[i] + "\n\n"
        biaoti.append(kuai[i].split("\n")[0][:34])

    if defen[0][0] < 0.5:
        return defen[0][0], biaoti, None

    prompt = "以下是我资料里的几个片段：\n\n" + ziliao + "\n\n我的问题是：" + wenti
    hui = client_chat.chat.completions.create(
        model="glm-4-flash",
        messages=[{"role": "system", "content": SHEZHI_ZHISHI},
                  {"role": "user", "content": prompt}],
    ).choices[0].message.content
    return defen[0][0], biaoti, hui


WENTI = [
    ("资料里有", "向量检索的阈值是怎么定出来的？"),
    ("资料里有", "global 是用来干嘛的？"),
    ("资料里没有", "怎么监控 AI 的回答有没有胡说？"),
    ("资料里没有", "怎么给这个项目写单元测试？"),
]

for zu, w in WENTI:
    fenshu, biaoti, hui = cha(w)
    print("=" * 72)
    print(f"【{zu}】{w}")
    print(f"最高分：{fenshu:.3f}   检索到：{' / '.join(biaoti)}")
    if hui is None:
        print("→ 闸门拦下（分数 < 0.5）")
        continue
    for lun in (1, 2):
        if lun == 2:                       # 第二轮（同一问题再问一次，看稳定性）
            _, _, hui = cha(w)
        d = qu_json(hui)
        if d is None:
            print(f"  第{lun}轮 ❌ JSON 没守住：{hui.strip()[:110]}")
            continue
        daan = str(d.get("答案", "")).strip()
        yiju = str(d.get("依据", "")).strip()
        print(f"  第{lun}轮 答案：{daan[:70]}")
        print(f"        依据：{(yiju[:70] if yiju else '（空）')}")
        lv, jielun_yan = yan(yiju)
        print(f"        校验：命中率 {lv:.0%}   {jielun_yan}")
