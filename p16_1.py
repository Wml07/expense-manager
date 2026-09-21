from tools import client, SHEZHI, ask

xiaoxi = [
    {"role":"system", "content":SHEZHI},
]

def shuo(wo_de_hua):
    """带历史地说一句:我塞进去，整份发过去，它的话也塞回去"""

    xiaoxi.append({"role":"user", "content":wo_de_hua})
    resp = client.chat.completions.create(model="qwen-plus", messages=xiaoxi)
    ta_de_hua = resp.choices[0].message.content

    xiaoxi.append({"role":"assistant","content":ta_de_hua})
    return ta_de_hua


print("========== 第一组：带历史（用 shuo）==========")
print(shuo("今天早饭23，午饭60，晚饭25"))
print("【本轮之后，列表里有", len(xiaoxi), "条】")
print(shuo("今天总共花了多少？"))


print("----- 分隔线：下面这句话里，一个数字都没有 -----")
print(shuo("把刚才那三笔再说一遍"))
print("【本轮之后，列表里有", len(xiaoxi), "条】")


print("========== 第二组：对照组，不带历史（用 ask）==========")
print(ask("今天早饭23，午饭60，晚饭25"))
print("----- 同样一句，一个数字都没有 -----")
print(ask("把刚才那三笔再说一遍"))
print(ask("把刚才那三笔再说一遍，直接报数字，不要问我要"))

