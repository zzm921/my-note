# -*- coding: utf-8 -*-
"""README → 域内唯一名 批量改名

问题：Obsidian 图谱按**文件名**标识节点，不显示文件夹。
      19 个 README 在图上全是同名节点，无法区分。

方案：改名为「<目录名>-地图.md」，域内唯一、图谱可直接辨识。

安全约定（吸取之前 git 中文路径截断的教训）：
  - 用 Python shutil.move，不用 git mv
  - 先 dry-run，逐条打印
  - 改名后自动改写全库引用（[[README]] → [[新名]]）
  - 幂等：目标已存在则跳过
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]

# 目录 → 新文件名（不含 .md）
RENAME = {
    ".": "库总览",
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


def md_files():
    for p in ROOT.rglob("*.md"):
        parts = p.parts
        if ".git" in parts or ".obsidian" in parts or ".workbuddy-ai" in parts:
            continue
        yield p


def main() -> None:
    apply = "--apply" in sys.argv

    plan = []          # (src, dst, new_stem, dir_path)
    problems = []

    for d, stem in RENAME.items():
        src = (ROOT / d / "README.md") if d != "." else (ROOT / "README.md")
        if not src.exists():
            problems.append(f"源不存在：{src.relative_to(ROOT).as_posix()}")
            continue
        dst = src.with_name(stem + ".md")
        plan.append((src, dst, stem, d))

    # 唯一性校验：新名字不能与库内任何 md 撞名
    existing_stems = {}
    for p in md_files():
        existing_stems.setdefault(p.stem, []).append(p.relative_to(ROOT).as_posix())

    print("=" * 74)
    print("改名计划")
    print("=" * 74)
    for src, dst, stem, d in plan:
        mark = "  "
        if stem in existing_stems:
            others = [x for x in existing_stems[stem]
                      if x != src.relative_to(ROOT).as_posix()]
            if others:
                mark = "❌"
                problems.append(f"新名撞车：{stem} 已存在于 {others}")
        print(f"{mark} {src.relative_to(ROOT).as_posix():42s} → {dst.name}")

    print()
    if problems:
        print("⚠️  发现问题：")
        for x in problems:
            print("   -", x)
        if not apply:
            print("\n（dry-run 结束，未做任何改动）")
        return

    if not apply:
        print(f"（dry-run，共 {len(plan)} 个文件待改名，加 --apply 执行）")
        return

    # ---- 执行改名 ----
    done = []
    for src, dst, stem, d in plan:
        if dst.exists():
            print(f"  跳过（目标已存在）: {dst.name}")
            continue
        src.rename(dst)
        done.append((src, dst, stem))
        print(f"  ✓ {src.relative_to(ROOT).as_posix()} → {dst.name}")

    # ---- 改写全库引用 ----
    # [[README]] / [[README|别名]] / [[../README]] / [[10-AI/README|xxx]]
    # 统一策略：按目录上下文替换。简单可靠做法是不动 wiki 链接，
    # 因为 Obsidian 的 [[README]] 在改名后会失效 —— 必须逐条按原路径重写。
    print()
    print("=" * 74)
    print("改写引用")
    print("=" * 74)

    # 路径 → 新 stem 映射（用于解析 [[a/b/README|alias]] 形式）
    path_map = {}
    for src, dst, stem, d in plan:
        rel = src.relative_to(ROOT).with_suffix("").as_posix()   # 如 10-AI/rag/README
        path_map[rel] = stem

    fixed_files = 0
    fixed_refs = 0

    for f in md_files():
        t = f.read_text(encoding="utf-8")
        orig = t

        def repl(m):
            nonlocal fixed_refs
            inner = m.group(1)
            # 拆出路径部分与别名部分
            if "|" in inner:
                target, alias = inner.split("|", 1)
            else:
                target, alias = inner, None
            tgt = target.strip().lstrip("/")
            # 去掉可能的 .md
            if tgt.endswith(".md"):
                tgt = tgt[:-3]

            # 命中：路径以 README 结尾
            if tgt.split("/")[-1] == "README":
                # 优先用完整路径匹配
                if tgt in path_map:
                    new = path_map[tgt]
                else:
                    # 只有 [[README]] 这种裸名 —— 无法确定是哪个域，
                    # 保留不动并记账（下面单独报告）
                    return m.group(0)
                fixed_refs += 1
                if alias is not None:
                    return f"[[{new}|{alias}]]"
                return f"[[{new}]]"
            return m.group(0)

        t = re.sub(r"\[\[([^\]\n]+)\]\]", repl, t)
        if t != orig:
            f.write_text(t, encoding="utf-8", newline="\n")
            fixed_files += 1

    print(f"  改写文件数：{fixed_files}")
    print(f"  改写引用数：{fixed_refs}")

    # ---- 报告残留的裸 [[README]] ----
    print()
    print("=" * 74)
    print("残留裸引用检查（[[README]] 这种无法自动定位）")
    print("=" * 74)
    leftover = []
    for f in md_files():
        t = f.read_text(encoding="utf-8", errors="ignore")
        for i, line in enumerate(t.splitlines(), 1):
            if re.search(r"\[\[README(\||\]\])", line):
                leftover.append((f.relative_to(ROOT).as_posix(), i, line.strip()[:100]))
    if leftover:
        for rel, ln, txt in leftover:
            print(f"  {rel}:{ln}  {txt}")
    else:
        print("  ✓ 无残留")

    print()
    print(f"✓ 改名完成：{len(done)} 个文件")


if __name__ == "__main__":
    main()
