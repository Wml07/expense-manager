# 借工具箱：工具箱住在隔壁的「工具箱」文件夹里
#   Python 默认只找"自己这一层"，东西放到隔壁就找不到了，
#   所以开头要先把地址报给它。（__file__ = 本文件自己的完整路径）
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "工具箱"))
from tools import Rc_02

records = Rc_02("ZB.txt")
wufan = [r for r in records if r[0] == "午饭" ]
print(wufan)