# -*- coding: utf-8 -*-
"""全库链接完整性校验：wiki 链接 + Markdown 链接 + 附件引用"""
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(r"D:\workspace\my-note")
SKIP_DIRS = {".git", ".obsidian", ".workbuddy-ai", "node_modules", "_site"}
FENCE = re.compile(r"```.*?```", re.S)
IMG_EXT = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".pdf", ".canvas"}

mds, attach = [], set()
for p in ROOT.rglob("*"):
    if any(s in p.parts for s in SKIP_DIRS):
        continue
    if not p.is_file():
        continue
    if p.suffix.lower() == ".md":
        mds.append(p)
    elif p.suffix.lower() in IMG_EXT:
        attach.add(p.name)

stems = {m.stem for m in mds}


def resolve_wiki(target, src: Path) -> bool:
    t = target.strip().split("|")[0].split("#")[0].strip()
    if not t:
        return True
    cands = [t] if t.lower().endswith(".md") else [t + ".md", t]
    for c in cands:
        c = c.replace("\\", "/")
        if (src.parent / c).exists():
            return True
        if (ROOT / c).exists():
            return True
        base = Path(c).name
        if Path(base).suffix.lower() == ".md":
            if Path(base).stem in stems:
                return True
        elif base in attach:
            return True
    return False


broken = []
wiki_cnt = md_cnt = 0

for p in mds:
    t = FENCE.sub("", p.read_text(encoding="utf-8", errors="ignore"))
    tn = t.replace("\\[\\[", "[[").replace("\\[", "[")

    for m in re.finditer(r"\[\[([^\]\n]+?)\]\]", tn):
        tgt = re.split(r"\\?\|", m.group(1), maxsplit=1)[0].strip()
        if not tgt:
            continue
        wiki_cnt += 1
        if not resolve_wiki(tgt, p):
            broken.append((str(p.relative_to(ROOT)), tgt, "wiki"))

    for m in re.finditer(r"(?<!!)\[[^\]]*\]\(\s*<?([^)>\s]+?)>?\s*\)", t):
        u = m.group(1)
        if re.match(r"^(https?:|mailto:|#)", u, re.I):
            continue
        md_cnt += 1
        uu = unquote(u.split("#")[0])
        if (p.parent / uu).exists() or (ROOT / uu).exists():
            continue
        broken.append((str(p.relative_to(ROOT)), u, "md"))

print(f"扫描 md 文件: {len(mds)}")
print(f"wiki 链接: {wiki_cnt}   md 链接: {md_cnt}   附件名池: {len(attach)}")
print(f"断链总数: {len(broken)}")
if broken:
    print("\n--- 断链明细（前 40）---")
    for f, u, k in broken[:40]:
        print(f"[{k}] {f}  ->  {u}")
else:
    print("\n[OK] 全部链接可解析，零断链")
