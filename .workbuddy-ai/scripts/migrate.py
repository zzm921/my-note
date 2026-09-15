"""执行笔记库迁移：老结构 → 新结构。

改用 Python 文件系统操作（shutil.move）而非 git mv：
git mv 在 Windows + 中文路径 + 子进程编码组合下会静默失败。

用法：
  python migrate.py            # 预览
  python migrate.py --apply    # 执行
"""
from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

VAULT = Path(r"D:\workspace\my-note")
SKIP_DIRS = {".git", ".obsidian", ".idea", ".workbuddy-ai", ".gitbook", "images",
             "00-Inbox", "01-Maps", "_Templates", "99-Archive", "99-Attachments"}

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
]

DIR_FIX = {
    "数据库mysql": "mysql", "数据库redis": "redis", "数据库mongodb": "mongodb",
    "node学习node基础": "", "node学习vscode使用": "vscode", "node学习数据库": "db",
    "node学习采坑日记": "pitfall", "常用工具包": "tools",
}

EXACT = {
    "技术学习/rag/advance rag.md": "10-AI/rag/advanced-rag-碎片.md",
    "技术学习/rag/naive  rag.md": "10-AI/rag/naive-rag-碎片.md",
    "技术学习/rag/Rag 评估.md": "10-AI/rag/RAG评估.md",
    "技术学习/rag/rag.md": "10-AI/rag/RAG总览.md",
    "技术学习/node/node学习数据库/eslint.md": "20-Backend/node/db/eslint-sequelize规范.md",
    "技术学习/node/mysql优化.md": "30-Data/mysql/mysql优化.md",
    "技术学习/Hermes Agent 配置指南.md": "10-AI/agent/Hermes-Agent配置指南.md",
    "技术学习/从机器学习到大模型-技术演进关键节点.md": "10-AI/ml/从机器学习到大模型-技术演进关键节点.md",
    "技术学习/大模型与AI Agent 技术资源汇总.md": "10-AI/大模型与AI-Agent技术资源汇总.md",
    "技术学习/诗词AI Agent 技术设计方案.md": "80-Projects/诗词KG-RAG_Agent方案/诗词AI-Agent技术设计方案.md",
    "技术学习/需加固问题.md": "50-Ops/需加固问题.md",
    "技术学习/http.md": "40-Network/HTTP协议详解.md",
    "技术学习/计算机网络原理/（传输层）TCP传输可靠性保障.md": "40-Network/传输层-TCP传输可靠性保障.md",
    "技术学习/计算机网络原理/（传输层）TCP的三次握手和四次挥手.md": "40-Network/传输层-TCP三次握手和四次挥手.md",
    "技术学习/计算机网络原理/（应用层）DNS域名系统详解.md": "40-Network/应用层-DNS域名系统详解.md",
    "技术学习/计算机网络原理/（应用层）HTTP常见状态码总结.md": "40-Network/应用层-HTTP常见状态码总结.md",
    "技术学习/计算机网络原理/（应用层）应用层常见协议总结.md": "40-Network/应用层-常见协议总结.md",
    "技术学习/计算机网络原理/（网络层）ARP协议详解.md": "40-Network/网络层-ARP协议详解.md",
    "技术学习/计算机网络原理/（网络层）NAT协议详解.md": "40-Network/网络层-NAT协议详解.md",
    "技术学习/计算机网络原理/网络原理基础（上）.md": "40-Network/网络原理基础(上).md",
    "技术学习/计算机网络原理/网络原理基础（下）.md": "40-Network/网络原理基础(下).md",
}

FRAGMENT = {
    "技术学习/docker/docker常用命令.md": "50-Ops/docker/docker常用命令.md",
    "技术学习/node/node学习vscode使用/格式化问题.md": "99-Archive/碎片/格式化问题.md",
    "技术学习/windows/激活.md": "50-Ops/windows/激活.md",
    "技术学习/日志系统/elk.md": "99-Archive/碎片/ELK安装链接.md",
    "技术学习/自然语言处理/实践.md": "99-Archive/碎片/NLP实践-spacy.md",
    "技术学习/语音识别/语音识别.md": "99-Archive/碎片/语音识别-token.md",
    "技术学习/面试题/nest.js.md": "99-Archive/碎片/nest.js.md",
}

