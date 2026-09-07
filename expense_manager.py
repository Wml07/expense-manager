
records =  []
def add(desc ,amount):
    """记一笔账：把“描述+金额”打包成字典。在放进账本列表。"""
    one = {
        "desc":desc, "amount":amount
    }
    records.append(one)

def tatal():
    """算总花费：把账本里的每一笔 amount 累加起来"""
    s = 0
    for r in records:
        s = s + r["amount"]
    return s

def show():
    """看账本：把每一笔账打印出来。"""
    for r in records:
        print(r["desc"],r["amount"])

add("早饭",8)
add("午饭",15)
add("晚饭",45)
show()
print("总花费: ", tatal())