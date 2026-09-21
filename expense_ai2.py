# expense_ai2.py —— 代码管数，AI 管话
# 分工铁律：数字全部由代码算好；AI 只负责把算好的数字说成人话
#
# 注意：tools.py 里 ask() 的人设已经改成「只点评、一个字都不许出现数字」了，
#       所以这里不用再拼规矩 —— 规矩已经在 system 里站着了。

from tools import Rc_02, ask


if __name__ == "__main__":
    # ① 读账本（已经会了，照写）
    records = Rc_02("ZB.txt")

    # ② 字典汇总：类别当钥匙，金额往里累加
    hz = {}
    zonge = 0
    for r, v in records:
        hz[r] = hz.get(r,0) + v          # ← 空① 累加到对应类别（提示：.get(钥匙, 0) + 金额）
        zonge = zonge + v         # ← 空② 总额累加

    # ③ 先让代码把"真数"打出来 —— 这一步锁死，谁也不能推翻
    huiwen = ""
    for k, v in hz.items():
        zhanbi = round(v / zonge * 100)
        huiwen = huiwen + f"{k}: {v}元 (占{zhanbi}%)\n"
        print(f"{k}: {v}元 (占{zhanbi}%)")
    huiwen = huiwen + f"总计: {zonge}元"
    print(f"总计: {zonge}元")

    # ④ 把算好的汇总交给 AI —— 它只管说话，不碰数字
    prompt = "这是我记账的汇总，数字已由程序算好，是准确的：\n" + huiwen
    print("【AI 的话】")
    hua = ask(prompt)                # ← 空③ 调 ask，把 prompt 发过去

    print(hua)
