# -*- coding: utf-8 -*-
"""补齐 rename_readmes.py 漏掉的引用形态。

第一版只处理了标准 wiki 链接 `[[path/README|alias]]`，漏了三类：
  1. 表格内转义管道符   [[10-AI/agent/README\|alias]]   ← 正文里是 \| 
  2. Markdown 链接      [文本](10-AI/README.md)          ← SUMMARY.md 大量使用
  3. frontmatter/正文里的纯路径描述（不改，只报告）

本脚本幂等：只替换仍含旧路径的部分。
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]

RENAME = {
    "": "库总览",
    "10-AI": "AI-地图",
    "10-AI/agent-engineering": "Agent工程演进-地图",
    "10-AI/agent": "Agent范式-地图",
    "10-AI/rag": "RAG-地图",
    "10-AI/protocol": "协议-地图",
    "10-AI/eval": "评估评测-地图",
    "10-AI/ops": "生产治理-地图",
    "10-AI/ml": "机器学习-地图",
    "20-Backend": "后端-地图",
    "20-Backend/golang": "Golang-地图",
    "30-Data": "数据-地图",
    "40-Network": "计算机网络-地图",
    "50-Ops": "运维-地图",
    "60-Frontend": "前端-地图",
    "70-Interview": "面试题-地图",
    "80-Projects": "项目实践-地图",
    "90-Daily": "日报-地图",
    "99-Archive": "归档区-地图",
}

# 路径(无扩展) → 新 stem
PATH2STEM = {}
for d, stem in RENAME.items():
    p = f"{d}/README" if d else "README"
    PATH2STEM[p] = stem

# 跳过这些文件：迁移记录、git 教程正文（讲 git 机制的 README 示例不算引用）
SKIP = {
    "01-Maps/迁移清单-待确认.md",
    "50-Ops/gitlab/git操作.md",
}


def md_files():
    for p in ROOT.rglob("*.md"):
        parts = p.parts
        if ".git" in parts or ".obsidian" in parts or ".workbuddy-ai" in parts:
            continue
        yield p


def main() -> None:
    apply = "--apply" in sys.argv
    total = 0
    files_touched = 0
    report = []

    for f in md_files():
        rel = f.relative_to(ROOT).as_posix()
        if rel in SKIP:
            continue
        t = f.read_text(encoding="utf-8")
        orig = t
        n_before = 0

        # --- 1) wiki 链接，兼容 \| 转义管道 ---
        # 形如 [[10-AI/agent/README|a]] 或 [[10-AI/agent/README\|a]] 或 [[10-AI/agent/README]]
        def repl_wiki(m):
            nonlocal n_before
            target = m.group("tgt")
            alias_raw = m.group("alias")   # 含前导 | 或 \|
            key = target.strip().lstrip("/")
            if key.endswith(".md"):
                key = key[:-3]
            if key not in PATH2STEM:
                return m.group(0)
            n_before += 1
            new = PATH2STEM[key]
            return f"[[{new}{alias_raw}]]" if alias_raw else f"[[{new}]]"

        t = re.sub(
            r"\[\[(?P<tgt>[^\]\|\\\n]*?/README|README)(?P<alias>\\?\|[^\]\n]*)?\]\]",
            repl_wiki,
            t,
        )

        # --- 2) Markdown 链接 [文本](path/README.md) ---
        def repl_md(m):
            nonlocal n_before
            url = m.group("url")
            key = url.lstrip("./").lstrip("/")
            if key.endswith(".md"):
                key = key[:-3]
            if key not in PATH2STEM:
                return m.group(0)
            n_before += 1
            new = PATH2STEM[key]
            # 保留原目录前缀
            if "/" in url:
                prefix = url[: url.rfind("/") + 1]
                return f"[{m.group('txt')}]({prefix}{new}.md)"
            return f"[{m.group('txt')}]({new}.md)"

        t = re.sub(
            r"\[(?P<txt>[^\]]*)\]\((?P<url>[^)\s]*?/?README\.md)\)",
            repl_md,
            t,
        )

        if t != orig:
            if apply:
                f.write_text(t, encoding="utf-8", newline="\n")
            files_touched += 1
            total += n_before
            report.append((rel, n_before))

    print("=" * 68)
    for rel, n in report:
        print(f"  {n:3d} 处  {rel}")
    print("=" * 68)
    print(f"{'✓ 已改写' if apply else '将改写'} {total} 处引用，涉及 {files_touched} 个文件")
    if not apply:
        print("(dry-run) 加 --apply 执行")


if __name__ == "__main__":
    main()
