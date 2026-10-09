
import os
total = 0
if os.path.exists("Z_h.txt"):
    with open("Z_h.txt", encoding="utf-8") as f:
        total = int(f.read())

while True:
    s = 0
    s = input("输入数字（q退出）:")
    if s == "q":
        break
    total = total + int(s)

with open("Z_h.txt", "w", encoding="utf-8") as f:
    print("总和:", total)
    f.write(str(total))