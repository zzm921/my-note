---
created: 2026-06-27
tags: [hermes, ai-agent, configuration]
---

# Hermes Agent 配置指南

> Hermes Agent 是由 Nous Research 开发的开源 AI 代理框架，支持终端、飞书、Telegram、Discord 等多平台运行。

## 环境信息

| 项目 | 值 |
|------|-----|
| 运行用户 | zhexia |
| 配置文件 | `~/.hermes/config.yaml` |
| 环境变量 | `~/.hermes/.env` |
| 笔记仓库 | `~/my-note`（Obsidian Vault） |
| 当前模型 | deepseek-v4-flash（阿里云 DashScope） |
| 飞书集成 | ✅ 已配置 |

---

## 常用 CLI 命令

### 基础操作

```bash
hermes              # 启动交互式对话
hermes chat -q "xxx"  # 单次查询
hermes --continue   # 恢复上次会话
hermes config       # 查看配置
hermes config edit  # 编辑配置
```

### 模型与提供商

```bash
hermes model              # 交互式切换模型/提供商
hermes config set model.provider <name>   # 设置提供商
hermes config set model.default <model>   # 设置模型
```

### 技能管理

```bash
hermes skills list          # 列出已安装技能
hermes skills search <关键词>  # 搜索技能
hermes skills install <id>   # 安装技能
hermes skills config         # 配置技能
```

### 定时任务

```bash
hermes cron list            # 列出定时任务
hermes cron create <schedule>  # 创建
hermes cron pause/resume <id>  # 暂停/恢复
hermes cron remove <id>       # 删除
```

### 会话管理

```bash
hermes sessions list        # 列出最近会话
hermes sessions rename <id>  # 重命名
hermes sessions delete <id>  # 删除
```

---

## 当前定时任务

| 任务 | 时间 | 说明 |
|------|------|------|
| AI热点日报 | 每天 9:00 | 搜索6大平台（知乎/36氪/微博/百度/头条/公众号）的大模型、AI Agent 热门资讯，带原文链接推送至飞书 |

---

## 常用斜杠命令（会话中使用）

| 命令 | 说明 |
|------|------|
| `/model <name>` | 切换模型 |
| `/new` | 新会话 |
| `/retry` | 重试上次回复 |
| `/stop` | 停止后台进程 |
| `/compress` | 手动压缩上下文 |
| `/skills` | 搜索/安装技能 |
| `/cron` | 管理定时任务 |
| `/yolo` | 跳过命令审批 |
| `/platforms` | 查看平台连接状态 |

---

## 笔记仓库集成

笔记仓库地址：`git@github.com:zzm921/my-note.git`

通过 Hermes + Obsidian 技能可直接：
- **创建笔记**：在 `~/my-note` 下写入 `.md` 文件
- **搜索笔记**：使用 `search_files` 搜索笔记内容
- **编辑笔记**：使用 `patch` 或 `write_file` 修改

> 需在 `~/.hermes/.env` 中设置：
> ```
> OBSIDIAN_VAULT_PATH=/home/zhangzheming/my-note
> ```
> 设置后重启 Hermes 生效。

---

## 飞书集成

当前通过飞书（Feishu）与 Hermes 交互，支持：
- 文本对话
- 文件传输（MEDIA: 路径）
- Markdown 渲染
- 定时任务推送

---

## 日常维护

```bash
hermes doctor          # 健康检查
hermes update          # 更新 Hermes
hermes status          # 组件状态
hermes insights        # 使用分析
```

---

## 文档链接

- 官方文档：https://hermes-agent.nousresearch.com/docs
- GitHub：https://github.com/NousResearch/hermes-agent