# -*- coding: utf-8 -*-
"""
工银科创桥 — 项目汇报 PPTX 生成器
深蓝 #0A1730 + 工行红 #C7000B + 金 #E8B34B，严格对齐官网 dark 主题。
输出：artifacts/presentation.pptx（可编辑）
"""
import os, math
from lxml import etree
from pptx import Presentation
from pptx.util import Pt
from pptx.dml.color import RGBColor
from pptx.oxml.ns import qn
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(ROOT, "frontend", "public", "assets", "images")
TMP = os.path.join(ROOT, "build")
OUT = os.path.join(ROOT, "artifacts")
os.makedirs(TMP, exist_ok=True)
os.makedirs(OUT, exist_ok=True)

NAVY_D, NAVY_C, NAVY_P = "0A1730", "0E2145", "143061"
RED, RED_L = "C7000B", "FF5A4E"
GOLD, GOLD_L = "E8B34B", "F5D488"
BLUE, GREY, WHITE = "5B7DBB", "9FB4DA", "E0E6F0"
FONT = "Microsoft YaHei"
SCALE = 2.0 / 3.0
FS = 1.18          # 字号增益：原始 px 设计值换算后偏小，投影不可读
MIN_PT = 10.0      # 最小字号下限


def P(v):
    return Pt(v * SCALE)


def fsz(px):
    """设计 px -> 实际磅值（含增益与下限）"""
    return max(px * SCALE * FS, MIN_PT)


def RGB(h):
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


# ---------------- 填充 ----------------
def solid_fill(shape, color, alpha=100):
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGB(color)
    if alpha < 100:
        sf = shape._element.spPr.find(qn("a:solidFill"))
        if sf is not None:
            clr = sf.find(qn("a:srgbClr"))
            if clr is not None:
                for c in clr.findall(qn("a:alpha")):
                    clr.remove(c)
                etree.SubElement(clr, qn("a:alpha"), val=str(int(alpha * 1000)))


def grad_fill(shape, c1, a1, c2, a2, ang=0):
    spPr = shape._element.spPr
    for ch in list(spPr):
        if ch.tag.split("}")[-1] in ("solidFill", "gradFill", "noFill", "pattFill"):
            spPr.remove(ch)
    g = etree.Element(qn("a:gradFill"), rotWithShape="0")
    gsl = etree.SubElement(g, qn("a:gsLst"))

    def gs(pos, col, al):
        e = etree.SubElement(gsl, qn("a:gs"), pos=str(pos))
        c = etree.SubElement(e, qn("a:srgbClr"), val=col)
        if al < 100:
            etree.SubElement(c, qn("a:alpha"), val=str(int(al * 1000)))

    gs(0, c1, a1)
    gs(100000, c2, a2)
    lin = etree.SubElement(g, qn("a:lin"))
    lin.set("ang", str(int(ang * 60000)))
    lin.set("scaled", "0")
    idx = None
    for i, ch in enumerate(spPr):
        if ch.tag.split("}")[-1] in ("prstGeom", "custGeom"):
            idx = i + 1
            break
    spPr.insert(idx if idx is not None else len(spPr), g)


def rect(slide, x, y, w, h, fill=None, alpha=100, grad=None,
         line=None, lw=1.2):
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, P(x), P(y), P(w), P(h))
    sh.shadow.inherit = False
    sh.line.fill.background()
    if grad:
        grad_fill(sh, grad[0], grad[1], grad[2], grad[3], grad[4] if len(grad) > 4 else 0)
    elif fill:
        solid_fill(sh, fill, alpha)
    else:
        sh.fill.background()
    if line:
        sh.line.fill.solid()
        sh.line.fill.fore_color.rgb = RGB(line)
        sh.line.width = Pt(lw)
    return sh


def bar(slide, x, y, w, h, c1=GOLD, c2=RED):
    return grad_fill(rect(slide, x, y, w, h), c2, 100, c1, 100, 0)


def text(slide, x, y, w, h, runs, size=17, color=WHITE, bold=False,
         align="left", anchor="top", ls=1.35, ls_px=None):
    tb = slide.shapes.add_textbox(P(x), P(y), P(w), P(h))
    tf = tb.text_frame
    tf.word_wrap = True
    for m in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
        setattr(tf, m, 0)
    tf.vertical_anchor = {"top": MSO_ANCHOR.TOP, "middle": MSO_ANCHOR.MIDDLE,
                          "bottom": MSO_ANCHOR.BOTTOM}[anchor]
    if isinstance(runs, str):
        runs = [{"t": runs}]
    al = {"left": PP_ALIGN.LEFT, "center": PP_ALIGN.CENTER, "right": PP_ALIGN.RIGHT}[align]
    p = tf.paragraphs[0]
    p.alignment = al
    p.line_spacing = ls
    if ls_px:
        p.line_spacing = ls_px / fsz(size)
    for it in runs:
        t = it.get("t", "")
        if "\n" in t:
            parts = t.split("\n")
            for i, part in enumerate(parts):
                if i > 0:
                    p = tf.add_paragraph()
                    p.alignment = al
                    p.line_spacing = ls
                    if ls_px:
                        p.line_spacing = ls_px / fsz(size)
                r = p.add_run()
                r.text = part
                r.font.name = FONT
                r.font.size = Pt(fsz(it.get("s", size)))
                r.font.bold = it.get("b", bold)
                r.font.color.rgb = RGB(it.get("c", color))
        else:
            r = p.add_run()
            r.text = t
            r.font.name = FONT
            r.font.size = Pt(fsz(it.get("s", size)))
            r.font.bold = it.get("b", bold)
            r.font.color.rgb = RGB(it.get("c", color))
    return tb


def pic(slide, path, x, y, w, h):
    return slide.shapes.add_picture(path, P(x), P(y), P(w), P(h))


