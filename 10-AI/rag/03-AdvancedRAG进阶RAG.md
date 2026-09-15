---
type: tutorial
domain: ai/rag
tags: [AdvancedRAG, RAG]
status: done
updated: 2026-09-16
---

# Advanced RAG 进阶 RAG

## 定义

Advanced RAG 在 Naive RAG 基础上，针对**入库前、检索中、生成前**三个阶段做精细化优化，核心是三类：优化入库策略、优化检索策略、检索结果重排。

## 一、入库阶段优化（Pre-Retrieval）

目标：让切出来的块"好检索、有语义"。

| 优化项 | 做法 |
|---|---|
| 文档清洗 | 去除页眉页脚、水印、乱码、重复内容 |
| 智能切分 | 按语义边界（段落/标题/句子）切分，而非纯固定长度 |
| 元数据标注 | 给每个块打标签：来源文档、章节、日期、作者 |
| 父子块结构 | 检索命中父块上下文更完整，返回父块（Hierarchical Index） |
| 多粒度索引 | 同时建立粗粒度（总结）和细粒度（原文）索引 |

## 二、检索阶段优化（Retrieval）

目标：提高召回率与准确率。

### 混合检索（Hybrid Search）
关键词（BM25）+ 语义（向量）双路召回，合并去重，兼顾精确匹配与语义相似。

```
bm25_hits   = bm25.search(query)
vector_hits = vector_db.search(query)
results     = merge_and_dedup(bm25_hits, vector_hits)
```

### 查询改写（Query Rewriting）
原始问题往往简短含糊，先改写再检索：
- **HyDE**：先用 LLM 生成一个假设答案，用假设答案去检索，更贴近文档语义
- **Query Expansion**：把问题拆成多个子问题 / 同义扩展，多路召回
- **Query Rewrite**：LLM 把口语化问题改写为规范检索式

### 多路召回（Multi-recall）
不同检索器、不同向量模型并行召回，扩充候选集。

## 三、生成阶段优化（Post-Retrieval）

目标：喂给 LLM 的上下文"精、准、短"。

- **重排序（Rerank）**：用 Cross-Encoder 对召回结果精排，前 N 个进入上下文
- **上下文压缩（Context Compression）**：裁剪冗余、保留关键句
- **去重**：合并语义重复的片段
- **引用溯源**：标注每个答案依据来源，便于可信与排查

```
recall_chunks = retrieve(query)            # 粗召回
reranked      = reranker.rerank(query, recall_chunks)
final_ctx     = compress(reranked[:top_n])
answer        = llm.generate(final_ctx, query)
```

## 效果对比（Naive vs Advanced）

| 指标 | Naive RAG | Advanced RAG |
|---|---|---|
| 召回准确率 | 低 | 高（重排 + 改写） |
| 上下文质量 | 冗余混乱 | 精炼相关 |
| 答案幻觉率 | 较高 | 明显降低 |
| 实现复杂度 | 低 | 中 |
