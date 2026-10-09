
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