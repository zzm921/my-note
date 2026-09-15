---
type: moc
domain: ai/eval
tags: [评测, RAGAS, 可观测性, 离线评测, AI-Agent]
status: living
created: 2026-09-16
updated: 2026-09-16
---

# 评估评测 · Eval

> 从离线确定性断言到线上反馈闭环——回答「Agent 到底行不行」。
> 本域笔记**反向认领自站点 `eval` 分区**，现已成为该分区的写作源。

## 核心命题

**能力 ≠ 一致性。** 一次跑通不算数，要能在 CI 里稳定复现。

## 分层评测体系

| 层级 | 手段 | 对应笔记 |
|---|---|---|
| **L0 任务层** | 端到端任务断言 | [[agent-eval]] |
| **L1 架构层** | 确定性断言挂 CI（路由 / 检索 / 闸门） | [[agent-eval]]、[[rag-eval]] |
| **L2 语义层** | 语义评分 | [[rag-eval]] |
| **L3 生成层** | RAGAS 生成指标 | [[rag-eval]] |
| **线上闭环** | 在线采集 → 用户反馈 → 回流评测 | [[rag-online-eval]] |
| **可观测性** | 日志 + 指标 + 链路追踪三支柱 | [[observability-eval]] |

## 本域全部笔记

| 笔记 | 一句话 |
|---|---|
| [[agent-eval]] | 企业级 Agent 评测：L0 任务层 / L1 架构层确定性断言挂 CI |
| [[rag-eval]] | RAG 四层评测：确定性回归 → 语义评分 → RAGAS → 人工 |
| [[rag-online-eval]] | 线上自动评测闭环，让「是不是变好了」有数据回答 |
| [[observability-eval]] | 可观测性三支柱，单进程全链路运行记录 |

## 与站点的关系

- **发布**：带 `publish: true` / `site: eval` / `cardId: <id>`
- **注意**：`rag-eval` / `rag-online-eval` 两张卡在站点 `rag` 分区**也出现**（交叉引用），本站点用 `tags.md` 控制顺序，笔记库只保留一份实体
- **改法**：改笔记 → 跑同步脚本 → 站点生效
