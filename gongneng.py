import json
from tools import client_embed, ask_zhishi
#判断有没有原始文件数据
with open("xiangliang.json", encoding="utf-8") as f:
    ku = json.load(f)
    kuai = ku["kuai"]
    vecs = ku["vecs"]
#算问题相似度
def xiangsidu(a, b):
    """两串数字对位相乘，再全加起来。值越大 = 意思越接近。"""
    zong = 0
    for i in range(len(a)):
        zong = zong + a[i] * b[i]
    return zong


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
    for d, i in defen[:3]:
        ziliao = ziliao + kuai[i] + "\n\n"

    zui_gao = defen[0][0] 
    if(zui_gao < 0.5):
        return "资料里没写"
    else:
        prompt = "以下是我资料里的几个片段：\n\n" + ziliao + "\n\n我的问题是：" + wenti
        hua = ask_zhishi(prompt)
    return hua
