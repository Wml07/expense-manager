import os
todos = []                      
if os.path.exists("todo.txt"):
      with open("todo.txt", encoding="utf-8") as f:
           for line in f:
            line = line.strip()
            todos.append(line)
print(todos)
while True:
      a = input("加什么待办?(q结束)")
      if(a == "q"):
           break
      elif(a == "show"):
           for i,t in enumerate(todos):
                print(i + 1, ".", t)
      elif a == "d":
           n = int(input("删除第几条? "))          # 用户输编号
           t = todos.pop(n - 1)                  # ① 填：第几条 = 下标几？
           print("已删除:", t)  
      else:
           todos.append(a)
with open("todo.txt", "w", encoding="utf-8") as f:
      for r in todos:
            f.write(r + "\n")