"""通过 Chrome DevTools Protocol 精确截取工银科创桥网页各功能区块。

用法: python capture.py
产物: 本目录下 *.png
"""
import json
import time
import base64
import socket
import subprocess
import urllib.request
import os
import sys

import websocket

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PORT = 9223
PROFILE = r"C:\Users\lenovo\wbshots\chrome-profile2"
OUT = os.path.dirname(os.path.abspath(__file__))
BASE = "http://127.0.0.1:3000"
ENT_ID = "4f6f0454-cb85-4c2e-a522-4476fba27d50"  # 芯动微电子 / 半导体 / 流片成功

VIEW_W = 1600


def wait_port(port, timeout=60):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=1):
                return True
        except OSError:
            time.sleep(0.5)
    return False


def get_ws_url():
    for _ in range(40):
        try:
            data = json.load(urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/list", timeout=3))
            for t in data:
                if t.get("type") == "page":
                    return t["webSocketDebuggerUrl"]
        except Exception:
            pass
        time.sleep(0.5)
    raise RuntimeError("无法获取调试目标")


class CDP:
    def __init__(self, ws_url):
        self.ws = websocket.create_connection(ws_url, timeout=120, max_size=None)
        self.mid = 0

    def call(self, method, **params):
        self.mid += 1
        self.ws.send(json.dumps({"id": self.mid, "method": method, "params": params}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == self.mid:
                if "error" in msg:
                    raise RuntimeError(f"{method}: {msg['error']}")
                return msg.get("result", {})

    def js(self, expr):
        r = self.call("Runtime.evaluate", expression=expr, returnByValue=True, awaitPromise=True)
        return r.get("result", {}).get("value")

    def wait(self, expr, timeout=30, tag=""):
        t0 = time.time()
        while time.time() - t0 < timeout:
            try:
                if self.js(expr):
                    return True
            except Exception:
                pass
            time.sleep(0.5)
        print(f"  [warn] 等待超时: {tag or expr[:40]}")
        return False

    def close(self):
        try:
            self.ws.close()
        except Exception:
            pass


def shot(cdp, name, selector, pad=0, index=0):
    """截取指定选择器的元素区域（先滚动到元素，确保已绘制）"""
    # 1. 滚动到元素并等待（触发可能的入场动画）
    cdp.js(f"""
    (() => {{
      const els = document.querySelectorAll({json.dumps(selector)});
      if (!els.length) return null;
      els[{index}].scrollIntoView({{block: 'start', behavior: 'instant'}});
      return true;
    }})()
    """)
    time.sleep(1.4)

    expr = f"""
    (() => {{
      const els = document.querySelectorAll({json.dumps(selector)});
      if (!els.length) return null;
      const el = els[{index}];
      const r = el.getBoundingClientRect();
      return {{x: r.x + window.scrollX, y: r.y + window.scrollY,
               w: r.width, h: r.height,
               text: (el.innerText || '').slice(0, 60),
               dh: document.documentElement.scrollHeight}};
    }})()
    """
    rect = cdp.js(expr)
    if not rect:
        print(f"  [miss] {name}: 未找到 {selector}")
        return None
    x = max(0, rect["x"] - pad)
    y = max(0, rect["y"] - pad)
    w = rect["w"] + pad * 2
    h = rect["h"] + pad * 2
    clip = {"x": x, "y": y, "width": w, "height": h, "scale": 1}
    r = cdp.call("Page.captureScreenshot", format="png", clip=clip, captureBeyondViewport=True)
    data = r.get("data")
    if not data:
        print(f"  [fail] {name}")
        return None
    path = os.path.join(OUT, name + ".png")
    with open(path, "wb") as f:
        f.write(base64.b64decode(data))
    txt = (rect.get("text") or "").replace("\n", " ")
    print(f"  [ok] {name}.png  {int(w)}x{int(h)}  {os.path.getsize(path)//1024}KB  | {txt[:44]}")
    return path


def open_page(cdp, url, ready_expr, tag):
    cdp.call("Page.navigate", url=url)
    time.sleep(1.2)
    cdp.wait(ready_expr, timeout=40, tag=tag)
    time.sleep(2.5)  # 给 ECharts 动画收尾
    return True


def main():
    os.makedirs(PROFILE, exist_ok=True)
    proc = subprocess.Popen(
        [CHROME, "--headless=new", f"--remote-debugging-port={PORT}",
         f"--user-data-dir={PROFILE}", "--disable-gpu", "--no-sandbox",
         "--hide-scrollbars", "--disable-extensions", "--no-first-run",
         "--remote-allow-origins=*",
         f"--window-size={VIEW_W},1000", "about:blank"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    cdp = None
    try:
        wait_port(PORT)
        cdp = CDP(get_ws_url())
        cdp.call("Page.enable")
        cdp.call("Runtime.enable")
        cdp.call("Emulation.setDeviceMetricsOverride",
                 width=VIEW_W, height=1000, deviceScaleFactor=1, mobile=False)

        # ---------- 首页 ----------
        print("首页 /")
        open_page(cdp, BASE + "/",
                  "document.querySelector('.capability-card') && document.querySelectorAll('.capability-card').length>=4",
                  "首页能力卡")
        shot(cdp, "home_hero", ".hero")
        shot(cdp, "home_capability", ".capability-section")
        shot(cdp, "home_milestone", ".milestone-section")
        shot(cdp, "home_enterprise", ".enterprise-section")

        # ---------- 数据大屏 ----------
        print("数据大屏 /dashboard")
        open_page(cdp, BASE + "/dashboard",
                  "document.querySelectorAll('canvas').length>=4", "大屏图表")
        shot(cdp, "dash_full", ".dashboard", pad=8)

        # ---------- 企业详情 ----------
        print(f"企业详情 /enterprise/{ENT_ID[:8]}")
        open_page(cdp, f"{BASE}/enterprise/{ENT_ID}",
                  "document.querySelector('[data-section=\"credit\"]') && document.querySelectorAll('canvas').length>=1",
                  "企业详情")
        shot(cdp, "detail_profile", '[data-section="profile"]', pad=6)
        shot(cdp, "detail_team", '[data-section="team"]', pad=6)
        shot(cdp, "detail_risk", '[data-section="risk"]', pad=6)
        shot(cdp, "detail_patents", '[data-section="patents"]', pad=6)
        shot(cdp, "detail_milestone", '[data-section="milestone"]', pad=6)
        shot(cdp, "detail_credit", '[data-section="credit"]', pad=6)

        # ---------- 企业列表（首页局部，用于首页说明） ----------
        print("完成")
    finally:
        if cdp:
            cdp.close()
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except Exception:
            proc.kill()


if __name__ == "__main__":
    main()
