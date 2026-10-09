import os
def read_records():
    Sddc = []
    if os.path.exists("ZB.txt"):
        with open("ZB.txt",encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                line_s = line.split(",")
                Sddc.append([line_s[0],int(line_s[1])])
    return Sddc
print(read_records())