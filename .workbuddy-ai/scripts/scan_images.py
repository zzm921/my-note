"""扫描图片引用（正确的 Obsidian wiki-embed 语法）。

Obsidian 的 ![[x.png]] 按**文件名**解析，与所在目录无关 —— 所以把图片
从 images/ 移到 99-Attachments/ 不会断链。本脚本确认这一结论并找出例外。
"""
from __future__ import annotations

import re
from pathlib import Path

VAULT = Path(r"D:\workspace\my-note")
SKIP_DIRS = {".git", ".obsidian", ".idea", ".workbuddy-ai", ".gitbook"}
IMG_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp"}

WIKI = re.compile(r"!\[\[([^\]|]+?)(?:\|[^\]]*)?\]\]")   # ![[x.png]] 或 ![[x.png|alt]]
MD = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")                # ![](x.png)
HTML = re.compile(r"<img[^>]+src=[\"']([^\"']+)[\"']")    # <img src="x.png">


def main() -> None:
    assets: dict[str, Path] = {}
    for ad in ("images", ".gitbook/assets"):
        d = VAULT / ad
        if d.exists():
            for p in d.rglob("*"):
                if p.is_file() and p.suffix.lower() in IMG_EXT:
                    assets[p.relative_to(VAULT).as_posix()] = p
    by_name: dict[str, list[str]] = {}
    for k in assets:
        by_name.setdefault(Path(k).name, []).append(k)

    notes = [p for p in VAULT.rglob("*.md")
             if not any(s in p.parts for s in SKIP_DIRS)]

    wiki_refs: dict[str, list[str]] = {}
    path_refs: list[tuple[str, str, str]] = []   # (note, raw, style)
    unresolved: list[tuple[str, str]] = []
    http_count = 0

    for note in notes:
        rel = note.relative_to(VAULT).as_posix()
        text = note.read_text(encoding="utf-8", errors="ignore")
        for m in WIKI.finditer(text):
            name = m.group(1).strip()
            if Path(name).suffix.lower() not in IMG_EXT:
                continue
            key = Path(name).name
            if key in by_name:
                wiki_refs.setdefault(key, []).append(rel)
            else:
                unresolved.append((rel, name))
        for style, rgx in (("md", MD), ("html", HTML)):
            for m in rgx.finditer(text):
                raw = m.group(1).strip()
                if raw.startswith("http"):
                    http_count += 1
                    continue
                key = Path(raw).name
                if Path(raw).suffix.lower() not in IMG_EXT:
                    continue
                path_refs.append((rel, raw, style))
                if key not in by_name:
                    unresolved.append((rel, raw))

    print("=" * 60)
    print(f"图片总数        {len(assets)}")
    print(f"  其中 images/          {len([k for k in assets if k.startswith('images/')])}")
    print(f"  其中 .gitbook/assets/ {len([k for k in assets if k.startswith('.gitbook')])}")
    print()
    print(f"wiki 引用 ![[x.png]]    {sum(len(v) for v in wiki_refs.values())} 处，涉及 {len(wiki_refs)} 张图")
    print(f"路径引用 (md/html)      {len(path_refs)} 处")
    print(f"http 外链               {http_count} 处（不动）")
    print()
    print(f"孤儿图片（零引用）      {len(assets) - len(wiki_refs)}")
    print(f"引用不到的图片名        {len(unresolved)}")

    print("\n" + "=" * 60)
    print("路径引用明细（迁移后需改写这些）")
    if path_refs:
        for note, raw, style in path_refs:
            print(f"  [{style}] {note}\n        -> {raw}")
    else:
        print("  （无）")

    print("\n" + "=" * 60)
    print("引用不到的图片名（可能已丢失）")
    if unresolved:
        for note, name in unresolved[:30]:
            print(f"  {note}  ->  {name}")
    else:
        print("  （无，全部可解析）")

    print("\n" + "=" * 60)
    print("重名图片（同一文件名存在于两个附件目录）")
    dup = {n: v for n, v in by_name.items() if len(v) > 1}
    for n, v in sorted(dup.items()):
        print(f"  {n}")
        for k in v:
            print(f"      {assets[k].stat().st_size:>9}B  {k}")
    print(f"  共 {len(dup)} 个重名")


if __name__ == "__main__":
    main()
