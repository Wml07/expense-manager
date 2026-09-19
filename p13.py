from tools import Rc_02

records = Rc_02("ZB.txt")
wufan = [r for r in records if r[0] == "午饭" ]
print(wufan)