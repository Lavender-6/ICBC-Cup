# -*- coding: utf-8 -*-
"""用 PIL 绘制专利引用网络图与趋势图（PNG，透明底），供 PPTX 生成器使用。"""
import os
from PIL import Image, ImageDraw, ImageFont

GOLD = (232, 179, 75)
GOLD_L = (245, 212, 136)
RED = (199, 0, 11)
BLUE = (91, 125, 187)
GREY = (159, 180, 218)

_FONT_CACHE = {}


def _font(size):
    key = size
    if key in _FONT_CACHE:
        return _FONT_CACHE[key]
    cands = [
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/msyhbd.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/simsun.ttc",
    ]
    f = None
    for p in cands:
        if os.path.exists(p):
            try:
                f = ImageFont.truetype(p, size)
                break
            except Exception:
                continue
    if f is None:
        f = ImageFont.load_default()
    _FONT_CACHE[key] = f
    return f


# ---------------- 大网络图 560 x 292 ----------------
NODES = [
    (280, 140, 26, GOLD),   # hub
    (100, 60, 14, GOLD_L),
    (150, 225, 16, GOLD),
    (250, 60, 18, GOLD_L),
    (330, 215, 17, GOLD_L),
    (400, 90, 19, GOLD),
    (470, 190, 13, GOLD_L),
    (520, 60, 10, BLUE),
    (80, 150, 9, BLUE),
    (200, 265, 10, BLUE),
    (430, 265, 12, BLUE),
    (540, 135, 9, RED),
    (350, 45, 11, BLUE),
    (170, 110, 8, BLUE),
]
EDGES = [
    (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 7), (0, 13),
    (3, 12), (5, 6), (4, 10), (2, 9), (5, 7), (6, 11), (1, 13), (3, 13),
]


def draw_network(path, W=560, H=292, s=3):
    img = Image.new("RGBA", (W * s, H * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    lw = max(1, int(1.4 * s))
    for a, b in EDGES:
        x1, y1 = NODES[a][0] * s, NODES[a][1] * s
        x2, y2 = NODES[b][0] * s, NODES[b][1] * s
        d.line([x1, y1, x2, y2], fill=BLUE + (150,), width=lw)
    for (x, y, r, c) in NODES:
        d.ellipse([(x - r) * s, (y - r) * s, (x + r) * s, (y + r) * s],
                  fill=c + (255,))
    f = _font(int(13 * s))
    d.text((NODES[0][0] * s - 34 * s, NODES[0][1] * s + NODES[0][2] * s + 8 * s),
           "核心专利", font=f, fill=GOLD_L + (255,))
    img.save(path)
    return path


# ---------------- 趋势图 624 x 292 ----------------
def draw_trend(path, W=624, H=292, s=3):
    img = Image.new("RGBA", (W * s, H * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    S = lambda v: v * s
    # 网格
    for y in (40, 100, 160, 220):
        d.line([S(50), S(y), S(600), S(y)], fill=BLUE + (70,), width=max(1, int(s)))
    l1 = [(50, 235), (130, 213), (210, 178), (290, 138), (370, 98), (450, 68), (530, 52)]
    l2 = [(50, 245), (130, 238), (210, 222), (290, 198), (370, 172), (450, 150), (530, 128)]
    # 折线1（金色实线）
    d.line([(S(x), S(y)) for x, y in l1], fill=GOLD + (255,),
           width=max(2, int(3 * s)), joint="curve")
    # 折线2（红色虚线）
    seg = max(4, int(6 * s))
    gap = max(3, int(4 * s))
    for i in range(len(l2) - 1):
        x1, y1 = S(l2[i][0]), S(l2[i][1])
        x2, y2 = S(l2[i + 1][0]), S(l2[i + 1][1])
        import math as _m
        L = _m.hypot(x2 - x1, y2 - y1)
        n = max(1, int(L / (seg + gap)))
        for k in range(n):
            t0 = (k * (seg + gap)) / L
            t1 = min(1.0, (k * (seg + gap) + seg) / L)
            d.line([x1 + (x2 - x1) * t0, y1 + (y2 - y1) * t0,
                    x1 + (x2 - x1) * t1, y1 + (y2 - y1) * t1],
                   fill=RED + (255,), width=max(2, int(3 * s)))
    # 数据点
    rr = max(2, int(4 * s))
    for (x, y) in l1:
        d.ellipse([S(x) - rr, S(y) - rr, S(x) + rr, S(y) + rr], fill=GOLD + (255,))
    for (x, y) in l2:
        d.ellipse([S(x) - rr, S(y) - rr, S(x) + rr, S(y) + rr], fill=RED + (255,))
    # 年份
    fy = _font(int(12 * s))
    years = ["2020", "2021", "2022", "2023", "2024", "2025", "2026"]
    for i, yv in enumerate(years):
        d.text((S(50 + i * 80) - S(14), S(272)), yv, font=fy, fill=GREY + (255,))
    # 图例
    fl = _font(int(13 * s))
    d.rectangle([S(70), S(26), S(86), S(31)], fill=GOLD + (255,))
    d.text((S(94), S(18)), "引用次数", font=fl, fill=GREY + (255,))
    d.rectangle([S(190), S(26), S(206), S(31)], fill=RED + (255,))
    d.text((S(214), S(18)), "质量评分", font=fl, fill=GREY + (255,))
    img.save(path)
    return path


# ---------------- 小网络图 506 x 158 ----------------
SN = [(60, 79, 12, BLUE), (160, 32, 15, GOLD), (160, 126, 11, BLUE),
      (275, 79, 26, GOLD), (380, 38, 13, GOLD_L), (380, 120, 10, BLUE),
      (440, 79, 9, RED)]
SE = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4), (3, 5), (4, 6), (5, 6)]


def draw_small_net(path, W=506, H=158, s=3):
    img = Image.new("RGBA", (W * s, H * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for a, b in SE:
        d.line([SN[a][0] * s, SN[a][1] * s, SN[b][0] * s, SN[b][1] * s],
               fill=BLUE + (150,), width=max(1, int(1.4 * s)))
    for (x, y, r, c) in SN:
        d.ellipse([(x - r) * s, (y - r) * s, (x + r) * s, (y + r) * s],
                  fill=c + (255,))
    f = _font(int(12 * s))
    d.text((248 * s, 112 * s), "枢纽专利", font=f, fill=GOLD_L + (255,))
    img.save(path)
    return path
