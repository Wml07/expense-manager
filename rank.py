import os

def read_records_01():
    Sd = []
    if os.path.exists("ZB.txt"):
        with open("ZB.txt",encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                line_1 = line.split(",")
                Sd.append([line_1[0], int(line_1[1])])
    return Sd

pl = []
Sd_1 = read_records_01()
for t in Sd_1:
    pl.append([(t[1]),t[0]])
pl.sort(reverse=True)
for v in pl[:3]:
    print(v[0],"元 -",v[1])