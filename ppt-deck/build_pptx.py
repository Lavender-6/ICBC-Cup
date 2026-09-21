# -*- coding: utf-8 -*-
"""
工银科创桥 — 项目汇报 PPTX 生成器
深蓝 #0A1730 + 工行红 #C7000B + 金 #E8B34B，对齐官网 dark 主题。
"""
import os, math
from lxml import etree
from pptx import Presentation
from pptx.util import Pt, Inches
from pptx.oxml.ns import qn
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from PIL import Image

# ---------- 路径 ----------
ROOT = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(ROOT, "frontend", "public", "assets", "images")
TMP = os.path.join(ROOT, "build")
os.makedirs(TMP, exist_ok=True)

# ---------- 主题色 ----------
NAVY_D  = "0A1730"
NAVY_C  = "0E2145"
NAVY_P  = "143061"
RED     = "C7000B"
RED_L   = "FF5A4E"
GOLD    = "E8B34B"
GOLD_L  = "F5D488"
BLUE    = "5B7DBB"
GREY    = "9FB4DA"
WHITE   = "E0E6F0"

FONT = "Microsoft YaHei"

# ---------- 坐标：使用 1440x810 布局坐标系 ----------
SCALE = 2.0 / 3.0   # px -> pt


def P(v):
    """布局像素 -> PPT 长度"""
    return Pt(v * SCALE)


# ============================================================
# 基础绘制工具
# ============================================================
def _srgb(parent, hexcolor, alpha=None):
    clr = etree.SubElement(parent, qn("a:srgbClr"), val=hexcolor)
    if alpha is not None and alpha < 100:
        from lxml import etree as _e
        etree.SubElement(clr, qn("a:alpha"), val=str(int(alpha * 1000)))
    return clr


def _spPr_insert(shape, elem):
    """按 DrawingML 顺序把 fill 元素插到 prstGeom 之后"""
    spPr = shape._element.spPr
    for child in list(spPr):
        tag = child.tag.split("}")[-1]
        if tag in ("solidFill", "gradFill", "noFill", "pattFill", "blipFill"):
            spPr.remove(child)
    insert_at = None
    for i, child in enumerate(spPr):
        if child.tag.split("}")[-1] in ("prstGeom", "custGeom"):
            insert_at = i + 1
            break
    if insert_at is None:
        spPr.append(elem)
    else:
        spPr.insert(insert_at, elem)


def solid_fill(shape, hexcolor, alpha=100):
    from lxml import etree as _e
    shape.fill.solid()
    sf = shape.fill._xPr
    for c in list(sf):
        if c.tag.split("}")[-1] != "srgbClr":
            sf.remove(c)
    for c in list(sf.findall(qn("a:srgbClr"))):
        c.getparent().remove(c)
    _srgb(sf, hexcolor, alpha)


def grad_fill(shape, c1, a1, c2, a2, angle_deg=0):
    from lxml import etree as _e
    grad = etree.Element(qn("a:gradFill"), rotWithShape="0")
    gsl = etree.SubElement(grad, qn("a:gsLst"))
    gs0 = etree.SubElement(gsl, qn("a:gs"), pos="0")
    _srgb(gs0, c1, a1)
    gs1 = etree.SubElement(gsl, qn("a:gs"), pos="100000")
    _srgb(gs1, c2, a2)
    lin = etree.SubElement(grad, qn("a:lin"))
    lin.set("ang", str(int(angle_deg * 60000)))
    lin.set("scaled", "0")
    _spPr_insert(shape, grad)


def no_line(shape):
    shape.line.fill.background()


def no_fill(shape):
    shape.fill.background()


def rect(slide, x, y, w, h, fill=None, alpha=100, grad=None,
         line=None, line_w=1, radius=None, shape_type=MSO_SHAPE.RECTANGLE):
    """矩形 / 圆角矩形。grad=(c1,a1,c2,a2,angle)"""
    sh = slide.shapes.add_shape(shape_type, P(x), P(y), P(w), P(h))
    sh.shadow.inherit = False
    no_line(sh)
    if grad:
        grad_fill(sh, grad[0], grad[1], grad[2], grad[3], grad[4] if len(grad) > 4 else 0)
    elif fill:
        solid_fill(sh, fill, alpha)
    else:
        no_fill(sh)
    if line:
        sh.line.color.rgb = None
        sh.line.fill.solid()
        sh.line.fill.fore_color.rgb = hex2rgb(line)
        sh.line.width = Pt(line_w)
    if radius is not None and shape_type == MSO_SHAPE.ROUNDED_RECTANGLE:
        try:
            sh.adjustments[0] = radius
        except Exception:
            pass
    return sh


def hex2rgb(h):
    from pptx.dml.color import RGBColor
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def text(slide, x, y, w, h, runs, size=17, color=WHITE, bold=False,
         align="left", anchor="top", line_spacing=1.35, space_after=0, wrap=True):
    """
    runs: str 或 list[dict{t:文本, c:颜色, b:粗体, s:字号}]
    """
    tb = slide.shapes.add_textbox(P(x), P(y), P(w), P(h))
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    tf.vertical_anchor = {"top": MSO_ANCHOR.TOP, "middle": MSO_ANCHOR.MIDDLE,
                          "bottom": MSO_ANCHOR.BOTTOM}[anchor]
    if isinstance(runs, str):
        runs = [{"t": runs}]
    p = tf.paragraphs[0]
    p.alignment = {"left": PP_ALIGN.LEFT, "center": PP_ALIGN.CENTER,
                   "right": PP_ALIGN.RIGHT}[align]
    p.line_spacing = line_spacing
    p.space_after = Pt(space_after)
    first = True
    for it in runs:
        t = it.get("t", "")
        if "\n" in t:
            parts = t.split("\n")
            for i, part in enumerate(parts):
                if i > 0:
                    p = tf.add_paragraph()
                    p.alignment = {"left": PP_ALIGN.LEFT, "center": PP_ALIGN.CENTER,
                                   "right": PP_ALIGN.RIGHT}[align]
                    p.line_spacing = line_spacing
                    p.space_after = Pt(space_after)
                _run(p, part, it, size, color, bold)
            first = False
            continue
        _run(p, t, it, size, color, bold)
        first = False
    return tb


