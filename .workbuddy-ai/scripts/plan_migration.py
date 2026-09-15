"""生成笔记库迁移映射清单（只读扫描，不移动任何文件）。

用法：python plan_migration.py > 迁移清单.md
"""
from __future__ import annotations

import hashlib
import os
from pathlib import Path

VAULT = Path(r"D:\workspace\my-note")
SKIP_DIRS = {".git", ".obsidian", ".idea", ".workbuddy-ai", ".gitbook", "images",
             "00-Inbox", "01-Maps", "_Templates", "99-Archive", "99-Attachments"}

# 老路径前缀 → 新路径前缀（按最长匹配优先）
RULE = [
    ("技术学习/机器学习/", "10-AI/ml/"),
    ("技术学习/rag/", "10-AI/rag/"),
    ("技术学习/agent/", "99-Archive/agent-旧提纲/"),
    ("技术学习/docker/", "50-Ops/docker/"),
    ("技术学习/CICD/", "50-Ops/cicd/"),
    ("技术学习/gitlab/", "50-Ops/gitlab/"),
    ("技术学习/nas/", "50-Ops/nas/"),
    ("技术学习/阿里云api/", "50-Ops/aliyun/"),
    ("技术学习/日志系统/", "50-Ops/elk/"),
    ("技术学习/虚拟机/", "50-Ops/vm/"),
    ("技术学习/windows/", "50-Ops/windows/"),
    ("技术学习/node/", "20-Backend/node/"),
    ("技术学习/python/", "20-Backend/python/"),
    ("技术学习/golang/", "20-Backend/golang/"),
    ("技术学习/数据库/", "30-Data/"),
    ("技术学习/计算机网络原理/", "40-Network/"),
    ("技术学习/前端/", "60-Frontend/"),
    ("技术学习/typescript/", "60-Frontend/typescript/"),
    ("技术学习/vue/", "60-Frontend/vue/"),
    ("技术学习/面试题/", "70-Interview/"),
    ("技术学习/", "99-Archive/技术学习-散篇/"),
    ("自研项目/", "80-Projects/"),
    ("AI热点日报/", "90-Daily/2026/"),
    ("images/", "99-Attachments/"),
]

# 主题名清理：目录里的冗余词
DIR_FIX = {
    "数据库mysql": "mysql", "数据库redis": "redis", "数据库mongodb": "mongodb",
    "node学习node基础": "", "node学习vscode使用": "vscode", "node学习数据库": "db",
    "node学习采坑日记": "pitfall", "常用工具包": "tools",
}

# 文件名清理规则
def clean_name(stem: str) -> str:
    s = stem
    for a, b in [("（", "("), ("）", ")"), ("　", "")]:
        s = s.replace(a, b)
    # 多个连续空格压成一个（用于 advance rag / naive  rag）
    while "  " in s:
        s = s.replace("  ", " ")
    s = s.replace("--", "-")
    # 术语大小写统一
    if s.lower().startswith("rag"):
        s = "RAG" + s[3:]
    s = s.replace("Rag ", "RAG ")
    s = s.replace("-RAG-", "-RAG-")
    return s.strip("-_")


def digest(p: Path) -> str:
    return hashlib.md5(p.read_bytes()).hexdigest()[:8]


# 特定文件的精确改名（消除空格 / 中英混排）
EXACT = {
    "技术学习/rag/advance rag.md": "10-AI/rag/advanced-rag-碎片.md",
    "技术学习/rag/naive  rag.md": "10-AI/rag/naive-rag-碎片.md",
    "技术学习/rag/Rag 评估.md": "10-AI/rag/RAG评估.md",
    "技术学习/rag/rag.md": "10-AI/rag/RAG总览.md",
    "技术学习/node/node学习node基础/.md": "99-Archive/空碎片/待删-无名文件.md",
}


def main() -> None:
    files: list[Path] = []
    for root, dirs, names in os.walk(VAULT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for n in names:
            if n.endswith(".md"):
                files.append(Path(root) / n)
    files.sort()

    # 内容指纹 → 重复组
    by_hash: dict[str, list[Path]] = {}
    for f in files:
        by_hash.setdefault(digest(f), []).append(f)

    def target(f: Path) -> str:
        rel = f.relative_to(VAULT).as_posix()
        if rel in EXACT:
            return EXACT[rel]
        for old, new in RULE:
            if rel.startswith(old):
                tail = rel[len(old):]
                stem = Path(tail).stem
                # 空名文件（如 ".md"）直接进归档标记为待删
                if not stem.strip() or stem.strip() == ".md":
                    return "99-Archive/空碎片/待删-无名文件.md"
                parts = [DIR_FIX.get(p, p) for p in Path(tail).parts[:-1]]
                parts = [p for p in parts if p]
                stem = clean_name(stem)
                if parts:
                    return "/".join([new.rstrip("/")] + parts + [stem + ".md"])
                return new + stem + ".md"
        return rel

    print("# 笔记库迁移映射清单\n")
    print(f"> 扫描根目录：`{VAULT}`  \n> 共 {len(files)} 篇 md。**本清单仅为预览，未移动任何文件。**\n")

    dupes = {h: v for h, v in by_hash.items() if len(v) > 1}
    print(f"## 一、重复内容组（同内容多份）：{len(dupes)} 组\n")
    if dupes:
        print("| 内容摘要 | 文件 | 建议 |")
        print("|---|---|---|")
        for h, v in sorted(dupes.items(), key=lambda x: -len(x[1])):
            for i, f in enumerate(v):
                rel = f.relative_to(VAULT).as_posix()
                act = "**保留主本**" if i == 0 else "删除/归档"
                print(f"| `{h}` | `{rel}` ({f.stat().st_size}B) | {act} |")
    else:
        print("（无）")

    print(f"\n## 二、碎片文件（≤200B）：\n")
    frags = [f for f in files if f.stat().st_size <= 200]
    print("| 文件 | 大小 | 内容预览 | 建议 |")
    print("|---|---|---|---|")
    for f in frags:
        rel = f.relative_to(VAULT).as_posix()
        txt = f.read_text(encoding="utf-8", errors="ignore").strip().replace("\n", " ")[:40]
        sug = "删除（空文件）" if f.stat().st_size == 0 else "并入相邻笔记 / 归档"
        print(f"| `{rel}` | {f.stat().st_size}B | {txt or '（空）'} | {sug} |")

    print(f"\n## 三、全量迁移映射：\n")
    print("| # | 老路径 | 新路径 |")
    print("|---|---|---|")
    for i, f in enumerate(files, 1):
        rel = f.relative_to(VAULT).as_posix()
        tgt = target(f)
        mark = " ⚠️" if rel == tgt else ""
        print(f"| {i} | `{rel}` | `{tgt}`{mark} |")

    changed = sum(1 for f in files if target(f) != f.relative_to(VAULT).as_posix())
    print(f"\n## 四、统计\n")
    print(f"- 总文件：{len(files)}")
    print(f"- 需要移动：{changed}")
    print(f"- 位置不变：{len(files) - changed}")
    print(f"- 碎片：{len(frags)}")
    print(f"- 重复组：{len(dupes)}")


if __name__ == "__main__":
    main()
