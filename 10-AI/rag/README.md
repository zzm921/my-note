---
type: moc
domain: ai/rag
tags: [RAG, NaiveRAG, AdvancedRAG, ModularRAG, GraphRAG, AgenticRAG]
status: living
created: 2026-09-16
updated: 2026-09-16
---

# RAG 范式与工程 · 域地图

> 「怎么检索」——外部知识怎么进来、怎么被找到、怎么被用上。
> 与 [[10-AI/agent/README|Agent 范式]] 的分界：那边讲**循环怎么转**，这边讲**上下文怎么来**。`agentic-rag` 是两条线的交汇点。
> 本域 11 篇**反向认领自站点 `rag` 分区**，现已成为该分区的写作源。

## 范式演进脉络

```
五代范式（能力递进）
  ├─ naive-rag          切块 → 向量检索 → 生成，一切的原点与基线
  ├─ advanced-rag       检索前后全链路优化：改写 / 混合 / 重排 / 压缩
  ├─ modular-rag        模块与算子可插拔，按查询复杂度动态组合
  ├─ graph-rag          实体-关系图谱 + 多跳推理，解全局性问题
  └─ agentic-rag        五角色编排 + 预算治理，RAG 变成自治系统

工程分层（离线 / 在线）
  离线：offline-processing        解析 → 清洗 → 切分 → 向量化 → 入库
  在线：online-hybrid-retrieval   查询改写 → 混合召回 → 重排 → 注入

专项增强
  ├─ rag-variants       多模态 / 表格 / 层级索引 / 自适应等变体
  ├─ kb-routing         多知识库路由（D2 决策）
  └─ text-to-sql        结构化查询，把 NL 翻译成 SQL 而非检索
```

## 本域全部笔记

| 笔记 | 站点名 | 难度 | 一句话 |
|---|---|---|---|
| [[00-RAG总表导航]] | 检索增强生成 | 中 | 全库导航：五代范式路线图 + 各类型索引 |
| [[naive-rag]] | 朴素 RAG | 入门 | 极简基线，一切 RAG 的对照原点 |
| [[advanced-rag]] | 高级 RAG | 中 | 查询改写 + 混合检索 + Rerank + 压缩 |
| [[modular-rag]] | 模块化 RAG | 高阶 | 检索/生成/路由拆成可插拔模块与算子 |
| [[graph-rag]] | 知识图谱 RAG | 高阶 | 实体-关系建模 + 多跳，答跨文档关联问题 |
| [[agentic-rag]] | 智能体式 RAG | 高阶 | 五角色编排（路由/检索/评估/生成/守卫）+ 预算治理 |
| [[offline-processing]] | 离线数据处理 | 高阶 | 文档解析、清洗、语义切分、向量化入库 |
| [[online-hybrid-retrieval]] | 在线混合检索策略 | 中 | 向量 + 关键词 + 重排的在线链路 |
| [[rag-variants]] | RAG 专项增强技术 | 高阶 | 多模态 / 表格 / 层级索引等专项方案 |
| [[kb-routing]] | 多知识库路由 | 高阶 | 按问题判定该查哪个知识库 |
| [[text-to-sql]] | Text-to-SQL 结构化查询 | 高阶 | 数值/聚合类问题走 SQL 而非向量检索 |

## 选型速查

| 场景 | 推荐方案 |
|---|---|
| 快速验证、语料结构规整 | [[naive-rag]] |
| 召回质量不稳、需要调优 | [[advanced-rag]] |
| 查询类型混杂（简单/复杂/寒暄） | [[modular-rag]] |
| 问题需要跨文档串联实体关系 | [[graph-rag]] |
| 需要多步检索、自我纠错、控成本 | [[agentic-rag]] |
| 多套知识库需分流 | [[kb-routing]] |
| 问题涉及统计、求和、排行 | [[text-to-sql]] |
| 入库质量差导致下游全崩 | 先修 [[offline-processing]] |
| 召回不全、关键词漏召回 | [[online-hybrid-retrieval]] |

## 与站点的关系

- **发布**：11 篇均带 `publish: true` / `site: rag` / `cardId: <id>`
- **站点字段**：各笔记 `site_meta` 块保留完整卡片渲染字段（`name`/`icon`/`prompts`/`rag_scheme`/`techFilters`…）
- **改法**：改笔记 → 跑同步脚本 → 站点生效
- **源的方向**：本域与 `ml` 相反 —— `rag` 是**站点内容更成熟**，所以由站点反向认领；`ml` 是**笔记更完整**，所以笔记为源、只补发布声明

## 旧提纲去向

`99-Archive/rag-旧提纲/` 下的 9 篇薄提纲（1.7~2.9KB）已被本域正式笔记取代，仅作历史留痕：
`01-RAG概念与演进` / `02-NaiveRAG朴素RAG` / `03-AdvancedRAG进阶RAG` / `04-ModularRAG模块化RAG` /
`05-GraphRAG图谱增强` / `RAG总览` / `RAG评估` / `advanced-rag-碎片` / `naive-rag-碎片`

> 注：原 `RAG评估.md` 属**评估**主题，正式内容已归入 [[10-AI/eval/README|eval 域]] 的
> [[rag-eval]] 与 [[rag-online-eval]]，不在本域重复。

## 交叉引用

- [[10-AI/eval/rag-eval|rag-eval]] / [[10-AI/eval/rag-online-eval|rag-online-eval]] —— RAG 的评估指标与线上评估
- [[10-AI/agent/README|Agent 范式]] —— `agentic-rag` 的循环形态可对照 [[react]] / [[plan-execute]]
- [[10-AI/ops/README|生产与治理]] —— RAG 上线的成本、缓存、可观测性约束
