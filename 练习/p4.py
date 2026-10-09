while True:
    a = input("请输入被除数(q退): ")    # ① 接 a（文字）
    if a == "q":                        # ② 判 q
        break
    b = input("请输入除数: ")            # ③ 接 b（文字）
    try:
        a = int(a)                      # ④ 转数字
        b = int(b)
        print(a, "÷", b, "=", a / b)    # ⑤ 算（除 0 在这儿炸）
    except:
        print("输入有误，重新来")         # ⑥ 不 break → 回到顶部重来
