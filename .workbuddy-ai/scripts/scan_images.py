"""扫描图片引用：找出库里所有对 images/ 与 .gitbook/assets/ 的引用。

只读，不改任何文件。输出：
1. 每个图片被哪些笔记引用（相对路径写法）
2. 未被任何笔记引用的孤儿图片
3. 引用写法分类（markdown / obsidian / html）
"""
from __future__ import annotations

import re
from pathlib import Path

VAULT = Path(r"D:\workspace\my-note")
SKIP_DIRS = {".git", ".obsidian", ".idea", ".workbuddy-ai", ".gitbook"}
ASSET_DIRS = ["images", ".gitbook/assets"]
IMG_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp"}


def main() -> None:
    # 收集所有图片
    assets: dict[str, Path] = {}
    for ad in ASSET_DIRS:
        d = VAULT / ad
        if d.exists():
            for p in d.rglob("*"):
                if p.is_file() and p.suffix.lower() in IMG_EXT:
                    assets[p.relative_to(VAULT).as_posix()] = p
    print(f"图片总数：{len(assets)}")
    for ad in ASSET_DIRS:
        d = VAULT / ad
        n = len([p for p in d.rglob('*') if p.is_file()]) if d.exists() else 0
        print(f"  {ad}/  {n}")

    # 收集所有笔记
    notes = [p for p in VAULT.rglob("*.md")
             if not any(s in p.parts for s in SKIP_DIRS)]
    print(f"\n笔记总数：{len(notes)}")

    # 找引用
    # markdown: ![](path)  ![alt](path)
    md_re = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
    # html: <img src="path">
    html_re = re.compile(r"<img[^>]+src=[\"']([^\"']+)[\"']")
    # obsidian: ![[path]]
    obs_re = re.compile(r"!\[\[([^\]]+)\]\]")

    refs: dict[str, list[tuple[str, str]]] = {}  # asset_key -> [(note, style)]
    by_name: dict[str, str] = {}                 # 文件名 -> asset_key

    for k in assets:
        by_name.setdefault(Path(k).name, k)

    for note in notes:
        rel = note.relative_to(VAULT).as_posix()
        text = note.read_text(encoding="utf-8", errors="ignore")
        for style, rgx in (("md", md_re), ("html", html_re), ("obs", obs_re)):
            for m in rgx.finditer(text):
                raw = m.group(1).strip()
                # 归一化：去掉 ./ 前缀
                cand = raw.lstrip("./")
                key = None
                if cand in assets:
                    key = cand
                else:
                    # 用文件名兜底匹配（处理相对路径 ../images/x.png）
                    base = Path(cand).name
                    if base in by_name:
                        key = by_name[base]
                if key:
                    refs.setdefault(key, []).append((rel, raw))

    print(f"\n被引用的图片：{len(refs)}")
    print(f"孤儿图片（无引用）：{len(assets) - len(refs)}")

    print("\n=== 引用明细（前 40）===")
    for k in sorted(refs)[:40]:
        print(f"\n{k}")
        for note, raw in refs[k]:
            print(f"    <- {note}   [原写法: {raw}]")

    print("\n=== 孤儿图片（未被引用，可考虑清理）===")
    orphans = [k for k in sorted(assets) if k not in refs]
    for k in orphans:
        print(f"  {assets[k].stat().st_size:>8}B  {k}")

    # 引用写法分类：指向 assets 的引用里，有多少是相对路径
    print("\n=== 风险提示：相对路径引用 ===")
    risky = [(k, n, r) for k, v in refs.items() for n, r in v
             if r.startswith("../") or r.startswith("./")]
    print(f"使用 ./ 或 ../ 相对路径的引用：{len(risky)} 处")
    # ../ 的等级
    lvl = {}
    for k, n, r in risky:
        d = r.count("../")
        lvl[d] = lvl.get(d, 0) + 1
    for d in sorted(lvl):
        print(f"  深度 {d} 层 ../ ：{lvl[d]} 处")


if __name__ == "__main__":
    main()
