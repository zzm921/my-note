# -*- coding: utf-8 -*-
"""严格版孤儿图片扫描 —— 只认**本地**引用。

与 find_orphan_images.py 的区别：
  上一版用「文件名是否出现在正文」做兜底，结果把远程 URL
  （如 https://github.com/.../Pasted%20image%2020240118151434.png）
  和清单文档的自我登记都算成了引用，导致结论虚高（78/78 全活）。

本版规则：
  1. 只统计**能解析到本地 99-Attachments/ 的真实引用**：
     - wiki-embed        ![[x.png]]            （按文件名）
     - Markdown 本地路径  ![alt](x.png) / (99-Attachments/x.png)
     - 裸本地路径         x.png 前面不带 http(s)://
  2. 显式排除：
     - http(s):// 远程 URL（含编码后的 %20 形态）
     - 清单文档（99-Archive/孤儿图片清单.md）的自我登记
     - code fence 内的示例文本
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]
ATT = ROOT / "99-Attachments"
IMG_EXT = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp")
EXT_RE = r"\.(?:png|jpg|jpeg|gif|webp|svg|bmp)"

# 自我登记类文档：里面列文件名不等于「引用」
SELF_LIST = {"99-Archive/孤儿图片清单.md"}

FENCE = re.compile(r"```.*?```", re.S)


def md_files():
    for p in ROOT.rglob("*.md"):
        parts = p.parts
        if ".git" in parts or ".obsidian" in parts or ".workbuddy-ai" in parts:
            continue
        yield p


def strip_fences(t: str) -> str:
    return FENCE.sub("", t)


def main() -> None:
    imgs = {p.name: p for p in ATT.iterdir()
            if p.is_file() and p.suffix.lower() in IMG_EXT}

    refs: dict[str, list[str]] = {n: [] for n in imgs}
    remote_hits = 0

    for f in md_files():
        rel = f.relative_to(ROOT).as_posix()
        if rel in SELF_LIST:
            continue
        t = strip_fences(f.read_text(encoding="utf-8", errors="ignore"))

        # 1) wiki-embed（含被转义的 !\[\[ —— 归一化后再匹配）
        t_norm = t.replace("\\[\\[", "[[").replace("\\[", "[")
        for m in re.finditer(r"!\[\[([^\]|#]+?)\]\]", t_norm):
            tgt = m.group(1).strip().split("|")[0].strip()
            name = Path(tgt).name
            if name in refs:
                refs[name].append(f"{rel} [wiki]")

        # 2) Markdown 图片：排除 http(s)://
        for m in re.finditer(r"!\[[^\]]*\]\(\s*<?([^>\s)]+" + EXT_RE + r")>?\s*\)", t, re.I):
            url = m.group(1)
            if re.match(r"https?://", url, re.I):
                remote_hits += 1
                continue
            name = Path(url.replace("%20", " ")).name
            if name in refs:
                refs[name].append(f"{rel} [md]")

    orphans = sorted(n for n, r in refs.items() if not r)
    alive = sorted(n for n, r in refs.items() if r)

    print("=" * 72)
    print(f"附件目录：99-Attachments/")
    print(f"图片总数：{len(imgs)}")
    print(f"有本地引用：{len(alive)}")
    print(f"无本地引用：{len(orphans)}   ← 候选孤儿")
    print(f"（顺带跳过远程 URL 图片 {remote_hits} 处，非本地附件）")
    print("=" * 72)

    if orphans:
        print("\n【候选孤儿清单】")
        total = 0
        for n in orphans:
            sz = imgs[n].stat().st_size
            total += sz
            print(f"  {sz:>10,} B   {n}")
        print(f"\n  合计 {len(orphans)} 张，{total:,} B（{total/1024/1024:.2f} MB）")
    else:
        print("\n✓ 没有孤儿图片。")

    out = ROOT / ".workbuddy-ai" / "scripts" / "_orphan_list.txt"
    out.write_text("\n".join(orphans), encoding="utf-8")
    print(f"\n清单已写入：{out.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
