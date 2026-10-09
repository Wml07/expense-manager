# 开销管家 —— 第 3 天：账存进文件，关掉程序不丢

FILE_NAME = "账本.txt"      # 账本存在这个文件里（名字自己定）

records = []                # 账本：空列表（启动后会从文件读回旧账）

def add(desc, amount):
    """记一笔账：把"描述+金额"打包成字典，再放进账本列表。"""
    one = {"desc": desc, "amount": amount}
    records.append(one)

def total():
    """算总花费：把账本里每一笔的 amount 累加起来。"""
    s = 0
    for r in records:
        s = s + r["amount"]
    return s

def show():
    """看账本：把每一笔账打印出来。"""
    for r in records:
        print(r["desc"], r["amount"])

def load():
    """启动时读文件：把上次存的账一条条搬回 records。"""
    f = open(FILE_NAME, encoding="utf-8")   # 打开文件准备读
    for line in f:                          # 一行一笔账
        line = line.strip()                 # 去掉行尾换行符
        if line == "":                      # 空行就跳过（文件末尾常有）
            continue
        parts = line.split(",")             # "早饭,8" 拆成 ["早饭", "8"]
        add(parts[0], int(parts[1]))        # 加回账本（金额转回数字）
    f.close()

def save():
    """退出前写文件：把账本里每一笔写成一行存进硬盘。"""
    f = open(FILE_NAME, "w", encoding="utf-8")   # 打开准备写（清空旧文件）
    for r in records:                            # 一笔一笔写
        f.write(r["desc"] + "," + str(r["amount"]) + "\n")
    f.close()                                    # 关上，数据落盘

load()                                  # 启动：先读回旧账
while True:
    desc = input("记了什么？(q 结束) ")
    if desc == "q":
        break
    amount = int(input("花了多少？"))
    add(desc, amount)
save()                                  # 退出：把账写进文件
show()
print("目前一共", len(records), "笔，花了", total(), "元")
