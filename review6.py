import os
def R_c():
    records_02 = []
    dc = {}
    if os.path.exists("ZB.txt"):
        with open("ZB.txt",encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                try:
                    line_01 = line.split(",")
                    records_02.append([line_01[0],int(line_01[1])])
                except:
                    continue
    return records_02
print(R_c())


dc = {}
for r in R_c():
    cate = r[0]
    dc[cate] = dc.get(cate, 0) + r[1]   # 累加金额
print(dc)