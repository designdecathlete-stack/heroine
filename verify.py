from playwright.sync_api import sync_playwright
import os

target_html = r"c:\Users\kanat\Desktop\dec-athlete\reproduction\heroinepilates-mens\index.html"
out_dir = r"c:\Users\kanat\Desktop\dec-athlete\reproduction\heroinepilates-mens\verify_shots"
os.makedirs(out_dir, exist_ok=True)
url = "file:///" + target_html.replace("\\", "/")

with sync_playwright() as p:
    browser = p.chromium.launch()
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()
    page.goto(url, wait_until="load")
    page.wait_for_timeout(2000)
    total = page.evaluate("() => document.body.scrollHeight")
    vh = 800
    y = 0; i = 1
    while y < total:
        page.evaluate(f"window.scrollTo(0, {y})")
        page.wait_for_timeout(400)
        page.screenshot(path=os.path.join(out_dir, f"{i:02d}.png"), clip={"x": 0, "y": 0, "width": 1280, "height": 800})
        y += vh; i += 1
    print("done, total:", total)
    browser.close()