# ---------------- 图片 ----------------
def prep_bg(name, w=1920):
    dst = os.path.join(TMP, name.replace(".png", "_169.png"))
    if os.path.exists(dst):
        return dst
    im = Image.open(os.path.join(IMG, name)).convert("RGB")
    th = int(w * 810 / 1440)
    sw, sh = im.size
    s = max(w / sw, th / sh)
    im = im.resize((int(sw * s), int(sh * s)), Image.LANCZOS)
    sw, sh = im.size
    im.crop(((sw - w) // 2, (sh - th) // 2,
             (sw - w) // 2 + w, (sh - th) // 2 + th)).save(dst)
    return dst


def make_glow(name, rgb, size=520, ma=95):
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
                px[x, y] = (rgb[0], rgb[1], rgb[2], int(ma * (1 - d) ** 2.4))
    img.save(dst)
    return dst


# ---------------- 页面构件 ----------------
def page(slide, bgfile, grad, glows=()):
    pic(slide, bgfile, 0, 0, 1440, 810)
    ov = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, P(1440), P(810))
    ov.shadow.inherit = False
    ov.line.fill.background()
    grad_fill(ov, grad[0], grad[1], grad[2], grad[3], grad[4] if len(grad) > 4 else 0)
    for g in glows:
        pic(slide, g[0], g[1], g[2], g[3], g[4])


def head(slide, kicker, title, sub=None, kw=1100):
    rect(slide, 60, 48, 4, 26, fill=GOLD)
    text(slide, 78, 46, 800, 26, kicker, size=15, color=GOLD, bold=True, ls=1.0)
    text(slide, 60, 80, kw, 50, title, size=37, color=GOLD_L, bold=True, ls=1.05)
    y = 140
    if sub:
        text(slide, 60, y + 2, kw, 28, sub, size=17, color=GREY, ls=1.1)
        y += 38
    rect(slide, 60, y, 110, 3, fill=GOLD)
    return y + 22


def card(slide, x, y, w, h, top=None, border=BLUE, alpha=68, fill=NAVY_C):
    rect(slide, x, y, w, h, fill=fill, alpha=alpha, line=border, lw=1.1)
    if top:
        rect(slide, x, y, w, 4, fill=top)


def chip(slide, x, y, w, h, txt, color=GOLD_L, border=GOLD, alpha=55, size=15):
    rect(slide, x, y, w, h, fill=NAVY_P, alpha=alpha, line=border, lw=1.0)
    text(slide, x, y, w, h, txt, size=size, color=color, align="center",
         anchor="middle", ls=1.0)


def dot(slide, x, y, c=GOLD):
    rect(slide, x, y, 7, 7, fill=c)


def note(slide, x, y, w, h, label, label_c, body, body_runs=None, accent=GOLD, ls=1.3):
    """左侧色条提示条"""
    rect(slide, x, y, w, h, fill=NAVY_C, alpha=62, line=BLUE, lw=1.0)
    rect(slide, x, y, 4, h, fill=accent)
    text(slide, x + 20, y + h / 2 - 12, 110, 24, label, size=15, color=label_c,
         bold=True, ls=1.0)
    if body_runs:
        text(slide, x + 122, y + 4, w - 140, h - 8, body_runs, size=17, color=WHITE,
             anchor="middle", ls=ls)
    else:
        text(slide, x + 122, y + 4, w - 140, h - 8, body, size=17, color=WHITE,
             anchor="middle", ls=ls)


# ============================================================
# 幻灯片
# ============================================================
def s1(sl, B, G):
    page(sl, B["cover"], (NAVY_D, 97, NAVY_P, 55, 25),
         [(G["gold"], 760, -170, 740, 740), (G["red"], -120, 560, 620, 620)])
    text(sl, 78, 44, 700, 26, "第十七届「工行杯」全国大学生金融科技创新大赛",
         size=16, color=GREY, ls=1.0)
    text(sl, 1040, 44, 340, 26, "科 技 金 融 方 向", size=14, color=GOLD,
         align="right", ls=1.0)
    text(sl, 60, 210, 700, 26, "HARD-TECH  FINANCING  PLATFORM",
         size=16, color=GREY, ls=1.0)
    text(sl, 60, 252, 900, 92, "工银科创桥", size=78, color=GOLD_L, bold=True, ls=1.0)
    bar(sl, 62, 366, 220, 5)
    text(sl, 60, 396, 900, 42, "硬科技企业里程碑式投贷联动平台",
         size=30, color=WHITE, ls=1.0)
    text(sl, 60, 452, 900, 34, "让研发的每一步，都成为可计量的信用",
         size=22, color=GOLD_L, ls=1.0)
    labels = ["AI 动态估值", "专利知识图谱", "里程碑触发", "投贷联动"]
    x = 60
    for lb in labels:
        w = len(lb) * 18 + 40
        chip(sl, x, 640, w, 40, lb, GREY, BLUE, 55, 16)
        x += w + 14
    text(sl, 1180, 634, 200, 44, [{"t": "8", "s": 42, "c": GOLD, "b": True},
                                  {"t": " min", "s": 21, "c": GOLD}],
         align="right", ls=1.0)
    text(sl, 1180, 682, 200, 24, "项目汇报 · 20 页", size=14, color=GREY,
         align="right", ls=1.0)


def s2(sl, B, G):
    page(sl, B["bridge"], (NAVY_D, 96, NAVY_P, 60, 40),
         [(G["gold"], -150, -200, 700, 700), (G["red"], 900, 560, 660, 660)])
    head(sl, "汇报导览", "先回答价值，再证明技术")
    # PART 01
    card(sl, 60, 214, 760, 380, top=GOLD)
    text(sl, 84, 240, 300, 50, "PART 01", size=46, color=GOLD_L, bold=True, ls=1.0)
    text(sl, 480, 250, 320, 30, "应用价值 · 13 页", size=16, color=GREY,
         align="right", ls=1.0)
    text(sl, 84, 300, 700, 34, "这条路子，解决什么问题、值多少钱",
         size=23, color=WHITE, ls=1.0)
    items = [("困境洞察", "三重金融困境 · 死亡谷 · 政策窗口"),
             ("破局方案", "四核能力 · 五阶里程碑 · 三方共赢"),
             ("落地验证", "产品演示 · 场景推演 · 成效测算")]
    yy = 352
    for i, (t, d) in enumerate(items):
        rect(sl, 84, yy + 6, 28, 28, fill=GOLD, alpha=None) if False else None
        rect(sl, 84, yy + 6, 28, 28, fill=None, line=GOLD, lw=1.2)
        text(sl, 84, yy + 6, 28, 28, str(i + 1), size=14, color=GOLD_L, bold=True,
             align="center", anchor="middle", ls=1.0)
        text(sl, 124, yy + 2, 400, 30, t, size=21, color=GOLD_L, bold=True, ls=1.0)
        text(sl, 124, yy + 34, 640, 26, d, size=16, color=GREY, ls=1.0)
        yy += 78
    # PART 02
    card(sl, 848, 214, 530, 380, top=RED)
    text(sl, 872, 240, 300, 50, "PART 02", size=46, color=GOLD_L, bold=True, ls=1.0)
    text(sl, 1160, 250, 194, 30, "技术价值 · 5 页", size=16, color=GREY,
         align="right", ls=1.0)
    text(sl, 872, 300, 460, 34, "凭什么是我们做得到", size=23, color=WHITE, ls=1.0)
    items2 = [("架构与 AI 引擎", "XGBoost 双模型 · PageRank 图算法"),
              ("工程实现", "优雅降级 · 实时联动 · 可追溯")]
    yy = 352
    for i, (t, d) in enumerate(items2):
        rect(sl, 872, yy + 6, 28, 28, fill=None, line=RED, lw=1.2)
        text(sl, 872, yy + 6, 28, 28, str(i + 4), size=14, color=RED_L, bold=True,
             align="center", anchor="middle", ls=1.0)
        text(sl, 912, yy + 2, 400, 30, t, size=21, color=GOLD_L, bold=True, ls=1.0)
        text(sl, 912, yy + 34, 430, 26, d, size=16, color=GREY, ls=1.0)
        yy += 100
    # 配比条
    text(sl, 60, 636, 120, 26, "篇幅配比", size=16, color=GREY, ls=1.0)
    rect(sl, 190, 640, 1080, 16, fill=None, line=BLUE, lw=1.0)
    rect(sl, 190, 640, 778, 16, fill=GOLD, alpha=90)
    rect(sl, 968, 640, 302, 16, fill=RED, alpha=90)
    text(sl, 1285, 630, 95, 34, "7 : 3", size=19, color=GOLD_L, bold=True,
         align="right", ls=1.0)


def s3(sl, B, G):
    page(sl, B["pain"], (NAVY_D, 97, NAVY_P, 70, 30),
         [(G["red"], 800, -180, 660, 660), (G["blue"], -160, 520, 680, 680)])
    head(sl, "PART 01 · 困境洞察", "银行惜贷、创投观望、保险缺位的三重困境")
    note(sl, 60, 196, 1320, 62, "核心论点", RED_L,
         None, [{"t": "硬科技企业不是缺资金，而是缺一套「把技术翻译成信用」的语言",
                 "s": 20, "c": WHITE}])
    cols = [("银行不敢贷", "50.2%", "科技型中小企业获贷率 · 2025Q4",
             "近半数科技型中小企业被挡在银行体系之外；高新技术企业获贷率也仅 57.3%。核心资产是专利与人，缺少合格抵押物。", RED_L, RED),
            ("创投不敢投", "4%", "长期资本占比 · 美国为 70%~80%",
             "计入政府引导基金也仅 10%~20%；国内创投基金普遍「5+2」周期，短于成熟市场的「10+2」，早期项目更难被托住。", GOLD_L, GOLD),
            ("保险不敢保", "评估难 · 风控难 · 处置难", "知识产权融资的三道闸门",
             "不同机构估值差异大；违约后面临找买家难、定价难、过户难，导致研发失败风险难以被合理定价。", GREY, BLUE)]
    x = 60
    for title, big, sub, desc, tc, top in cols:
        card(sl, x, 282, 420, 330, top=top)
        text(sl, x + 24, 304, 370, 26, title, size=16, color=GREY, ls=1.0)
        if big == "评估难 · 风控难 · 处置难":
            text(sl, x + 24, 340, 372, 40, big, size=25, color=GOLD_L, bold=True, ls=1.0)
        else:
            text(sl, x + 24, 338, 372, 52,
                 [{"t": big[:-1] if big.endswith("%") else big, "s": 44, "c": GOLD_L, "b": True},
                  {"t": "%", "s": 22, "c": GOLD_L}], ls=1.0)
        text(sl, x + 24, 400, 372, 24, sub, size=14, color=GREY, ls=1.0)
        text(sl, x + 24, 436, 372, 160, desc, size=16, color=WHITE, ls=1.5)
        x += 450
    note(sl, 60, 634, 940, 66, "关键洞察", GOLD, None,
         [{"t": "问题不在「不愿贷」，而在「不会评」——缺的是可解释、可追溯、可审计的非财务评价体系",
           "s": 18, "c": WHITE}])
    rect(sl, 1016, 634, 364, 66, fill=NAVY_C, alpha=62, line=BLUE, lw=1.0)
    text(sl, 1036, 644, 330, 22, "金融机构能力短板", size=14, color=GREY, ls=1.0)
    text(sl, 1036, 668, 330, 28, "看不懂 · 不会评 · 不敢贷", size=19, color=RED_L,
         bold=True, ls=1.0)


def s4(sl, B, G):
    page(sl, B["lab"], (NAVY_D, 97, NAVY_P, 52, 20),
         [(G["gold"], 820, 480, 640, 640)])
    head(sl, "PART 01 · 困境洞察", "错位的时间与资金：跨不过的死亡谷")
    ms = [("1", "期限错位", "硬科技从研发到量产普遍需 5~10 年，创新药更有「双十定律」——10 亿美元、10 年；而银行信贷以短期为主，风投多聚焦接近 IPO 的后期项目。", "半导体研发投入强度", "22%", RED_L, RED),
          ("2", "资产错位", "核心资产是专利与人才团队等无形资产，价值评估难、波动性强、流转变现难，与银行「重抵押」的准入标准形成结构性冲突。", "传统贷款的判定依据", "土地 · 厂房 · 设备", GOLD_L, GOLD),
          ("3", "风险错位", "科技创新天然伴随高失败率，与银行追求安全性、流动性的逻辑直接冲突；基层信贷人员的终身追责机制进一步限制了早期投放意愿。", "耐心资本考核约束", "短期财务绩效", GREY, BLUE)]
    x = 60
    for n, t, d, lp, lv, nc, top in ms:
        card(sl, x, 226, 420, 336, top=top)
        rect(sl, x + 22, 250, 28, 28, fill=None, line=top, lw=1.2)
        text(sl, x + 22, 250, 28, 28, n, size=14, color=nc, bold=True,
             align="center", anchor="middle", ls=1.0)
        text(sl, x + 60, 248, 320, 32, t, size=23, color=GOLD_L, bold=True, ls=1.0)
        text(sl, x + 22, 294, 376, 160, d, size=16, color=WHITE, ls=1.6)
        rect(sl, x + 22, 476, 376, 1, fill=BLUE, alpha=45)
        text(sl, x + 22, 490, 250, 24, lp, size=14, color=GREY, ls=1.0)
        text(sl, x + 22, 490, 376, 24, lv, size=20, color=GOLD_L, bold=True,
             align="right", ls=1.0)
        x += 450
    rect(sl, 60, 584, 300, 116, fill=RED, alpha=14, line=RED, lw=1.1)
    text(sl, 82, 598, 260, 22, "资金缺口导致的代价", size=15, color=GREY, ls=1.0)
    text(sl, 82, 622, 260, 52, [{"t": "75", "s": 54, "c": RED_L, "b": True},
                                {"t": "%+", "s": 26, "c": RED_L}], ls=1.0)
    text(sl, 82, 678, 260, 20, "新材料、高端装备等硬科技赛道夭折率", size=13,
         color=GREY, ls=1.0)
    card(sl, 380, 584, 1000, 116)
    text(sl, 404, 598, 700, 22, "一线调研 · 公开报道情境", size=15, color=GOLD, ls=1.0)
    text(sl, 404, 624, 950, 60,
         [{"t": "某国家级专精特新「小巨人」企业测算：上游需全款预付，设备生产 1~2 个月，下游账期 2~3 个月，再加 6 个月票据期限——", "s": 17, "c": WHITE},
          {"t": "资金需约一年才能周转一圈", "s": 17, "c": GOLD_L},
          {"t": "。扩产期正是现金流最容易断裂的时刻。", "s": 17, "c": WHITE}], ls=1.45)


def s5(sl, B, G):
    page(sl, B["policy"], (NAVY_D, 96, NAVY_P, 68, 50),
         [(G["gold"], -180, -200, 740, 740), (G["red"], 880, 580, 680, 680)])
    head(sl, "PART 01 · 时代窗口", "政策破壁、市场扩容，窗口期已经打开")
    ps = [("顶层设计密集落地", "2025", RED_L, RED,
           "3 月《银行业保险业科技金融高质量发展实施方案》；5 月《加快构建科技金融体制…若干政策举措》围绕创投、信贷、资本市场等 7 方面提出 15 项举措。"),
          ("制度试点系统性破壁", "8 省市", GOLD_L, GOLD,
           "知识产权金融生态综合试点围绕登记、评估、处置、补偿四大环节破壁；已有 13 个省份、124 个地市出台知识产权质押融资风险补偿政策。"),
          ("市场规模快速扩容", "同比 +56%", GREY, BLUE,
           "2025 年银行业累计发放知识产权质押贷款 2979 亿元、2.87 万户，较 2023 年分别增长 56% 和 33%；科技型中小企业贷款余额 3.63 万亿元（+19.8%）。"),
          ("行方业务基础扎实", "6 万亿元", GOLD_L, GOLD_L,
           "工商银行科技贷款余额 6 万亿元、科技型企业贷款 2.7 万亿元；已推出「五专」服务体系与研发贷、积分贷、知识产权融资等专属产品。")]
    pos = [(60, 226), (750, 226), (60, 420), (750, 420)]
    for (t, tag, tc, top, d), (x, y) in zip(ps, pos):
        card(sl, x, y, 630, 178, top=top)
        text(sl, x + 22, y + 20, 460, 30, t, size=21, color=GOLD_L, bold=True, ls=1.0)
        tw = len(tag) * 17 + 30
        chip(sl, x + 630 - 22 - tw, y + 20, tw, 30, tag, tc, top, 55, 14)
        text(sl, x + 22, y + 62, 586, 100, d, size=16, color=WHITE, ls=1.5)
    note(sl, 60, 632, 1320, 70, "政策指向", GOLD, None,
         [{"t": "监管明确倡导「运用", "s": 18, "c": WHITE},
          {"t": "内部模型", "s": 18, "c": GOLD_L, "b": True},
          {"t": "确定知识产权价值」「基于企业画像智能匹配产品服务」——本平台正是对这一导向的技术回应", "s": 18, "c": WHITE}], ls=1.35)


def s6(sl, B, G):
    page(sl, B["bridge"], (NAVY_D, 97, NAVY_P, 66, 25),
         [(G["gold"], 820, -180, 700, 700), (G["red"], -160, 540, 660, 660)])
    head(sl, "PART 01 · 破局方案", "让研发的每一步，都成为可计量的信用")
    card(sl, 60, 210, 1320, 96, top=GOLD)
    text(sl, 84, 226, 400, 22, "核 心 答 案", size=14, color=GREY, ls=1.0)
    text(sl, 84, 254, 1270, 40,
         [{"t": "以 ", "s": 25, "c": WHITE},
          {"t": "AI 评估引擎", "s": 25, "c": GOLD_L, "b": True},
          {"t": " 为非财务资产定价，以 ", "s": 25, "c": WHITE},
          {"t": "研发里程碑", "s": 25, "c": GOLD_L, "b": True},
          {"t": " 为触发器动态匹配金融工具包", "s": 25, "c": WHITE}], ls=1.0)
    caps = [("CAPABILITY 01", "AI 评估引擎",
             "专利引用网络 PageRank + 研发团队画像 + XGBoost 双模型，输出动态估值与风险评分，替代「拍脑袋」式评估。", GOLD),
            ("CAPABILITY 02", "里程碑触发",
             "5 个研发阶段各绑定一套金融工具包与授信比例；研发过一关，额度上一阶，无需重新走一遍完整审批流程。", RED),
            ("CAPABILITY 03", "投贷联动工作台",
             "银行授信与创投跟投在同一视图协同，「见投即贷、先投后贷」有了可复核的量化依据，不再依赖人情与经验。", RED_L),
            ("CAPABILITY 04", "风控看板",
             "风险评分与里程碑进度双线跟踪；里程碑延迟、进度偏低自动预警，把风险识别从事后处置提前到事前提示。", BLUE)]
    x = 60
    for k, t, d, top in caps:
        card(sl, x, 326, 315, 250, top=top)
        text(sl, x + 20, 346, 275, 22, k, size=13, color=GREY, ls=1.0)
        text(sl, x + 20, 372, 275, 32, t, size=22, color=GOLD_L, bold=True, ls=1.0)
        text(sl, x + 20, 414, 275, 150, d, size=16, color=WHITE, ls=1.55)
        x += 333
    rect(sl, 380, 620, 300, 56, fill=None, line=BLUE, lw=1.2)
    text(sl, 380, 620, 300, 56, "传统「静态审批」", size=21, color=GREY,
         align="center", anchor="middle", ls=1.0)
    text(sl, 700, 632, 60, 34, "➜", size=27, color=GOLD, align="center",
         anchor="middle", ls=1.0)
    rect(sl, 770, 620, 420, 56, fill=GOLD, alpha=100)
    text(sl, 770, 620, 420, 56, "里程碑驱动的「动态授信」", size=21, color="FFFFFF",
         bold=True, align="center", anchor="middle", ls=1.0)


def s7(sl, B, G):
    page(sl, B["policy"], (NAVY_D, 97, NAVY_P, 70, 35),
         [(G["gold"], -170, -190, 720, 720), (G["red"], 880, 560, 680, 680)])
    head(sl, "PART 01 · 核心机制", "五阶里程碑，自动触发五套金融工具包",
         "每一个研发里程碑，都是一次「信用释放事件」")
    steps = [("1", "立项 / 预研完成", "知识产权质押贷\n+ 研发补贴", "15", 30, BLUE, GREY),
             ("2", "原型验证通过", "AI 动态估值授信\n+ 股权跟投", "25", 50, GOLD, GOLD_L),
             ("3", "流片 / 临床 II 期", "投贷联动\n银行授信 + VC 跟投", "40", 80, RED, RED_L),
             ("4", "商业化量产", "供应链票据\n+ 订单融资", "30", 60, GREY, GREY),
             ("5", "上市预备", "可转债\n+ 科创专项债券", "50", 100, GOLD_L, GOLD_L)]
    x = 60
    for n, t, tl, pct, w, bc, tc in steps:
        hl = (n == "3")
        card(sl, x, 232, 240, 320, top=bc, alpha=(78 if hl else 68),
             fill=(NAVY_P if hl else NAVY_C))
        rect(sl, x + 16, 254, 24, 24, fill=None, line=bc, lw=1.2)
        text(sl, x + 16, 254, 24, 24, n, size=13, color=tc, bold=True,
             align="center", anchor="middle", ls=1.0)
        text(sl, x + 48, 250, 180, 30, t, size=17, color=GOLD_L, bold=True, ls=1.0)
        text(sl, x + 16, 296, 208, 70, tl, size=15, color=WHITE, ls=1.45)
        text(sl, x + 16, 424, 208, 22, "授信比例", size=14, color=GREY, ls=1.0)
        text(sl, x + 16, 448, 208, 44,
             [{"t": pct, "s": 34, "c": GOLD_L, "b": True}, {"t": "%", "s": 17, "c": GOLD_L}], ls=1.0)
        rect(sl, x + 16, 508, 208, 6, fill=BLUE, alpha=25)
        rect(sl, x + 16, 508, int(208 * w / 100), 6, fill=bc, alpha=100)
        x += 258
    note(sl, 60, 596, 940, 74, "授信公式", GOLD, None,
         [{"t": "最终授信 ＝ AI 估值 × 30% × ", "s": 20, "c": WHITE},
          {"t": "里程碑进度系数", "s": 20, "c": GOLD_L, "b": True},
          {"t": " ×（1 − ", "s": 20, "c": WHITE},
          {"t": "风险评分", "s": 20, "c": RED_L, "b": True},
          {"t": " × 0.5）", "s": 20, "c": WHITE}], ls=1.3)
    rect(sl, 1016, 596, 364, 74, fill=NAVY_C, alpha=62, line=BLUE, lw=1.0)
    text(sl, 1036, 610, 330, 22, "成功度量", size=14, color=GREY, ls=1.0)
    text(sl, 1036, 634, 330, 30, "5 阶段全覆盖 · 拖动进度实时重算",
         size=18, color=GOLD_L, bold=True, ls=1.0)


def s8(sl, B, G):
    page(sl, B["banker"], (NAVY_D, 97, NAVY_P, 52, 20),
         [(G["gold"], -170, -190, 700, 700)])
    head(sl, "PART 01 · 价值主张", "银行敢贷、企业好融、资本可投")
    roles = [("商业银行", "敢贷 · 会贷", RED_L, RED, "从「看抵押物」到「看创新力」",
              [("获得", "可解释", "的非财务评价体系，破解「看不懂、不会评」"),
               ("授信额度随研发进度", "动态调整", "，不必反复重走审批"),
               ("风险在", "前置指标", "上被识别，而非事后追偿")]),
             ("硬科技企业", "好融 · 稳融", GOLD_L, GOLD, "融资节奏与研发节奏对齐",
              [("最缺钱的中试 / 流片 / 临床阶段，", "恰好有对应工具包触发", ""),
               ("过一关释放一档额度，形成", "确定性预期", "，便于排产"),
               ("无需在最困难时", "贱卖股权", "，稀释节奏可控")]),
             ("创投 / AIC", "敢投 · 可核", GREY, BLUE, "从「各自判断」到「同一套数据」",
              [("获得第三方可复核的", "动态估值时间序列", ""),
               ("为「见投即贷」「先投后贷」提供", "量化前提", ""),
               ("尽调结果可直接转化为", "授信参数", "，减少重复劳动")])]
    x = 60
    for nm, tag, tc, top, turn, bl in roles:
        card(sl, x, 226, 420, 372, top=top)
        text(sl, x + 24, 248, 280, 34, nm, size=25, color=GOLD_L, bold=True, ls=1.0)
        tw = len(tag) * 15 + 26
        chip(sl, x + 444 - 24 - tw, 252, tw, 28, tag, tc, top, 55, 14)
        rect(sl, x + 24, 300, 372, 1, fill=BLUE, alpha=45)
        text(sl, x + 24, 312, 372, 22, "核心转变", size=14, color=GREY, ls=1.0)
        text(sl, x + 24, 336, 372, 30, turn, size=20, color=WHITE, ls=1.0)
        yy = 384
        for a, b, c in bl:
            dot(sl, x + 24, yy + 8, top)
            text(sl, x + 44, yy - 2, 352, 60,
                 [{"t": a, "s": 16, "c": WHITE},
                  {"t": b, "s": 16, "c": GOLD_L, "b": True},
                  {"t": c, "s": 16, "c": WHITE}], ls=1.45)
            yy += 62
        x += 450
    note(sl, 60, 634, 1320, 70, "延伸覆盖", BLUE, None,
         [{"t": "保险机构：破产概率输出可作为「中试保融通」类产品定价参考　│　政府性担保：为风险补偿资金池按比例分担提供量化依据",
           "s": 18, "c": WHITE}], ls=1.3)


def s9(sl, B, G):
    page(sl, B["circuit"], (NAVY_D, 97, NAVY_P, 70, 45),
         [(G["blue"], 840, -180, 680, 680), (G["gold"], -170, 560, 680, 680)])
    head(sl, "PART 01 · 业务流程", "从数据接入到额度释放：端到端闭环",
         "把分散的技术信号，压缩成一次可执行的授信决策")
    steps = [("1", "数据接入", "企业基础信息、专利数据与引用关系、团队成员学术产出，以及 95 维财务特征一次性归集。", "输入：工商 + 知识产权 + 人才 + 财务", BLUE, GREY),
             ("2", "AI 评估", "XGBoost 估值模型输出动态估值，破产风险模型输出破产概率，PageRank 计算专利影响力。", "产出：估值区间 + 风险评分 + 专利质量分", GOLD, GOLD_L),
             ("3", "工具匹配", "按当前研发里程碑匹配金融工具包；拖动进度即可实时重算授信额度，所见即所得。", "产出：工具包清单 + 可执行额度", RED, RED_L),
             ("4", "动态风控", "风险评分与里程碑进度双线跟踪；延迟或进度偏低自动预警，并联动调整授信额度。", "产出：预警事件 + 额度动态调整", GOLD_L, GOLD_L)]
    x = 60
    for i, (n, t, d, out, bc, tc) in enumerate(steps):
        card(sl, x, 246, 288, 292, top=bc)
        rect(sl, x + 22, 270, 36, 36, fill=None, line=bc, lw=1.2)
        text(sl, x + 22, 270, 36, 36, n, size=18, color=tc, bold=True,
             align="center", anchor="middle", ls=1.0)
        text(sl, x + 68, 274, 200, 30, t, size=22, color=GOLD_L, bold=True, ls=1.0)
        text(sl, x + 22, 322, 244, 150, d, size=16, color=WHITE, ls=1.55)
        rect(sl, x + 22, 476, 244, 1, fill=BLUE, alpha=45)
        text(sl, x + 22, 488, 244, 40, out, size=13, color=GREY, ls=1.35)
        if i < 3:
            text(sl, x + 296, 340, 30, 40, "➜", size=24, color=bc,
                 align="center", anchor="middle", ls=1.0)
        x += 330
    stats = [("13", "个 REST 端点，全链路贯通"),
             ("95", "维财务特征用于风险建模"),
             ("5", "个里程碑阶段各绑定工具包")]
    x = 60
    for v, lb in stats:
        rect(sl, x, 566, 268, 62, fill=NAVY_C, alpha=58, line=BLUE, lw=1.0)
        text(sl, x + 20, 580, 60, 36, v, size=27, color=GOLD_L, bold=True, ls=1.0)
        text(sl, x + 88, 580, 176, 40, lb, size=14, color=GREY, ls=1.25)
        x += 288
    note(sl, 924, 566, 456, 62, "服务连续性", RED, None,
         [{"t": "模型异常时自动回退规则公式，", "s": 16, "c": WHITE},
          {"t": "服务不中断", "s": 16, "c": GOLD_L, "b": True}], ls=1.3)


def s10(sl, B, G):
    page(sl, B["lab"], (NAVY_D, 97, NAVY_P, 52, 22),
         [(G["gold"], 860, -180, 660, 660), (G["red"], -160, 540, 660, 660)])
    head(sl, "PART 01 · 落地验证", "从实验室到量产：三类企业的融资推演")
    cases = [("半导体芯片", "流片是关键节点", BLUE, GREY,
              "流片成本高、周期长，缺少合格抵押物",
              "原型验证阶段按 25% 释放额度；流片成功后触发投贷联动，比例升至 40%，银行授信与产业资本同步进入",
              "参照：某 UWB 芯片企业以全量知识产权数据构建量化模型"),
             ("生物医药", "临床 II 期", GOLD_L, GOLD,
              "临床周期长、成败二元，财务报表不好看",
              "临床 II 期达标触发投贷联动；破产概率模型同步为「中试保融通」类保险提供定价参考",
              "参照：某国家级中试平台获超 1 亿元中长期授信"),
             ("高端装备 / 新材料", "量产爬坡", RED_L, RED,
              "中试资金密集，订单释放明显滞后",
              "量产阶段切换至供应链票据 + 订单融资（30%），以真实订单替代抵押物",
              "参照：某锂电材料企业经技术流评价获 6000 万元综合授信")]
    x = 60
    for nm, tag, tc, top, ch, pl, ref in cases:
        card(sl, x, 226, 420, 356, top=top)
        text(sl, x + 22, 246, 260, 32, nm, size=22, color=GOLD_L, bold=True, ls=1.0)
        tw = len(tag) * 15 + 26
        chip(sl, x + 444 - 22 - tw, 250, tw, 28, tag, tc, top, 55, 13)
        rect(sl, x + 22, 292, 376, 66, fill=RED, alpha=12)
        rect(sl, x + 22, 292, 3, 66, fill=RED)
        text(sl, x + 38, 300, 340, 20, "挑 战", size=13, color=GREY, ls=1.0)
        text(sl, x + 38, 322, 352, 34, ch, size=15, color=WHITE, ls=1.3)
        rect(sl, x + 22, 368, 376, 106, fill=GOLD, alpha=10)
        rect(sl, x + 22, 368, 3, 106, fill=GOLD)
        text(sl, x + 38, 376, 340, 20, "推 演", size=13, color=GREY, ls=1.0)
        text(sl, x + 38, 398, 348, 70, pl, size=15, color=WHITE, ls=1.45)
        rect(sl, x + 22, 490, 376, 1, fill=BLUE, alpha=45)
        text(sl, x + 22, 502, 376, 60, ref, size=13, color=GREY, ls=1.35)
        x += 450
    note(sl, 60, 622, 1320, 78, "合规说明", RED_L, None,
         [{"t": "以上为基于公开报道情境的适用性推演，用于验证方案在不同硬科技赛道的适配能力，", "s": 17, "c": WHITE},
          {"t": "并非本平台实际客户数据", "s": 17, "c": GOLD_L, "b": True}], ls=1.35)


def s11(sl, B, G):
    page(sl, B["banker"], (NAVY_D, 97, NAVY_P, 50, 20),
         [(G["gold"], -180, -200, 720, 720)])
    rect(sl, 60, 48, 4, 26, fill=GOLD)
    text(sl, 78, 46, 400, 26, "PART 01 · 产品演示 01", size=15, color=GOLD,
         bold=True, ls=1.0)
    text(sl, 60, 82, 400, 100, "企业画像\n非财务资产如何被定价", size=29,
         color=GOLD_L, bold=True, ls=1.18)
    bar(sl, 62, 196, 130, 4)
    text(sl, 60, 226, 360, 90, "系统把一家没有厂房、没有利润的硬科技企业，翻译成六个可直接比较的量化指标。",
         size=17, color=WHITE, ls=1.5)
    rect(sl, 60, 340, 360, 116, fill=GOLD, alpha=10, line=GOLD, lw=1.0)
    rect(sl, 60, 340, 4, 116, fill=GOLD)
    text(sl, 80, 354, 320, 20, "演 示 重 点", size=14, color=GREY, ls=1.0)
    text(sl, 80, 378, 320, 70,
         [{"t": "切换企业时估值与风险评分实时联动；标注估值来源，结果", "s": 15, "c": WHITE},
          {"t": "可追溯", "s": 15, "c": GOLD_L, "b": True}], ls=1.45)
    dot(sl, 60, 490, GOLD)
    text(sl, 80, 482, 340, 26, "三个核心模块协同输出", size=15, color=GREY, ls=1.0)
    # 界面
    px0, py0, pw = 470, 56, 910
    rect(sl, px0, py0, pw, 40, fill=NAVY_D, alpha=88, line=BLUE, lw=1.0)
    for i, c in enumerate([RED_L, GOLD, BLUE]):
        rect(sl, px0 + 18 + i * 20, py0 + 14, 11, 11, fill=c)
    text(sl, px0 + 76, py0 + 8, 460, 24, "工银科创桥 · 企业画像", size=14,
         color=GREY, ls=1.0)
    chip(sl, px0 + pw - 176, py0 + 7, 158, 26, "估值来源：ML 模型", GOLD_L, GOLD, 40, 13)
    rect(sl, px0, py0 + 40, pw, 660, fill=NAVY_C, alpha=74, line=BLUE, lw=1.1)
    # 基础信息
    rect(sl, px0 + 20, py0 + 60, 300, 180, fill=NAVY_P, alpha=55, line=BLUE, lw=0.9)
    text(sl, px0 + 38, py0 + 76, 260, 22, "基础信息", size=15, color=GREY, ls=1.0)
    rows = [("所属行业", "半导体"), ("研发阶段", "原型验证"),
            ("员工人数", "86 人"), ("研发占比", "42%")]
    ry = py0 + 106
    for a, b in rows:
        text(sl, px0 + 38, ry, 150, 24, a, size=14, color=GREY, ls=1.0)
        text(sl, px0 + 150, ry, 150, 24, b, size=14, color=(WHITE if a == "所属行业" or a == "研发阶段" else GOLD_L),
             align="right", ls=1.0)
        ry += 32
    # AI 估值
    rect(sl, px0 + 336, py0 + 60, 554, 180, fill=NAVY_P, alpha=55, line=BLUE, lw=0.9)
    text(sl, px0 + 354, py0 + 76, 300, 22, "AI 估值结果", size=15, color=GREY, ls=1.0)
    text(sl, px0 + 600, py0 + 76, 272, 22, "6 项指标同步输出", size=13, color=GREY,
         align="right", ls=1.0)
    stats = [("8,600", "万", "当前估值", BLUE), ("7,200", "万", "基础估值", BLUE),
             ("18.4%", "", "风险评分", RED), ("37", "", "专利数量", BLUE),
             ("0.82", "", "平均专利质量", BLUE), ("88", "", "团队评分", BLUE)]
    for i, (v, u, lb, bc) in enumerate(stats):
        cx = px0 + 354 + (i % 3) * 178
        cy = py0 + 106 + (i // 3) * 70
        rect(sl, cx, cy, 164, 60, fill=NAVY_D, alpha=55, line=bc, lw=0.9)
        text(sl, cx, cy + 10, 164, 28,
             [{"t": v, "s": 20, "c": (RED_L if bc == RED else GOLD_L), "b": True},
              {"t": u, "s": 12, "c": (RED_L if bc == RED else GOLD_L)}],
             align="center", ls=1.0)
        text(sl, cx, cy + 38, 164, 18, lb, size=12, color=GREY, align="center", ls=1.0)
    # 团队画像
    rect(sl, px0 + 20, py0 + 256, 870, 414, fill=NAVY_P, alpha=55, line=BLUE, lw=0.9)
    text(sl, px0 + 38, py0 + 274, 400, 22, "研发团队画像", size=15, color=GREY, ls=1.0)
    text(sl, px0 + 400, py0 + 274, 470, 22,
         "加权：论文 20% · 引用 20% · H 指数 15% · 专利 25% · 经验 20%",
         size=13, color=GREY, align="right", ls=1.0)
    wts = [("学术论文", 62, BLUE, "20%"), ("引用总量", 70, BLUE, "20%"),
           ("H 指数", 46, GOLD, "15%"), ("专利产出", 88, RED, "25%"),
           ("从业经验", 70, BLUE, "20%")]
    wy = py0 + 316
    for lb, w, c, pv in wts:
        text(sl, px0 + 38, wy, 90, 24, lb, size=14, color=GREY, ls=1.0)
        rect(sl, px0 + 138, wy + 8, 640, 11, fill=BLUE, alpha=22)
        rect(sl, px0 + 138, wy + 8, int(640 * w / 100), 11, fill=c, alpha=100)
        text(sl, px0 + 790, wy, 80, 24, pv, size=14, color=GOLD_L, align="right", ls=1.0)
        wy += 56


def s12(sl, B, G):
    page(sl, B["network"], (NAVY_D, 97, NAVY_P, 70, 40),
         [(G["gold"], -170, -190, 700, 700), (G["red"], 880, 560, 660, 660)])
    head(sl, "PART 01 · 产品演示 02", "专利引用网络：让单件专利的影响力被看见", kw=1000)
    text(sl, 1130, 60, 250, 60, "节点大小 ＝ PageRank 值\n颜色 ＝ 质量等级",
         size=14, color=GREY, align="right", ls=1.4)
    # 左：网络图
    card(sl, 60, 226, 620, 372)
    text(sl, 82, 246, 380, 26, "力导向引用网络", size=17, color=GOLD_L, bold=True, ls=1.0)
    text(sl, 470, 250, 190, 22, "可拖拽漫游", size=13, color=GREY, align="right", ls=1.0)
    import svg_network
    png = svg_network.draw_network(os.path.join(TMP, "net.png"))
    sl.shapes.add_picture(png, P(90), P(286), P(560), P(292))
    # 右：趋势图
    card(sl, 700, 226, 680, 372)
    text(sl, 722, 246, 380, 26, "引用趋势 · 质量评分", size=17, color=GOLD_L,
         bold=True, ls=1.0)
    text(sl, 1150, 250, 210, 22, "双 Y 轴", size=13, color=GREY, align="right", ls=1.0)
    png2 = svg_network.draw_trend(os.path.join(TMP, "trend.png"))
    sl.shapes.add_picture(png2, P(728), P(288), P(624), P(292))
    note(sl, 60, 622, 700, 74, "专利质量模型", GOLD, None,
         [{"t": "引用 30% ＋ PageRank 25% ＋ 同族 20% ＋ 国际布局 15% ＋ 诉讼 10%",
           "s": 17, "c": WHITE}], ls=1.3)
    rect(sl, 780, 622, 600, 74, fill=NAVY_C, alpha=62, line=BLUE, lw=1.0)
    text(sl, 800, 636, 560, 22, "团队画像联动", size=14, color=GREY, ls=1.0)
    text(sl, 800, 660, 560, 28, "论文总数 · 专利总数 · 总引用数 · 平均 H 指数",
         size=17, color=WHITE, ls=1.0)


def s13(sl, B, G):
    page(sl, B["bridge"], (NAVY_D, 97, NAVY_P, 66, 30),
         [(G["gold"], 860, -180, 700, 700), (G["red"], -160, 540, 660, 660)])
    head(sl, "PART 01 · 产品演示 03", "拖动一根滑块，看见授信额度如何生长")
    # 里程碑看板
    card(sl, 60, 226, 800, 372)
    text(sl, 82, 246, 380, 26, "里程碑看板", size=17, color=GOLD_L, bold=True, ls=1.0)
    text(sl, 620, 250, 220, 22, "状态随进度自动流转", size=13, color=GREY,
         align="right", ls=1.0)
    ms = [("1", "立项 / 预研", 100, BLUE, GREY, "已完成", GREY),
          ("2", "原型验证", 100, BLUE, GREY, "已完成", GREY),
          ("3", "流片 / 临床 II", 75, GOLD, GOLD_L, "75%", GOLD),
          ("4", "商业化量产", 0, BLUE, GREY, "待启动", GREY),
          ("5", "上市预备", 0, BLUE, GREY, "待启动", GREY)]
    my = 290
    for n, t, pct, bc, tc, st, sc in ms:
        rect(sl, 82, my + 5, 20, 20, fill=None, line=bc, lw=1.1)
        text(sl, 82, my + 5, 20, 20, n, size=12, color=tc, bold=True,
             align="center", anchor="middle", ls=1.0)
        text(sl, 112, my, 130, 24, t, size=15,
             color=(GOLD_L if pct and pct < 100 else (GREY if pct == 0 else WHITE)), ls=1.0)
        rect(sl, 250, my + 8, 380, 9, fill=BLUE, alpha=22)
        if pct:
            rect(sl, 250, my + 8, int(380 * pct / 100), 9, fill=bc, alpha=100)
        text(sl, 650, my, 190, 24, st, size=14, color=sc, align="right", ls=1.0)
        my += 46
    rect(sl, 82, 528, 756, 1, fill=BLUE, alpha=45)
    text(sl, 82, 540, 500, 22, "当前里程碑触发的工具包", size=14, color=GREY, ls=1.0)
    xx = 82
    for lb, c, b in [("投贷联动", RED_L, RED), ("银行授信 + VC 跟投", GOLD_L, GOLD),
                     ("授信比例 40%", GREY, BLUE)]:
        w = len(lb) * 16 + 30
        chip(sl, xx, 566, w, 34, lb, c, b, 55, 14)
        xx += w + 12
    # 授信模拟器
    card(sl, 880, 226, 500, 372, top=RED)
    text(sl, 902, 246, 300, 26, "授信模拟器", size=17, color=GOLD_L, bold=True, ls=1.0)
    text(sl, 1250, 250, 110, 22, "实时计算", size=13, color=GREY, align="right", ls=1.0)
    text(sl, 902, 288, 300, 22, "里程碑进度", size=15, color=GREY, ls=1.0)
    rect(sl, 902, 318, 458, 9, fill=BLUE, alpha=22)
    rect(sl, 902, 318, int(458 * 0.75), 9, fill=GOLD, alpha=100)
    rect(sl, 902 + int(458 * 0.75) - 10, 311, 20, 20, fill=NAVY_D, alpha=100)
    rect(sl, 902 + int(458 * 0.75) - 10, 311, 20, 20, fill=None, line=GOLD, lw=2.5)
    text(sl, 1200, 292, 160, 24, "75%", size=16, color=GOLD_L, align="right", ls=1.0)
    rows = [("基础额度（AI 估值 × 30%）", "2,580 万", BLUE),
            ("× 进度系数", "0.75", BLUE),
            ("× 风险系数（1 − 18.4% × 0.5）", "0.908", RED)]
    ry = 348
    for a, b, bc in rows:
        rect(sl, 902, ry, 458, 40, fill=NAVY_P, alpha=52, line=bc, lw=0.9)
        text(sl, 918, ry + 9, 300, 24, a, size=14, color=GREY, ls=1.0)
        text(sl, 1200, ry + 7, 146, 26, b, size=16,
             color=(RED_L if bc == RED else GOLD_L), align="right", ls=1.0)
        ry += 50
    rect(sl, 902, 508, 458, 76, fill=GOLD, alpha=20, line=GOLD, lw=1.2)
    text(sl, 902, 520, 458, 22, "最终授信额度", size=14, color=GREY,
         align="center", ls=1.0)
    text(sl, 902, 544, 458, 44,
         [{"t": "1,758", "s": 40, "c": GOLD_L, "b": True}, {"t": " 万元", "s": 19, "c": GOLD_L}],
         align="center", ls=1.0)
    note(sl, 60, 624, 1320, 74, "风控联动", RED_L, None,
         [{"t": "风险评分与里程碑进度双线趋势图实时跟踪；「里程碑延迟」「进度偏低」两类预警自动触发，并回写额度调整建议",
           "s": 17, "c": WHITE}], ls=1.3)


def s14(sl, B, G):
    page(sl, B["policy"], (NAVY_D, 97, NAVY_P, 68, 50),
         [(G["gold"], -180, -200, 740, 740), (G["red"], 880, 560, 680, 680)])
    head(sl, "PART 01 · 应用成效", "看得见的价值：三方收益与三条落地路径")
    ben = [("银行侧收益", RED, RED_L,
            [("获客面从有抵押物企业扩展至", "轻资产科创企业"),
             ("授信从一次性静态审批转为", "可动态调整"),
             ("风险在前置指标上被识别，降低处置成本", "")]),
           ("企业侧收益", GOLD, GOLD_L,
            [("融资节奏与研发节奏对齐，", "缓解死亡谷资金断档"),
             ("每过一个节点自动释放额度，形成", "确定性预期"),
             ("避免在困难期过度稀释股权", "")]),
           ("生态侧收益", BLUE, BLUE,
            [("为「见投即贷」「先投后贷」提供", "量化依据"),
             ("支撑「中试保融通」等", "投贷保联动", "产品创新"),
             ("呼应监管「敢贷、愿贷、能贷、会贷」导向", "")])]
    x = 60
    for t, top, dc, bl in ben:
        card(sl, x, 226, 420, 296, top=top)
        text(sl, x + 22, 246, 380, 30, t, size=21, color=GOLD_L, bold=True, ls=1.0)
        yy = 292
        for parts in bl:
            dot(sl, x + 22, yy + 8, dc)
            runs = []
            for i, p in enumerate(parts):
                if p:
                    runs.append({"t": p, "s": 16,
                                 "c": (GOLD_L if i % 2 == 1 else WHITE),
                                 "b": (i % 2 == 1)})
            text(sl, x + 42, yy, 358, 70, runs, size=16, color=WHITE, ls=1.45)
            yy += 74
        x += 450
    text(sl, 60, 552, 400, 24, "落 地 路 径", size=15, color=GREY, ls=1.0)
    paths = [("1", "接 入", "对接工行科技金融「五专」体系与现有研发贷、积分贷、知识产权融资产品线", RED),
             ("2", "试 点", "优先在知识产权金融生态综合试点省市落地，借力 13 省 124 市风险补偿政策", GOLD),
             ("3", "共 担", "联合政府性担保与风险补偿资金池按比例分担损失，提升一线放贷意愿", BLUE)]
    x = 60
    for i, (n, t, d, c) in enumerate(paths):
        card(sl, x, 584, 400, 116, alpha=62)
        rect(sl, x + 18, 606, 28, 28, fill=None, line=c, lw=1.2)
        text(sl, x + 18, 606, 28, 28, n, size=14, color=c, bold=True,
             align="center", anchor="middle", ls=1.0)
        text(sl, x + 56, 604, 200, 28, t, size=18, color=GOLD_L, bold=True, ls=1.0)
        text(sl, x + 18, 640, 364, 50, d, size=14, color=WHITE, ls=1.4)
        if i < 2:
            text(sl, x + 404, 616, 36, 40, "➜", size=22, color=c,
                 align="center", anchor="middle", ls=1.0)
        x += 450
    note(sl, 60, 716, 1320, 56, "数据边界", RED_L, None,
         [{"t": "本页收益为基于公开数据与模型逻辑的", "s": 16, "c": WHITE},
          {"t": "测算推断", "s": 16, "c": GOLD_L, "b": True},
          {"t": "，用于说明方案的价值方向，", "s": 16, "c": WHITE},
          {"t": "并非实际投放业绩", "s": 16, "c": GOLD_L, "b": True}], ls=1.3)


def s15(sl, B, G):
    page(sl, B["circuit"], (NAVY_D, 96, NAVY_P, 55, 0),
         [(G["gold"], 800, 480, 780, 780), (G["red"], -180, -200, 700, 700)])
    bar(sl, 60, 250, 120, 5)
    text(sl, 196, 240, 300, 30, "PART 02", size=17, color=GOLD, ls=1.0)
    text(sl, 60, 300, 900, 96, "技术价值", size=86, color=GOLD_L, bold=True, ls=1.0)
    text(sl, 60, 414, 900, 42, "从应用逻辑，走进 AI 引擎与工程实现",
         size=28, color=WHITE, ls=1.0)
    x = 60
    for lb, c, b in [("XGBoost 双模型", GOLD_L, GOLD), ("PageRank 图算法", RED_L, RED),
                     ("优雅降级", GREY, BLUE)]:
        w = len(lb) * 20 + 50
        chip(sl, x, 500, w, 46, lb, c, b, 62, 17)
        x += w + 16
    text(sl, 60, 590, 700, 26, "本部分 5 页 · 回答「凭什么我们做得到」",
         size=16, color=GREY, ls=1.0)


def s16(sl, B, G):
    page(sl, B["network"], (NAVY_D, 97, NAVY_P, 72, 45),
         [(G["blue"], 860, -180, 680, 680), (G["gold"], -170, 560, 680, 680)])
    head(sl, "PART 02 · 技术架构", "四层解耦：从交互界面到底层模型")
    layers = [("LAYER 01", "展现层", GOLD_L,
               ["Vue 3 Composition API", "TypeScript", "Vite 5", "Element Plus",
                "ECharts 5", "Pinia"],
               "玻璃拟态深色主题 · 1024px / 640px 双断点响应式"),
              ("LAYER 02", "服务层", GOLD,
               ["FastAPI", "SQLAlchemy 2", "企业服务", "估值服务", "授信服务", "风控服务"],
               "四组业务服务 · 13 个 REST 端点对外暴露"),
              ("LAYER 03", "AI 推理层", RED_L,
               ["XGBoost 估值模型", "XGBoost 破产风险模型", "NetworkX PageRank", ".joblib 热加载"],
               "双模型并行推理 ＋ 图计算，统一封装为单次 API 调用"),
              ("LAYER 04", "数据层", GREY,
               ["Enterprise", "Patent / PatentCitation", "TeamMember",
                "Milestone / FinancialTool", "CreditRecord / RiskAlert", "SQLite / MySQL"],
               "含 95 维财务特征 JSON · Redis 可选，降级不影响主流程")]
    y = 226
    for i, (k, t, tc, tags, foot) in enumerate(layers):
        hl = (i == 2)
        rect(sl, 60, y, 1320, 118, fill=(NAVY_P if hl else NAVY_C),
             alpha=(78 if hl else 68),
             line=(GOLD if hl else BLUE), lw=(1.3 if hl else 1.1))
        rect(sl, 60, y, 5, 118, fill=(RED if hl else tc))
        text(sl, 84, y + 22, 160, 20, k, size=13, color=GREY, ls=1.0)
        text(sl, 84, y + 46, 160, 32, t, size=21, color=GOLD_L, bold=True, ls=1.0)
        tx = 250
        fac = (11, 22) if i == 3 else (13, 26)
        for tg in tags:
            w = len(tg) * fac[0] + fac[1]
            chip(sl, tx, y + 18, w, 34, tg,
                 (RED_L if hl and "XGBoost" in tg else (GOLD_L if hl and "NetworkX" in tg else WHITE)),
                 (RED if hl and "XGBoost" in tg else (GOLD if hl and "NetworkX" in tg else BLUE)),
                 50, 13 if i == 3 else 14)
            tx += w + 10
        text(sl, 250, y + 74, 1100, 26, foot, size=14, color=GREY, ls=1.0)
        y += 134


def s17(sl, B, G):
    page(sl, B["lab"], (NAVY_D, 97, NAVY_P, 50, 20),
         [(G["gold"], -170, -190, 700, 700), (G["red"], 880, 560, 660, 660)])
    head(sl, "PART 02 · AI 引擎", "两个 XGBoost 模型，撑起估值与风险两侧")
    # 估值模型
    card(sl, 60, 226, 640, 360, top=GOLD)
    text(sl, 84, 248, 400, 32, "估值预测模型", size=23, color=GOLD_L, bold=True, ls=1.0)
    chip(sl, 560, 250, 116, 30, "Regressor", GOLD_L, GOLD, 55, 14)
    rect(sl, 84, 292, 282, 82, fill=NAVY_D, alpha=58, line=GOLD, lw=1.0)
    text(sl, 84, 306, 282, 34, "0.927", size=30, color=GOLD_L, bold=True,
         align="center", ls=1.0)
    text(sl, 84, 344, 282, 20, "基础估值 R²", size=13, color=GREY,
         align="center", ls=1.0)
    rect(sl, 392, 292, 282, 82, fill=NAVY_D, alpha=58, line=GOLD, lw=1.0)
    text(sl, 392, 306, 282, 34, "0.954", size=30, color=GOLD_L, bold=True,
         align="center", ls=1.0)
    text(sl, 392, 344, 282, 20, "当前估值 R²", size=13, color=GREY,
         align="center", ls=1.0)
    rows = [("训练样本", "2000 条硬科技企业数据"), ("输入特征", "8 个（含行业与阶段类别）"),
            ("模型配置", "300 棵树 · max_depth = 6"), ("预处理", "OneHotEncoder ＋ 数值直通")]
    ry = 390
    for a, b in rows:
        text(sl, 84, ry, 200, 24, a, size=14, color=GREY, ls=1.0)
        text(sl, 300, ry, 380, 24, b, size=14, color=WHITE, align="right", ls=1.0)
        ry += 32
    rect(sl, 84, 520, 592, 1, fill=BLUE, alpha=45)
    text(sl, 84, 532, 300, 20, "特 征 工 程", size=13, color=GREY, ls=1.0)
    text(sl, 84, 554, 592, 40,
         "引入非线性与交互项：patent_count^0.7、team_score^1.5、log(员工数)",
         size=13, color=WHITE, ls=1.25)
    # 风险模型
    card(sl, 740, 226, 640, 360, top=RED)
    text(sl, 764, 248, 400, 32, "破产风险预测模型", size=23, color=GOLD_L, bold=True, ls=1.0)
    chip(sl, 1264, 250, 92, 30, "Classifier", RED_L, RED, 55, 14)
    rect(sl, 764, 292, 282, 82, fill=NAVY_D, alpha=58, line=RED, lw=1.0)
    text(sl, 764, 306, 282, 34, "0.958", size=30, color=RED_L, bold=True,
         align="center", ls=1.0)
    text(sl, 764, 344, 282, 20, "AUC", size=13, color=GREY, align="center", ls=1.0)
    rect(sl, 1072, 292, 282, 82, fill=NAVY_D, alpha=58, line=RED, lw=1.0)
    text(sl, 1072, 306, 282, 34,
         [{"t": "96.9", "s": 30, "c": RED_L, "b": True}, {"t": "%", "s": 15, "c": RED_L}],
         align="center", ls=1.0)
    text(sl, 1072, 344, 282, 20, "Accuracy", size=13, color=GREY, align="center", ls=1.0)
    rows2 = [("训练数据", "真实企业财务公开数据集 6819 条"),
             ("特征维度", "95 个财务特征"),
             ("类别分布", "未破产 6599 vs 破产 220"),
             ("不平衡处理", "scale_pos_weight = 30")]
    ry = 390
    for a, b in rows2:
        text(sl, 764, ry, 200, 24, a, size=14, color=GREY, ls=1.0)
        text(sl, 980, ry, 374, 24, b, size=14, color=WHITE, align="right", ls=1.0)
        ry += 32
    rect(sl, 764, 520, 592, 1, fill=BLUE, alpha=45)
    text(sl, 764, 532, 300, 20, "TOP 5 特征", size=13, color=GREY, ls=1.0)
    text(sl, 764, 554, 592, 40,
         "税后持续利率 12.9% · 近四季 EPS 7.7% · 净利润/总资产 7.4% · 借款依赖度 4.1%",
         size=13, color=WHITE, ls=1.25)
    note(sl, 60, 622, 1320, 74, "推理链路", GOLD, None,
         [{"t": "请求进入 → 组装特征（专利数 · PageRank 质量 · 团队评分） → ", "s": 17, "c": WHITE},
          {"t": "双模型并行推理", "s": 17, "c": GOLD_L, "b": True},
          {"t": " → 输出基础/当前估值与风险评分 → 异常时回退规则公式", "s": 17, "c": WHITE}], ls=1.3)


def s18(sl, B, G):
    page(sl, B["network"], (NAVY_D, 97, NAVY_P, 70, 35),
         [(G["gold"], -170, -190, 700, 700), (G["red"], 880, 560, 660, 660)])
    head(sl, "PART 02 · 图算法", "用图算法量化一件专利的真实影响力")
    blocks = [("为什么用「图」而不是「计数」", GOLD,
               [{"t": "专利的价值不只在于被引用多少次，更在于它在整个技术脉络中的", "s": 16, "c": WHITE},
                {"t": "位置", "s": 16, "c": GOLD_L, "b": True},
                {"t": "——被一件核心专利引用，与被一件边缘专利引用，含金量完全不同。", "s": 16, "c": WHITE}]),
              ("算法实现", RED,
               [{"t": "以 NetworkX 构建", "s": 16, "c": WHITE},
                {"t": "有向引用图", "s": 16, "c": GOLD_L, "b": True},
                {"t": "（专利为节点、引用关系为边），运行 PageRank（", "s": 16, "c": WHITE},
                {"t": "alpha = 0.85", "s": 16, "c": GOLD_L, "b": True},
                {"t": "）计算每件专利的中心性权重。", "s": 16, "c": WHITE}]),
              ("如何进入风控链路", BLUE,
               [{"t": "PageRank 结果作为专利质量的维度之一合成质量分，再回流为企业估值与授信输入——让图计算的产出", "s": 16, "c": WHITE},
                {"t": "直接作用于额度", "s": 16, "c": GOLD_L, "b": True},
                {"t": "。", "s": 16, "c": WHITE}])]
    y = 226
    for t, c, runs in blocks:
        card(sl, 60, y, 740, 132, top=None)
        rect(sl, 60, y, 4, 132, fill=c)
        text(sl, 84, y + 18, 600, 30, t, size=20, color=GOLD_L, bold=True, ls=1.0)
        text(sl, 84, y + 58, 692, 62, runs, size=16, color=WHITE, ls=1.5)
        y += 148
    # 右侧
    card(sl, 830, 226, 550, 236)
    text(sl, 852, 246, 380, 26, "引用网络中的节点位置", size=17, color=GOLD_L,
         bold=True, ls=1.0)
    text(sl, 1180, 250, 180, 22, "节点越大，中心性越高", size=13, color=GREY,
         align="right", ls=1.0)
    import svg_network
    png = svg_network.draw_small_net(os.path.join(TMP, "smallnet.png"))
    sl.shapes.add_picture(png, P(852), P(288), P(506), P(158))
    card(sl, 830, 478, 550, 254)
    text(sl, 852, 498, 380, 26, "专利质量评分构成", size=17, color=GOLD_L,
         bold=True, ls=1.0)
    wts = [("引用次数", 100, BLUE, "30%"), ("PageRank", 83, RED, "25%"),
           ("同族规模", 67, BLUE, "20%"), ("国际布局", 50, BLUE, "15%"),
           ("诉讼情况", 33, GOLD, "10%")]
    wy = 538
    for lb, w, c, pv in wts:
        text(sl, 852, wy, 90, 24, lb, size=14, color=GREY, ls=1.0)
        rect(sl, 950, wy + 7, 320, 12, fill=BLUE, alpha=22)
        rect(sl, 950, wy + 7, int(320 * w / 100), 12, fill=c, alpha=100)
        text(sl, 1290, wy, 70, 24, pv, size=14, color=GOLD_L, align="right", ls=1.0)
        wy += 40
    note(sl, 60, 736, 1320, 62, "差异化价值", GOLD, None,
         [{"t": "把单件专利从「一个计数」升级为「一个位置」，让银行的知识产权评估", "s": 17, "c": WHITE},
          {"t": "从数量逻辑走向结构逻辑", "s": 17, "c": GOLD_L, "b": True}], ls=1.3)


def s19(sl, B, G):
    page(sl, B["circuit"], (NAVY_D, 97, NAVY_P, 70, 45),
         [(G["blue"], 860, -180, 680, 680), (G["gold"], -170, 560, 680, 680)])
    head(sl, "PART 02 · 工程实现", "让 AI 在银行生产环境里稳定落地")
    top2 = [("1", "优雅降级", GOLD, GOLD_L,
             [{"t": "模型文件缺失或推理失败时，自动回退到规则公式，并在结果中标注估值来源——", "s": 16, "c": WHITE},
              {"t": "保证服务可用性不因模型异常中断", "s": 16, "c": GOLD_L, "b": True},
              {"t": "。这是银行级系统的必备能力。", "s": 16, "c": WHITE}]),
            ("2", "实时联动", RED, RED_L,
             [{"t": "里程碑进度滑块拖动时，状态流转与授信额度同步重算；任一要素调整后全部指标一并刷新，做到", "s": 16, "c": WHITE},
              {"t": "所见即所得", "s": 16, "c": GOLD_L, "b": True},
              {"t": "。", "s": 16, "c": WHITE}])]
    x = 60
    for n, t, c, tc, runs in top2:
        card(sl, x, 226, 640, 172, top=c)
        rect(sl, x + 22, 250, 32, 32, fill=None, line=c, lw=1.2)
        text(sl, x + 22, 250, 32, 32, n, size=16, color=tc, bold=True,
             align="center", anchor="middle", ls=1.0)
        text(sl, x + 66, 252, 300, 30, t, size=22, color=GOLD_L, bold=True, ls=1.0)
        text(sl, x + 22, 300, 596, 90, runs, size=16, color=WHITE, ls=1.55)
        x += 670
    bot3 = [("3", "可追溯性", BLUE, GREY,
             "估值与风险结果均标注产出来源（ML 模型 / 规则回退），便于风控人员复核与监管审计。"),
            ("4", "可视化与响应式", GOLD_L, GOLD,
             "ECharts 深色主题深度适配；7 个业务组件、6 类图表形态，支持 1024px 与 640px 断点自适应。"),
            ("5", "链路完整性", RED_L, RED,
             "13 个 REST 端点覆盖企业、估值、团队、专利、里程碑、授信、风控全链路。")]
    x = 60
    for n, t, c, tc, d in bot3:
        card(sl, x, 414, 420, 154, top=c)
        rect(sl, x + 20, 436, 28, 28, fill=None, line=c, lw=1.2)
        text(sl, x + 20, 436, 28, 28, n, size=14, color=tc, bold=True,
             align="center", anchor="middle", ls=1.0)
        text(sl, x + 58, 436, 300, 28, t, size=20, color=GOLD_L, bold=True, ls=1.0)
        text(sl, x + 20, 474, 380, 80, d, size=15, color=WHITE, ls=1.5)
        x += 450
    stack1 = [("Vue 3 + TypeScript", GOLD), ("FastAPI + SQLAlchemy 2", GOLD),
              ("XGBoost + scikit-learn", RED)]
    stack2 = [("NetworkX PageRank", RED), ("SQLite / MySQL + Redis（可选）", BLUE)]
    for row, items in ((596, stack1), (654, stack2)):
        x = 60
        for lb, c in items:
            w = len(lb) * 16 + 40
            chip(sl, x, row, w, 44, lb,
                 (GREY if c == BLUE else (RED_L if c == RED else GOLD_L)), c, 55, 15)
            x += w + 14


def s20(sl, B, G):
    page(sl, B["cover"], (NAVY_D, 97, NAVY_P, 52, 25),
         [(G["gold"], 820, -170, 720, 720), (G["red"], -140, 560, 640, 640)])
    bar(sl, 60, 176, 100, 5)
    text(sl, 176, 166, 300, 30, "结 语", size=16, color=GOLD, ls=1.0)
    text(sl, 60, 226, 900, 170, "让研发的每一步\n都成为可计量的信用", size=54,
         color=GOLD_L, bold=True, ls=1.18)
    pil = [("AI 动态估值", "把专利与团队变成可比较的分数", GOLD),
           ("里程碑触发", "过一关，释放一档额度", RED),
           ("投贷联动", "银行与创投共用同一套判断", BLUE)]
    x = 60
    for t, d, c in pil:
        card(sl, x, 428, 280, 108, top=c)
        text(sl, x + 20, 448, 240, 30, t, size=21, color=GOLD_L, bold=True, ls=1.0)
        text(sl, x + 20, 482, 240, 40, d, size=14, color=GREY, ls=1.35)
        x += 300
    note(sl, 60, 562, 1320, 70, "展 望", GOLD, None,
         [{"t": "从「看抵押物」到「看创新力」，从「静态审批」到「动态授信」——让更多硬科技企业走出死亡谷",
           "s": 18, "c": WHITE}], ls=1.3)
    text(sl, 60, 668, 700, 26, "工银科创桥 · 硬科技企业里程碑式投贷联动平台",
         size=15, color=GREY, ls=1.0)
    text(sl, 900, 664, 480, 30, "感谢聆听　敬请指正", size=20, color=GOLD_L,
         align="right", ls=1.0)


# ============================================================
def main():
    print("[1/4] 预处理背景图与光晕 ...")
    B = {k: prep_bg("bg-" + k + ".png") for k in
         ["cover", "pain", "policy", "bridge", "lab-human",
          "banker-human", "network", "circuit"]}
    B["lab"] = B.pop("lab-human")
    B["banker"] = B.pop("banker-human")
    G = {"gold": make_glow("glow_gold.png", (232, 179, 75)),
         "red": make_glow("glow_red.png", (199, 0, 11)),
         "blue": make_glow("glow_blue.png", (91, 125, 187))}

    prs = Presentation()
    prs.slide_width = Pt(960)
    prs.slide_height = Pt(540)
    blank = prs.slide_layouts[6]

    builders = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10,
                s11, s12, s13, s14, s15, s16, s17, s18, s19, s20]
    print("[2/4] 生成 20 页 ...")
    for i, fn in enumerate(builders, 1):
        sl = prs.slides.add_slide(blank)
        fn(sl, B, G)
        print(f"      第 {i:02d} 页完成")

    out = os.path.join(OUT, "presentation.pptx")
    print("[3/4] 写入 ...")
    prs.save(out)
    print(f"[4/4] 完成：{out}")
    return out


if __name__ == "__main__":
    main()
