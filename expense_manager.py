FILE_NAME = "ZB.txt"

records = []

def add(desc, amount):
    """记一笔账:把描述+金额 打包成字典，在放进账本列表。"""
    one = {"desc":desc, "amount":amount}
    records.append(one)

def total():
    """算总花费:把账本里每一笔 amount 累加起来。"""
    s = 0
    for r in records:
        s = s + r["amount"]
    return s

def show():
    "看账本:把每一笔账打印出来。"
    for r in records:
        print(r["desc"], r["amount"])

def load():
    """启动时读文件:把上次存的账一条条搬回 records。"""
    with open(FILE_NAME, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line == " ":
                continue
            parts = line.split(",")
            add(parts[0], int(parts[1]))


def save():
    """退出前写进文件:把账本里每一笔写成一行存进硬盘。"""
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        for r in records:
            f.write(r["desc"] + "," + str(r["amount"]) + "\n")

load()
while True:
    desc = input("记了什么? (q 结束)")
    if desc == "q":
        break
    amount = int(input("花了多少?"))
    add(desc, amount)


save()
show()
print("目前一共", len(records), "笔，花了", total(), "元")