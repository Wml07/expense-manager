# scores = [78, 92, 85, 64, 99]
# tatl = 0
# for i in scores:
#     tatl+=i
# avg = tatl / len(scores)
# print(avg)


a = "hello world hello python"
words = a.split(" ")
dc = {}
for w in words:
    if w in dc:
        dc[w] = dc[w] + 1
    else:
        dc[w] = 1
print(dc) 