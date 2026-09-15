"""扫描全库 wiki 链接，找出迁移后失效的（断链）。

迁移会改变路径，而某些笔记用的是带路径的 wiki 链接 [[../a/b]] 或 [[目录/文件]]，
这类链接会失效。单纯的文件名链接 [[文件名]] 不受影响。
"""
from __future__ import annotations

import re
from pathlib import Path

VAULT = Path(r"D:\workspace\my-note")
SKIP_DIRS = {".git", ".obsidian", ".idea", ".workbuddy-ai"}

# ![[...]] 是嵌入（含图片），[[...]] 是链接
WIKI = re.compile(r"(?<!!)\[\[([^\]|]+?)(?:\|[^\]]*)?\]\]")


def main() -> None:
    notes = [p for p in VAULT.rglob("*.md")
             if not any(s in p.parts for s in SKIP_DIRS)]

    # 全库文件名索引（不含扩展名）+ 相对路径索引
    by_stem: dict[str, list[Path]] = {}
    for n in notes:
        by_stem.setdefault(n.stem, []).append(n)

    broken: list[tuple[str, str, str]] = []   # (note, link, reason)
    total = 0

    for note in notes:
        rel = note.relative_to(VAULT).as_posix()
        text = note.read_text(encoding="utf-8", errors="ignore")
        for m in WIKI.finditer(text):
            raw = m.group(1).strip()
            total += 1
            # 去掉 .md 后缀和锚点
            target = raw.split("#")[0].strip()
            if target.endswith(".md"):
                target = target[:-3]
            if not target:
                continue
            stem = Path(target).name
            if stem in by_stem:
                continue
            broken.append((rel, raw, "找不到同名笔记"))

    print(f"wiki 链接总数：{total}")
    print(f"断链：{len(broken)}\n")
    if broken:
        print("=== 断链明细 ===")
        cur = None
        for note, link, reason in broken:
            if note != cur:
                print(f"\n{note}")
                cur = note
            print(f"    [[{link}]]  ({reason})")
    else:
        print("无断链")


if __name__ == "__main__":
    main()
