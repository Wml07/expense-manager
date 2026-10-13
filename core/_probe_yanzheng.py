# _probe_yanzheng.py —— C 项验收：用【真实的 wen_wenti】跑一批问题
# ------------------------------------------------------------------
# 跟 _probe_chuchu.py 的分工：
#   _probe_chuchu.py  —— 诊断用，直接把 AI 原始返回打出来看
#   _probe_yanzheng.py —— 验收用，只看"用户最终拿到的那句话"长什么样
# 它借的是上一级的 gongneng，所以要报地址。
# 用法：cd core && python _probe_yanzheng.py
# ------------------------------------------------------------------
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from gongneng import wen_wenti      # noqa: E402

WENTI = [
    ("资料里有", "向量检索的阈值是怎么定出来的？"),
    ("资料里有", "global 是用来干嘛的？"),
    ("资料里没有", "怎么监控 AI 的回答有没有胡说？"),
    ("资料里没有", "Python 的装饰器怎么用？"),
    ("资料里没有", "怎么给这个项目写单元测试？"),
]

for zu, w in WENTI:
    print("=" * 72)
    print(f"【{zu}】{w}")
    print("最终回复：", wen_wenti(w).replace("\n", " ")[:220])
