---
type: moc
domain: ai/protocol
tags: [MCP, A2A, 函数调用, Agent-Skills, 协议]
status: living
created: 2026-09-16
updated: 2026-09-16
---

# 协议 · Protocol

> Agent ↔ 工具、Agent ↔ Agent 的互操作标准。
> 本域笔记**反向认领自站点 `protocol` 分区**，现已成为该分区的写作源。

## 演进脉络

```
函数调用（私有格式）
    ↓ 工具调用标准化
MCP（Agent ↔ 工具/数据源）
    ↓ 不止工具，还要打包能力
Agent Skills（能力封装）
    ↓ Agent 之间也要说话
A2A（Agent ↔ Agent）
```

## 本域全部笔记

| 笔记 | 一句话 |
|---|---|
| [[function-calling]] | 模型以结构化 JSON 发起工具调用；各家私有格式，MCP 的前身 |
| [[mcp]] | Model Context Protocol——工具调用的「USB 标准」 |
| [[a2a]] | Agent 间发现、委托与协作的开放协议 |
| [[agent-skills]] | 把可复用能力打包成「技能」，按需注入上下文 |

## 关键区分

- **MCP 解决「Agent 怎么用工具」** —— 纵向：Agent 到外部资源
- **A2A 解决「Agent 怎么找 Agent」** —— 横向：Agent 到 Agent
- **Agent Skills 解决「能力怎么复用」** —— 封装：把提示词 + 脚本 + 说明打成包

## 与站点的关系

- **发布**：带 `publish: true` / `site: protocol` / `cardId: <id>`
- **站点字段**：各笔记 `site_meta` 块保留卡片渲染字段
- **改法**：改笔记 → 跑同步脚本 → 站点生效
