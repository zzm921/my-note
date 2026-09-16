# -*- coding: utf-8 -*-
"""
把站点 content/*.md 卡片「反向认领」为笔记库源文件。

背景：
  站点 4 个分区（agent-engineering / protocol / eval / ops）的 21 张卡片
  当初是直接写在站点侧的，笔记库没有源头。本脚本把它们转成笔记库源文件，
  落在 10-AI/<分区>/ 下，让「笔记库 = 唯一源」成立。

转换规则：
  - 保留卡片全部站点字段（id/name/shortDesc/icon/difficulty/accent/prompts...）
  - 叠加笔记规范字段（type/domain/tags/status/created/updated）
  - 叠加发布字段（publish: true / site: <分区> / cardId: <id>）
  - 正文原样保留（卡片正文从 ## 开始，不含 H1，符合站点要求）
  - 首行插入 H1 标题（笔记库要求），用 name 作为标题

跨分区复用：ops 与 agent-engineering 共享 6 张卡（Harness 层），
  这些卡只在 agent-engineering 下建实体，ops 目录用 README 指向，避免双写。

默认 dry-run，--apply 才执行。
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
NOTE = ROOT
SITE = pathlib.Path(r"D:\workspace\my-agent-lab\backend\content")
TODAY = "2026-09-16"

apply = "--apply" in sys.argv

# 分区 → (笔记目录, 卡片顺序, 域标签, 分区中文名)
SECTIONS = [
    (
        "agent-engineering",
        "10-AI/agent-engineering",
        ["agent-engineering", "prompt-strategy", "structured-output", "context-mgmt",
         "context-caching", "memory", "cost-governance", "llm-gateway", "sandbox",
         "fault-injection", "hitl", "security", "task-system"],
        "ai/agent-engineering",
        "Agent 工程演进",
    ),
    (
        "agent",
        "10-AI/agent",
        ["react", "plan-execute", "reflection", "rewoo", "llm-compiler",
         "multi-agent", "task-driven-agent", "multimodal-agent"],
        "ai/agent",
        "Agent 范式",
    ),
    (
        "protocol",
        "10-AI/protocol",
        ["function-calling", "mcp", "a2a", "agent-skills"],
        "ai/protocol",
        "协议 · Protocol",
    ),
    (
        "eval",
        "10-AI/eval",
        ["agent-eval", "rag-eval", "rag-online-eval", "observability-eval"],
        "ai/eval",
        "评估评测",
    ),
    (
        "ops",
        "10-AI/ops",
        [],  # ops 的 6 张卡都在 agent-engineering 下建实体
        "ai/ops",
        "生产与治理",
    ),
]


def parse_card(path: pathlib.Path):
    t = path.read_text(encoding="utf-8")
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", t, re.S)
    if not m:
        return None, t
    return m.group(1), t[m.end():]


def fm_get(fm: str, key: str) -> str:
    for l in fm.splitlines():
        if l.startswith(key + ":"):
            return l.split(":", 1)[1].strip()
    return ""


def to_notes_tags(fm: str, section: str) -> list:
    """站点 tags -> 笔记 tags（清掉连字符风格，补分区标签）。"""
    raw = fm_get(fm, "tags")
    items = []
    if raw.startswith("[") and raw.endswith("]"):
        items = [x.strip() for x in raw[1:-1].split(",") if x.strip()]
    out = list(items)
    for extra in (section, "AI-Agent"):
        if extra.lower() not in [i.lower() for i in out]:
            out.append(extra)
    return out[:6]


def guess_type(fm: str, body: str) -> str:
    """站点卡片基本是概念讲解类。"""
    return "concept"


def build_note(card_id: str, fm: str, body: str, section: str, domain: str,
               section_dev: str) -> str:
    name = fm_get(fm, "name") or card_id
    short = fm_get(fm, "shortDesc")
    card_tags = to_notes_tags(fm, section_dev)

    head = [
        "---",
        "type: concept",
        f"domain: {domain}",
        f"tags: [{', '.join(card_tags)}]",
        "status: done",
        "created: " + TODAY,
        "updated: " + TODAY,
        "",
        "# —— 以下为站点卡片字段（同步回 my-agent-lab 时保留） ——",
        fm,
        "",
        "# —— 发布声明 ——",
        "publish: true",
        f"site: {section}",
        f"cardId: {card_id}",
        "---",
        "",
        f"# {name}",
        "",
    ]
    # 摘要行
    if short:
        head.append(f"> {short}")
        head.append("")
    return "\n".join(head) + "\n" + body.lstrip("\n")


total = 0
created_dirs = []

for section, rel, cards, domain, cn in SECTIONS:
    target_dir = NOTE / rel
    print("=" * 62)
    print(f"分区 {section}（{cn}） → {rel}")
    if not cards:
        print("  （无独立卡片，仅建 README 指向 agent-engineering）")
        created_dirs.append((target_dir, section, cn, domain, rel))
        continue
    for cid in cards:
        src = SITE / f"{cid}.md"
        if not src.exists():
            print(f"  !! 源不存在：{src}")
            continue
        fm, body = parse_card(src)
        if fm is None:
            print(f"  !! 无 frontmatter：{cid}")
            continue
        note = build_note(cid, fm, body, section, domain, section)
        dst = target_dir / f"{cid}.md"
        print(f"  {cid:24s} → {rel}/{cid}.md  ({len(note.encode('utf-8'))}B)")
        if apply:
            target_dir.mkdir(parents=True, exist_ok=True)
            if dst.exists():
                print(f"     !! 已存在，跳过")
                continue
            dst.write_text(note, encoding="utf-8", newline="\n")
        total += 1

print()
print(f"合计 {total} 篇")
if not apply:
    print("(dry-run) 加 --apply 执行")
    sys.exit(0)
print("✓ 完成")
