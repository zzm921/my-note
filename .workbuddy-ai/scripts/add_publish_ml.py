# -*- coding: utf-8 -*-
"""
ml 分区：为已有笔记补 publish 映射（笔记为源）。
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
apply = "--apply" in sys.argv

MAP = {
    "ml-intro": "10-AI/ml/1_机器学习导论.md",
    "ml-linear-regression": "10-AI/ml/2_线性回归模型.md",
    "ml-gradient-descent": "10-AI/ml/3_梯度下降.md",
    "ml-classification-logistic-regression": "10-AI/ml/4_分类与逻辑回归.md",
}

n = 0
for cid, rel in sorted(MAP.items()):
    p = ROOT / rel
    if not p.exists():
        print(f"  !! 笔记不存在：[{cid}] {rel}")
        continue
    t = p.read_text(encoding="utf-8")
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", t, re.S)
    if not m:
        print(f"  !! 无 frontmatter：{rel}")
        continue
    fm, body = m.group(1), t[m.end():]
    if f"cardId: {cid}" in fm:
        print(f"  -- 已有映射，跳过：{rel}")
        continue
    if "publish: true" in fm:
        print(f"  !! 已存在其它 publish，跳过：{rel}")
        continue
    new_fm = fm.rstrip("\n") + f"\n\npublish: true\nsite: ml\ncardId: {cid}"
    print(f"  {cid:40s} ← {rel}")
    if apply:
        p.write_text("---\n" + new_fm + "\n---\n" + body, encoding="utf-8", newline="\n")
    n += 1

print()
print(f"{'✓ 已补' if apply else '将补'} {n} 篇")
if not apply:
    print("(dry-run) 加 --apply")
