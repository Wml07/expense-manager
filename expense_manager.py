
# records =  []
# def add(desc ,amount):
#     """记一笔账：把“描述+金额”打包成字典。在放进账本列表。"""
#     one = {
#         "desc":desc, "amount":amount
#     }
#     records.append(one)

# def tatal():
#     """算总花费：把账本里的每一笔 amount 累加起来"""
#     s = 0
#     for r in records:
#         s = s + r["amount"]
#     return s

# def show():
#     """看账本：把每一笔账打印出来。"""
#     for r in records:
#         print(r["desc"],r["amount"])

# add("早饭",8)
# add("午饭",15)
# add("晚饭",45)
# show()
# print("总花费: ", tatal())


# 开销管家 —— 第 2 天：键盘输入记账

# records = []  # 账本：空列表

# def add(desc, amount):
#     """记一笔账：把"描述+金额"打包成字典，再放进账本列表。"""
#     one = {"desc": desc, "amount": amount}
#     records.append(one)

# def total():
#     """算总花费：把账本里每一笔的 amount 累加起来。"""
#     s = 0
#     for r in records:
#         s = s + r["amount"]
#     return s

# def show():
#     """看账本：把每一笔账打印出来。"""
#     for r in records:
#         print(r["desc"], r["amount"])

# # —— 键盘输入主循环：程序从"写死"变成"会问" ——
# while True:                               # 一直循环
#     desc = input("记了什么？(输 q 结束) ")   # 停下来等你输入，回车后交给你
#     if desc == "q":                       # 你输的是 q 吗？
#         break                             # 是 → 跳出循环，往下走
#     amount = int(input("花了多少？"))       # 金额过 int() 变成真数字
#     add(desc, amount)                     # 记进账本

# show()                                    # 循环结束，看账本
# print("总花费: ", total())
records = []
def add(desc, amount):
    """记一笔账:把描述+金额打包成字典，在放进账本列表"""
    one = {"desc":desc, "amount":amount}
    records.append(one)

def total():
    """算总花费:把账本里每一笔的 amount 累加起来"""
    s = 0
    for r in records:
        s= s + r["amount"]
    return s

def show():
    """看账本:把每一笔账打印出来"""
    for r in records:
        print(r["desc"], r["amount"])

while True:
    desc = input("记了什么？(输入q结束)")
    if desc == "q":
        break
    amount = int(input("花了多少？"))
    add(desc, amount)

show()
print("目前一共", len(records), "笔，花了", total(), "元")
