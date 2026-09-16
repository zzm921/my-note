---
type: moc
domain: ai/agent
tags: [Agent范式, ReAct, Plan-and-Execute, Reflection, 多智能体]
status: living
created: 2026-09-16
updated: 2026-09-16
---

# Agent 范式 · 域地图

> 「怎么跑」——Agent 内部的循环形态与协作拓扑。
> 与 [[Agent工程演进-地图|Agent 工程演进]]（定义轴）互补：那边讲「瓶颈在哪一层」，这边讲「循环怎么转」。
> 本域 8 篇**反向认领自站点 `agent` 分区**，现已成为该分区的写作源。

## 范式演进脉络

```
单循环范式
  ├─ react            思考-行动交替，一切范式的基座
  ├─ plan-execute     先规划再执行，复杂任务更稳
  └─ reflection       草稿-批评-修订，质量迭代

省 token / 提并行
  ├─ rewoo            计划与观察解耦，变量占位
  └─ llm-compiler     计划编译成 DAG，无依赖处并行

自主与协作
  ├─ task-driven-agent  任务队列自举，持续推动
  └─ multi-agent        Orchestrator + subagent 分工
```

## 本域全部笔记

| 笔记 | 一句话 |
|---|---|
| [[react]] | 观察 → 思考 → 行动 → 观察，所有后续范式的基座 |
| [[plan-execute]] | 先拆解为子步骤，再逐个执行 |
| [[reflection]] | 草稿—批评—修订三阶段迭代 |
| [[rewoo]] | Planner / Worker / Solver 三段解耦，变量占位省 token |
| [[llm-compiler]] | 计划编译成 DAG，无依赖步骤并行 |
| [[multi-agent]] | Orchestrator 统一拆解调度，subagent 按角色协作 |
| [[task-driven-agent]] | 任务队列自举 + 优先级执行（BabyAGI / AutoGPT 系） |
| [[multimodal-agent]] | 图像 / UI / 图表理解与视觉操作 |

## 选型速查

| 场景 | 推荐范式 |
|---|---|
| 需要实时外部信息、步骤不确定 | [[react]] |
| 任务复杂、步骤可预先拆解 | [[plan-execute]] |
| 输出质量要求高、可反复打磨 | [[reflection]] |
| 调用成本敏感、计划稳定 | [[rewoo]] |
| 子任务可并行、依赖清晰 | [[llm-compiler]] |
| 需要多个专业角色协作 | [[multi-agent]] |
| 开放式目标、需要长程自主推进 | [[task-driven-agent]] |
| 涉及图像 / 界面操作 | [[multimodal-agent]] |

## 其他笔记

- [[Hermes-Agent配置指南]] —— 工具链配置，非站点卡片

## 与站点的关系

- **发布**：8 篇均带 `publish: true` / `site: agent` / `cardId: <id>`
- **站点字段**：各笔记 `site_meta` 块保留了完整卡片渲染字段（`name`/`icon`/`prompts`/`mode`/`strategy`…）
- **改法**：改笔记 → 跑同步脚本 → 站点生效
- **交叉引用**：站点 `rag` 分区的 `agentic-rag` 与本站 [[react]] 相关，但笔记库中 `agentic-rag` 归属 `10-AI/rag/`
