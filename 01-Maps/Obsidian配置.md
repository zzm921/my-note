---
type: howto
domain: 元
tags: [Obsidian, 同步, Git, 配置]
status: done
created: 2026-09-16
updated: 2026-09-16
---

# Obsidian 配置

> 本库的同步方案：**电脑用 Obsidian + obsidian-git 插件，手机用 Obsidian + MGit**。
> 本文件原为 `库总览.md` 的内容，2026-09-16 拆出，总览页改为知识库导航。

## 方案总览

| 端 | 组合 | 同步方式 |
|---|---|---|
| 电脑 | Obsidian + GitHub + obsidian-git 插件 | 插件自动 commit / push |
| 手机 | Obsidian + MGit | 手动 pull / push |

## 配置流程

### 电脑端

1. 在 GitHub 创建笔记仓库，`git clone` 到本地。
2. 下载安装 Obsidian，**打开文件夹**选择 clone 下来的目录。
3. 打开设置 → 关闭安全模式 → 安装第三方插件 **obsidian-git** → 启用。
4. 配置自动保存（自动 commit / push）的时间间隔。

### 手机端

1. 安装 Obsidian，再安装 MGit。
2. 打开 MGit，配置 SSH key，clone GitHub 笔记仓库。
3. 打开 Obsidian，会自动导入对应的笔记库。

## 注意事项

- **两端不要同时改**，避免冲突；切换设备前先同步一次。
- 本库的 `.obsidian/graph.json` 配了颜色分组与图谱参数，
  若两端版本差异大，图谱显示可能不一致。
- 附件目录已设为 `99-Attachments/`（见 `.obsidian/app.json` 的 `attachmentFolderPath`）。

## 社区

- Obsidian 中文论坛：<https://forum-zh.obsidian.md/>

## 相关

- [[库总览]]
