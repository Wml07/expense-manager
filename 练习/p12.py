# p12.py —— 推导式最小实验：一行装完整个列表
# 说明：下面每一组都先写"老办法"（你会的），再用"新办法"（推导式）写一遍，自己对照

# 先准备一份原材料：跟你账本里读出来的东西一个样
records = [["早饭", 8], ["午饭", 15], ["晚饭", 12]]

# 第 1 组
lao = []                                  # 老办法：先建空列表
for r in records:                         # 一条一条遍历
    lao.append(r[0])                      # 每次往里塞一个东西
print(lao)

xin = [r[0] for r in records]             # 新办法：一行
print(xin)

# 第 2 组
lao2 = []
for r in records:
    lao2.append(r[1] * 2)
print(lao2)

xin2 = [r[1] * 2 for r in records]
print(xin2)
