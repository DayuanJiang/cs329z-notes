"""Turn a WebVTT caption file into plain text with a time mark every half minute.

usage: python3 scripts/vtt_to_text.py <captions.vtt> <out.txt>
"""
import re
import sys
from pathlib import Path

lines, last_mark, prev = [], -30, ""
start = 0
for raw in Path(sys.argv[1]).read_text().splitlines():
    m = re.match(r"(\d+):(\d+):(\d+)\.\d+ --> ", raw)
    if m:
        start = int(m[1]) * 3600 + int(m[2]) * 60 + int(m[3])
        continue
    text = re.sub(r"<[^>]+>", "", raw).strip()
    if not text or text == "WEBVTT" or text.startswith(("Kind:", "Language:")) or text == prev:
        continue
    prev = text
    if start - last_mark >= 30:
        lines.append(f"\n[{start // 60:02d}:{start % 60:02d}]")
        last_mark = start
    lines.append(text)
Path(sys.argv[2]).write_text(" ".join(lines).replace(" \n", "\n").strip() + "\n")
print(len(lines), "lines")
