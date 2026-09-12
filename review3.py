import os

records = []

if os.path.exists("ZB.txt"):
    with open("ZB.txt",encoding="utf-8") as f:
        for line in f:
            line =  line.strip()
            parts = line.split(",")
            one = {"desc":parts[0], "amount": int(parts[1])}
            records.append(one)
            print(one)
print(records)


while True:                          # 主循环
    desc = input("记了什么?(输入q结束):")
    if desc == "q":
        break
    amount = 0                       # 先占个位，下面会盖掉

    # ↓ 新增：反复问金额，直到输对
    while True:
        text = input("花了多少?")     # 先接住用户打的字，别急着转数字
        try:
            amount = int(text)       # 试着把它变成数字
            break                  # ① 成功 → 跳出这个问话循环（就是一个词）
        except:
            print("这不是数字，重新输一遍")   # 失败 → 不崩，提醒一句，接着问
    # ↑ 新增结束

    records.append({"desc": desc, "amount": amount})


print("有",len(records), "笔")

with open("ZB.txt", "w", encoding="utf-8") as f:
    for r in records:
        f.write(r["desc"] + "," + str(r["amount"]) + "\n")




    