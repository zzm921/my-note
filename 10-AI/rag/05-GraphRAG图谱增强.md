# Graph RAG 图谱增强

## 定义

Graph RAG 在 RAG 中引入**知识图谱**：把文档中的实体和关系抽取出来构造成图，检索时既做向量召回，也在图上做**多跳遍历与全局推理**，用于解决纯向量检索难以处理的复杂多跳问题。

## 为什么需要 Graph RAG

| 向量 RAG 的短板 | Graph RAG 的优势 |
|---|---|
| 只能召回语义相近的片段 | 可通过实体关系链式推理 |
| 无法回答"跨多个文档的关系问题" | 图遍历可跨越文档连接实体 |
| 全局总结（如"这些文档的共同主题"）困难 | 基于社区检测做全局归纳 |
| 多跳问题（A→B→C）依赖中间跳巧合命中 | 图路径天然支持多跳 |

## 构建流程

```
原始文档
  │  实体抽取 (LLM/NER)  实体链接 (对齐到同一节点)
  │  关系抽取 (LLM)      属性抽取
  ▼
知识图谱（节点=实体，边=关系）
  │  图嵌入/社区检测 建立索引
  ▼
向量索引 + 图索引
```

## 检索与生成流程

```
query_vec = embed(query)
# 1. 向量召回：粗找相关片段/实体
candidate_entities = vector_search(query)
# 2. 图遍历：从种子实体出发多跳扩散
related_entities = graph.bfs(candidate_entities, depth=2)
# 3. 子图提取 / 社区总结
subgraph = extract_subgraph(related_entities)
local_summary = llm.summarize(subgraph)
# 4. 全局检索（可选）：社区级信息
global_ctx = community_summary(query)
# 5. 生成
answer = llm.generate(query, local_summary + global_ctx)
```

## 两种典型模式

1. **局部检索（Local）**：以查询相关实体为中心，抽取邻接子图，把子图描述作为上下文
2. **全局检索（Global）**：先做社区检测，把每个社区的信息总结成索引，回答全局性问题

## 适用场景

- 复杂多跳问答：如"谁推荐了 X 给 Y，而 Y 是 Z 的员工"
- 全局性总结：对整库做主题归纳、关联分析
- 实体关系密集的领域：医疗、金融、知识图谱、语义网

## 挑战与成本

- **构建成本高**：实体/关系抽取依赖 LLM，准确率影响整体效果
- **图谱维护难**：数据更新需要增量更新图谱
- **图 + 向量混合**：工程复杂度上升
- 通常与向量 RAG 结合使用（Hybrid），而非完全替代
