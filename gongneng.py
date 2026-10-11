# 借工具箱 + 找向量库：它俩都住在隔壁的「core」文件夹里
#   Python 默认只找"自己这一层"，东西放到隔壁就找不到了，所以先报地址。
#   _core 这个变量就是那个地址，后面读向量库也用它。
# pylint: disable=wrong-import-position
# （跨文件夹借模块必须先报地址再 import，天然违反"import 放最上面"，故本文件放行）
import os, sys
_core = os.path.join(os.path.dirname(os.path.abspath(__file__)), "core")
sys.path.insert(0, _core)
import json
from tools import client_embed, ask_zhishi,client_chat, SHEZHI_JIZHANG
#判断有没有原始文件数据
with open(os.path.join(_core, "xiangliang.json"), encoding="utf-8") as f:
    ku = json.load(f)
    kuai = ku["kuai"]
    vecs = ku["vecs"]
#算问题相似度
def xiangsidu(a, b):
    """两串数字对位相乘，再全加起来。值越大 = 意思越接近。"""
    zongshu = 0
    for i in range(len(a)):
        zongshu = zongshu + a[i] * b[i]
    return zongshu

#接问的相应的方法
def wen_wenti(wenti):

    resp = client_embed.embeddings.create(
    model="BAAI/bge-m3",
    input=[wenti],
)
    w_vec = resp.data[0].embedding

    defen = []
    for i in range(len(vecs)):
        defen.append([xiangsidu(w_vec, vecs[i]), i])
    defen.sort(reverse=True)

    ziliao = ""
    for _ , i in defen[:3]:
        ziliao = ziliao + kuai[i] + "\n\n"

    zui_gao = defen[0][0]
    if zui_gao < 0.5:
        return "资料里没写"
    else:
        prompt = "以下是我资料里的几个片段：\n\n" + ziliao + "\n\n我的问题是：" + wenti
        hua = ask_zhishi(prompt)
    return hua
#接入记账的功能
xiaoxi = [
    {"role": "system", "content": SHEZHI_JIZHANG},
]


zhangben = os.path.join(os.path.dirname(os.path.abspath(__file__)), "zhangben.txt")

zong = 0
if os.path.exists(zhangben):
    with open(zhangben, encoding="utf-8") as f:
        for hang in f:
            try:
                zong = zong + int(hang)
            except ValueError:
                continue


def ji_zhang(wo_de_hua):
    global zong
    xiaoxi.append({"role": "user", "content": wo_de_hua})
    shuzi = ""
    for z in wo_de_hua:
        if z.isdigit():
            shuzi = shuzi + z

    jine = int(shuzi)
    zong = zong + jine

    with open(zhangben, "a", encoding="utf-8") as f_wj:
        f_wj.write(str(jine) + "\n")

    resp = client_chat.chat.completions.create(model="glm-4-flash", messages=xiaoxi)
    ta_de_hua = resp.choices[0].message.content
    xiaoxi.append({"role": "assistant", "content": ta_de_hua})

    return ta_de_hua + f"总计:{zong}元。"
