# -*- coding: utf-8 -*-
"""逐张图片的引用明细 —— 人工复核用。

不打聚合结论，直接把每张图的**每一个引用位置与原文片段**打出来，
便于肉眼判断哪些是「真引用」、哪些是「清单登记 / 示例文本 / 失效路径」。
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]
ATT = ROOT / "99-Attachments"
IMG_EXT = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp")
SELF_LIST = {"99-Archive/孤儿图片清单.md"}
FENCE = re.compile(r"```.*?```", re.S)


def main() -> None:
    names = sorted(p.name for p in ATT.iterdir()
                   if p.is_file() and p.suffix.lower() in IMG_EXT)

    # name -> [(file, 行号, 原文)]
    hits: dict[str, list] = {n: [] for n in names}

    for f in ROOT.rglob("*.md"):
        parts = f.parts
        if ".git" in parts or ".obsidian" in parts or ".workbuddy-ai" in parts:
            continue
        rel = f.relative_to(ROOT).as_posix()
        if rel in SELF_LIST:
            continue
        lines = f.read_text(encoding="utf-8", errors="ignore").splitlines()
        for i, line in enumerate(lines, 1):
            if "http://" in line or "https://" in line:
                # 只关心本地引用；远程 URL 行整体跳过
                continue
            for n in names:
                if n in line:
                    hits[n].append((rel, i, line.strip()[:110]))

    print("=" * 78)
    print("逐张图片引用明细（仅本地引用行）")
    print("=" * 78)

    orphan = []
    for n in names:
        h = hits[n]
        if not h:
            orphan.append(n)
            print(f"\n❌ 【无引用】 {n}")
            continue
        print(f"\n✅ {n}   ({len(h)} 处)")
        for rel, ln, txt in h:
            print(f"     {rel}:{ln}")
            print(f"       {txt}")

    print("\n" + "=" * 78)
    print(f"无引用图片：{len(orphan)} 张")
    for n in orphan:
        print(f"   {n}  ({(ATT/n).stat().st_size:,} B)")


if __name__ == "__main__":
    main()
