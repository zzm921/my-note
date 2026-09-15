# -*- coding: utf-8 -*-
"""
修复 GitBook 时代的图片引用路径。

背景：
  老笔记里图片用 `<../../.gitbook/assets/Pasted image xxx.png>` 引用，
  这个路径早已失效（.gitbook 目录不存在）。图片实体现已在 99-Attachments/。
  本脚本把它们统一改写为 Obsidian wiki-embed：`![[Pasted image xxx.png]]`
  —— 按文件名解析、与目录无关，是笔记库约定的引用方式。

同时把「误判为孤儿」的图片说明更新为「实为活图」。

默认 dry-run，--apply 才执行。
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
apply = "--apply" in sys.argv

# 匹配三种形态：
#   ![](<../../.gitbook/assets/xxx.png>)   ← 尖括号在圆括号内
#   <../../.gitbook/assets/xxx.png>
#   ../../.gitbook/assets/xxx.png
PAT = re.compile(
    r"!\[[^\]]*\]\(\s*<?((?:\.\./)+\.gitbook/assets/[^>)]+?\.(?:png|jpg|jpeg|gif|webp))>?\s*\)"
    r"|<?((?:\.\./)+\.gitbook/assets/[^>)]+?\.(?:png|jpg|jpeg|gif|webp))>?",
    re.I,
)

# 校验图片是否真在附件目录
ATT = ROOT / "99-Attachments"

total = 0
files = 0
missing = []

for p in sorted(ROOT.rglob("*.md")):
    if set(p.parts) & {".git", ".obsidian", ".workbuddy-ai", ".idea", "99-Archive"}:
        continue
    t = p.read_text(encoding="utf-8", errors="replace")
    if "gitbook/assets" not in t:
        continue
    hits = [m for m in PAT.finditer(t)]

    def repl(m):
        # 两组：第一组是 md 图片形态，第二组是裸路径形态
        path = m.group(1) or m.group(2)
        name = path.split("/")[-1]
        if not (ATT / name).exists():
            missing.append((p.as_posix(), name))
        return f"![[{name}]]"

    new = PAT.sub(repl, t)
    if new == t:
        continue
    files += 1
    total += len(hits)
    print(f"  {p.as_posix():52s} 改写 {len(hits)} 处")
    if apply:
        p.write_text(new, encoding="utf-8", newline="\n")

print()
print(f"{'✓ 已改写' if apply else '将改写'} {total} 处 / {files} 个文件")
if missing:
    print("\n!! 引用的图片不在 99-Attachments：")
    for f, n in missing:
        print(f"   {f}  ->  {n}")
else:
    print("✓ 所有被引用的图片都已在 99-Attachments")
if not apply:
    print("(dry-run) 加 --apply")
