# -*- coding: utf-8 -*-
"""生成 README 用的演示动图：终端风格，逐行播放【真实运行过的输出】。

跑法：  D:/python3.11.8/python.exe docs/make_demo.py
产物：  docs/demo-1-jizhang.gif   （记一笔账 → 查明细）
        docs/demo-2-wenti.gif     （问个问题 → 附来源）

为什么用脚本生成、而不是录屏？
  ① 不依赖录屏软件，随时能重跑；
  ② 下面 SCRIPT 里的每一句文字都来自真实运行（含真实 AI 回复），不是手画的；
  ③ 以后改了功能，重跑一次动图就更新，不会"图跟代码对不上"。

唯一"补"上去的东西：用户敲进去的字符（1 / 早饭23 / 3 / 2 / 4）。
真实终端会把它显示出来，但用管道喂输入时它不进 stdout，所以这里手动补画，
让它看起来就像有人坐在那儿操作。
"""
import os
import unicodedata
from PIL import Image, ImageDraw, ImageFont

# ─────────────── 外观参数 ───────────────
W, H = 960, 500                 # 画布尺寸
TITLE_H = 44                    # 顶部标题栏高度
PAD_X = 22                      # 左右留白
TOP_Y = 60                      # 第一行文字的位置
LINE_H = 20                     # 行高
FS_ASCII = 14                   # 英文/数字字号
FS_CJK = 15                     # 中文字号
CELL = 7.7                      # 一个"半宽字符"占几像素 —— 等宽排版的基准
MAX_UNITS = int((W - PAD_X * 2) / CELL)     # 一行最多放几个半宽单位

BG = (13, 17, 23)               # 终端底色
BAR = (22, 27, 34)              # 标题栏
DOTS = [(255, 95, 86), (255, 189, 46), (39, 201, 63)]   # 左上角三个圆点
COLOR = {
    "n":  (201, 209, 217),   # 普通输出
    "t":  (88, 166, 255),    # 提示符 / 菜单标题（蓝）
    "u":  (255, 255, 255),   # 用户敲进去的字（亮白）
    "hi": (210, 153, 34),    # 想让读者注意的行：来源 / 合计（琥珀）
    "d":  (139, 148, 158),   # 暗灰
}

def pick_font(paths, size):
    """按顺序挑第一个装得上的字体（找不到就退回雅黑，别让脚本崩）。"""
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", size)


FONT_ASCII = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", FS_ASCII)
FONT_CJK = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", FS_CJK)
FONT_TITLE = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 13)
# ⭐ 这类符号雅黑里没有字形，硬画会变成豆腐方块 —— 得单独找个符号字体
FONT_SYM = pick_font(["C:/Windows/Fonts/seguisym.ttf",
                      "C:/Windows/Fonts/seguiemj.ttf"], FS_CJK + 4)


def char_units(ch):
    """这个字占几个"半宽单位"：ASCII 占 1，其余（汉字/中文标点/⭐）占 2。"""
    return 1 if ord(ch) < 128 else 2


def is_symbol(ch):
    """是不是"符号字"（⭐ → ✓ ￥ 这类）—— 它们要走符号字体。"""
    return unicodedata.category(ch) in ("So", "Sm", "Sk", "Sc")


def wrap(text, max_units=MAX_UNITS):
    """一行太长就折行 —— 真终端也会这么折。"""
    out, cur, w = [], "", 0
    for ch in text:
        cw = char_units(ch)
        if w + cw > max_units:
            out.append(cur)
            cur, w = "", 0
        cur += ch
        w += cw
    out.append(cur)
    return out


def draw_text(d, x, y, text, color):
    """逐字画，按字符类型分三档字体：
         ASCII  → Consolas（更像真终端）
         符号   → Segoe UI Symbol（雅黑没有 ⭐ 这类字形）
         其余   → 微软雅黑（汉字 / 中文标点）
    返回画完后的 x。"""
    for ch in text:
        if ord(ch) < 128:
            d.text((x, y), ch, font=FONT_ASCII, fill=color)
        elif is_symbol(ch):
            d.text((x, y - 3), ch, font=FONT_SYM, fill=color)   # 上移一点，跟汉字对齐
        else:
            d.text((x, y), ch, font=FONT_CJK, fill=color)
        x += CELL * char_units(ch)
    return x


def draw_screen(rows, subtitle):
    """rows = [ [(文字, 颜色键), ...], ... ]，画成一整屏。"""
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, TITLE_H], fill=BAR)
    for i, c in enumerate(DOTS):
        x = PAD_X + i * 20
        d.ellipse([x, TITLE_H / 2 - 6, x + 12, TITLE_H / 2 + 6], fill=c)
    d.text((W / 2, TITLE_H / 2), subtitle, font=FONT_TITLE, fill=COLOR["d"], anchor="mm")
    y = TOP_Y
    for row in rows:
        x = PAD_X
        for text, key in row:
            x = draw_text(d, x, y, text, COLOR[key])
        y += LINE_H
    return img


