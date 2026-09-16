# -*- coding: utf-8 -*-
"""给 ML 九篇加「上一篇/下一篇」导航块，并把地图的 md 链接改为 wiki 链接。

图谱收益：九篇原本各自孤立，加上导航后连成一条路径，
并被 [[机器学习-地图]] 统一索引。
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]
ML = ROOT / "10-AI" / "ml"

# 学习路径顺序（按课程）
ORDER = [
    ("1_机器学习导论", "机器学习导论", "课程 1 · 第 1 周"),
    ("2_线性回归模型", "线性回归模型", "课程 1 · 第 1 周"),
    ("3_梯度下降", "梯度下降", "课程 1 · 第 1-2 周"),
    ("4_分类与逻辑回归", "分类与逻辑回归", "课程 1 · 第 3 周"),
    ("5_神经网络", "神经网络", "课程 2 · 第 1-2 周"),
    ("6_模型评估与调优", "模型评估与调优", "课程 2 · 第 3 周"),
    ("7_决策树", "决策树", "课程 2 · 第 4 周"),
    ("8_非监督学习", "非监督学习", "课程 3 · 第 1 周"),
    ("9_推荐系统", "推荐系统", "课程 3 · 第 2 周"),
    ("10_强化学习", "强化学习", "课程 3 · 第 3 周"),
]

MARK = "<!-- ml-nav -->"


def nav_block(idx: int) -> str:
    stem, title, week = ORDER[idx]
    prev_ = ORDER[idx - 1] if idx > 0 else None
    next_ = ORDER[idx + 1] if idx < len(ORDER) - 1 else None

    lines = ["", "---", "", "## 导航", ""]
    if prev_:
        lines.append(f"- ← 上一篇：[[{prev_[0]}|{prev_[1]}]]")
    else:
        lines.append("- ← 上一篇：（已是第一篇）")
    lines.append("- 索引：[[机器学习-地图]]")
    if next_:
        lines.append(f"- 下一篇 → [[{next_[0]}|{next_[1]}]]")
    else:
        lines.append("- 下一篇 →（已是最后一篇）")
    lines.append("")
    lines.append(f"> {week}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    apply = "--apply" in sys.argv
    changed = []

    for i, (stem, title, week) in enumerate(ORDER):
        p = ML / f"{stem}.md"
        if not p.exists():
            print(f"  ! 缺失 {stem}.md")
            continue
        t = p.read_text(encoding="utf-8")
        if MARK in t:
            print(f"  - 已处理 {stem}")
            continue
        new = t.rstrip("\n") + "\n" + nav_block(i) + MARK + "\n"
        if apply:
            p.write_text(new, encoding="utf-8", newline="\n")
        changed.append(stem)
        print(f"  ✓ {stem}  加导航（{week}）")

    # 地图：md 链接 → wiki 链接
    mp = ML / "机器学习-地图.md"
    mt = mp.read_text(encoding="utf-8")
    orig = mt
    for stem, title, week in ORDER:
        mt = mt.replace(f"[{title}]({stem}.md)", f"[[{stem}|{title}]]")
    if mt != orig:
        if apply:
            mp.write_text(mt, encoding="utf-8", newline="\n")
        print(f"  ✓ 机器学习-地图.md  链接改为 wiki 形态")

    print()
    print(f"{'✓ 已处理' if apply else '将处理'} {len(changed)} 篇")
    if not apply:
        print("(dry-run) 加 --apply")


if __name__ == "__main__":
    main()
