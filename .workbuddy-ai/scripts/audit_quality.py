# -*- coding: utf-8 -*-
"""全库内容质量盘点 —— 逐篇给出客观指标，供人工判断。

指标维度：
  size        字节数
  lines       行数
  h2/h3       小节数（结构骨架）
  words       正文字符数（去 frontmatter / 代码块 / 链接语法）
  code        代码块数
  links       出链数
  toc         todo 标记数
  imgs        图片数
  headless    是否缺 H1
  fm          是否有 frontmatter
  updated     frontmatter 里的 updated
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]
FM_RE = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n", re.S)
FENCE_RE = re.compile(r"```.*?```", re.S)
TODO_RE = re.compile(r"(TODO|FIXME|待补|待写|待完善|占位|xxx|XXX|略|待定)")


def md_files():
    for p in ROOT.rglob("*.md"):
        if any(x in p.parts for x in (".git", ".obsidian", ".workbuddy-ai")):
            continue
        yield p


def analyze(p: Path) -> dict:
    raw = p.read_text(encoding="utf-8", errors="ignore")
    rel = p.relative_to(ROOT).as_posix()
    top = rel.split("/")[0] if "/" in rel else "(根)"

    fm_txt = ""
    body = raw
    m = FM_RE.match(raw)
    if m:
        fm_txt = m.group(1)
        body = raw[m.end():]

    noscript = FENCE_RE.sub("", body)
    code_blocks = len(FENCE_RE.findall(body))

    h1 = len(re.findall(r"^# ", noscript, re.M))
    h2 = len(re.findall(r"^## ", noscript, re.M))
    h3 = len(re.findall(r"^### ", noscript, re.M))

    # 正文净字数：去链接语法、去 markdown 符号
    plain = re.sub(r"!?\[\[([^\]|]+)(\|[^\]]*)?\]\]", r"\1", noscript)
    plain = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", plain)
    plain = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", plain)
    plain = re.sub(r"[#>*`\-|]", "", plain)
    words = len(re.sub(r"\s+", "", plain))

    links = len(re.findall(r"(?<!\\)!?\[\[", body))
    imgs = len(re.findall(r"!\[\[|!\[[^\]]*\]\(", body))
    todos = len(TODO_RE.findall(noscript))

    upd = ""
    mu = re.search(r"^updated:\s*(.+)$", fm_txt, re.M)

    # 代码行数：代码密集型笔记（如手写实现、面试题）正文文字少但价值高
    code_lines = sum(b.count("\n") + 1 for b in FENCE_RE.findall(body))

    # 质量分档：用「正文净字数 + 代码行数×8」作为有效体量，
    # 避免把代码密集型笔记误判为「薄」。
    effective = words + code_lines * 8
    if effective < 80:
        grade = "空壳"
    elif effective < 300:
        grade = "薄"
    elif effective < 1200:
        grade = "一般"
    elif effective < 3000:
        grade = "充实"
    else:
        grade = "厚重"

    return dict(
        path=rel, top=top, size=len(raw.encode("utf-8")), lines=raw.count("\n") + 1,
        h1=h1, h2=h2, h3=h3, words=words, code=code_blocks, code_lines=code_lines,
        effective=effective,
        links=links, imgs=imgs, todos=todos,
        has_fm=bool(fm_txt), updated=mu.group(1).strip() if mu else "",
        grade=grade,
    )


def main() -> None:
    rows = [analyze(p) for p in md_files()]
    rows.sort(key=lambda r: (r["top"], r["words"]))

    # 按档统计
    from collections import Counter
    by_grade = Counter(r["grade"] for r in rows)
    print("=" * 76)
    print("全库内容质量盘点")
    print("=" * 76)
    print(f"总篇数：{len(rows)}")
    for g in ("厚重", "充实", "一般", "薄", "空壳"):
        print(f"  {g:4s}  {by_grade.get(g, 0):3d} 篇")

    print()
    print("=" * 76)
    print("【空壳 + 薄】(words < 300) —— 需要处理")
    print("=" * 76)
    print(f"{'字数':>6}{'行':>5}{'链':>4}{'图':>4}{'TODO':>6}  {'档':<5} 路径")
    for r in rows:
        if r["grade"] in ("空壳", "薄"):
            print(f"{r['words']:>6}{r['lines']:>5}{r['links']:>4}{r['imgs']:>4}"
                  f"{r['todos']:>6}  {r['grade']:<5} {r['path']}")

    out = ROOT / ".workbuddy-ai" / "scripts" / "_quality.json"
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n全量指标已写入 {out.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