# ─────────────── 演示脚本 ───────────────
# 每一句都来自真实运行。用 out() 表示"程序打印一行"，用 inp() 表示"用户敲进去的"。
def out(steps, text, key="n", delay=170):
    """程序输出一行（太长会自动折行）。"""
    for i, line in enumerate(wrap(text)):
        steps.append({"kind": "out", "text": line, "key": key,
                      "delay": delay if i == 0 else 90})


def inp(steps, prompt, typed, delay=80):
    """提示符 + 用户逐字敲进去的输入。"""
    steps.append({"kind": "in", "prompt": prompt, "typed": typed, "delay": delay})


def caidan(steps):
    """那五行菜单 —— 每次回到主界面都会重打一遍，真实输出就是这样。"""
    out(steps, "===== 开销管家 =====", "t", 420)
    out(steps, "1. 记一笔账")
    out(steps, "2. 问个问题")
    out(steps, "3. 查明细")
    out(steps, "4. 退出")


def seg_jizhang():
    """第一幕：记一笔账（真实输出：早饭花了23元，还挺丰盛的啊。总计:88元。）"""
    s = []
    caidan(s)
    inp(s, "请输入编号:", "1", 260)
    inp(s, "请记账:", "早饭23", 95)
    out(s, "早饭花了23元，还挺丰盛的啊。总计:88元。", "n", 1300)   # 这里在等 AI 回话
    return s


def seg_mingxi():
    """第二幕：查明细（真实输出：5 笔，合计 88 元）"""
    s = []
    caidan(s)
    inp(s, "请输入编号:", "3", 260)
    out(s, "账本明细：", "t", 320)
    for i in ("1. 早饭10", "2. 午饭15", "3. 晚饭20", "4. 打车20", "5. 早饭23"):
        out(s, i, "n", 130)
    out(s, "共 5 笔，合计 88 元。", "hi", 2600)
    return s


def seg_wenti():
    """第三幕：问个问题 —— 重点是末尾那行【来源】（代码给的，不是 AI 说的）"""
    s = []
    caidan(s)
    inp(s, "请输入编号:", "2", 260)
    inp(s, "请输入你的问题:", "向量检索的阈值是怎么定出来的", 65)
    out(s, "阈值必须拿一批“已知答案”的问题去标定", "n", 1300)    # 在等 AI 回话
    out(s, "", "n", 260)
    out(s, "（来源：30. 向量检索：不比“字”，比“意思” ⭐⭐、4. 循环：批量干活的引擎、"
           "25. system 人设：给 AI 立规矩（prompt 工程第一颗螺丝）⭐）", "hi", 3200)
    return s


def seg_tuichu():
    """第四幕：退出"""
    s = []
    caidan(s)
    inp(s, "请输入编号:", "4", 260)
    out(s, "再见", "n", 2400)
    return s


# ─────────────── 播放并导出 GIF ───────────────
def play(steps, subtitle):
    """把 steps 逐帧画出来。返回 (帧列表, 每帧停留毫秒列表)。"""
    rows, frames, durations = [], [], []
    for st in steps:
        if st["kind"] == "out":
            rows.append([(st["text"], st["key"])])
            frames.append(draw_screen(rows, subtitle))
            durations.append(st["delay"])
        else:
            rows.append([(st["prompt"], "t")])
            frames.append(draw_screen(rows, subtitle))
            durations.append(240)
            for i in range(1, len(st["typed"]) + 1):
                rows[-1] = [(st["prompt"], "t"), (st["typed"][:i], "u")]
                frames.append(draw_screen(rows, subtitle))
                durations.append(st["delay"])
    frames.append(frames[-1])          # 末尾多停一拍再循环
    durations.append(2600)
    return frames, durations


def save_gif(frames, durations, path):
    # 统一调色板 + 帧间差分：先转成 64 色的 P 模式，文件能小一大截
    pal = [f.quantize(colors=64, method=Image.MEDIANCUT) for f in frames]
    pal[0].save(path, save_all=True, append_images=pal[1:],
                duration=durations, loop=0, optimize=True, disposal=2)
    print("已生成 %s  （%d 帧，%.0f KB）" % (path, len(frames), os.path.getsize(path) / 1024))


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    jobs = [
        (seg_jizhang() + seg_mingxi(), "开销管家 · 记一笔账 / 查明细", "demo-1-jizhang.gif"),
        (seg_wenti() + seg_tuichu(), "开销管家 · 资料问答（附来源）", "demo-2-wenti.gif"),
    ]
    for steps, subtitle, name in jobs:
        frames, durations = play(steps, subtitle)
        save_gif(frames, durations, os.path.join(here, name))


if __name__ == "__main__":
    main()
