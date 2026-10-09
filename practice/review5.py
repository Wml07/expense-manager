import os
todos_1 = []
if os.path.exists("todos_1.txt"):
    with open("todos_1.txt", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            todos_1.append(line)
print(todos_1)
while True:
    a = input("加什么待办(q结束)")
    if(a == "q"):
        break
    elif(a == "show"):
        for i,t in enumerate(todos_1):
            print(i+1, "." , "- " + t)
    elif(a == "d"):
        b = int(input("删除第几条?:"))
        v = todos_1.pop(b - 1)
        print("已删除:", v)
    else:
        todos_1.append(a)
with open("todos_1.txt", "w", encoding="utf-8") as f:
    for r in todos_1:
        f.write(i + "\n")