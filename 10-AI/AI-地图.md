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
| [[Agent工程演进-地图\|agent-engineering]] | Agent 工程演进（Prompt → Context → Harness → Loop → Graph） | `agent-engineering` | ✅ 13 篇（已认领） |
| [[Agent范式-地图\|agent]] | Agent 范式（怎么跑） | `agent` | ✅ 8 篇（已认领） |
| [[RAG-地图\|rag]] | RAG 范式与工程（怎么检索） | `rag` | ✅ 11 篇（已认领） |
| [[协议-地图\|protocol]] | 协议（函数调用 / MCP / A2A / Skills） | `protocol` | ✅ 4 篇（已认领） |
| [[评估评测-地图\|eval]] | 评估评测 | `eval` | ✅ 4 篇（已认领） |
| [[生产治理-地图\|ops]] | 生产与治理 | `ops` | 📍 复用 agent-engineering 的 6 张卡 |
| [[机器学习-地图\|ml]] | 机器学习课程笔记 | `ml` | ✅ 12 篇（笔记为源） |

## 学习路径建议

### 打地基
1. [[RAG-地图\|rag]] — 先建立 RAG 全局观（五代范式演进）
2. [[1_机器学习导论]] — 建立 ML 全景框架

### 进 Agent
3. [[Agent范式-地图\|agent]] — ReAct → Plan-Execute → Reflection → Multi-Agent
4. [[agent-engineering]] — 理解「瓶颈外移」这条主线

### 工程化
5. [[modular-rag]] / [[graph-rag]] / [[agentic-rag]] — 进阶与自治
6. [[生产治理-地图\|ops]] — 让 Agent 跑得住
7. [[评估评测-地图\|eval]] — 证明 Agent 真的行

## 待补清单

- [ ] `30-Data/{linux,mongodb}`：已在 [[数据-地图]] 登记为「待补主题」，按约定**不建空目录占位**
- [ ] 站点侧同步脚本（`sync_to_site.py`）：笔记 → 站点的自动回写，暂缓

> 已认领的 6 个分区（`agent-engineering` / `agent` / `rag` / `protocol` / `eval` / `ops`）：
> 笔记库已是写作源，改笔记 → 跑同步脚本 → 站点生效。详见各域地图（如 `RAG-地图.md`）的「与站点的关系」。
> `ml` 例外：内容以笔记为准，只补了发布声明。

## 源的方向（重要）

| 域 | 谁的版本更完整 | 处理方式 |
|---|---|---|
| `agent-engineering` / `agent` / `protocol` / `eval` | 相当 | 反向认领站点卡片为笔记源 |
| `rag` | **站点更成熟**（卡片 7~27KB vs 旧提纲 1.7~2.9KB） | 反向认领，旧提纲归档到 `99-Archive/rag-旧提纲/` |
| `ml` | **笔记更完整**（14~16KB vs 卡片 4~5KB） | 笔记为源，只补 `publish` 声明 |

> 判断依据：先抽 3 对同名笔记/卡片比字节数与结构，再决定谁当源。**不要默认笔记一定更全。**

## 旧内容去向

`99-Archive/agent-旧提纲/` 下的 29 篇旧提纲曾覆盖本域大部分主题，但内容单薄（多为 1~2KB 提纲），
**六个已认领分区均已由正式笔记取代**。
`99-Archive/rag-旧提纲/` 存放 RAG 的 9 篇旧提纲，同样已被取代。
