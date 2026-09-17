import os

def Rc_02(wenjian):
    Lt = []
    if os.path.exists(wenjian):
        with open(wenjian,encoding="utf-8") as f:
            for lines in f:
                lines = lines.strip()
                try:
                    lineser = lines.split(",")
                    Lt.append([lineser[0],int(lineser[1])])
                except:
                    continue
    return Lt

Dc = {}
for r in Rc_02("ZB.txt"):
    cate = r[0]
    Dc[cate] = Dc.get(cate,0) + r[1]

for D,M in Dc.items():
    print(f"{D}:{M}元")

