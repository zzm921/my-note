# -*- coding: utf-8 -*-
"""
合并 TypeScript 碎片笔记。

诊断结论：
  - 1基础.md  = 基础篇正文 + 尾部一段「声明文件【todo】」的残缺副本
  - 2声明文件.md = 声明文件完整版（应取代 1 尾部残缺副本）
  - 3内置对象.md = 内置对象小节
  - 4进阶.md   = 高级类型 / 枚举
  - 5类.md     = 纯大纲草稿（与 基础知识.md「类」章节重复）
  - 基础知识.md = 独立知识体系（基础类型/变量/接口/类/函数/泛型…），保留

产出：
  60-Frontend/typescript/TypeScript教程-xcatliu.md  （1基础 截断尾部 + 2 + 3 + 4 顺序拼接）
  60-Frontend/typescript/基础知识.md                 （原样保留，补 frontmatter）
  被合并的原文件 → 99-Archive/typescript-碎片/

默认 dry-run，--apply 才执行。
"""
import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
TS = ROOT / "60-Frontend" / "typescript"
ARCHIVE = ROOT / "99-Archive" / "typescript-碎片"
TARGET = TS / "TypeScript教程-xcatliu.md"

apply = "--apply" in sys.argv


def read(name):
    return (TS / name).read_text(encoding="utf-8")


def norm_sep(s):
    return s.replace("\r\n", "\n").replace("\r", "\n").strip("\n")


# ---- 1. 切掉 1基础.md 尾部的「声明文件【todo】」残缺副本 ----
t1 = norm_sep(read("1基础.md"))
marker = "### 声明文件【todo】"
if marker in t1:
    t1_base = t1[: t1.index(marker)].rstrip("\n")
    dropped = t1[t1.index(marker) :]
else:
    t1_base = t1
    dropped = ""
print(f"[1基础] 保留 {len(t1_base)} 字符，丢弃尾部残缺副本 {len(dropped)} 字符")

t2 = norm_sep(read("2声明文件.md"))
t3 = norm_sep(read("3内置对象.md"))
t4 = norm_sep(read("4进阶.md"))
t5 = norm_sep(read("5类.md"))

# ---- 2. 组装新文档 ----
FRONT = """---
type: tutorial
domain: frontend/typescript
tags: [TypeScript, 类型系统, 教程, xcatliu]
status: done
source: https://ts.xcatliu.com/
created: 2026-09-16
updated: 2026-09-16
---

# TypeScript 教程（xcatliu）

> 本文由原 `1基础` / `2声明文件` / `3内置对象` / `4进阶` 四篇碎片合并而成，
> 内容来源：[TypeScript 入门教程](https://ts.xcatliu.com/)。

## 目录

- [一、基础篇](#一基础篇)
- [二、声明文件](#二声明文件)
- [三、内置对象](#三内置对象)
- [四、进阶篇](#四进阶篇)
- [附：类 · 学习大纲](#附类--学习大纲)

---

## 一、基础篇

"""

body = FRONT + t1_base + "\n\n---\n\n## 二、声明文件\n\n" + t2
body += "\n\n---\n\n## 三、内置对象\n\n" + t3
body += "\n\n---\n\n## 四、进阶篇\n\n" + t4

if t5:
    body += (
        "\n\n---\n\n## 附：类 · 学习大纲\n\n"
        "> 以下为原始学习大纲草稿（OOP 概念速览）。完整讲解见 [[基础知识]] 的「类」章节。\n\n"
        + t5
    )

body = body.rstrip("\n") + "\n"

print(f"[合并] 新文档 {len(body.encode('utf-8'))} 字节 → {TARGET.name}")
for n in ["1基础.md", "2声明文件.md", "3内置对象.md", "4进阶.md", "5类.md"]:
    print(f"  [归档] {n} → 99-Archive/typescript-碎片/")

if not apply:
    print("\n(dry-run) 加 --apply 执行")
    sys.exit(0)

# ---- 3. 执行 ----
if TARGET.exists():
    print(f"!! 目标已存在，跳过：{TARGET}")
    sys.exit(1)

ARCHIVE.mkdir(parents=True, exist_ok=True)
TARGET.write_text(body, encoding="utf-8", newline="\n")
print(f"✓ 写入 {TARGET}")

for n in ["1基础.md", "2声明文件.md", "3内置对象.md", "4进阶.md", "5类.md"]:
    src = TS / n
    if src.exists():
        dst = ARCHIVE / n
        if dst.exists():
            print(f"!! 归档目标已存在，跳过：{dst}")
            continue
        shutil.move(str(src), str(dst))
        print(f"✓ 归档 {n}")

print("\n完成。")
