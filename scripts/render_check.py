"""Open built pages in headless Chromium and report script errors, broken images and overflow.

usage: uv run --with playwright python scripts/render_check.py <site_dir> <lectureNN> [screenshot_dir]

Checks every page of the lecture at desktop (1440 px) and phone (390 px) width.
With a screenshot folder, saves a full-page PNG of each page at desktop width.
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

site = Path(sys.argv[1]).resolve()
lecture = sys.argv[2]
shots = Path(sys.argv[3]) if len(sys.argv) > 3 else None
if shots:
    shots.mkdir(parents=True, exist_ok=True)
problems = 0
with sync_playwright() as p:
    browser = p.chromium.launch()
    for width in (1440, 390):
        ctx = browser.new_context(viewport={"width": width, "height": 900})
        for path in sorted((site / lecture).glob("*.html")):
            page = ctx.new_page()
            errs = []
            page.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
            page.on("pageerror", lambda e: errs.append(str(e)))
            page.goto(f"file://{path}")
            page.wait_for_load_state("networkidle")
            page.evaluate("document.querySelectorAll('img').forEach(i => i.loading = 'eager')")
            page.wait_for_timeout(500)
            info = page.evaluate("""() => {
              const broken = [...document.images].filter(i => i.complete && !i.naturalWidth).map(i => i.src);
              const spill = [...document.querySelectorAll('.plate')].flatMap(pl => {
                const r = pl.getBoundingClientRect().right;
                return [...pl.querySelectorAll('table, img, pre, .bars')]
                  .filter(e => getComputedStyle(e).overflowX !== 'auto' && e.getBoundingClientRect().right > r - 10)
                  .map(e => e.tagName + ' +' + Math.round(e.getBoundingClientRect().right - r) + 'px');
              });
              const sideways = document.documentElement.scrollWidth > document.documentElement.clientWidth + 1;
              return {broken, spill, sideways};
            }""")
            bad = errs or info["broken"] or info["spill"] or info["sideways"]
            if bad:
                problems += 1
                print(f"{path.name} at {width}px: errors={errs} broken={info['broken']} "
                      f"overflow={info['spill']} page_scrolls_sideways={info['sideways']}")
            if shots and width == 1440:
                page.screenshot(path=shots / f"{path.stem}.png", full_page=True)
            page.close()
        ctx.close()
    browser.close()
print("ok" if not problems else f"{problems} pages with problems")
sys.exit(1 if problems else 0)
