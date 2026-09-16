# -*- coding: utf-8 -*-
"""孤岛笔记诊断 —— 找出零入链且零出链的笔记。

判定口径：
  - 出链：该笔记正文里有没有 [[...]] 指向别处
  - 入链：全库有没有别的笔记 [[...]] 指向它
  - 孤岛 = 出链 0 且 入链 0（在 Obsidian 图谱上是一个游离的点）

分类统计，并排除：
  - 归档区（99-Archive 本来就是留档，孤立是正常的）
  - 模板（_Templates 含占位符链接）
  - 日报（90-Daily 靠文件名做时序检索，规范里就允许无链接）
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]

# 不参与孤岛判定的目录（孤立属正常）
EXEMPT_TOP = {"99-Archive", "_Templates", "90-Daily", ".obsidian", ".git", ".workbuddy-ai"}

PLACEHOLDER = {
    "创建链接", "双链", "笔记名", "X", "笔记", "笔记1", "笔记2",
    "runners", "文件名.png", "...", "test",
}


def md_files():
    for p in ROOT.rglob("*.md"):
        parts = p.parts
        if any(x in parts for x in (".git", ".obsidian", ".workbuddy-ai")):
            continue
        yield p


def top_dir(p: Path) -> str:
    """取相对 ROOT 的顶层目录名。

    注意：p.parts 对于绝对路径会包含盘符（如 'D:\\'），
    必须先 relative_to(ROOT)，否则豁免规则会静默失效。
    """
    rel = p.relative_to(ROOT)
    return rel.parts[0] if len(rel.parts) > 1 else "(根)"


def parse_links(text: str):
    """返回 (目标列表, 是否用了 embed)"""
    out = []
    for m in re.finditer(r"(!?)\[\[([^\]\n]+?)\]\]", text):
        inner = m.group(2)
        tgt = re.split(r"\\?\|", inner, maxsplit=1)[0].strip().lstrip("/")
        if not tgt:
            continue
        name = tgt.split("/")[-1]
        if name in PLACEHOLDER:
            continue
        out.append(name)
    return out


def main() -> None:
    files = list(md_files())

    # 建索引：stem → 路径
    stems = {}
    for p in files:
        stems.setdefault(p.stem, []).append(p.relative_to(ROOT).as_posix())

    out_links = {}     # stem → set(目标 stem)
    in_count = {}      # stem → 入链数

    for p in files:
        text = p.read_text(encoding="utf-8", errors="ignore")
        # 剥掉 frontmatter，避免把 tags 里的词当链接
        text = re.sub(r"^---\r?\n.*?\r?\n---\r?\n", "", text, count=1, flags=re.S)
        tgts = parse_links(text)
        out_links[p.stem] = set(tgts)
        for t in tgts:
            in_count[t] = in_count.get(t, 0) + 1

    # 统计
    cats = {}
    islands = []

    for p in files:
        rel = p.relative_to(ROOT).as_posix()
        top = top_dir(p)
        exempt = top in EXEMPT_TOP

        o = len(out_links.get(p.stem, ()))
        i = in_count.get(p.stem, 0)

        cats.setdefault(top, {"总": 0, "孤立": 0})["总"] += 1
        if o == 0 and i == 0:
            cats[top]["孤立"] += 1
            islands.append({
                "path": rel,
                "top": top,
                "size": p.stat().st_size,
                "exempt": exempt,
            })

    print("=" * 72)
    print("孤岛笔记诊断")
    print("=" * 72)
    print(f"全库 md：{len(files)} 篇")
    print(f"孤岛（零入链 + 零出链）：{len(islands)} 篇")
    print()

    print("按目录分布：")
    print(f"  {'目录':<16}{'总数':>6}{'孤立':>6}{'占比':>9}   ")
    for k, v in sorted(cats.items(), key=lambda x: -x[1]["孤立"]):
        ratio = v["孤立"] / v["总"] * 100 if v["总"] else 0
        flag = "  ← 豁免" if k in EXEMPT_TOP else ""
        print(f"  {k:<16}{v['总']:>6}{v['孤立']:>6}{ratio:>8.0f}%{flag}")

    real = [x for x in islands if not x["exempt"]]
    print()
    print(f"其中**需要处理**的（排除归档/模板/日报）：{len(real)} 篇")
    for x in sorted(real, key=lambda y: -y["size"]):
        print(f"  {x['size']:>7,} B  {x['path']}")

    # 存一份 JSON 供后续使用
    out = ROOT / ".workbuddy-ai" / "scripts" / "_islands.json"
    out.write_text(json.dumps(islands, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n明细已写入 {out.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
