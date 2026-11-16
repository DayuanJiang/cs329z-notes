"""Check the wording rules in one lecture's pages.

usage: python3 scripts/check_text.py lectureNN

The body must read like a textbook: it never mentions the source slides, never uses a dash as
punctuation, never uses the forced contrast "不是……而是……", and has no author markers.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
lecture = ROOT / "lectures" / sys.argv[1]
RULES = [
    (r"讲义|幻灯片|讲者|课堂|演讲者|授课", "mentions the source lecture"),
    (r"\{\{slides?\b|data-p=", "old slide shortcut or page badge"),
    (r"——|—|–", "dash used as punctuation"),
    (r"→|⇒|->", "arrow instead of a sentence"),
    (r"而不是|不是[^。；，！？<]{0,40}而是|并非", "forced contrast"),
    (r"我的|我加|我认为|我对|我按|我做|我整理|我们认为|笔者|整理者", "author marker"),
    (r"拉扯|落点|使劲|阴暗|抓手|赋能|闭环|打通", "metaphor or jargon"),
]
errors = 0
files = sorted((lecture / "content").glob("*.html")) + [lecture / "lecture.json"]
for path in files:
    for no, line in enumerate(path.read_text().splitlines(), 1):
        text = re.sub(r'href="[^"]*"', "", line)
        for pattern, why in RULES:
            for m in re.finditer(pattern, text):
                errors += 1
                start = max(0, m.start() - 20)
                print(f"{path.name}:{no}: {why}: …{text[start:m.end() + 20]}…")
print("ok" if not errors else f"{errors} problems")
sys.exit(1 if errors else 0)
