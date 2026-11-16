"""Render each PDF page to a JPEG and dump the page text.

usage: pdf_extract.py <pdf> <out_dir>
"""
import sys
from pathlib import Path
import fitz

pdf, out = Path(sys.argv[1]), Path(sys.argv[2])
(out / "pages").mkdir(parents=True, exist_ok=True)
doc = fitz.open(pdf)
texts = []
for i, page in enumerate(doc, 1):
    pix = page.get_pixmap(matrix=fitz.Matrix(1600 / page.rect.width, 1600 / page.rect.width))
    pix.save(out / "pages" / f"p{i:02d}.jpg", jpg_quality=82)
    links = [l["uri"] for l in page.get_links() if l.get("uri")]
    texts.append(f"===== page {i} =====\n{page.get_text().strip()}\n" + ("".join(f"[link] {u}\n" for u in links)))
(out / "slides.txt").write_text("\n".join(texts))
print(len(doc), "pages", doc[0].rect)
