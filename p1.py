with open("Rj.txt", "w",encoding="utf-8") as f:
    f.write("今天学了open打开文件\n")
    f.write("今天学了open打开文件和多加了练习题\n")
    f.write("明天继续\n")

with open("Rj.txt", encoding="utf-8") as f:
    for i in f:
        print(i)