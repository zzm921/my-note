---
type: moc
domain: ai/agent-engineering
tags: [Agent工程, Prompt工程, Context工程, Harness工程, AI-Agent]
status: living
created: 2026-09-16
updated: 2026-09-16
---

# Agent 工程演进 · 域地图

> 定义轴——从「怎么说」到「谁运行」的五层工程瓶颈外移地图。
> 本域笔记**反向认领自站点 `agent-engineering` 分区**，现已成为该分区的写作源。

## 五层瓶颈外移

| 层 | 问题 | 本域笔记 |
|---|---|---|
| **Prompt 层**（怎么说） | 输出格式与推理质量 | [[prompt-strategy]]、[[structured-output]] |
| **Context 层**（喂什么） | 窗口有限、信息过载 | [[context-mgmt]]、[[context-caching]]、[[memory]] |
| **Harness 层**（环境） | 跑得住、花得起、不出事 | [[cost-governance]]、[[llm-gateway]]、[[sandbox]]、[[fault-injection]]、[[hitl]]、[[security]]、[[task-system]] |
| **Loop 层**（怎么跑） | 单轮循环的范式选择 | → 见 [[Agent范式-地图\|Agent 范式]] |
| **Graph 层**（怎么编排） | 多节点协作拓扑 | → 见 [[Agent范式-地图\|Agent 范式]] |

入口总览：[[agent-engineering]]

## 本域全部笔记

| 笔记 | 一句话 |
|---|---|
| [[agent-engineering]] | 五层瓶颈外移总览地图 |
| [[prompt-strategy]] | Standard / Few-Shot / CoT 三种策略对比 |
| [[structured-output]] | JSON Schema 约束 + CoT/自洽性/思维树 |
| [[context-mgmt]] | 四层压缩：落盘 → 修剪 → 占位 → 摘要 |
| [[context-caching]] | Prompt Caching + 渐进式披露 / JIT 检索 |
| [[memory]] | 跨会话长期记忆与语义召回 |
| [[cost-governance]] | token 预算 / 缓存 / 模型分级 / 并发管控 |
| [[llm-gateway]] | 多模型统一接入与自动路由 |
| [[sandbox]] | 隔离环境执行系统命令 |
| [[fault-injection]] | 两层重试 + 熔断短路 |
| [[hitl]] | 执行前审批门（人在回路） |
| [[security]] | 三层 Guardrails + 注入防御 + 脱敏 |
| [[task-system]] | todo write 任务拆解与调度 |

## 与站点的关系

- **发布**：本域笔记带 `publish: true` / `site: agent-engineering` / `cardId: <id>`，同步脚本据此生成站点卡片
- **站点字段**：各笔记 `site_meta` 块内保留了完整的卡片渲染字段（`name`/`icon`/`difficulty`/`prompts`…）
- **改法**：**改笔记 → 跑同步脚本 → 站点生效**。不要再直接改站点侧文件
- 交叉视图：Harness 层 7 张卡同时出现在站点 `ops` 分区，见 [[生产治理-地图\|生产与治理]]
