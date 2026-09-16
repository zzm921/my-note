# -*- coding: utf-8 -*-
"""给诗词项目 5 篇加导航块，接回项目索引与项目实践地图。"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / "80-Projects" / "诗词KG-RAG_Agent方案"
MARK = "<!-- poetry-nav -->"

DOCS = [
    ("项目需求与技术计划", "需求"),
    ("诗词KG-RAG_Agent方案", "方案"),
    ("诗词AI-Agent技术设计方案", "设计"),
    ("搜韵API分析", "API 调研"),
    ("搜韵API实测分析", "API 实测"),
]


def main() -> None:
    apply = "--apply" in sys.argv
    n = 0
    for stem, kind in DOCS:
        p = DIR / f"{stem}.md"
        if not p.exists():
            print(f"  ! 缺失 {stem}.md")
            continue
        t = p.read_text(encoding="utf-8")
        if MARK in t:
            print(f"  - 已处理 {stem}")
            continue
        others = " · ".join(f"[[{s}]]" for s, _ in DOCS if s != stem)
        nav = (
            f"\n---\n\n## 导航\n\n"
            f"- 项目索引：[[诗词项目-索引]]\n"
            f"- 同类文档：{others}\n"
            f"- 索引：[[项目实践-地图]]\n"
        )
        if apply:
            p.write_text(t.rstrip("\n") + "\n" + nav + MARK + "\n",
                         encoding="utf-8", newline="\n")
        n += 1
        print(f"  ✓ {stem}（{kind}）加导航")

    # 项目实践-地图 顺手补上项目入口
    mp = ROOT / "80-Projects" / "项目实践-地图.md"
    if mp.exists():
        mt = mp.read_text(encoding="utf-8")
        if "诗词项目-索引" not in mt:
            add = (
                "\n\n## 项目清单\n\n"
                "| 项目 | 一句话 | 索引 |\n|---|---|---|\n"
                "| 诗词 KG-RAG Agent | 用知识图谱 + RAG 做诗词问答 | [[诗词项目-索引]] |\n"
            )
            if apply:
                mp.write_text(mt.rstrip("\n") + add, encoding="utf-8", newline="\n")
            print("  ✓ 项目实践-地图.md 补项目入口")

    print()
    print(f"{'✓ 已处理' if apply else '将处理'} {n} 篇")
    if not apply:
        print("(dry-run) 加 --apply")


if __name__ == "__main__":
    main()
