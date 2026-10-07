import json
from tools import client_embed

with open("../学习笔记.md",encoding="utf-8") as f:
    quanwen = f.read()

kuai = quanwen.split("\n## ")
print("切车了", len(kuai), "块")

vecs = []
for k in range(0, len(kuai), 10):
    pi = kuai[k:k + 10]

    resp = client_embed.embeddings.create(
        model="BAAI/bge-m3",
        input=pi,
    ) 
    for d in resp.data:
        vecs.append(d.embedding)

    print("已完成",len(vecs),"块")

print("第一条向量有几个数字:", len(vecs[0]))



with open("xiangliang.json","w", encoding="utf-8") as f:
    json.dump({"kuai":kuai, "vecs":vecs}, f, ensure_ascii=False)

print("向量库已存好 → xiangliang.json")