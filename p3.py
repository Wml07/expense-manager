count = 0
total = 0
over10 = 0
with open("ZB.txt", encoding="utf-8") as f:
    for line in f:
        print(line)
        count = count + 1
        past = line.split(",")
        total = total + int(past[1])
        if int(past[1]) > 10:
            over10 = over10 + 1
print("总共", count, "笔")

print("总共", total, "元")
print("超过10元的笔数", over10)
