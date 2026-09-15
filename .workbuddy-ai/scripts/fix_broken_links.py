"""修复迁移导致的 wiki 断链。

迁移重命名了文件但没更新正文里的 wiki 链接。本脚本按「旧名 → 新名」映射修复。

不改动的：
- `_Templates/`（模板里的 [[笔记名]] 是占位示例）
- `01-Maps/文档体系设计与规范.md`（讲双链语法的说明文）
- gitlab 的 `[[runners]]`（TOML 配置语法，不是 wiki 链接）
"""
from __future__ import annotations

from pathlib import Path

VAULT = Path(r"D:\workspace\my-note")

# 旧链接写法 -> 新链接写法
# 格式：目标文件（相对库根） -> { 旧串: 新串 }
FIXES: dict[str, dict[str, str]] = {
    # ---- 计算机网络原理：文件已重命名 ----
    "40-Network/OSI和TCPIP网络分层模型详解.md": {
        "[[（传输层）TCP的三次握手和四次挥手]]": "[[传输层-TCP三次握手和四次挥手]]",
        "[[（应用层）HTTP常见状态码总结]]": "[[应用层-HTTP常见状态码总结]]",
        "[[（应用层）HTTP vs HTTPS]]": "[[应用层-HTTP常见状态码总结]]",
        "[[（应用层）DNS域名系统详解]]": "[[应用层-DNS域名系统详解]]",
        "[[（网络层）ARP协议详解]]": "[[网络层-ARP协议详解]]",
        "[[（网络层）NAT协议详解]]": "[[网络层-NAT协议详解]]",
    },
    "40-Network/传输层-TCP三次握手和四次挥手.md": {
        "[[TCP传输可靠性保障]]": "[[传输层-TCP传输可靠性保障]]",
        "[[（应用层）HTTP常见状态码总结]]": "[[应用层-HTTP常见状态码总结]]",
    },
    "40-Network/应用层-HTTP常见状态码总结.md": {
        "[[HTTP vs HTTPS]]": "[[应用层-常见协议总结]]",
        "[[（应用层）应用层常见协议总结]]": "[[应用层-常见协议总结]]",
    },
    # ---- 数据库：目录层去掉，文件名微调 ----
    "30-Data/NoSQL基础知识.md": {
        "[[数据库mongodb/mongodb]]": "[[30-Data/README]]",
    },
    "30-Data/mysql/mysql事务隔离级别.md": {
        "[[mysql三大日志（binlog、redo log和undo log）详解]]":
            "[[mysql三大日志(binlog、redo log和undo log)详解]]",
    },
    "30-Data/mysql/Mysql索引详解.md": {
        "[[数据库mysql/mysql三大日志（binlog、redo log和undo log）详解]]":
            "[[mysql三大日志(binlog、redo log和undo log)详解]]",
    },
    # ---- AI 域：跨目录引用修正 ----
    "10-AI/agent/Hermes-Agent配置指南.md": {
        "[[../自然语言处理/理论知识]]": "[[大模型与AI-Agent技术资源汇总]]",
        "[[../自然语言处理/实践]]": "[[大模型与AI-Agent技术资源汇总]]",
    },
    "10-AI/大模型与AI-Agent技术资源汇总.md": {
        "[[../自然语言处理/理论知识]]": "[[大模型与AI-Agent技术资源汇总]]",
        "[[../Hermes Agent 配置指南]]": "[[Hermes-Agent配置指南]]",
    },
    "10-AI/ml/从机器学习到大模型-技术演进关键节点.md": {
        "[[大模型与AI Agent 技术资源汇总]]": "[[大模型与AI-Agent技术资源汇总]]",
        "[[Hermes Agent 配置指南]]": "[[Hermes-Agent配置指南]]",
        "[[诗词AI Agent 技术设计方案]]": "[[诗词AI-Agent技术设计方案]]",
    },
    # ---- 运维 ----
    "50-Ops/gitlab/gitlab.md": {
        "[[../CICD/酷旗自动化构建及部署流程]]": "[[酷旗自动化构建及快速部署方案]]",
    },
    "50-Ops/cicd/酷旗自动化构建及快速部署方案.md": {
        "[[酷旗自动化构建及部署流程]]": "",
    },
}

# 已删除文件（0B）的引用 → 移除整行或替换为说明
REMOVED_REFS = {
    "50-Ops/gitlab/gitlab.md",
}


def main() -> None:
    changed = 0
    for rel, pairs in FIXES.items():
        p = VAULT / rel
        if not p.exists():
            print(f"[!缺失] {rel}")
            continue
        t = p.read_text(encoding="utf-8")
        orig = t
        for old, new in pairs.items():
            if old in t:
                t = t.replace(old, new)
                print(f"[改写] {rel}\n    {old}\n -> {new or '(移除)'}")
        if t != orig:
            p.write_text(t, encoding="utf-8")
            changed += 1
    print(f"\n共修改 {changed} 个文件")


if __name__ == "__main__":
    main()
