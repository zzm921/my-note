# -*- coding: utf-8 -*-
"""
为全库无 frontmatter 的笔记批量补写规范 frontmatter。

规则：
  - domain  : 由目录路径决定（映射表）
  - type    : 由文件名/标题/内容特征判定（tutorial / concept / howto / issue / moc / daily）
  - tags    : 标题分词 + 正文高频技术词
  - status  : 默认 done；标题含「todo/待办/WIP」→ draft
  - created : 从正文中提取日期线索，否则留空（不编造）

范围：排除 99-Archive / 99-Attachments / _Templates / 90-Daily / 已有 frontmatter 的文件
已有 frontmatter 的 5 篇老笔记走「升级」分支：保留 created/tags，补 type/domain/status/updated

默认 dry-run，--apply 才写入。
"""
import pathlib
import re
import sys
from datetime import date

ROOT = pathlib.Path(__file__).resolve().parents[2]
SKIP = {".git", ".obsidian", ".workbuddy-ai", ".idea", "99-Archive", "99-Attachments", "_Templates", "90-Daily"}
TODAY = "2026-09-16"

apply = "--apply" in sys.argv

# ---------- domain 映射（按目录前缀，长前缀优先） ----------
DOMAIN_MAP = [
    ("10-AI/ml", "ai/ml"),
    ("10-AI/rag", "ai/rag"),
    ("10-AI/agent", "ai/agent"),
    ("10-AI", "ai"),
    ("20-Backend/node/db", "backend/node/db"),
    ("20-Backend/node/pitfall", "backend/node/pitfall"),
    ("20-Backend/node/tools", "backend/node/tools"),
    ("20-Backend/node/vscode", "backend/node/vscode"),
    ("20-Backend/node", "backend/node"),
    ("20-Backend/python", "backend/python"),
    ("20-Backend/golang", "backend/golang"),
    ("20-Backend", "backend"),
    ("30-Data/mysql", "data/mysql"),
    ("30-Data/redis", "data/redis"),
    ("30-Data", "data"),
    ("40-Network", "network"),
    ("50-Ops/docker", "ops/docker"),
    ("50-Ops/gitlab", "ops/gitlab"),
    ("50-Ops/cicd", "ops/cicd"),
    ("50-Ops/aliyun", "ops/aliyun"),
    ("50-Ops/nas", "ops/nas"),
    ("50-Ops/vm", "ops/vm"),
    ("50-Ops/windows", "ops/windows"),
    ("50-Ops", "ops"),
    ("60-Frontend/typescript", "frontend/typescript"),
    ("60-Frontend/vue", "frontend/vue"),
    ("60-Frontend", "frontend"),
    ("70-Interview", "interview"),
    ("80-Projects", "projects"),
    ("01-Maps", "元"),
]

# ---------- 文件名 → tags 关键词 ----------
KEYWORDS = [
    "TypeScript", "JavaScript", "Node", "NodeJs", "nodejs", "Vue", "CSS", "HTML", "React",
    "Promise", "ESLint", "Puppeteer", "Sequelize", "CommonJS", "ECMAScript", "VSCode",
    "MySQL", "Mysql", "mysql", "Redis", "redis", "NoSQL", "SQL", "索引", "事务隔离", "binlog",
    "redo log", "undo log", "缓存", "持久化", "数据类型", "面试题",
    "TCP", "UDP", "HTTP", "HTTPS", "DNS", "ARP", "NAT", "OSI", "TCPIP",
    "Docker", "GitLab", "Gitlab", "gitlab", "CI/CD", "git", "Git", "Jenkins",
    "阿里云", "负载均衡", "NAS", "CentOS", "虚拟机", "Windows", "激活",
    "RAG", "NaiveRAG", "AdvancedRAG", "ModularRAG", "GraphRAG", "检索", "向量",
    "机器学习", "深度学习", "神经网络", "线性回归", "逻辑回归", "梯度下降", "决策树",
    "非监督学习", "强化学习", "推荐系统", "模型评估", "分类",
    "Python", "pip", "Golang", "Go",
    "诗词", "Agent", "大模型",
]
# 出现顺序稳定化：按关键词长度倒序匹配，避免 "node" 吃掉 "nodejs"
KEYWORDS_SORTED = sorted(set(KEYWORDS), key=len, reverse=True)


def rel(p):
    return p.relative_to(ROOT).as_posix()


def get_domain(p: pathlib.Path) -> str:
    r = rel(p)
    for prefix, dom in DOMAIN_MAP:
        if r.startswith(prefix + "/") or r.startswith(prefix):
            return dom
    return "未分类"


