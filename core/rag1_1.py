from tools import ask_zhishi

with open("../../学习笔记.md",encoding="utf-8") as f:
    quanwen = f.read()


print("整份资料一共", len(quanwen),"个字")



kuai = quanwen.split("\n## ")
print("切成了", len(kuai), "块")


wenti = "我家猫叫什么名字？"


def jiansuo(wenti, kuai, jige=3):
    """土办法检索：问题里每一个字出现在这块里，就加1分。分高 = 更相关。"""
    denfn = []
    for i in range(len(kuai)):
        mingzhong = 0
        for zi in wenti:
            if zi in kuai[i]:
                mingzhong = mingzhong + 1
        denfn.append([mingzhong, i])
    denfn.sort(reverse=True)
    return denfn[:jige]

paihang = jiansuo(wenti, kuai)

print("问题:", wenti)
print("【它跳出来的是这几块】")
for d, i in paihang:
    biaoti = kuai[i].split("\n")[0]
    print("  得分", d, "→", biaoti[:38])


ziliao = ""
for d, i in paihang:
    ziliao = ziliao + kuai[i] + "\n\n"

prompt = "以下是我资料里的几个片段:\n\n" + ziliao + "\n\n我的问题是:" + wenti

print("【送出去的字数】", len(prompt), "字 （原文",len(quanwen),"字）")

hua = ask_zhishi(prompt)
print("【AI 的回答】")
print(hua)