# -*- coding: utf-8 -*-
"""给「网络原理基础（上）/（下）」加互相链接 + 接回网络地图。

另外把两篇的 md 链接改为 wiki 链接不是必须的（它们本来没有内部链接），
这里只追加导航块。
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]
NET = ROOT / "40-Network"

MARK = "<!-- net-nav -->"

PAIR = [
    ("网络原理基础(上)", "网络原理基础（上）", "网络原理基础(下)", "网络原理基础（下）", "上"),
    ("网络原理基础(下)", "网络原理基础（下）", "网络原理基础(上)", "网络原理基础（上）", "下"),
]


def main() -> None:
    apply = "--apply" in sys.argv
    n = 0
    for stem, title, other_stem, other_title, which in PAIR:
        p = NET / f"{stem}.md"
        if not p.exists():
            print(f"  ! 缺失 {stem}.md")
            continue
        t = p.read_text(encoding="utf-8")
        if MARK in t:
            print(f"  - 已处理 {stem}")
            continue

        if which == "上":
            nav = (
                "\n---\n\n## 导航\n\n"
                f"- 接续：[[{other_stem}|{other_title}]]\n"
                "- 同域：[[网络层-ARP协议详解]] · [[网络层-NAT协议详解]] · [[HTTP协议详解]]\n"
                "- 索引：[[计算机网络-地图]]\n"
            )
        else:
            nav = (
                "\n---\n\n## 导航\n\n"
                f"- 上篇：[[{other_stem}|{other_title}]]\n"
                "- 同域：[[应用层-DNS域名系统详解]] · [[应用层-常见协议总结]] · [[OSI和TCPIP网络分层模型详解]]\n"
                "- 索引：[[计算机网络-地图]]\n"
            )

        new = t.rstrip("\n") + "\n" + nav + MARK + "\n"
        if apply:
            p.write_text(new, encoding="utf-8", newline="\n")
        n += 1
        print(f"  ✓ {stem}  加导航")

    print()
    print(f"{'✓ 已处理' if apply else '将处理'} {n} 篇")
    if not apply:
        print("(dry-run) 加 --apply")


if __name__ == "__main__":
    main()
