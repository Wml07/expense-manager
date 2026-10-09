import os
def R_c(wenj):
    records_02 = []
    if os.path.exists(wenj):
        with open(wenj,encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                try:
                    line_01 = line.split(",")
                    records_02.append([line_01[0],int(line_01[1])])
                except:
                    continue
    return records_02
print(R_c("ZB.txt"))


dc = {}
for r in R_c("ZB.txt"):
    cate = r[0]
    dc[cate] = dc.get(cate, 0) + r[1]   # 累加金额

for C,M in dc.items():
    print(f"{C}:{M}元")