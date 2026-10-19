# 借工具箱：它住在隔壁的「core」文件夹里
#   Python 默认只找"自己这一层"，东西放到隔壁就找不到了，
#   所以开头要先把地址报给它。（__file__ = 本文件自己的完整路径）
# pylint: disable=wrong-import-position
# （跨文件夹借模块必须先报地址再 import，天然违反"import 放最上面"，故本文件放行）
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "core"))


from gongneng import wen_wenti,ji_zhang,cha_mingxi,kan_tongji

# ⚠️ 菜单号和下面那串 if shuru == 是【绑死的】：
#    菜单上写几号，下面的引号里就得是几号。改一个必须改另一个，
#    否则会出现"点了 3 却弹出别的功能"——程序不报错，纯静默错位。
#    （10/19 加"看统计"就是一次示范：菜单多了 4，退出必须从 4 挪到 5，
#      两处一起改。规矩是【退出永远排在最后一个号】。）
while True:
    print("===== 开销管家 =====")
    print("1. 记一笔账")
    print("2. 问个问题")
    print("3. 查明细")
    print("4. 看统计")
    print("5. 退出")

    shuru = input("请输入编号:")
    if shuru == '1':
        ji_zhang_01 = input("请记账:")
        print(ji_zhang(ji_zhang_01))
    elif shuru == '2':
        wenti_01 = input("请输入你的问题:")
        print(wen_wenti(wenti_01))
    elif shuru == '3':
        print(cha_mingxi())          # 明细在 gongneng 里拼好，这里只负责打印
    elif shuru == '4':
        print(kan_tongji())          # 统计也是 gongneng 拼好，门只管打印
    elif shuru == '5':
        print("再见")
        break
    else:
        print("请重新输入编号")
