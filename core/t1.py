# t1.py —— 验证人设效果（一次性测试脚本）

from tools import ask                       # 把工具箱里的 ask 借过来用

print(ask("今天早饭23，午饭60，晚饭25"))   # 正常
print(ask("帮我写一首诗"))                 # 越界
print(ask("推荐个便宜点的手机"))            # 灰色地带 ← 重点看这个
               # ② 越界问题：看它挡不挡
