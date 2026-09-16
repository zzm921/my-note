# -*- coding: utf-8 -*-
"""
为 rag / ml 分区「已存在但缺 id 映射」的笔记补 publish 声明。

背景：
  这两个分区的笔记内容早已在库里，但文件名与站点卡片 id 不一致，
  且没有 publish 声明，导致同步链路认不出对应关系。
  本脚本只在 frontmatter 里补三行：
      publish: true
      site: <分区>
      cardId: <卡片 id>
  **不碰正文、不改 tags、不引入 site_meta**（正文与站点卡片各自维护）。

映射依据（逐条人工核对）：
  rag 分区 13 张 → 10-AI/rag/ 下对应笔记
  ml  分区  4 张 → 10-AI/ml/ 下对应笔记

默认 dry-run，--apply 才写入。
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
apply = "--apply" in sys.argv

# 卡片 id -> 笔记相对路径
MAP = {
    # ---- rag 分区 ----
    "rag": "10-AI/rag/01-RAG概念与演进.md",
    "naive-rag": "10-AI/rag/02-NaiveRAG朴素RAG.md",
    "advanced-rag": "10-AI/rag/03-AdvancedRAG进阶RAG.md",
    "modular-rag": "10-AI/rag/04-ModularRAG模块化RAG.md",
    "graph-rag": "10-AI/rag/05-GraphRAG图谱增强.md",
    "agentic-rag": "10-AI/rag/RAG总览.md",
    "rag-variants": "10-AI/rag/advanced-rag-碎片.md",
    "rag-eval": "10-AI/rag/RAG评估.md",
    # ---- ml 分区 ----
    "ml-intro": "10-AI/ml/1_机器学习导论.md",
    "ml-linear-regression": "10-AI/ml/2_线性回归模型.md",
    "ml-gradient-descent": "10-AI/ml/3_梯度下降.md",
    "ml-classification-logistic-regression": "10-AI/ml/4_分类与逻辑回归.md",
}

# 这些卡片在站点没有对应笔记，需要标注「待补」
TODO = {
    "offline-processing": "站点有卡、笔记库无对应笔记",
    "online-hybrid-retrieval": "站点有卡、笔记库无对应笔记",
    "kb-routing": "站点有卡、笔记库无对应笔记",
    "text-to-sql": "站点有卡、笔记库无对应笔记",
    "rag-online-eval": "已作为 eval 分区卡片认领（site: eval）",
}

SITE_OF = lambda cid: "ml" if cid.startswith("ml-") else "rag"


def add_publish(p: pathlib.Path, cid: str):
    t = p.read_text(encoding="utf-8")
    if not t.lstrip().startswith("---"):
        print(f"  !! 无 frontmatter：{p.as_posix()}")
        return None
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", t, re.S)
    fm = m.group(1)
    body = t[m.end():]

    if f"cardId: {cid}" in fm:
        print(f"  -- 已有映射，跳过：{p.as_posix()}")
        return None
    if "publish: true" in fm:
        print(f"  !! 已有其它 publish 声明，跳过：{p.as_posix()}")
        return None

    site = SITE_OF(cid)
    new_fm = fm.rstrip("\n") + f"\n\npublish: true\nsite: {site}\ncardId: {cid}"
    return "---\n" + new_fm + "\n---\n" + body


n = 0
print("=" * 66)
print("补 publish 声明")
print("=" * 66)
for cid, rel in sorted(MAP.items()):
    p = ROOT / rel
    if not p.exists():
        print(f"  !! 笔记不存在：[{cid}] → {rel}")
        continue
    r = add_publish(p, cid)
    if r is None:
        continue
    print(f"  {cid:40s} ← {rel}")
    if apply:
        p.write_text(r, encoding="utf-8", newline="\n")
    n += 1

print()
print("=" * 66)
print("站点有卡但笔记库暂无对应笔记（需另行补写）")
print("=" * 66)
for cid, why in sorted(TODO.items()):
    print(f"  {cid:28s} {why}")

print()
print(f"{'✓ 已补' if apply else '将补'} {n} 篇")
if not apply:
    print("(dry-run) 加 --apply")
