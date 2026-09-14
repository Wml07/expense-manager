# # nums = [3, 1, 4, 1, 5, 9, 2, 6]
# # nums.sort(reverse=True)          # 排序
# # print(nums)

# nums = [3, 1, 4, 1, 5, 9]
# nums = nums.sort()       # ← 注意这里多了 "="
# print(nums)
# words = ["8", "15", "12"]
# words.sort(reverse=True)
# print(words)


# 1. import os
# 2. 建一个空列表 amounts，装金额（数字）
# 3. 判断 ZB.txt 在不在：
#       在 → with open 读
# 4. for 逐行：
#       strip() 去换行
#       split(",") 拆开
#       取第二段（金额），int() 转成数字
#       append 进 amounts
# 5. amounts.sort(reverse=True)     ← 不接 =
# 6. print(amounts)
import os
Sd = []
if os.path.exists("ZB.txt"):
    with open("ZB.txt",encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            r = line.split(",")
            Sd.append([int(r[1]),r[0]])
        Sd.sort(reverse=True)
        v = Sd[:3]
        for t in v:
            print(t[0], "元 -", t[1])