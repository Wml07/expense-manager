# 借工具箱：工具箱住在隔壁的「工具箱」文件夹里
#   Python 默认只找"自己这一层"，东西放到隔壁就找不到了，
#   所以开头要先把地址报给它。（__file__ = 本文件自己的完整路径）
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "工具箱"))
# 借工具箱：工具箱住在隔壁的「工具箱」文件夹里
#   Python 默认只找"自己这一层"，东西放到隔壁就找不到了，
#   所以开头要先把地址报给它。（__file__ = 本文件自己的完整路径）
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "工具箱"))


from gongneng import wen_wenti
while True:
    print("===== 开销管家 =====")
    print("1. 记一笔账")
    print("2. 问个问题")
    print("3. 退出")

    shuru = input("请输入编号:")
    if shuru == '1':
        print("你选了", shuru)
        print("【记账】功能还没接")
    elif shuru == '2':
        wenti_01 = input("请输入你的问题:")
        print(wen_wenti(wenti_01))
    elif shuru == '3':
        print("再见")
        break
    else:
        print("请重新输入编号")