"""Build the CS329Z study notes site into _site/.

Layout:
  course.json                         course home page: modules and lectures
  lectures/lectureNN/lecture.json     nav and page headers of one lecture
  lectures/lectureNN/content/*.html   page bodies
  lectures/lectureNN/img/pNN.jpg      slide images used by the pages
  assets/                             shared style and script

Content shortcuts:
  <section class="sec" id="x" data-p="7-15">   shows "讲义第 7 至 15 页" beside the heading
  {{slide 13 | caption}} or {{slides 18 19 | caption}}   inserts the slide images from img/,
                                                         caption prefixed with the slide numbers
  {{fig 13 | caption}} or {{figs 18 19 | caption}}       same images, caption shown as written
"""
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "_site"
SITE_NAME = "CS329Z 中文学习笔记"

SEC_RE = re.compile(r'<section class="sec" id="([\w-]+)"((?: data-p="[\d-]+")?)>\s*<h2>(.*?)</h2>', re.S)
SLIDE_RE = re.compile(r"\{\{(slides?|figs?) ([\d ]+)\|(.*?)\}\}", re.S)


def strip_tags(html):
    return re.sub("<.*?>", "", html)


def add_section_heads(content):
    """Wrap each h2 in a heading row; show the slide range when the section has one."""
    def repl(m):
        sid, attrs, title = m[1], m[2], m[3]
        badge = ""
        pages = re.findall(r"\d+", attrs)
        if len(pages) == 2:
            badge = f'<span class="time">讲义第 {pages[0]} 至 {pages[1]} 页</span>'
        elif len(pages) == 1:
            badge = f'<span class="time">讲义第 {pages[0]} 页</span>'
        return f'<section class="sec" id="{sid}"{attrs}>\n  <div class="sec-head"><h2>{title}</h2>{badge}</div>'
    return SEC_RE.sub(repl, content)


def expand_slides(content, img_dir):
    """Replace {{slide N | caption}} with a figure showing the slide images."""
    def repl(m):
        plain = m[1].startswith("fig")
        nums = [int(n) for n in m[2].split()]
        for n in nums:
            if not (img_dir / f"p{n:02d}.jpg").exists():
                raise SystemExit(f"missing image {img_dir}/p{n:02d}.jpg")
        alt = "配图" if plain else "讲义原图"
        imgs = "".join(f'<a href="img/p{n:02d}.jpg" target="_blank" rel="noopener">'
                       f'<img src="img/p{n:02d}.jpg" alt="{alt}" loading="lazy" width="1600" height="900"></a>'
                       for n in nums)
        cls = "slides slides-2" if len(nums) > 1 else "slides"
        pages = "、".join(str(n) for n in nums)
        prefix = "" if plain else f"讲义第 {pages} 页。"
        return (f'<figure class="plate"><div class="{cls}">{imgs}</div>'
                f'<figcaption>{prefix}{m[3].strip()}</figcaption></figure>')
    return SLIDE_RE.sub(repl, content)


TABLE_RE = re.compile(r'<table class="tbl">.*?</table>', re.S)


CELL_RE = re.compile(r"<(td|th)([^>]*)>(.*?)</\1>", re.S)


def label_cells(content):
    """Give every body cell its column header as data-label, so phones can show each row as a card.

    A cell merged across several rows is repeated in the later rows as a hidden copy (class rs-copy),
    which only phones display, so every card is complete. A cell merged across columns gets no label.
    Tables whose header has more than one row or merged cells keep the grid and scroll sideways.
    """
    def table(m):
        html = m[0]
        head = re.search(r"<thead>(.*?)</thead>", html, re.S)
        if not head:
            return html
        if head[1].count("<tr") > 1 or "span=" in head[1]:
            return html.replace('<table class="tbl">', '<table class="tbl tbl-scroll">', 1)
        labels = [strip_tags(re.sub(r"<span.*?</span>", "", c, flags=re.S)).strip()
                  for c in re.findall(r"<th[^>]*>(.*?)</th>", head[1], re.S)]
        pending = {}  # column index -> [rows left, copy of the merged cell]

        def copies(col, out):
            while col in pending:
                out.append(pending[col][1])
                pending[col][0] -= 1
                if not pending[col][0]:
                    del pending[col]
                col += 1
            return col

        def row(r):
            out, col = [], 0
            for tag, attrs, inner in CELL_RE.findall(r[2]):
                col = copies(col, out)
                label = labels[col] if col < len(labels) else ""
                colspan = int((re.search(r'colspan="(\d+)"', attrs) or [0, 1])[1])
                rowspan = int((re.search(r'rowspan="(\d+)"', attrs) or [0, 1])[1])
                data = f' data-label="{label}"' if label and colspan == 1 else ""
                out.append(f"<{tag}{attrs}{data}>{inner}</{tag}>")
                if rowspan > 1:
                    pending[col] = [rowspan - 1, f'<td class="rs-copy"{data}>{inner}</td>']
                col += colspan
            copies(col, out)
            return f"<tr{r[1]}>{''.join(out)}</tr>"
        body = re.sub(r"<tr([^>]*)>(.*?)</tr>", lambda r: row((r[0], r[1], r[2])), html[head.end():], flags=re.S)
        return html[:head.end()] + body
    return TABLE_RE.sub(table, content)


