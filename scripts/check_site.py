"""Check the built site: every internal link and anchor resolves, every image exists.

usage: python3 scripts/check_site.py [site_dir] [lectureNN]   (run after build.py;
       with a lecture name only that lecture's pages are checked)
"""
import re
import sys
from pathlib import Path

OUT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).parent.parent / "_site"
ONLY = sys.argv[2] if len(sys.argv) > 2 else ""
errors = []
ids = {}
for page in OUT.rglob("*.html"):
    ids[page] = set(re.findall(r'id="([^"]+)"', page.read_text()))

for page in OUT.rglob("*.html"):
    if ONLY and ONLY not in page.relative_to(OUT).parts:
        continue
    html = page.read_text()
    for attr, target in re.findall(r'(href|src)="([^"]+)"', html):
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        path, _, anchor = target.partition("#")
        dest = (page.parent / path).resolve() if path else page
        if not dest.exists():
            errors.append(f"{page.relative_to(OUT)}: missing file {target}")
        elif anchor and dest.suffix == ".html" and anchor not in ids.get(dest, set()):
            errors.append(f"{page.relative_to(OUT)}: missing anchor {target}")
    if "<!--" in html or "{{" in html:
        errors.append(f"{page.relative_to(OUT)}: leftover placeholder")

print("\n".join(errors) or f"ok: {len(ids)} pages checked")
sys.exit(1 if errors else 0)
