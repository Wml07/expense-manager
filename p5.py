import os
def read_records():
    Sddc = []
    if os.path.exists("ZB_bad.txt"):
        with open("ZB_bad.txt",encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                try:
                    line_s = line.split(",")
                    Sddc.append([line_s[0],int(line_s[1])])
                except:
                    continue
    return Sddc
print(read_records())