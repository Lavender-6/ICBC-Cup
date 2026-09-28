"""把网页界面截图排版成一份介绍性 PDF（A4 横向，深色主题，控制体积在 1MB 内）。"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = r"C:\Users\lenovo\Desktop\工行杯\工银科创桥-平台界面介绍.pdf"

# A4 横向 @150dpi
W, H = 1754, 1240
PAD = 64
TOP = 148          # 页眉下沿
BOTTOM = 1160      # 页脚上沿
AVAIL_W = W - PAD * 2
AVAIL_H = BOTTOM - TOP

BG = (10, 23, 48)
BG2 = (14, 33, 69)
GOLD = (232, 179, 75)
GOLD_L = (245, 212, 136)
RED = (199, 0, 11)
GREY = (159, 180, 218)
WHITE = (224, 230, 240)
LINE = (91, 125, 187)

F_B = "C:/Windows/Fonts/msyhbd.ttc"
F_R = "C:/Windows/Fonts/msyh.ttc"


def ft(path, size):
    return ImageFont.truetype(path, size)


def new_page():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 7], fill=RED)
    d.rectangle([0, 7, W, 10], fill=GOLD)
    return img, d


def header(d, kicker, title, page_no, total):
    """页眉：左侧小标签 + 主标题，右侧页码"""
    d.text((PAD, 44), kicker, font=ft(F_R, 22), fill=GREY)
    d.text((PAD, 78), title, font=ft(F_B, 44), fill=GOLD_L)
    d.rectangle([PAD, 128, PAD + 70, 132], fill=RED)
    d.rectangle([PAD + 78, 128, PAD + 150, 132], fill=GOLD)
    right = f"{page_no} / {total}"
    w = d.textlength(right, font=ft(F_R, 24))
    d.text((W - PAD - w, 82), right, font=ft(F_R, 24), fill=GREY)


def footer(d, note):
    d.line([(PAD, BOTTOM + 22), (W - PAD, BOTTOM + 22)], fill=(31, 55, 100), width=2)
    d.text((PAD, BOTTOM + 40), note, font=ft(F_R, 21), fill=GREY)
    tag = "工银科创桥 · 硬科技企业里程碑式投贷联动平台"
    w = d.textlength(tag, font=ft(F_R, 21))
    d.text((W - PAD - w, BOTTOM + 40), tag, font=ft(F_R, 21), fill=(91, 125, 187))


def fit(img, box_w, box_h):
    """等比缩放使图片落入 box"""
    iw, ih = img.size
    s = min(box_w / iw, box_h / ih)
    nw, nh = max(1, int(iw * s)), max(1, int(ih * s))
    return img.resize((nw, nh), Image.LANCZOS)


def put(img, shot, box, d, label=None):
    """把截图放进 box=(x,y,w,h) 区域（居中），带金色细边框"""
    x, y, bw, bh = box
    s = fit(shot, bw, bh)
    px = x + (bw - s.width) // 2
    py = y + (bh - s.height) // 2
    d.rectangle([px - 3, py - 3, px + s.width + 3, py + s.height + 3],
                outline=(59, 92, 148), width=2)
    img.paste(s, (px, py))
    if label:
        d.text((px, py + s.height + 12), label, font=ft(F_R, 20), fill=GREY)
    return s


def load(name):
    p = os.path.join(HERE, name)
    if not os.path.exists(p):
        raise FileNotFoundError(p)
    return Image.open(p).convert("RGB")


def bullets(d, x, y, items, size=24, lh=42, color=WHITE, key_color=GOLD_L):
    """要点列表：金色圆点 + 文字"""
    for i, (k, v) in enumerate(items):
        yy = y + i * lh
        d.ellipse([x, yy + size // 2 - 4, x + 9, yy + size // 2 + 5], fill=key_color)
        d.text((x + 22, yy), k, font=ft(F_B, size), fill=key_color)
        kw = d.textlength(k, font=ft(F_B, size))
        d.text((x + 22 + kw + 12, yy + 3), v, font=ft(F_R, size - 2), fill=color)
    return y + len(items) * lh


def wrap(d, text, font, max_w):
    """按像素宽度换行（中文逐字）"""
    lines, cur = [], ""
    for ch in text:
        if ch == "\n":
            lines.append(cur)
            cur = ""
            continue
        if d.textlength(cur + ch, font=font) > max_w:
            lines.append(cur)
            cur = ch
        else:
            cur += ch
    if cur:
        lines.append(cur)
    return lines


def para(d, xy, text, font, fill, lh, max_w):
    x, y = xy
    for ln in wrap(d, text, font, max_w):
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


TOTAL = 9


def p1_cover():
    img, d = new_page()
    hero = load("home_hero.png")
    # 标题区
    d.rectangle([0, 0, W, 300], fill=BG2)
    d.text((PAD, 92), "ICBC TECH INNOVATION BRIDGE", font=ft(F_B, 26), fill=RED)
    d.text((PAD, 150), "工银科创桥", font=ft(F_B, 96), fill=GOLD_L)
    d.text((PAD, 272), "硬科技企业里程碑式投贷联动平台 · 产品界面介绍", font=ft(F_R, 30), fill=GREY)
    # hero 图
    s = fit(hero, AVAIL_W, 620)
    px = (W - s.width) // 2
    img.paste(s, (px, 340))
    d.rectangle([px - 3, 337, px + s.width + 3, 340 + s.height + 3], outline=LINE, width=2)
    y = 340 + s.height + 40
    d.text((PAD, y), "平台首页", font=ft(F_B, 28), fill=GOLD)
    y = para(d, (PAD, y + 44),
             "以 AI 评估引擎对轻资产科创企业做动态估值，以研发里程碑为触发器动态匹配金融工具包，"
             "把一次性静态审批转变为随研发进度滚动释放的动态授信——让研发的每一步，都成为可计量的信用。",
             ft(F_R, 25), WHITE, 42, AVAIL_W)
    d.rectangle([PAD, H - 150, W - PAD, H - 146], fill=RED)
    d.text((PAD, H - 130), "参赛项目：工行杯  |  界面截图取自实际运行的系统（Vue 3 + FastAPI + XGBoost）",
           font=ft(F_R, 22), fill=GREY)
    return img


def p2_capability():
    img, d = new_page()
    header(d, "01  平台首页", "四大核心能力", 2, TOTAL)
    put(img, load("home_capability.png"), (PAD, TOP + 10, AVAIL_W, 430), d)
    y = TOP + 470
    d.text((PAD, y), "能力解读", font=ft(F_B, 28), fill=GOLD)
    bullets(d, PAD, y + 50, [
        ("AI 评估引擎", "专利引用网络 + 研发团队画像，输出动态估值与破产风险"),
        ("里程碑触发动态授信", "进度系数 × 风险系数实时重算额度，资金匹配研发节奏"),
        ("投贷联动工作台", "股 · 债 · 保三维工具包智能匹配，覆盖全生命周期"),
        ("风控看板", "风险评分趋势监控，进度偏低与延迟自动预警"),
    ], size=25, lh=48)
    footer(d, "截图：平台首页「平台核心能力」区块")
    return img


def p3_milestone():
    img, d = new_page()
    header(d, "02  首页", "里程碑式投贷联动 · 硬科技企业库", 3, TOTAL)
    put(img, load("home_milestone.png"), (PAD, TOP + 6, AVAIL_W, 330), d)
    put(img, load("home_enterprise.png"), (PAD, TOP + 380, AVAIL_W, 480), d,
        label="企业库支持按行业 / 阶段筛选，可勾选 2–4 家企业横向对比")
    footer(d, "截图：首页里程碑流程与企业列表区块")
    return img


def p4_dashboard():
    img, d = new_page()
    header(d, "03  数据大屏", "全局资产与风险概览", 4, TOTAL)
    put(img, load("dash_full.png"), (PAD, TOP + 6, 1180, AVAIL_H - 10), d)
    x = PAD + 1210
    d.text((x, TOP + 10), "大屏说明", font=ft(F_B, 28), fill=GOLD)
    para(d, (x, TOP + 58),
         "顶部四项为平台核心指标：企业总数、平均估值、专利总数、研发人员。\n\n"
         "下方四张图表分别呈现行业分布、研发阶段分布、风险等级分布与里程碑状态统计，"
         "全部由后端实时聚合计算，前端 ECharts 渲染。\n\n"
         "管理层可据此把握在管科创资产的行业集中度、阶段结构与风险敞口。",
         ft(F_R, 22), WHITE, 38, W - x - PAD)
    footer(d, "截图：/dashboard 数据大屏（数据来自系统内真实企业样本）")
    return img


def p5_profile():
    img, d = new_page()
    header(d, "04  企业详情页", "企业画像 · 团队画像 · 风控预警", 5, TOTAL)
    box_w = (AVAIL_W - 40) // 3
    put(img, load("detail_profile.png"), (PAD, TOP + 8, box_w, 760), d)
    put(img, load("detail_team.png"), (PAD + box_w + 20, TOP + 8, box_w, 760), d)
    put(img, load("detail_risk.png"), (PAD + (box_w + 20) * 2, TOP + 8, box_w, 760), d)
    y = TOP + 800
    d.text((PAD, y), "画像引擎", font=ft(F_B, 28), fill=GOLD)
    bullets(d, PAD, y + 50, [
        ("企业画像", "基础信息 + AI 估值区间 + 破产风险概率，双模型并行输出"),
        ("研发团队画像", "核心成员背景、学历与 Stability 指标量化团队质量"),
        ("风控预警", "里程碑延迟、风险分攀升等触发分级预警，供客户经理跟进"),
    ], size=24, lh=44)
    footer(d, "截图：/enterprise/{id} 左侧三张卡片（示例企业：芯动微电子 / 半导体 / 流片成功）")
    return img


def p6_patent():
    img, d = new_page()
    header(d, "05  专利评估", "专利引用趋势与影响力网络", 6, TOTAL)
    put(img, load("detail_patents.png"), (PAD, TOP + 8, 1120, AVAIL_H - 20), d)
    x = PAD + 1170
    d.text((x, TOP + 12), "技术要点", font=ft(F_B, 28), fill=GOLD)
    y = para(d, (x, TOP + 62),
             "基于 NetworkX 构建专利引用图谱，以 PageRank 算法（alpha=0.85）量化单件专利的真实影响力。\n\n"
             "专利质量分权重：引用 30%、PageRank 25%、同族 20%、国际布局 15%、诉讼 10%。\n\n"
             "实现从「数专利数量」到「看专利结构」的范式转变，"
             "使无形资产评估有可解释、可复核的量化依据。",
             ft(F_R, 22), WHITE, 38, W - x - PAD)
    y += 26
    d.rectangle([x, y, x + 480, y + 4], fill=RED)
    y += 24
    d.text((x, y), "支持折线图 / 力导向网络两种视图切换", font=ft(F_R, 21), fill=GREY)
    footer(d, "截图：专利引用趋势模块")
    return img


def p7_milestone_board():
    img, d = new_page()
    header(d, "06  里程碑管理", "里程碑看板与进度跟踪", 7, TOTAL)
    put(img, load("detail_milestone.png"), (PAD, TOP + 8, 760, AVAIL_H - 20), d)
    x = PAD + 820
    d.text((x, TOP + 12), "五阶里程碑", font=ft(F_B, 28), fill=GOLD)
    items = [
        ("①  立项 / 预研", "知识产权质押贷 + 研发补贴"),
        ("②  原型验证", "AI 动态估值授信 + 股权跟投"),
        ("③  流片 / 临床 II 期", "投贷联动（银行授信 + VC 跟投）"),
        ("④  商业化量产", "供应链票据 + 订单融资"),
        ("⑤  上市预备", "可转债 + 科创专项债"),
    ]
    yy = TOP + 62
    for k, v in items:
        d.text((x, yy), k, font=ft(F_B, 25), fill=GOLD_L)
        d.text((x, yy + 36), v, font=ft(F_R, 22), fill=WHITE)
        yy += 84
    yy += 12
    para(d, (x, yy),
         "每个阶段绑定对应金融工具包；里程碑状态（未开始 / 进行中 / 已完成 / 已延迟）"
         "由客户经理维护，一经更新即触发额度重算。",
         ft(F_R, 22), GREY, 36, W - x - PAD)
    footer(d, "截图：里程碑看板（可新增、完成、删除里程碑）")
    return img


def p8_credit():
    img, d = new_page()
    header(d, "07  授信决策", "授信模拟器", 8, TOTAL)
    put(img, load("detail_credit.png"), (PAD, TOP + 8, 980, 700), d)
    x = PAD + 1040
    d.text((x, TOP + 12), "授信公式", font=ft(F_B, 28), fill=GOLD)
    yy = TOP + 62
    d.rectangle([x, yy, x + 560, yy + 92], fill=BG2, outline=LINE, width=2)
    d.text((x + 22, yy + 22), "额度 = AI 估值 × 30% × 进度系数 × (1 − 风险评分 × 0.5)",
           font=ft(F_B, 22), fill=GOLD_L)
    d.text((x + 22, yy + 56), "拖动进度滑块，额度实时联动重算", font=ft(F_R, 20), fill=GREY)
    yy += 122
    para(d, (x, yy),
         "模拟器把估值、里程碑进度、风险评分三者耦合为一个可交互的推演工具：\n\n"
         "· 进度系数随里程碑完成情况线性释放\n"
         "· 风险评分越高，折减越强\n"
         "· 模型异常时自动回退规则公式，并标注估值来源（优雅降级）\n\n"
         "客户经理可在面谈现场与客户共同推演「再过一个里程碑能多拿多少额度」。",
         ft(F_R, 22), WHITE, 38, W - x - PAD)
    yy2 = TOP + 730
    d.text((PAD, yy2), "工程实现", font=ft(F_B, 26), fill=GOLD)
    bullets(d, PAD, yy2 + 46, [
        ("实时联动", "进度滑块拖动即刻重算，无需提交"),
        ("全程可追溯", "结果标注产出来源，便于风控复核与监管审计"),
    ], size=23, lh=42)
    footer(d, "截图：授信模拟器（示例：里程碑进度 50%，基础额度 1,820 万元）")
    return img


def p9_summary():
    img, d = new_page()
    header(d, "08  技术架构", "系统实现与三方价值", 9, TOTAL)
    # 架构三列
    cols = [
        ("前端展示层", ["Vue 3 + TypeScript", "Element Plus 组件库", "ECharts 数据可视化", "Vite 构建"]),
        ("后端服务层", ["FastAPI + SQLAlchemy", "13 个 REST 端点", "SQLite / MySQL 存储", "Pydantic 数据校验"]),
        ("算法引擎层", ["XGBoost 双模型", "NetworkX + PageRank", "里程碑授信引擎", "优雅降级策略"]),
    ]
    cw = (AVAIL_W - 40) // 3
    for i, (t, items) in enumerate(cols):
        x = PAD + i * (cw + 20)
        d.rectangle([x, TOP, x + cw, TOP + 260], fill=BG2, outline=LINE, width=2)
        d.rectangle([x, TOP, x + cw, TOP + 6], fill=RED if i % 2 == 0 else GOLD)
        d.text((x + 26, TOP + 34), t, font=ft(F_B, 28), fill=GOLD_L)
        for j, it in enumerate(items):
            d.ellipse([x + 30, TOP + 104 + j * 38, x + 38, TOP + 112 + j * 38], fill=GOLD)
            d.text((x + 50, TOP + 92 + j * 38), it, font=ft(F_R, 22), fill=WHITE)
    y = TOP + 300
    d.text((PAD, y), "三方价值", font=ft(F_B, 30), fill=GOLD)
    vals = [
        ("银行", "把无形资产翻译成可解释、可追溯、可审计的风险参数，让「敢贷」有依据"),
        ("硬科技企业", "把不确定的融资预期，变成随里程碑递进的确定性安排"),
        ("创投与保险", "动态估值时间序列与破产概率输出，为见投即贷、中试保融通提供定价参考"),
    ]
    yy = y + 54
    for k, v in vals:
        d.rectangle([PAD, yy, PAD + 8, yy + 62], fill=RED)
        d.text((PAD + 26, yy + 4), k, font=ft(F_B, 25), fill=GOLD_L)
        kw = d.textlength(k, font=ft(F_B, 25))
        d.text((PAD + 26 + kw + 20, yy + 8), v, font=ft(F_R, 22), fill=WHITE)
        yy += 78
    yy += 10
    d.rectangle([PAD, yy, W - PAD, yy + 3], fill=LINE)
    d.text((PAD, yy + 22),
           "说明：本项目为演示型产品原型，已完成系统实现与算法验证；"
           "界面中数据为系统内置样本数据，尚无真实投放金额与客户运营数据。",
           font=ft(F_R, 21), fill=GREY)
    footer(d, "工银科创桥 · 平台界面介绍")
    return img


def main():
    builders = [p1_cover, p2_capability, p3_milestone, p4_dashboard,
                p5_profile, p6_patent, p7_milestone_board, p8_credit, p9_summary]
    pages = []
    for b in builders:
        pages.append(b())
        print("  页面完成:", b.__name__)

    # 轻微降采样（≈138dpi）换取更高的 JPEG 质量，保证文字清晰且体积可控
    OUT_W, OUT_H = 1620, 1145
    pages = [p.resize((OUT_W, OUT_H), Image.LANCZOS) for p in pages]

    # 自适应压缩：确保 < 1MB
    target = 1_000_000
    for q in (88, 82, 76, 70, 64, 58):
        pages[0].save(OUT, "PDF", save_all=True, append_images=pages[1:],
                      resolution=138.0, quality=q)
        size = os.path.getsize(OUT)
        print(f"  quality={q} -> {size/1024:.0f} KB")
        if size <= target:
            break
    print("输出:", OUT, f"{os.path.getsize(OUT)/1024:.0f} KB, {len(pages)} 页")


if __name__ == "__main__":
    main()
