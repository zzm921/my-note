---
type: moc
domain: ai
status: living
created: 2026-09-16
updated: 2026-09-16
---

# AI 技术 · 地图

> 本域是整个库的重心，7 个子目录与线上站点 7 个分区一一对应。每篇笔记的最终归宿都是「成为一张站点卡片」。

## 子域导航

| 子目录 | 主题 | 站点分区 | 现有笔记 |
|---|---|---|---|
| [[10-AI/agent-engineering/README\|agent-engineering]] | Agent 工程演进（Prompt → Context → Harness → Loop → Graph） | `agent-engineering` | ✅ 13 篇（已认领） |
| [[10-AI/agent/README\|agent]] | Agent 范式（怎么跑） | `agent` | 待建（旧提纲在 `99-Archive/`） |
| [[10-AI/rag/README\|rag]] | RAG 范式与工程 | `rag` | ✅ 9 篇 |
| [[10-AI/protocol/README\|protocol]] | 协议（函数调用 / MCP / A2A / Skills） | `protocol` | ✅ 4 篇（已认领） |
| [[10-AI/eval/README\|eval]] | 评估评测 | `eval` | ✅ 4 篇（已认领） |
| [[10-AI/ops/README\|ops]] | 生产与治理 | `ops` | 📍 复用 agent-engineering 的 6 张卡 |
| [[10-AI/ml/README\|ml]] | 机器学习课程笔记 | `ml` | ✅ 12 篇 |

## 学习路径建议

### 打地基
1. [[01-RAG概念与演进]] — 先建立 RAG 全局观
2. [[1_机器学习导论]] — 建立 ML 全景框架

### 进 Agent
3. `agent/` — ReAct → Plan-Execute → Reflection → Multi-Agent（旧提纲可先看）
4. [[agent-engineering]] — 理解「瓶颈外移」这条主线

### 工程化
5. `rag/03~05` — Advanced / Modular / Graph
6. [[10-AI/ops/README\|ops]] — 让 Agent 跑得住
7. [[10-AI/eval/README\|eval]] — 证明 Agent 真的行

## 待补清单

- [ ] `agent/`：ReAct / Plan-Execute / Reflection / Multi-Agent 四篇
      —— 站点已有这 8 张卡，笔记库**尚未认领**，是可选的下一步
- [ ] `ml/`：需与站点 `ml` 分区核对卡片对应关系

> 已认领的分区（`agent-engineering` / `protocol` / `eval`）：笔记库已是写作源，
> 改笔记 → 跑同步脚本 → 站点生效。详见各域 README 的「与站点的关系」。

## 旧内容去向

`99-Archive/agent-旧提纲/` 下的 29 篇旧提纲曾覆盖本域大部分主题，但内容单薄（多为 1~2KB 提纲）。
**`agent-engineering` / `protocol` / `eval` 三域已由认领的正式笔记取代；`agent` 域仍可参考旧提纲。**
