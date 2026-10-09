# 借工具箱：工具箱住在隔壁的「工具箱」文件夹里
#   Python 默认只找"自己这一层"，东西放到隔壁就找不到了，
#   所以开头要先把地址报给它。（__file__ = 本文件自己的完整路径）
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "工具箱"))
from tools import client_chat, SHEZHI, ask

xiaoxi = [
    {"role":"system", "content":SHEZHI},
]

def shuo(wo_de_hua):
    """带历史地说一句:我塞进去，整份发过去，它的话也塞回去"""

    xiaoxi.append({"role":"user", "content":wo_de_hua})
    resp = client_chat.chat.completions.create(model="glm-4-flash", messages=xiaoxi)
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

