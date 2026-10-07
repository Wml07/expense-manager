import json
from tools import client_embed, ask_zhishi

with open("xiangliang.json", encoding="utf-8") as f:
    ku = json.load(f)
    kuai = ku["kuai"]
    vecs = ku["vecs"]

wenti = "怎么让它别瞎编？" 

resp = client_embed.embeddings.create(
    model="BAAI/bge-m3",
    input=[wenti],
)
w_vec = resp.data[0].embedding


def xiangsidu(a, b):
    """两串数字对位相乘，再全加起来。值越大 = 意思越接近。"""
    zong = 0
    for i in range(len(a)):
        zong = zong + a[i] * b[i]
    return zong


defen = []
for i in range(len(vecs)):
    defen.append([xiangsidu(w_vec, vecs[i]), i])
defen.sort(reverse=True)

print("问题:",wenti)
print("【向量检索挑出来的】")
for d,i in defen[:3]:
    print("  相似度", round(d, 3),"→", kuai[i].split("\n")[0][:38])

ziliao = ""
for d, i in defen[:3]:
    ziliao = ziliao + kuai[i] + "\n\n"

prompt = "以下是我资料里的几个片段：\n\n" + ziliao + "\n\n我的问题是：" + wenti

print("【送出去的字数】", len(prompt), "字")

hua = ask_zhishi(prompt)
print("【AI 的回答】")
print(hua)
