# -*- coding: utf-8 -*-
"""评估 rag/ml 笔记与站点卡片的内容匹配度（只读）。"""
import pathlib
import re

SITE = pathlib.Path(r"D:\workspace\my-agent-lab\backend\content")
NOTE = pathlib.Path(r"D:\workspace\my-note")


def first_h(text):
    for l in text.splitlines():
        if l.startswith("#"):
            return l.lstrip("#").strip()
    return ""


def card_meta(cid):
    t = (SITE / f"{cid}.md").read_text(encoding="utf-8")
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", t, re.S)
    nm = sd = ""
    for l in m.group(1).splitlines():
        if l.startswith("name:"):
            nm = l.split(":", 1)[1].strip()
        if l.startswith("shortDesc:"):
            sd = l.split(":", 1)[1].strip()
    body = t[m.end():]
    h2 = re.findall(r"^##\s+(.+)$", body, re.M)
    return nm, sd, h2, len(t.encode("utf-8"))


RAG_CARDS = ["rag", "naive-rag", "advanced-rag", "modular-rag", "graph-rag", "agentic-rag",
             "rag-variants", "offline-processing", "online-hybrid-retrieval", "kb-routing",
             "text-to-sql"]
ML_CARDS = ["ml-intro", "ml-linear-regression", "ml-gradient-descent",
            "ml-classification-logistic-regression"]

print("#" * 72)
print("# 站点 rag / ml 卡片的内容骨架")
print("#" * 72)
for c in RAG_CARDS + ML_CARDS:
    nm, sd, h2, sz = card_meta(c)
    print(f"\n[{c}] {nm}  ({sz}B)")
    print(f"  {sd[:70]}")
    print(f"  章节: {' / '.join(h2[:8])}")

print()
print("#" * 72)
print("# 笔记库 rag / ml 笔记的实际内容")
print("#" * 72)
for sub in ["10-AI/rag", "10-AI/ml"]:
    print(f"\n--- {sub} ---")
    for p in sorted((NOTE / sub).glob("*.md")):
        t = p.read_text(encoding="utf-8", errors="replace")
        m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", t, re.S)
        body = t[m.end():] if m else t
        h2 = re.findall(r"^##\s+(.+)$", body, re.M)
        print(f"  {p.name:42s} {len(t.encode('utf-8')):6d}B  首行={first_h(body)[:26]:28s} 章节数={len(h2)}")
