# Modular RAG 模块化 RAG

## 定义

Modular RAG 把 RAG 拆成**独立、可插拔的模块**，通过调度器（Orchestrator）按需组装。相比 Advanced RAG，新增了**路由器、多跳/迭代检索、自检/校验**等模块，模块之间解耦，可以自由替换升级。

## 核心模块

| 模块 | 职责 |
|---|---|
| 路由器（Router） | 判断问题类型，分派到不同检索路径（向量/图谱/API/直接回答） |
| 查询引擎（Query Engine） | 组织多次检索，支持迭代与多跳 |
| 检索器（Retriever） | 具体执行召回（向量、BM25、图谱等可插拔） |
| 重排器（Reranker） | 精排候选 |
| 记忆模块（Memory） | 携带历史对话与任务状态 |
| 校验器（Validator） | 自检答案是否充分、是否满足约束，决定是否重试 |
| 任务适配器 | 将特定任务转成检索 + 生成子流程 |

## 关键模式

### 1. 路由器（Routing）

```
route = router.classify(query)      # 意图/主题分类
case route:
  "向量检索"   -> vector_retriever
  "精确匹配"   -> sql/bm25
  "多跳推理"   -> graph_rag
  "闲聊/常识"  -> llm_direct
```

### 2. 多跳 / 迭代循环检索（Multi-hop / Iterative Retrieval）

一个复杂问题拆成多步，每步检索、生成中间答案，再带中间答案进行下一步，类似思维链。

```
answer = ""
for step in 1..max_steps:
    need   = planner.next_need(query, answer)   # 决定下一步查什么
    chunks = retriever.search(need)
    answer = llm.generate(query, answer, chunks)
    if validator.is_satisfied(answer): break
```

### 3. 自检 / 校验（Self-reflective）

模型对自己的答案做一次"质检"，不合格则重新检索或换策略。

```
answer = generate(query, context)
score  = validator.check(answer, context, query)   # 充分性/相关性/事实性
if score < threshold:
    refine_query = rewrite(query, feedback)        # 改进查询
    retry
```

### 4. 模块解耦与可插拔调度

每个模块定义标准接口（输入/输出），调度器按配置组装流程，替换任一模块不影响其他模块。

```
pipeline = Pipeline([
    RouterModule(config),
    RetrieverModule(kind="hybrid"),
    RerankModule(top_n=5),
    GenerateModule(model=...),
    ValidateModule(retry=2)
])
```

## 与 Naive / Advanced 的区别

| 能力 | Naive | Advanced | Modular |
|---|---|---|---|
| 固定流水线 | ✅ | ✅ | ❌（可组装） |
| 检索优化/重排 | ❌ | ✅ | ✅ |
| 路由分发 | ❌ | ❌ | ✅ |
| 多跳/迭代检索 | ❌ | ❌ | ✅ |
| 自检/校验 | ❌ | ❌ | ✅ |
| 模块可插拔 | ❌ | ❌ | ✅ |

## 适用场景

- 问题类型多样、需要分类处理的问答系统
- 复杂多步推理任务（研究报告、多文档综合）
- 需要持续迭代优化的生产系统
