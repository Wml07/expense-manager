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
