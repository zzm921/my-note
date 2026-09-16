# -*- coding: utf-8 -*-
"""归档 rag 旧薄提纲到 99-Archive/rag-旧提纲/

背景：10-AI/rag 已按站点卡片反向认领 11 篇正式笔记，
旧的薄提纲（1.7~2.9KB）已被取代，移入归档区留痕。

注意：不碰 git 的中文路径子命令，用纯 Python 文件操作。
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "10-AI" / "rag"
DST = ROOT / "99-Archive" / "rag-旧提纲"

STUBS = [
    "01-RAG概念与演进.md",
    "02-NaiveRAG朴素RAG.md",
    "03-AdvancedRAG进阶RAG.md",
    "04-ModularRAG模块化RAG.md",
    "05-GraphRAG图谱增强.md",
    "RAG总览.md",
    "RAG评估.md",
    "advanced-rag-碎片.md",
    "naive-rag-碎片.md",
]

# 这些文件虽小但与站点的 rag-eval / rag-online-eval 是两回事，
# RAG评估.md 需先确认是否已被认领笔记覆盖 → 由调用方决定，这里只做搬运。


def main() -> None:
    apply = "--apply" in sys.argv
    DST.mkdir(parents=True, exist_ok=True)

    moved = 0
    skipped = 0
    for name in STUBS:
        src = SRC / name
        if not src.exists():
            print(f"  - 跳过（不存在）: {name}")
            skipped += 1
            continue
        dst = DST / name
        if dst.exists():
            print(f"  - 跳过（归档已有）: {name}")
            skipped += 1
            continue
        print(f"  → {name}  ({src.stat().st_size} B)")
        if apply:
            src.replace(dst)
        moved += 1

    print()
    print(f"合计 搬运 {moved} 篇，跳过 {skipped} 篇")
    if not apply:
        print("（dry-run，加 --apply 才真正执行）")


if __name__ == "__main__":
    main()