def first_heading(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("#"):
            return line.lstrip("#").strip()
    return ""


def guess_type(p: pathlib.Path, text: str) -> str:
    name = p.name
    if name.lower() in ("readme.md", "summary.md"):
        return "moc"
    # issue 优先（含"解决xx"的排障记录）
    if re.search(r"(踩坑|pitfall|卡死|报错|失败|异常|修复|排查)", name):
        return "issue"
    if re.search(r"(解决|问题)", name) and "面试" not in name:
        return "issue"
    if re.search(r"(设计方案|技术方案|架构设计|设计方案)", name):
        return "tutorial"
    if re.search(r"(安装|配置|部署|命令|使用|插件|规范|方案|优化|指南)", name):
        return "howto"
    if re.search(r"(详解|深入|原理|总结|知识|基础|教程|进阶|高级|学习|介绍|分析|概念|演进)", name):
        return "tutorial"
    if "碎片" in name:
        return "concept"
    if re.search(r"(面试题|面试)", name):
        return "concept"
    return "concept"


def title_words(p: pathlib.Path, text: str) -> list:
    """从文件名/首个标题中切出有意义的中文词块，作为 tags 补充。"""
    stem = re.sub(r"^\d+[_\-]", "", p.stem)          # 去掉 01- / 1_ 前缀
    stem = re.sub(r"\.md$", "", stem)
    words = []
    # 中文词块（2-6 字），按分隔符切
    for chunk in re.split(r"[\s\-_()（）,，、。：:【】\[\]/\\+]+", stem):
        chunk = chunk.strip()
        if not chunk:
            continue
        # 纯中文 2-6 字直接要
        if re.fullmatch(r"[\u4e00-\u9fa5]{2,6}", chunk):
            words.append(chunk)
        else:
            # 含英文：抽出英文单词 / 英文+中文混排的英文部分
            for m in re.findall(r"[A-Za-z][A-Za-z0-9\.\+/#]{1,20}", chunk):
                words.append(m)
    return words


def guess_tags(p: pathlib.Path, text: str) -> list:
    hay = p.stem + "\n" + first_heading(text)
    found = []
    for kw in KEYWORDS_SORTED:
        if kw in hay and kw.lower() not in [f.lower() for f in found]:
            found.append(kw)
        if len(found) >= 5:
            break
    # 标题分词补足（不再用目录名兜底）
    if len(found) < 3:
        for w in title_words(p, text):
            if len(found) >= 4:
                break
            if w.lower() in [f.lower() for f in found]:
                continue
            if w.lower() in ("md", "readme", "summary"):
                continue
            found.append(w)
    # 去重（大小写不敏感），最多 5 个
    out, seen = [], set()
    for f in found:
        k = f.lower()
        if k in seen:
            continue
        seen.add(k)
        out.append(f)
    return out[:5]


def guess_status(p: pathlib.Path, text: str) -> str:
    hay = p.stem + first_heading(text) + text[:400]
    if re.search(r"(todo|TODO|待办|待补|WIP|草稿)", hay):
        return "draft"
    if len(text.strip()) < 300:
        return "draft"
    return "done"


def yaml_list(items):
    return "[" + ", ".join(items) + "]"


# ---------- 老笔记 frontmatter 升级 ----------
LEGACY = [
    "10-AI/agent/Hermes-Agent配置指南.md",
    "10-AI/ml/从机器学习到大模型-技术演进关键节点.md",
    "10-AI/大模型与AI-Agent技术资源汇总.md",
    "80-Projects/诗词KG-RAG_Agent方案/搜韵API分析.md",
    "80-Projects/诗词KG-RAG_Agent方案/搜韵API实测分析.md",
    "80-Projects/诗词KG-RAG_Agent方案/诗词AI-Agent技术设计方案.md",
    "80-Projects/诗词KG-RAG_Agent方案/项目需求与技术计划.md",
]


def split_fm(text):
    """返回 (frontmatter_dict_lines, body)。假定已确认以 --- 开头。"""
    end = text.find("\n---", 3)
    if end < 0:
        return [], text
    block = text[3:end].strip("\n")
    body = text[end + 4 :].lstrip("\n")
    return block.splitlines(), body


def upgrade_legacy():
    from collections import Counter

    print("\n=== 老笔记 frontmatter 升级 ===")
    n = 0
    for k in LEGACY:
        p = ROOT / k
        if not p.exists():
            print(f"  !! 不存在：{k}")
            continue
        t = p.read_text(encoding="utf-8", errors="replace")
        if not t.lstrip().startswith("---"):
            print(f"  !! 无 frontmatter，跳过：{k}")
            continue
        fm_lines, body = split_fm(t)
        keys = [l.split(":", 1)[0].strip() for l in fm_lines if ":" in l]
        if "type" in keys:
            print(f"  -- 已是新格式，跳过：{k}")
            continue
        created = next((l.split(":", 1)[1].strip() for l in fm_lines if l.startswith("created:")), "")
        tags_raw = next((l.split(":", 1)[1].strip() for l in fm_lines if l.startswith("tags:")), "")
        dom = get_domain(p)
        typ = guess_type(p, t)
        new_fm = [
            "---",
            f"type: {typ}",
            f"domain: {dom}",
            f"tags: {tags_raw}" if tags_raw else f"tags: {yaml_list(guess_tags(p, t))}",
            f"status: {guess_status(p, t)}",
        ]
        if created:
            new_fm.append(f"created: {created}")
        new_fm.append(f"updated: {TODAY}")
        new_fm.append("---")
        new_text = "\n".join(new_fm) + "\n\n" + body
        if apply:
            p.write_text(new_text, encoding="utf-8", newline="\n")
            print(f"  ✓ 升级 {k}  (type={typ}, domain={dom})")
        else:
            print(f"  ~ 将升级 {k}  → type={typ}, domain={dom}, tags={tags_raw}")
        n += 1
    print(f"  处理 {n} 篇")
    return n


upgrade_legacy()

if not apply:
    print("\n(dry-run) 加 --apply 写入")
    sys.exit(0)


# ---------- 人工覆写（脚本无法可靠推断的特例） ----------
OVERRIDE = {
    "50-Ops/cicd/酷旗自动化构建及快速部署方案.md": {
        "tags": ["CI/CD", "自动化构建", "部署方案", "Jenkins"],
    },
    "50-Ops/gitlab/自动化部署培训.md": {
        "tags": ["GitLab", "CI/CD", "自动化部署", "培训"],
    },
    "README.md": {"domain": "元", "tags": ["导航", "README"]},
    "SUMMARY.md": {"domain": "元", "tags": ["导航", "目录"]},
    "欢迎.md": {"domain": "元", "type": "moc", "tags": ["Obsidian", "入门"], "status": "done"},
    "20-Backend/golang/readme.md": {"tags": ["Golang", "Go", "后端"]},
    "60-Frontend/js.md": {"tags": ["JavaScript", "面向对象", "原型"]},
    "60-Frontend/html.md": {"tags": ["HTML", "前端基础"]},
    "60-Frontend/CSS.md": {"tags": ["CSS", "前端基础", "布局"]},
    "50-Ops/windows/激活.md": {"tags": ["Windows", "激活", "KMS"]},
    "50-Ops/vm/centos.md": {"tags": ["CentOS", "虚拟机", "运维"]},
}


def apply_override(p, typ, dom, tags, st):
    key = rel(p)
    ov = OVERRIDE.get(key)
    if not ov:
        return typ, dom, tags, st
    return (
        ov.get("type", typ),
        ov.get("domain", dom),
        ov.get("tags", tags),
        ov.get("status", st),
    )


# ---------- 扫描 ----------
targets = []
for p in sorted(ROOT.rglob("*.md")):
    if set(p.parts) & SKIP:
        continue
    t = p.read_text(encoding="utf-8", errors="replace")
    if t.lstrip().startswith("---"):
        continue
    targets.append(p)

print(f"待补 frontmatter：{len(targets)} 篇\n")

plan = []
for p in targets:
    t = p.read_text(encoding="utf-8", errors="replace")
    dom = get_domain(p)
    typ = guess_type(p, t)
    tags = guess_tags(p, t)
    st = guess_status(p, t)
    typ, dom, tags, st = apply_override(p, typ, dom, tags, st)
    plan.append((p, typ, dom, tags, st))

# 输出清单
cur = None
for p, typ, dom, tags, st in plan:
    d = p.parent.as_posix()
    if d != cur:
        print(f"\n--- {d} ---")
        cur = d
    print(f"  {p.name[:36]:36s} | {typ:8s} | {dom:22s} | {yaml_list(tags)[:44]:44s} | {st}")

print(f"\n合计 {len(plan)} 篇")

if not apply:
    print("\n(dry-run) 加 --apply 写入")
    sys.exit(0)

# ---------- 写入 ----------
ok = 0
for p, typ, dom, tags, st in plan:
    t = p.read_text(encoding="utf-8", errors="replace")
    fm = (
        "---\n"
        f"type: {typ}\n"
        f"domain: {dom}\n"
        f"tags: {yaml_list(tags)}\n"
        f"status: {st}\n"
        f"updated: {TODAY}\n"
        "---\n\n"
    )
    p.write_text(fm + t, encoding="utf-8", newline="\n")
    ok += 1

print(f"✓ 已写入 {ok} 篇")