# 删除的空文件（0B / 无实质内容）
DELETE_EMPTY = {
    "技术学习/计算机网络原理/（应用层）HTTP vs HTTPS.md",
    "技术学习/面试题/mysql.md",
    "技术学习/CICD/酷旗自动化构建及部署流程.md",
    "技术学习/node/node学习node基础/.md",
    "技术学习/数据库/数据库mongodb/mongodb.md",
    "技术学习/自然语言处理/理论知识.md",
}

# 保留但归档的空文件（给将来补写留位置）
ARCHIVE_EMPTY = {
    "技术学习/计算机网络原理/（应用层）HTTP vs HTTPS.md": "99-Archive/空碎片/待补-应用层HTTP vs HTTPS.md",
    "技术学习/面试题/mysql.md": "99-Archive/空碎片/待补-mysql面试题.md",
    "技术学习/CICD/酷旗自动化构建及部署流程.md": "99-Archive/空碎片/待补-酷旗自动化构建及部署流程.md",
    "技术学习/node/node学习node基础/.md": "99-Archive/空碎片/待删-无名文件.md",
    "技术学习/数据库/数据库mongodb/mongodb.md": "99-Archive/空碎片/待补-mongodb.md",
    "技术学习/自然语言处理/理论知识.md": "99-Archive/空碎片/待补-NLP理论知识.md",
}


def clean_name(stem: str) -> str:
    s = stem
    for a, b in [("（", "("), ("）", ")"), ("　", "")]:
        s = s.replace(a, b)
    while "  " in s:
        s = s.replace("  ", " ")
    s = s.replace("--", "-")
    if s.lower().startswith("rag"):
        s = "RAG" + s[3:]
    s = s.replace("Rag ", "RAG ")
    return s.strip("-_")


def target_of(rel: str) -> str:
    if rel in EXACT:
        return EXACT[rel]
    if rel in FRAGMENT:
        return FRAGMENT[rel]
    if rel in ARCHIVE_EMPTY:
        return ARCHIVE_EMPTY[rel]
    for old, new in RULE:
        if rel.startswith(old):
            tail = rel[len(old):]
            stem = Path(tail).stem
            if not stem.strip() or stem.strip() == ".md":
                return "99-Archive/空碎片/待删-无名文件.md"
            parts = [DIR_FIX.get(p, p) for p in Path(tail).parts[:-1]]
            parts = [p for p in parts if p]
            stem = clean_name(stem)
            if parts:
                return "/".join([new.rstrip("/")] + parts + [stem + ".md"])
            return new + stem + ".md"
    return rel


def main() -> None:
    apply = "--apply" in sys.argv
    files: list[Path] = []
    for root, dirs, names in os.walk(VAULT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for n in names:
            if n.endswith(".md"):
                files.append(Path(root) / n)
    files.sort()

    moves: list[tuple[str, str]] = []
    deletes: list[str] = []
    for f in files:
        rel = f.relative_to(VAULT).as_posix()
        tgt = target_of(rel)
        if rel == tgt:
            continue
        if rel in DELETE_EMPTY:
            deletes.append(rel)
        else:
            moves.append((rel, tgt))

    print(f"{'执行模式' if apply else '预览模式（dry-run）'}")
    print(f"待移动：{len(moves)}    待删除空文件：{len(deletes)}\n")

    ok = fail = skip = 0
    for rel in deletes:
        if apply:
            (VAULT / rel).unlink(missing_ok=True)
        print(f"[删除] {rel}")

    for src, dst in moves:
        src_p, dst_p = VAULT / src, VAULT / dst
        if not src_p.exists():
            print(f"[!不存在] {src}")
            fail += 1
            continue
        if dst_p.exists() and src_p.resolve() != dst_p.resolve():
            print(f"[跳过·目标已存在] {src} -> {dst}")
            skip += 1
            continue
        if apply:
            try:
                dst_p.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(src_p), str(dst_p))
                ok += 1
            except Exception as e:
                print(f"[失败] {src} :: {e}")
                fail += 1
        else:
            print(f"[移动] {src}\n    -> {dst}")

    if apply:
        print(f"\n成功 {ok}  跳过 {skip}  失败 {fail}")
        for d in sorted(VAULT.rglob("*"), reverse=True):
            if d.is_dir() and not any(d.iterdir()) and d.name not in {".git", ".obsidian"}:
                try:
                    d.rmdir()
                    print(f"[清理空目录] {d.relative_to(VAULT)}")
                except OSError:
                    pass
    else:
        print(f"\n以上为预览，加 --apply 执行")


if __name__ == "__main__":
    main()
