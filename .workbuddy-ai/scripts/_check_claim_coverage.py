# -*- coding: utf-8 -*-
"""核对站点 7 分区与笔记库的对应完整性。"""
import pathlib
import re

SITE = pathlib.Path(r"D:\workspace\my-agent-lab\backend\content")
NOTE = pathlib.Path(r"D:\workspace\my-note")

# 站点 tags.md 中每个分区声明的卡片
tags_md = (SITE / "tags.md").read_text(encoding="utf-8")
sections = {}
cur = None
for line in tags_md.splitlines():
    m = re.match(r"\s*-\s*id:\s*(\S+)", line)
    if m:
        cur = m.group(1)
        sections[cur] = []
        continue
    m = re.match(r"\s*-\s*id:\s*(\S+)", line)
    if cur and "cards:" in line:
        inner = line.split("cards:", 1)[1].strip()
        if inner.startswith("["):
            sections[cur] = [x.strip() for x in inner.strip("[]").split(",") if x.strip()]
        continue

print("站点分区声明：")
for k, v in sections.items():
    print(f"  {k:22s} {len(v):2d} 张")

# 笔记库认领的卡片（看 publish 声明）
claimed = {}
for p in NOTE.rglob("*.md"):
    if set(p.parts) & {".git", ".obsidian", ".workbuddy-ai", ".idea", "99-Archive"}:
        continue
    t = p.read_text(encoding="utf-8", errors="replace")
    if "publish: true" not in t:
        continue
    m = re.search(r"^site:\s*(\S+)", t, re.M)
    c = re.search(r"^cardId:\s*(\S+)", t, re.M)
    if m and c:
        claimed.setdefault(m.group(1), []).append(c.group(1))

print("\n笔记库已认领：")
for k in sections:
    got = claimed.get(k, [])
    print(f"  {k:22s} {len(got):2d} 篇  {sorted(got)}")

# 差集
print("\n未认领的卡片：")
all_claimed = {c for v in claimed.values() for c in v}
for k, cards in sections.items():
    miss = [c for c in cards if c not in all_claimed]
    if miss:
        print(f"  {k:22s} {miss}")
if not any(c not in all_claimed for v in sections.values() for c in v):
    print("  （无，全部已认领）")
