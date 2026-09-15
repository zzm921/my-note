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
| `agent-engineering/` | Agent 工程演进（Prompt → Context → Harness → Loop → Graph） | `agent-engineering` | 待建 |
| `agent/` | Agent 范式（怎么跑） | `agent` | 待建 |
| `rag/` | RAG 范式与工程 | `rag` | 5 篇（01~05） |
| `protocol/` | 协议（函数调用 / MCP / A2A） | `protocol` | 待建 |
| `eval/` | 评估评测 | `eval` | 待建 |
| `ops/` | 生产与治理 | `ops` | 待建 |
| `ml/` | 机器学习课程笔记 | `ml` | 11 篇 |

## 学习路径建议

### 打地基
1. `rag/01-RAG概念与演进.md` — 先建立 RAG 全局观
2. `ml/1_机器学习导论.md` — 建立 ML 全景框架

### 进 Agent
3. `agent/` — ReAct → Plan-Execute → Reflection → Multi-Agent
4. `agent-engineering/` — 理解「瓶颈外移」这条主线

### 工程化
5. `rag/03~05` — Advanced / Modular / Graph
6. `ops/` — 让 Agent 跑得住
7. `eval/` — 证明 Agent 真的行

## 待补清单

- [ ] `agent/`：ReAct / Plan-Execute / Reflection / Multi-Agent 四篇（旧提纲在 `99-Archive/agent-旧提纲/`）
- [ ] `agent-engineering/`：工程演进五层
- [ ] `protocol/`：函数调用、MCP、A2A
- [ ] `eval/`：评测体系、RAGAS
- [ ] `ops/`：沙箱、容错、成本治理
- [ ] `ml/`：课程进度 5~10 尚未整理为完整笔记

## 旧内容去向

`99-Archive/agent-旧提纲/` 下的 29 篇旧提纲曾覆盖本域大部分主题，但内容单薄（多为 1~2KB 提纲）。**待各子域正式笔记建立后，旧提纲仅作参考。**
