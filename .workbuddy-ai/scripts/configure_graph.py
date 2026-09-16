# -*- coding: utf-8 -*-
"""配置 Obsidian 图谱颜色分组 + 过滤规则。

目的：README 改名解决「同名节点」后，再让图谱一眼能看出**域归属**。

配色原则：
  - 核心笔记域（10-AI / 20-Backend / 30-Data / 40-Network / 50-Ops）
    用鲜艳色，是图谱主体
  - 导航层（01-Maps / *-地图）用中性色
  - 归档 / 日报 / 模板 用灰色系淡化，避免干扰

Obsidian colorGroups 结构：
  {"query": "path:10-AI", "color": {"a": 1, "rgb": 0xRRGGBB}}
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]
GJ = ROOT / ".obsidian" / "graph.json"

# (查询表达式, RGB, 说明)
GROUPS = [
    ("path:10-AI",                     0x7F77DD, "AI 技术（紫）"),
    ("path:20-Backend",                0x378ADD, "后端（蓝）"),
    ("path:30-Data",                   0x1D9E75, "数据（青绿）"),
    ("path:40-Network",                0xD85A30, "计算机网络（珊瑚）"),
    ("path:50-Ops",                    0xBA7517, "运维（琥珀）"),
    ("path:60-Frontend",               0xD4537E, "前端（粉）"),
    ("path:70-Interview",              0x639922, "面试题（绿）"),
    ("path:80-Projects",               0x534AB7, "自研项目（深紫）"),
    ("path:01-Maps",                   0x888780, "地图索引（灰）"),
    ("path:99-Archive",                0xB4B2A9, "归档（浅灰）"),
    ("path:90-Daily",                  0xD3D1C7, "日报（更浅灰）"),
    ("path:_Templates",                0xB4B2A9, "模板（浅灰）"),
]


def main() -> None:
    apply = "--apply" in sys.argv

    d = json.loads(GJ.read_text(encoding="utf-8"))

    d["colorGroups"] = [
        {"query": q, "color": {"a": 1, "rgb": rgb}}
        for q, rgb, _ in GROUPS
    ]
    d["collapse-color-groups"] = False

    # 隐藏未解析链接与附件，图谱更干净
    d["hideUnresolved"] = True
    d["showAttachments"] = False
    d["showTags"] = False
    d["showOrphans"] = True

    # 布局微调：同一域的节点更容易聚拢
    d["linkDistance"] = 180
    d["linkStrength"] = 0.8
    d["repelStrength"] = 12
    d["centerStrength"] = 0.45

    print("=" * 62)
    print("图谱颜色分组")
    print("=" * 62)
    for q, rgb, desc in GROUPS:
        print(f"  #{rgb:06X}  {desc:24s} {q}")
    print()
    print("其他调整：")
    print("  hideUnresolved   = true   隐藏未解析链接")
    print("  linkDistance     = 180    （原 250）节点更聚拢")
    print("  repelStrength    = 12     （原 10）")
    print("  collapse-color-groups = false  展开颜色分组面板")

    if apply:
        GJ.write_text(
            json.dumps(d, ensure_ascii=False, indent=2),
            encoding="utf-8", newline="\n",
        )
        print("\n✓ 已写入 .obsidian/graph.json")
        print("  提示：Obsidian 中图谱面板可能需要重开一次才生效。")
    else:
        print("\n(dry-run) 加 --apply 执行")


if __name__ == "__main__":
    main()
