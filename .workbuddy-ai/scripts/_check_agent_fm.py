# -*- coding: utf-8 -*-
"""检查 10-AI/agent 认领笔记的 frontmatter 结构。"""
import pathlib
import re
from collections import Counter

for p in sorted(pathlib.Path("10-AI/agent").glob("*.md")):
    t = p.read_text(encoding="utf-8")
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", t, re.S)
    if not m:
        print(f"  无 frontmatter: {p.name}")
        continue
    fm = m.group(1)
    top = [l.split(":", 1)[0] for l in fm.splitlines()
           if l and not l.startswith((" ", "-", "#")) and ":" in l]
    dups = {k: v for k, v in Counter(top).items() if v > 1}
    has_meta = "site_meta:" in fm
    print(f"  {p.name:26s} site_meta={'Y' if has_meta else 'N'}  dups={dups or '-'}")