def topbar(brand, nav, current, home):
    links = [f'<a href="{home}">课程目录</a>'] if home else []
    for slug, label in nav:
        current_attr = ' aria-current="page"' if slug == current else ""
        links.append(f'<a href="{slug}.html"{current_attr}>{label}</a>')
    return ('<header class="topbar"><div class="topbar-in">'
            f'<a class="brand" href="index.html">{brand}</a>'
            f'<nav class="modnav" aria-label="页面导航">{"".join(links)}</nav></div></header>')


def hero(meta):
    chips = "".join(f'<span class="chip" style="--c:var({c})"><span class="dot"></span>{n}</span>'
                    for n, c in meta.get("chips", []))
    chips_html = f'<div class="chips">{chips}</div>' if chips else ""
    return (f'<div class="hero"><div class="hero-eyebrow">{meta["eyebrow"]}</div>'
            f'<h1>{meta["title"]}</h1><p class="lede">{meta["lede"]}</p>{chips_html}</div>')


def html_page(title, assets, body):
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="{assets}/style.css">
</head>
<body class="layout-single">
{body}
<script src="{assets}/app.js"></script>
</body>
</html>
"""


def build_lecture(src):
    """Build every page of one lecture folder into _site/<folder name>/."""
    meta = json.loads((src / "lecture.json").read_text())
    out = OUT / src.name
    out.mkdir(parents=True)
    if (src / "img").exists():
        shutil.copytree(src / "img", out / "img")
    for slug, page in meta["pages"].items():
        raw = (src / "content" / f"{slug}.html").read_text()
        content = label_cells(expand_slides(add_section_heads(raw), src / "img"))
        if meta.get("credit"):
            content += f'\n<p class="muted small credit">{meta["credit"]}</p>'
        toc = "".join(f'<li><a href="#{m[1]}"><span>{strip_tags(m[3])}</span></a></li>' for m in SEC_RE.finditer(raw))
        body = (f'{topbar(meta["brand"], meta["nav"], slug, "../index.html")}\n{hero(page)}\n'
                f'<div class="wrap"><nav class="toc" aria-label="本页目录"><div class="toc-title">本页内容</div><ol>{toc}</ol></nav>\n'
                f'<main>{content}</main></div>')
        (out / f"{slug}.html").write_text(html_page(f'{strip_tags(page["title"])} · {meta["brand"]}', "../assets", body))
    print("built", src.name, len(meta["pages"]), "pages")


def build_home():
    """Build the course home page: one list of lectures per module."""
    course = json.loads((ROOT / "course.json").read_text())
    secs = []
    for i, mod in enumerate(course["modules"], 1):
        rows = []
        for lec in mod["lectures"]:
            links = f'<a href="{lec["slides"]}">课程 PDF</a>'
            if lec.get("video"):
                links += f'，<a href="{lec["video"]}">课程视频</a>'
            text = f'<b>{lec["title"]}</b><p>{lec["summary"]}</p><p class="small">原始材料：{links}</p>'
            label = f'第 {lec["n"]} 讲 · {lec["date"]}'
            if lec.get("dir"):
                state = f'<a class="dur go" href="{lec["dir"]}/index.html">读笔记</a>'
            else:
                state = '<span class="dur">待整理</span>'
            rows.append(f'<div class="lec"><span class="m">{label}</span><span>{text}</span>{state}</div>')
        secs.append(f'<section class="sec" id="m{i}">\n  <div class="sec-head"><h2>{mod["name"]}</h2></div>\n'
                    f'  <div class="leclist">{"".join(rows)}</div>\n</section>')
    toc = "".join(f'<li><a href="#m{i}"><span>{mod["name"]}</span></a></li>' for i, mod in enumerate(course["modules"], 1))
    body = (f'{topbar(SITE_NAME, [], "", "")}\n{hero(course["hero"])}\n'
            f'<div class="wrap"><nav class="toc" aria-label="本页目录"><div class="toc-title">课程的各部分</div><ol>{toc}</ol></nav>\n'
            f'<main>{"".join(secs)}\n{course["footer"]}</main></div>')
    (OUT / "index.html").write_text(html_page(SITE_NAME, "assets", body))
    print("built home")


if __name__ == "__main__":
    # usage: build.py [--out DIR] [lectureNN ...]   (no lecture names: build all)
    args = sys.argv[1:]
    if args[:1] == ["--out"]:
        OUT = Path(args[1]).resolve()
        args = args[2:]
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    shutil.copytree(ROOT / "assets", OUT / "assets")
    build_home()
    for src in sorted((ROOT / "lectures").iterdir()):
        if (not args or src.name in args) and (src / "lecture.json").exists():
            build_lecture(src)
