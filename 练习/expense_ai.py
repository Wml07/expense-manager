# 借工具箱：工具箱住在隔壁的「工具箱」文件夹里
#   Python 默认只找"自己这一层"，东西放到隔壁就找不到了，
#   所以开头要先把地址报给它。（__file__ = 本文件自己的完整路径）
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "工具箱"))
import json
from tools import Rc_02, ask       # ← 从 tools 这个文件里，取这两样


if __name__ == "__main__":
    text = ""
    for r,v in Rc_02("ZB.txt"):
        text = text + f"{r},{v}元\n"


    prompt = ("这是我这周的消费账本：\n" + text +
          "\n请按类别汇总金额，只返回 JSON，格式：{\"类别\": 金额}。不要任何其他文字、解释或代码块标记。")

    answer = ask(prompt)          # ① 先原样看它回了什么
# print("AI 原话：", answer)

    data = json.loads(answer)                     # ② 把它变回字典 ← 你来填
    print(data)                    #    看看它长什么样
# print(type(data))

    with open("AI分析结果.json","w",encoding="utf-8") as f:
        a = json.dumps(data,ensure_ascii=False)
        f.write(a)


    with open("AI分析结果.json",encoding="utf-8") as f:
        neirong = f.read()

    huilai = json.loads(neirong)
    print(huilai["午饭"])

