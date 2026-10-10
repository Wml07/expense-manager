# 借工具箱：它住在隔壁的「core」文件夹里
#   Python 默认只找"自己这一层"，东西放到隔壁就找不到了，
#   所以开头要先把地址报给它。（__file__ = 本文件自己的完整路径）
# pylint: disable=wrong-import-position
# （跨文件夹借模块必须先报地址再 import，天然违反"import 放最上面"，故本文件放行）
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "core"))
from tools import Rc_02

records = Rc_02("ZB.txt")
wufan = [r for r in records if r[0] == "午饭" ]
print(wufan)