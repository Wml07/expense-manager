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
while True:
    desc = input("记了什么?(输入q结束):")
    if desc == "q":
        break
    amount = int(input("花了多少?(输入q结束)"))
    one_1 = {"desc":desc, "amount":amount}
    records.append(one_1)


print("有",len(records), "笔")

with open("ZB.txt", "w", encoding="utf-8") as f:
    for r in records:
        f.write(r["desc"] + "," + str(r["amount"]) + "\n")
    