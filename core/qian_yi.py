"""一次性迁移脚本：把 zhangben.txt 里的每一笔，灌进 MySQL 的 zhangmu 表。

跑法：
    python core/qian_yi.py            # 表是空的就直接灌
    python core/qian_yi.py --force    # 表里已有数据，确认清空重灌

这个脚本只跑一次（历史数据搬家用）。以后记账走 gongneng.py 的 ji_zhang()，
不再经过它。留着它是为了"哪天换了电脑、txt 还在，还能重新灌一遍"。

⚠️ 它会把 zhangmu 表清空再灌。所以默认有保护：表非空就停下，除非加 --force。
"""

# pylint: disable=duplicate-code
# （上面这个 zhua_shuzi 故意跟 gongneng.py 重复一份，理由见它的 docstring：
#   一次性脚本要能独立跑。pylint 会把雷同代码当警告，这里明确放行。）
import os
import sys

# 报地址：db.py 跟本文件住在同一个 core 文件夹里，直接能 import
_core = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _core)

from db import lian_jie, jian_biao, cun_yi_bi, he_ji  # pylint: disable=wrong-import-position

# 账本文件在项目根目录（core 的上一层）
ZHANGBEN = os.path.join(os.path.dirname(_core), "zhangben.txt")


def zhua_shuzi(wo_de_hua):
    """从一句话里把数字抠出来，转成整数。

    这里【故意】跟 gongneng.py 里那份重复了一遍，理由：
      本脚本是一次性搬家工具，要能在业务代码改坏、或者不想加载 OpenAI 客户端
      的情况下独立跑起来。为了独立性，宁可重复这三行。
      （如果是长期共用的代码，就该抽一份出来共用，而不是抄。）
    """
    shuzi = ""
    for z in wo_de_hua:
        if z.isdigit():
            shuzi = shuzi + z
    return int(shuzi)


def du_txt():
    """读 zhangben.txt，返回 [(原文, 金额), ...]，顺手算一个 Python 侧的总额。

    跳过空行、跳过一个字都没有数字的行（跟原来 gongneng 启动读回的逻辑一致）。
    """
    if not os.path.exists(ZHANGBEN):
        print(f"找不到账本文件：{ZHANGBEN}")
        sys.exit(1)

    jilu = []
    py_he = 0                         # Python 侧自己加一遍，待会儿跟 SQL 的 SUM 对账
    with open(ZHANGBEN, encoding="utf-8") as f:
        for hang in f:
            hang = hang.strip()
            if hang == "":
                continue
            try:
                jine = zhua_shuzi(hang)
            except ValueError:        # 这行一个数字都没有 → 跳过，不崩
                print(f"  [跳过] 抠不出数字：{hang}")
                continue
            jilu.append((hang, jine))
            py_he = py_he + jine
    return jilu, py_he


def main():
    """主流程：建表 → 防重复保护 → 清空 → 逐笔灌入 → 对账。"""
    jian_biao()                       # 表不存在就先建（第一次跑用得上）

    # ── 保护：表里已经有数据就不动，除非明确 --force ──────────────────
    with lian_jie() as lian:
        with lian.cursor() as youbiao:
            youbiao.execute("SELECT COUNT(*) AS n FROM zhangmu")
            yiyou = youbiao.fetchone()["n"]

    if yiyou > 0 and "--force" not in sys.argv:
        print(f"zhangmu 表里已经有 {yiyou} 笔了，为防止灌重，先停下。")
        print("确认要清空重灌，就加参数：python core/qian_yi.py --force")
        sys.exit(1)

    jilu, py_he = du_txt()
    print(f"从 txt 读到 {len(jilu)} 笔，Python 累加合计 {py_he} 元\n")

    with lian_jie() as lian:
        with lian.cursor() as youbiao:
            youbiao.execute("TRUNCATE TABLE zhangmu")   # 清空（自增 id 也归零）
        lian.commit()

    for i, (neirong, jine) in enumerate(jilu, 1):
        cun_yi_bi(neirong, jine)                         # 一笔一条 INSERT
        print(f"  第 {i} 笔：{neirong}  →  {jine} 元")

    # ── 对账：Python 加一遍 vs SQL 现算一遍，两条不同的路应该走到同一个数 ──
    sql_he = he_ji()
    print(f"\n数据库合计：{sql_he} 元（SQL 的 SUM 算的）")
    if sql_he == py_he:
        print(f"✅ 对上了：{len(jilu)} 笔，{sql_he} 元。")
    else:
        print(f"❌ 对不上！Python 算 {py_he}，SQL 算 {sql_he}，差 {py_he - sql_he}。")


if __name__ == "__main__":
    main()
