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


def qu_json(hua):
    """把 AI 回的一段文字，尽量抠成一个字典（dict）。

    为什么要这一步？因为 AI 回话永远是【文字】，不是程序能用的【数据】。
    它可能守规矩只回 {"答案":..., "依据":...}，
    也可能手滑包一层 ```json ... ```，或者前后啰嗦两句。
    这个函数就负责"从一堆文字里把那个 JSON 抠出来"。

    抠成功 → 返回字典；抠不出来 → 返回 None（代表"连格式都没守住"）。
    """
    t = hua.strip()
    if t.startswith("```"):              # 拆掉可能存在的 ```json ... ``` 包裹
        t = t.strip("`")                 # 先削掉两头的反引号
        if t.lower().startswith("json"):  # 如果开头是 json 这四个字母
            t = t[4:]                     # 也削掉
        t = t.strip()
    zuo = t.find("{")                    # 第一个左花括号
    you = t.rfind("}")                   # 最后一个右花括号
    if zuo == -1 or you == -1:           # 根本没有花括号 → 不是 JSON
        return None
    try:
        return json.loads(t[zuo:you + 1])   # 只取中间那一段来解析
    except ValueError:                      # 解析不了 = 格式坏了
        return None


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
    biaoti = []                              # 顺手记下"命中了哪几节"—— 待会儿要当来源用
    for _ , i in defen[:3]:
        ziliao = ziliao + kuai[i] + "\n\n"
        # 只取每节第一行当标题。⚠️ 这里【不要截断】：早先写了 [:24]，
        # 结果把「25. system 人设：给 AI 立规矩（prompt 工程）」腰斩成
        # 「...立规矩（p」—— 半个括号挂在来源里，一眼就看得出糙。
        # 标题本来就不长，完整显示反而更像"出处"。
        biaoti.append(kuai[i].split("\n")[0].strip())

    zui_gao = defen[0][0]
    if zui_gao < 0.5:                        # 闸门：分数太低 → 连问都不问
        return "资料里没写"

    prompt = "以下是我资料里的几个片段：\n\n" + ziliao + "\n\n我的问题是：" + wenti
    hua = ask_zhishi(prompt)

    # ── 把 AI 的结构化回复拆开，只取「答案」那一格 ────────────────────
    # 人设要求它回 {"答案":..., "依据":...}。这里只取"答案"，不取"依据"——
    # 为什么？（这是 C 项实测换来的结论，见下方注释）
    d = qu_json(hua)
    if d is None:
        daan = hua.strip()                   # 它没守住 JSON 格式 → 退回原文，别把话弄丢
    else:
        daan = str(d.get("答案", "")).strip()

    if daan == "资料里没写":                  # AI 自己说了没写 → 直接放行
        return "资料里没写"

    # ── 【来源透明】把"这段话是从哪几节召回的"附在后面 ──────────────
    # ⭐ C 项实测结论：想用"代码校验依据真假"来防编造，这条路【走不通】——
    #    实测发现判据是【反向】的：编造的答案因为照抄了喂给它的片段，
    #    依据命中率反而高达 92%~100%；真答案跨块拼接，只有 64%。
    #    而且"依据是否支撑答案"是【语义问题】，字面匹配根本管不了。
    # 所以换个诚实的做法：不判真假，改把【来源摊开】——
    #    AI 说的来源它自己能编，代码说的来源（= 检索命中哪几节）编不了。
    #    让用户看着来源自己核对。这是"代码管'话从哪来'"。
    laiyuan = "、".join(biaoti)
    return daan + "\n\n（来源：" + laiyuan + "）"
#接入记账的功能
xiaoxi = [
    {"role": "system", "content": SHEZHI_JIZHANG},
]


zhangben = os.path.join(os.path.dirname(os.path.abspath(__file__)), "zhangben.txt")

# ── 两个"钱袋子"，都放在模块级（= 活到程序结束，不关就不丢）────────────
zong = 0        # ① 总额：所有笔加起来的那个数（一笔一加）
mingxi = []     # ② 明细：一笔占一个格子，按先后顺序排队（存"原文"，不是抠出来的数字）


def zhua_shuzi(wo_de_hua):
    """从一句话里把数字抠出来，转成整数返回。例：「早饭23」→ 23。

    为什么单独拎成一个函数？因为有【两个地方】要干同一件事：
      ① 记账时（从用户刚说的话里抠）
      ② 启动读回时（从文件里的每一行里抠）
    —— 同一件事要干两遍，就该抽成函数：以后只维护这一份，改一处两处都生效。
    """
    shuzi = ""
    for z in wo_de_hua:          # 一个字一个字过
        if z.isdigit():          # 是 0-9 的数字就拼进去
            shuzi = shuzi + z
    return int(shuzi)            # 先拼字（"2"+"3"→"23"），最后一次性转成数（23）


# ── 启动读回：把账本文件里的每一笔读进内存 ────────────────────────────
# 现在文件里每行长这样：「早饭23」——名字 + 金额【原样】存着。
# （比只存数字更"原始"：昨天存的是算过的金额，今天存的是用户原话）
if os.path.exists(zhangben):                 # 第一次跑还没这个文件，先问一句在不在
    with open(zhangben, encoding="utf-8") as f:
        for hang in f:                       # 一行 = 一笔
            hang = hang.strip()              # 削掉行尾看不见的换行符
            if hang == "":
                continue                     # 空行跳过（防文件末尾的脏空行）
            try:
                hang_jine = zhua_shuzi(hang)     # 从这一行里把金额抠出来
            except ValueError:
                continue                     # 万一这行一个数字都没有，跳过、不崩
            mingxi.append(hang)              # ① 明细：把这一笔原文留住
            zong = zong + hang_jine          # ② 总额：顺手累加上去


def cha_mingxi():
    """查明细：把账本里每一笔列出来，末尾带上笔数和合计。返回一段字符串。

    注意：这里【只 return、不 print】—— 打印是"门"（zhushou.py）的活。
    （10/9 那次"答案打两遍"就是函数里多 print 了一遍，踩过的坑）
    """
    if len(mingxi) == 0:                     # 一笔都还没有
        return "账本还是空的，先记一笔吧。"
    hua = "账本明细：\n"
    xuhao = 1                                # 第几笔（从 1 开始数，给人看的）
    for yi_bi in mingxi:                     # 一笔一笔过
        hua = hua + str(xuhao) + ". " + yi_bi + "\n"
        xuhao = xuhao + 1
    hua = hua + "共 " + str(len(mingxi)) + " 笔，合计 " + str(zong) + " 元。"
    return hua


def ji_zhang(wo_de_hua):
    """记一笔账：抠出金额 → 累加总额 → 落盘 → 让 AI 点评一句。"""
    global zong                                  # 要【重新赋值】外面的 zong（= 换本子），必须声明
    xiaoxi.append({"role": "user", "content": wo_de_hua})

    jine = zhua_shuzi(wo_de_hua)                 # 抠数字（跟读回用的是同一个函数）
    zong = zong + jine                           # 总额累加
    mingxi.append(wo_de_hua)                     # 明细也留一份（.append 是"改本子"，不用 global）

    with open(zhangben, "a", encoding="utf-8") as f_wj:     # "a" = 追加（不是 "w" 清空）
        f_wj.write(wo_de_hua + "\n")             # 存【整句原文】，含"早饭"这种名字

    resp = client_chat.chat.completions.create(model="glm-4-flash", messages=xiaoxi)
    ta_de_hua = resp.choices[0].message.content
    xiaoxi.append({"role": "assistant", "content": ta_de_hua})

    return ta_de_hua + f"总计:{zong}元。"
