"""图片迁移：images/ + .gitbook/assets/ → 99-Attachments/

安全前提（已扫描确认）：
- 54 处引用是 Obsidian wiki-embed ![[文件名]]，按文件名解析，与目录无关，移动不断链
- 仅 1 处相对路径引用需要改写
- 11 个重名文件内容完全相同，可安全去重
- 35 张零引用图片 → 移入 99-Archive/孤儿图片/（不直接删，留可查）

用法：
  python migrate_images.py            # 预览
  python migrate_images.py --apply    # 执行
"""
from __future__ import annotations

import hashlib
import re
import shutil
import sys
from pathlib import Path

VAULT = Path(r"D:\workspace\my-note")
SKIP_DIRS = {".git", ".obsidian", ".idea", ".workbuddy-ai", ".gitbook"}
IMG_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp"}

DEST = VAULT / "99-Attachments"
ORPHAN = VAULT / "99-Archive" / "孤儿图片"

# 需要改写的路径引用：老写法 -> 新写法
PATH_REWRITE = {
    "99-Archive/碎片/nest.js.md": [
        ("../../.gitbook/assets/2ff55d9978d0c69024e0966a197a352.png",
         "99-Attachments/2ff55d9978d0c69024e0966a197a352.png"),
    ],
}

WIKI = re.compile(r"!\[\[([^\]|]+?)(?:\|[^\]]*)?\]\]")
MD = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
HTML = re.compile(r"<img[^>]+src=[\"']([^\"']+)[\"']")


def md5(p: Path) -> str:
    return hashlib.md5(p.read_bytes()).hexdigest()


def main() -> None:
    apply = "--apply" in sys.argv

    # 1. 收集所有图片
    srcs: list[Path] = []
    for ad in ("images", ".gitbook/assets"):
        d = VAULT / ad
        if d.exists():
            srcs.extend(p for p in d.rglob("*")
                        if p.is_file() and p.suffix.lower() in IMG_EXT)

    # 2. 按内容去重（优先保留 images/ 里的那份）
    #    ⚠️ 重要：只删除「同名重复」（同一文件名在两处各有一份，内容相同）。
    #    不同文件名但内容相同 → 不动，因为可能被分别引用，删了会断链。
    srcs.sort(key=lambda p: (".gitbook" in p.as_posix(), p.as_posix()))
    by_name: dict[str, list[Path]] = {}
    for p in srcs:
        by_name.setdefault(p.name, []).append(p)

    keep: list[Path] = []
    dupes: list[Path] = []
    for name, group in by_name.items():
        if len(group) == 1:
            keep.append(group[0])
            continue
        # 同名多份：保留第一份，其余仅在内容相同时删除
        first = group[0]
        keep.append(first)
        h0 = md5(first)
        for p in group[1:]:
            if md5(p) == h0:
                dupes.append(p)
            else:
                keep.append(p)          # 内容不同 → 必须保留

    print(f"{'执行模式' if apply else '预览模式（dry-run）'}")
    print(f"源图片 {len(srcs)} 张 → 去重后保留 {len(keep)} 张，重复 {len(dupes)} 张\n")

    # 3. 统计引用
    notes = [p for p in VAULT.rglob("*.md")
             if not any(s in p.parts for s in SKIP_DIRS)]
    referenced: set[str] = set()
    for note in notes:
        t = note.read_text(encoding="utf-8", errors="ignore")
        for m in list(WIKI.finditer(t)) + list(MD.finditer(t)):
            raw = m.group(1).strip()
            if raw.startswith("http"):
                continue
            referenced.add(Path(raw).name)
        for m in HTML.finditer(t):
            raw = m.group(1).strip()
            if not raw.startswith("http"):
                referenced.add(Path(raw).name)

    orphans = [p for p in keep if p.name not in referenced]
    used = [p for p in keep if p.name in referenced]
    print(f"被引用 {len(used)} 张 ｜ 零引用 {len(orphans)} 张\n")

    if not apply:
        print("=== 将移动（被引用）===")
        for p in used:
            print(f"  {p.relative_to(VAULT)}  ->  99-Attachments/{p.name}")
        print("\n=== 将移动（零引用，进 99-Archive/孤儿图片/）===")
        for p in orphans:
            print(f"  {p.relative_to(VAULT)}  ->  99-Archive/孤儿图片/{p.name}")
        print("\n=== 将删除（内容重复）===")
        for p in dupes:
            print(f"  {p.relative_to(VAULT)}")
        print("\n=== 将改写引用 ===")
        for f, pairs in PATH_REWRITE.items():
            for old, new in pairs:
                print(f"  {f}\n      {old}\n   -> {new}")
        print(f"\n{'以上为预览，加 --apply 执行'}")
        return

    # ---- 执行 ----
    DEST.mkdir(parents=True, exist_ok=True)
    ORPHAN.mkdir(parents=True, exist_ok=True)

    ok = 0
    for p in used:
        dst = DEST / p.name
        if dst.exists():
            dst = DEST / p.name
        shutil.move(str(p), str(dst))
        ok += 1
    print(f"[移动] {ok} 张被引用图片 -> 99-Attachments/")

    ok2 = 0
    for p in orphans:
        dst = ORPHAN / p.name
        if dst.exists():
            continue
        shutil.move(str(p), str(dst))
        ok2 += 1
    print(f"[移动] {ok2} 张零引用图片 -> 99-Archive/孤儿图片/")

    for p in dupes:
        p.unlink()
    print(f"[删除] {len(dupes)} 张内容重复图片")

    # 改写引用
    cnt = 0
    for rel, pairs in PATH_REWRITE.items():
        f = VAULT / rel
        if not f.exists():
            print(f"[!缺失] {rel}")
            continue
        t = f.read_text(encoding="utf-8")
        for old, new in pairs:
            if old in t:
                t = t.replace(old, new)
                cnt += 1
        f.write_text(t, encoding="utf-8")
    print(f"[改写] {cnt} 处路径引用")

    # 清理空目录
    for d in (VAULT / "images", VAULT / ".gitbook" / "assets", VAULT / ".gitbook"):
        if d.exists() and not any(d.iterdir()):
            d.rmdir()
            print(f"[清理空目录] {d.relative_to(VAULT)}")

    print(f"\n完成：移动 {ok + ok2} 张，删除重复 {len(dupes)} 张，改写 {cnt} 处")


if __name__ == "__main__":
    main()