def _run(p, t, it, size, color, bold):
    r = p.add_run()
    r.text = t
    r.font.name = FONT
    r.font.size = Pt(it.get("s", size) * SCALE)
    r.font.bold = it.get("b", bold)
    r.font.color.rgb = hex2rgb(it.get("c", color))


def pic(slide, path, x, y, w, h):
    return slide.shapes.add_picture(path, P(x), P(y), P(w), P(h))


# ============================================================
# 图片预处理：裁剪为 16:9 + 生成径向光晕
# ============================================================
def prep_bg(name, quality_w=1920):
    src = os.path.join(IMG, name)
    dst = os.path.join(TMP, name.replace(".png", "_169.png"))
    if os.path.exists(dst):
        return dst
    im = Image.open(src).convert("RGB")
    tw, th = quality_w, int(quality_w * 810 / 1440)
    sw, sh = im.size
    s = max(tw / sw, th / sh)
    im = im.resize((int(sw * s), int(sh * s)), Image.LANCZOS)
    sw, sh = im.size
    im.crop(((sw - tw) // 2, (sh - th) // 2,
             (sw - tw) // 2 + tw, (sh - th) // 2 + th)).save(dst)
    return dst


def make_glow(name, rgb, size=560, max_alpha=90):
    dst = os.path.join(TMP, name)
    if os.path.exists(dst):
        return dst
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    px = img.load()
    c = size / 2.0
    for y in range(size):
        for x in range(size):
            d = math.hypot(x - c, y - c) / c
            if d < 1.0:
                px[x, y] = (rgb[0], rgb[1], rgb[2], int(max_alpha * (1 - d) ** 2.4))
    img.save(dst)
    return dst


# ============================================================
# 页面通用构件
# ============================================================
def page_base(slide, bgfile, grad, glows=()):
    """grad=(c1,a1,c2,a2,angle)；glows=[(path,x,y,w,h)]"""
    pic(slide, bgfile, 0, 0, 1440, 810)
    ov = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, P(1440), P(810))
    ov.shadow.inherit = False
    no_line(ov)
    grad_fill(ov, grad[0], grad[1], grad[2], grad[3], grad[4] if len(grad) > 4 else 0)
    for g in glows:
        pic(slide, g[0], g[1], g[2], g[3], g[4])


def header(slide, kicker, title, sub=None, part_color=GOLD):
    rect(slide, 60, 46, 4, 26, fill=GOLD)
    text(slide, 76, 44, 700, 26, kicker, size=15, color=part_color, bold=True,
         line_spacing=1.0)
    text(slide, 60, 78, 1000, 52, title, size=38, color=GOLD_L, bold=True,
         line_spacing=1.05)
    y = 138
    if sub:
        text(slide, 60, y + 6, 900, 28, sub, size=17, color=GREY, line_spacing=1.1)
        y += 36
    rect(slide, 60, y, 110, 3, fill=GOLD)
    return y + 14


def card(slide, x, y, w, h, top_color=None, border=BLUE, alpha=70, fill=None):
    """卡片：顶部色条 + 半透明底 + 描边"""
    rect(slide, x, y, w, h, fill=fill or NAVY_C, alpha=alpha,
         line=border, line_w=1)
    if top_color:
        rect(slide, x, y, w, 4, fill=top_color)


def chips(slide, x, y, items, size=15, h=34, gap=10, max_w=None):
    """横向标签"""
    cx = x
    for txt, c, b in items:
        est = int(len(txt) * size * 1.05) + 28
        w = min(est, 340)
        rect(slide, cx, y, w, h, fill=None, line=b, line_w=1)
        ca = {"#E8B34B": GOLD, "#F5D488": GOLD_L, "#FF5A4E": RED_L,
              "#C7000B": RED, "#5B7DBB": BLUE, "#9FB4DA": GREY}.get(c, GOLD)
        bgdone = False
        # 浅色描边容器内部再叠一层淡底
        rect(slide, cx, y, w, h, fill=NAVY_P, alpha=45)
        if c in ("#FF5A4E", "#E8B34B"):
            rect(slide, cx, y, w, h, fill=(RED if c == "#FF5A4E" else GOLD), alpha=12)
        text(slide, cx, y + h / 2 - h / 2, w, h, txt, size=size, color=ca,
             align="center", anchor="middle", line_spacing=1.0)
        cx += w + gap
    return cx


def bullets(slide, x, y, items, size=16, color=WHITE, gap=13, w=None,
            dot=GOLD, made=None):
    cy = y
    for it in items:
        rect(slide, x, cy + 9, 7, 7, fill=dot)
        if isinstance(it, list):
            text(slide, x + 20, cy - 2, (w or 380) - 20, 60, it,
                 size=size, color=color, line_spacing=1.45)
            # 估算高度
            cy += gap + 26 * max(1, len("".join(i.get("t", "") for i in it)) // int((w or 380) / (size * 1.2)) + 1)
        else:
            text(slide, x + 20, cy - 2, (w or 380) - 20, 60, it,
                 size=size, color=color, line_spacing=1.45)
            cy += gap + 26 * max(1, len(it) // int((w or 380) / (size * 1.2)) + 1)
    return cy


# 复用 asta
made = locals().get("made", None)
