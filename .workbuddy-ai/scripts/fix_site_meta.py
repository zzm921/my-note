# -*- coding: utf-8 -*-
"""
修复「反向认领」笔记的 frontmatter 重复键问题。

原写法把站点字段原样平铺，导致根级出现两个 tags 键（笔记的 + 站点的）。
改为：站点字段收敛进 site_meta 嵌套块，站点的 tags 在块内保留原名，
根级只有笔记规范的 tags。这样 YAML 严格解析也不冲突。
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
apply = "--apply" in sys.argv

DIRS = ["10-AI/agent", "10-AI/agent-engineering", "10-AI/protocol", "10-AI/eval"]

# 站点字段名（块内保留），其余行按原样
CARDS = ["agent-engineering", "prompt-strategy", "structured-output", "context-mgmt",
         "context-caching", "memory", "cost-governance", "llm-gateway", "sandbox",
         "fault-injection", "hitl", "security", "task-system",
         "function-calling", "mcp", "a2a", "agent-skills",
         "agent-eval", "rag-eval", "rag-online-eval", "observability-eval"]


def rebuild(p: pathlib.Path):
    t = p.read_text(encoding="utf-8")
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", t, re.S)
    if not m:
        return None
    fm = m.group(1)
    body = t[m.end():]

    if "site_meta:" in fm:
        return None  # 已修过

    # 切三段：笔记字段 / 站点字段 / 发布声明
    i_site = fm.find("# —— 以下为站点卡片字段")
    i_pub = fm.find("# —— 发布声明")
    if i_site < 0 or i_pub < 0:
        return None

    note_part = fm[:i_site].rstrip("\n")
    site_part = fm[i_site:i_pub]
    pub_part = fm[i_pub:]

    # 站点字段块：去掉注释行，逐行缩进
    site_lines = [l for l in site_part.splitlines() if not l.strip().startswith("#")]
    while site_lines and not site_lines[0].strip():
        site_lines.pop(0)
    indented = []
    for l in site_lines:
        indented.append(("  " + l) if l.strip() else "")

    # 发布字段块
    pub_lines = [l for l in pub_part.splitlines() if not l.strip().startswith("#")]
    while pub_lines and not pub_lines[0].strip():
        pub_lines.pop(0)

    new_fm = [note_part, "", "site_meta:"]
    new_fm.extend(indented)
    new_fm.extend(pub_lines)

    return "---\n" + "\n".join(new_fm).rstrip("\n") + "\n---\n" + body


n = 0
for d in DIRS:
    for p in sorted((ROOT / d).glob("*.md")):
        r = rebuild(p)
        if r is None:
            print(f"  跳过 {p.as_posix()}")
            continue
        if apply:
            p.write_text(r, encoding="utf-8", newline="\n")
        n += 1
        if n <= 2:
            print("=" * 60)
            print(p.as_posix())
            print(r[: r.find("---", 4) + 3])

print()
print(f"{'✓ 已修复' if apply else '将修复'} {n} 篇")
if not apply:
    print("(dry-run) 加 --apply")
