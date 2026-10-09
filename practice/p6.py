# # 9/7 那题：数每个词出现几次
# dc = {}
# for w in ["apple", "b", "apple"]:
#     if w in dc:                  # 问：格子里已经有吗？
#         dc[w] = dc[w] + 1        # 有 → 在原来的数上 +1
#     else:
#         dc[w] = 1                # 没有 → 开个新格子，从 1 开始
# print(dc)                        # {'apple': 2, 'b': 1}
dc  = {}
for w in ["apple","b","apple"]:
    if w in dc:
        dc[w] = dc[w] + 1
    else:
        dc[w] = 1
print(dc)