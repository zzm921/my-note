# -*- coding: utf-8 -*-
"""删除 4 篇空壳文件，有保留价值的内容并入同级地图。

清单：
  1. 欢迎.md                          → 删除（Obsidian 出厂模板，自身说明「可删除」）
  2. 50-Ops/windows/激活.md            → 命令并入 运维-地图.md
  3. 50-Ops/docker/docker常用命令.md   → 命令并入 运维-地图.md
  4. 50-Ops/vm/centos.md               → 内容并入 运维-地图.md

原文副本归档到 99-Archive/空壳清理-2026-09-16/，可随时回查。
"""
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / "99-Archive" / "空壳清理-2026-09-16"

OPS_MAP = ROOT / "50-Ops/运维-地图.md"

MERGE_BODY = """
---

## 速查：常用命令与配置

> 以下内容原为 3 篇独立短记（`windows/激活.md`、`docker/docker常用命令.md`、`vm/centos.md`），
> 2026-09-16 合并至此。原文件已归档到 `99-Archive/空壳清理-2026-09-16/`。

### Windows 激活（KMS）

```bat
slmgr /skms kms.03k.org
slmgr /ato
```

### Docker：清理 none 镜像

```bash
docker rmi $(docker images | grep "none" | awk '{print $3}')
```

### CentOS 虚拟机

**安装后无网络**

```bash
vi /etc/sysconfig/network-scripts/ifcfg-ens33
# ONBOOT=no 改为 ONBOOT=yes
# 追加：DNS1=8.8.8.8

systemctl restart network
```

**开放端口**：见 [参考资料](https://codeantenna.com/a/gdutDTE2Tj)
"""


def archive(src: Path) -> None:
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    dst = ARCHIVE / src.name
    if dst.exists():
        print(f"      (归档已存在) {src.name}")
        return
    shutil.copy2(src, dst)
    print(f"      归档 → 99-Archive/空壳清理-2026-09-16/{src.name}")


def main() -> None:
    apply = "--apply" in sys.argv
    targets = [
        ROOT / "欢迎.md",
        ROOT / "50-Ops/windows/激活.md",
        ROOT / "50-Ops/docker/docker常用命令.md",
        ROOT / "50-Ops/vm/centos.md",
    ]

    if not apply:
        print("(dry-run) 将删除：")
        for t in targets:
            print(f"  - {t.relative_to(ROOT).as_posix()}  ({t.stat().st_size if t.exists() else '?'} B)")
        print("\n并把这 3 篇的内容合并进 50-Ops/运维-地图.md")
        print("加 --apply 执行")
        return

    # 1. 内容并入运维地图
    t = OPS_MAP.read_text(encoding="utf-8")
    if "<!-- merged-ops-stubs -->" not in t:
        t = t.rstrip("\n") + "\n" + MERGE_BODY + "\n<!-- merged-ops-stubs -->\n"
        OPS_MAP.write_text(t, encoding="utf-8", newline="\n")
        print("  ✓ 运维-地图.md ← 3 篇短记内容")

    # 2. 归档并删除
    for src in targets:
        if not src.exists():
            print(f"  - 跳过（不存在）{src.relative_to(ROOT).as_posix()}")
            continue
        print(f"  ✓ {src.relative_to(ROOT).as_posix()}")
        archive(src)
        src.unlink()

    # 3. 清理空目录
    for d in [ROOT / "50-Ops/windows", ROOT / "50-Ops/vm", ROOT / "50-Ops/docker"]:
        if d.exists() and not any(d.iterdir()):
            d.rmdir()
            print(f"  ✓ 清理空目录 {d.relative_to(ROOT).as_posix()}/")

    print()
    print("✓ 空壳清理完成")


if __name__ == "__main__":
    main()
