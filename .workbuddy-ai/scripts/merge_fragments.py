# -*- coding: utf-8 -*-
"""合并同主题碎片进相邻主文件。

处理清单（经内容复核后，只保留真正单薄的两篇）：
  1. 20-Backend/node/ECMAScript.md  (156字) → 并入 js知识.md
  2. 20-Backend/python/pip下载慢配置阿里源.md (166字) → 并入 后端-地图.md

⚠️ 不做的事：
  - Promise详解.md 虽有 453 行但正文仅 202 字——它是**代码密集型**笔记
    （手写 Promise 实现 + 事件循环面试题），属优质内容，**不合并**。

原文归档到 99-Archive/合并-2026-09-16/，不直接删除。
"""
import re
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / "99-Archive" / "合并-2026-09-16"


def append_section(target: Path, heading: str, body: str, marker: str) -> bool:
    """把一段内容追加到目标文件末尾。幂等：marker 已存在则跳过。"""
    t = target.read_text(encoding="utf-8")
    if marker in t:
        return False
    t = t.rstrip("\n") + f"\n\n---\n\n{heading}\n\n{body.strip()}\n\n{marker}\n"
    target.write_text(t, encoding="utf-8", newline="\n")
    return True


def archive(src: Path) -> None:
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    dst = ARCHIVE / src.name
    if dst.exists():
        print(f"    (归档已存在，跳过) {src.name}")
        return
    shutil.copy2(src, dst)
    print(f"    已归档副本 → 99-Archive/合并-2026-09-16/{src.name}")


def main() -> None:
    apply = "--apply" in sys.argv
    if not apply:
        print("(dry-run)")
        print("将执行：")
        print("  1. ECMAScript.md  → 追加进 js知识.md 【ES6 变量声明】小节")
        print("  2. pip配置        → 追加进 后端-地图.md 【常用配置】小节")
        print("  原文件副本归档到 99-Archive/合并-2026-09-16/")
        print("\n加 --apply 执行")
        return

# ---- 1. ECMAScript → js知识 ----
src = ROOT / "20-Backend/node/ECMAScript.md"
tgt = ROOT / "20-Backend/node/js知识.md"
body = """
### ES6 变量声明：let / const / var

| 关键字 | 作用域 | 说明 |
|---|---|---|
| `var` | 函数作用域（顶层变量） | 有变量提升，可重复声明 |
| `let` | 块级作用域 | 变量，可重新赋值 |
| `const` | 块级作用域 | 常量，声明后不可重新赋值（对象属性仍可改） |

**顶层对象在不同环境下的差异**（常见面试点）：

- 浏览器里顶层对象是 `window`，但 Node 和 Web Worker 没有 `window`。
- 浏览器和 Web Worker 里，`self` 也指向顶层对象，但 Node 没有 `self`。
- Node 里顶层对象是 `global`，但其他环境都不支持。

> 记忆口诀：**浏览器 window / Worker self / Node global，三者互不通用。**

### 解构赋值

从数组或对象中按模式提取值，简化赋值。Node 中常用于 `const { a, b } = obj`
与模块导入 `const { readFile } = require('fs')`。
"""
ok = append_section(tgt, "## ES6 补充（原 ECMAScript.md）", body, "<!-- merged-ecmascript -->")
print(f"  {'✓' if ok else '-'} js知识.md ← ECMAScript.md")
archive(src)
src.unlink()
print(f"  ✓ 已删除 20-Backend/node/ECMAScript.md")

# ---- 2. pip 配置 → 后端-地图 ----
src2 = ROOT / "20-Backend/python/pip下载慢配置阿里源.md"
tgt2 = ROOT / "20-Backend/后端-地图.md"
body2 = """
### Python：pip 换阿里源（解决下载慢）

**第一步**：创建配置文件 `C:\\Users\\<用户名>\\pip\\pip.ini`

**第二步**：写入内容

```ini
[global]
index-url = https://mirrors.aliyun.com/pypi/simple/
[install]
trusted-host = mirrors.aliyun.com
```

> 同理可换清华源 `https://pypi.tuna.tsinghua.edu.cn/simple`。
"""
ok2 = append_section(tgt2, "## 常用环境配置", body2, "<!-- merged-pip -->")
print(f"  {'✓' if ok2 else '-'} 后端-地图.md ← pip配置")
archive(src2)
src2.unlink()
print(f"  ✓ 已删除 20-Backend/python/pip下载慢配置阿里源.md")

print()
print("✓ 合并完成，共 2 组")


if __name__ == "__main__":
    main()
