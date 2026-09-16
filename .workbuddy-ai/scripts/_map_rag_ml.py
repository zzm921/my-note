# -*- coding: utf-8 -*-
"""
核对 rag / ml 分区卡片与笔记库笔记的对应关系（只读，供人工确认）。
"""
import pathlib
import re

SITE = pathlib.Path(r"D:\workspace\my-agent-lab\backend\content")
NOTE = pathlib.Path(r"D:\workspace\my-note")


def card_name(cid):
    t = (SITE / f"{cid}.md").read_text(encoding="utf-8")
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", t, re.S)
    for l in m.group(1).splitlines():
        if l.startswith("name:"):
            return l.split(":", 1)[1].strip()
    return ""


print("=" * 70)
print("rag 分区：站点卡片 id  vs  笔记库文件")
print("=" * 70)
RAG = ["rag", "naive-rag", "advanced-rag", "modular-rag", "graph-rag", "agentic-rag",
       "rag-variants", "offline-processing", "online-hybrid-retrieval", "kb-routing",
       "text-to-sql", "rag-eval", "rag-online-eval"]
for c in RAG:
    print(f"\n卡 {c:26s} ({card_name(c)})")
    for p in sorted((NOTE / "10-AI/rag").glob("*.md")):
        t = p.read_text(encoding="utf-8", errors="replace")
        has_pub = "publish: true" in t
        cid = ""
        m = re.search(r"^cardId:\s*(\S+)", t, re.M)
        if m:
            cid = m.group(1)
        mark = "★已认领" if cid == c else ""
        print(f"    {p.name:44s} {mark}")

print()
print("=" * 70)
print("ml 分区：站点卡片 id  vs  笔记库文件")
print("=" * 70)
ML = ["ml-intro", "ml-linear-regression", "ml-gradient-descent",
      "ml-classification-logistic-regression"]
for c in ML:
    print(f"\n卡 {c:36s} ({card_name(c)})")
    for p in sorted((NOTE / "10-AI/ml").glob("*.md")):
        t = p.read_text(encoding="utf-8", errors="replace")
        cid = ""
        m = re.search(r"^cardId:\s*(\S+)", t, re.M)
        if m:
            cid = m.group(1)
        mark = "★已认领" if cid == c else ""
        print(f"    {p.name:44s} {mark}")
