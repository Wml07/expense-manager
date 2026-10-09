# rag1.py —— 手写 RAG：让 AI 先读"你的资料"，再回答问题
# ------------------------------------------------------------------
# RAG 三步（今天一次走完，一个环节都不缺）：
#   ① 切块  —— 把一整份长资料，切成一块一块小的
#   ② 检索  —— 拿"问题"去每一块里找，挑出最相关的几块
#   ③ 拼装  —— 只把挑出来的那几块 + 问题，拼成 prompt 发给 AI
#
# 为什么不一整份全塞给 AI？
#   这份资料 6 万多字 —— 又长又贵，而且每问一次都要重发一遍。
#   RAG 只送"相关的那几千字"，又快又准。
# ------------------------------------------------------------------

from tools import ask_zhishi


# ① 读整份资料 ------------------------------------------------------
# "../学习笔记.md" 里的 ".." = 上一层的文件夹（脚本在这层，笔记在上一层）
with open("../../学习笔记.md", encoding="utf-8") as f:
    quanwen = f.read()              # 一个文件 → 一个大字符串

print("整份资料一共", len(quanwen), "个字")


# ② 切块：按 "## " 标题砍开，每一节算一块 --------------------------
kuai = quanwen.split("\n## ")       # 砍在标题上 → 得到一个列表
print("切成了", len(kuai), "块")


# ③ 检索：拿问题去每一块里逐字找，给每块打分 -----------------------
wenti = "静默错误家族有哪几个成员？"


def jiansuo(wenti, kuai, jige=3):
    """土办法检索：问题里每有一个字出现在这块里，就加 1 分。分高 = 更相关。"""
    defen = []                              # 记分表：每一行是 [得分, 第几块]
    for i in range(len(kuai)):              # i 依次走过每一块的编号
        mingzhong = 0                       # 这一块命中了几个字
        for zi in wenti:                    # 把问题拆成一个一个字
            if zi in kuai[i]:               # 这个字在这块里出现过吗？
                mingzhong = mingzhong + 1
        defen.append([mingzhong, i])        # 往记分表里加一行
    defen.sort(reverse=True)                # 分数高的排前面
    return defen[:jige]                     # 只要前 jige 名


paihang = jiansuo(wenti, kuai)

print("问题：", wenti)
print("【它挑出来的是这几块】")
for d, i in paihang:                        # 一行拆成两个：得分、第几块
    biaoti = kuai[i].split("\n")[0]         # 每块的第一行就是那节的标题
    print("  得分", d, "→", biaoti[:38])


# ④ 拼装：只把挑出来的这几块 + 问题，拼成 prompt --------------------
ziliao = ""
for d, i in paihang:
    ziliao = ziliao + kuai[i] + "\n\n"      # 把挑中的块挨个接起来

prompt = "以下是我资料里的几个片段：\n\n" + ziliao + "\n\n我的问题是：" + wenti

print("【送出去的字数】", len(prompt), "字（原文", len(quanwen), "字）")


# ⑤ 交给 AI --------------------------------------------------------
# 人设已经把丑话说在前头了：资料里没写，就直说"资料里没写"
hua = ask_zhishi(prompt)
print("【AI 的回答】")
print(hua)
