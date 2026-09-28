# -*- coding: utf-8 -*-
"""把报告内容依次写入 editor_sdk 中的新建 docx。"""
import json
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")

EDSDK = r"E:\Program Files\WorkBuddy\resources\app.asar.unpacked\resources\plugins\workbuddy-builtin\skills\tencent-local-office-edit\edsdk.py"
PY = r"C:\Users\lenovo\.workbuddy\binaries\python\envs\default\Scripts\python.exe"
BASE = r"C:\Users\lenovo\Desktop\工行杯\ppt-deck\report"
FILE_ID = "gongyin-report"
TMP = os.path.join(BASE, "_args.json")


def call(tool, args):
    args = dict(args)
    args.setdefault("file_id", FILE_ID)
    with open(TMP, "w", encoding="utf-8") as f:
        json.dump(args, f, ensure_ascii=False)
    r = subprocess.run([PY, EDSDK, "call", tool, "--json-file", TMP],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = (r.stdout or "").strip()
    if not out:
        out = (r.stderr or "").strip()
    try:
        data = json.loads(out)
    except Exception:
        data = {}
        print("  [非JSON返回]", out[:200])
    if data.get("ok") is False:
        print("  [失败]", tool, str(data.get("error"))[:200])
    return data


def last_pos():
    d = call("doc_get_last_operable_pos", {})
    return d.get("position", 0)


def md(name):
    with open(os.path.join(BASE, name), encoding="utf-8") as f:
        return f.read()


def main():
    # 1. 封面
    print("[1] 插入封面 ...")
    with open(os.path.join(BASE, "00_cover.html"), encoding="utf-8") as f:
        cover = f.read()
    call("doc_insert_html_content", {"idx": 0, "html_text": cover})
    p = last_pos()
    print("    position =", p)

    # 2. 分页 + 摘要
    print("[2] 插入摘要 ...")
    call("doc_insert_page_break", {"idx": p})
    p = last_pos()
    call("doc_insert_markdown", {"idx": p, "markdown": md("01_abstract.md")})
    p = last_pos()
    print("    position =", p)

    # 3. 分页 + 目录
    print("[3] 插入目录 ...")
    call("doc_insert_page_break", {"idx": p})
    p = last_pos()
    call("doc_insert_toc", {"idx": p, "max_level": 2})
    p = last_pos()
    print("    position =", p)

    # 4. 分页 + 各章节
    parts = ["02_ch1_2.md", "03_ch3_4_5.md", "04_ch6_7_8.md", "05_ch9_10.md"]
    for i, name in enumerate(parts, 1):
        print("[4.%d] 插入 %s ..." % (i, name))
        call("doc_insert_page_break", {"idx": p})
        p = last_pos()
        d = call("doc_insert_markdown", {"idx": p, "markdown": md(name)})
        p = d.get("position") or last_pos()
        print("    position =", p)

    print("[5] 完成，末尾坐标 =", p)


if __name__ == "__main__":
    main()
