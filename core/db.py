"""数据库工具箱：账本从 zhangben.txt 搬进 MySQL 之后，读写全走这里。

为什么单独开一个文件？
    「连数据库」这件事，记一笔要干、查明细要干、算合计也要干 ——
    同一件事要干好几遍，就该【抽成函数放一处】，以后只维护这一份。
    （跟当初抽 zhua_shuzi() 是同一个道理）

四件事，一个函数一件：
    lian_jie()    开一条到 MySQL 的连接
    jian_biao()   建表（每次启动跑一遍，表已在就跳过）
    cun_yi_bi()   存一笔（原来往 txt 里 append 的那一步）
    du_mingxi()   读全部明细（原来启动时读 txt 的那一步）
    he_ji()       算总额（原来手动累加的 zong 变量，现在由 SQL 现算）
"""

import os
import sys

import pymysql
from dotenv import load_dotenv

# 找 .env：不带参数 = 从本文件所在目录一层层往上找，最终找到工作区根目录那个。
# 数据库的账号密码也放在 .env 里，不写死在代码里（跟 API Key 同一个道理）。
load_dotenv()


def lian_jie(ku_ming=None):
    """开一条到 MySQL 的连接，返回连接对象。

    ku_ming 给了就连那个库；不给就用 .env 里的 MYSQL_DB。
    （之所以允许不指定库，是为了 jian_ku() —— 要建一个还不存在的库，
      必须先用"不指定库"的身份连上去，否则连都连不上。）

    注意：连接是【用完要还】的资源，不是普通变量。
    每次用完必须 .close()，否则 MySQL 那边的连接数会被慢慢占满。
    本文件里统一用 with 语句管它（with 会在块结束时自动 close）。
    """
    return pymysql.connect(
        host=os.getenv("MYSQL_HOST", "127.0.0.1"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        # 注意这里必须判 is not None，不能写 `ku_ming or ...`：
        #   jian_ku() 传进来的是空字符串 ""，它会被 or 当成"假"，直接退回默认库名，
        #   那就变成"连着一个可能还不存在的库去建库"，必然报 Unknown database。
        database=ku_ming if ku_ming is not None else os.getenv("MYSQL_DB", "expense"),
        charset="utf8mb4",          # 中文必须用 utf8mb4，不然 emoji 和生僻字会存成问号
        # DictCursor = 查询结果按【列名】给你，而不是按位置。
        #   默认是按位置给元组：row[0] 是 id、row[1] 是内容……一改表结构全乱。
        #   用字典就能写 row["neirong"]，列名写错会直接报错，不会静默取错列。
        cursorclass=pymysql.cursors.DictCursor,
    )


def jian_ku():
    """建库（不存在才建）。换一台电脑、库还没影子的时候，这一步能自己把家搭好。

    ⚠️ 库名不能像金额那样用 %s 占位 —— 库名是 SQL 的【结构】不是【数据】，
       占位符只能填数据。所以只能把名字拼进语句里，那就必须先校验：
       只允许字母、数字、下划线，别的一律拒掉，防止被人从 .env 里塞奇怪的东西进来。
    """
    ku = os.getenv("MYSQL_DB", "expense")
    if not ku.replace("_", "").isalnum():
        raise ValueError(f"MYSQL_DB 名字不合法：{ku}（只允许字母、数字、下划线）")

    with lian_jie(ku_ming="") as lian:      # 注意：这里【不带库名】连
        with lian.cursor() as youbiao:
            youbiao.execute(f"CREATE DATABASE IF NOT EXISTS `{ku}` DEFAULT CHARSET utf8mb4")
        lian.commit()


def jian_biao():
    """建库 + 建表。都已经存在就跳过，所以每次启动都能安心跑。

    三列的设计用意：
      neirong  存【整句原文】——「喝酒 200」原样留着，名字和钱都在里头。
               跟 txt 时代一个原则：存原始的东西，不存加工过的东西。
      jine     这一笔多少钱。它是从 neirong 里抠出来的（zhua_shuzi 干的活）。
               ⚠️ 只存【每一笔】，绝对不存"累计总额"——累计一存就会翻倍，
               那是踩过的坑。总额永远由 SUM() 现算，见 he_ji()。
      id       自增编号。好处是"第几笔"不用自己数，数据库按插入顺序给号。
    """
    try:
        jian_ku()                                   # 库不在就先建库（连不上也是在这里炸）
        with lian_jie() as lian:
            with lian.cursor() as youbiao:
                youbiao.execute("""
                    CREATE TABLE IF NOT EXISTS zhangmu (
                        id          INT AUTO_INCREMENT PRIMARY KEY,
                        neirong     VARCHAR(200) NOT NULL,
                        jine        INT NOT NULL,
                        jilu_shijian DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
                    ) DEFAULT CHARSET=utf8mb4
                """)
            lian.commit()      # 建表属于"改动"，必须 commit 才真正写进去
    except pymysql.err.OperationalError as cuo:
        # 最常见的一种情况：MySQL 服务没开，3306 没在监听。
        # 报错原文是英文的 (2003, "Can't connect to MySQL server ...")，看不懂容易卡住，
        # 所以这里加一句人话提示。⚠️ 提示完照样 raise 抛出去——
        # 不能把错误"吃掉"假装没事，那样程序会带着坏状态继续跑（又是一个静默错）。
        # ⚠️ 提示走 stderr（跟下面的 traceback 同一个流），这样看到的顺序才是
        #    "先中文提示、后原始报错"。打到 stdout 的话，两股流各走各的，
        #    终端里常常是 traceback 先冒出来把提示盖住。
        print("❌ 连不上 MySQL。先把数据库开起来：双击 D:\\MySQL\\一键启动MySQL.bat",
              file=sys.stderr)
        print(f"   （原始报错：{cuo.args[0]}）", file=sys.stderr)
        raise


def cun_yi_bi(neirong, jine):
    """存一笔账，返回这笔的 id。

    ⚠️ 参数用 %s 占位，把值交给 PyMySQL 去填，【不要用字符串拼接】。
       拼接的写法遇到带引号的内容会把 SQL 撑坏，更严重的是有注入风险。
    """
    with lian_jie() as lian:
        with lian.cursor() as youbiao:
            youbiao.execute(
                "INSERT INTO zhangmu (neirong, jine) VALUES (%s, %s)",
                (neirong, jine),
            )
            xin_id = youbiao.lastrowid     # 刚插进去那行的自增 id
        lian.commit()                      # 写的操作不 commit 等于没写
    return xin_id


def du_mingxi():
    """读出全部明细，按记账先后排好，返回一个列表（每项是个字典）。"""
    with lian_jie() as lian:
        with lian.cursor() as youbiao:
            youbiao.execute("SELECT id, neirong, jine FROM zhangmu ORDER BY id")
            return youbiao.fetchall()


def he_ji():
    """算总花费。账本空的时候返回 0 而不是 None。

    为什么用 COALESCE(SUM(...), 0)？
        一行都没有时，SUM() 返回的是 NULL（"没有值"），不是 0。
        NULL 一参与后面的 += 或字符串拼接，整个结果就废了。
        COALESCE 的意思是"取第一个不是 NULL 的"，所以空表也能给出 0。

    为什么外面再套一层 int()？
        MySQL 对 INT 列求和，返回的类型是 DECIMAL（带小数的定点数），
        PyMySQL 原样给回来就是 Decimal 对象，不是 int。
        显示 "265" 看着没事，但一跟 int 做运算就要来回转类型。
        金额这里全是整数，所以统一转成 int，出这个函数就只剩一种数。
    """
    with lian_jie() as lian:
        with lian.cursor() as youbiao:
            youbiao.execute("SELECT COALESCE(SUM(jine), 0) AS he FROM zhangmu")
            return int(youbiao.fetchone()["he"])
