a = "hello world hello python"
b = a.split(" ")
dic = {}
for w in b:
    if w in dic:
        dic[w] = dic[w] + 1
    else:
        dic[w] = 1
print(dic)