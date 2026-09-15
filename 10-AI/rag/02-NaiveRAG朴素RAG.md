# Naive RAG 朴素 RAG

## 定义

Naive RAG 是 RAG 最基础的实现形态，流程固定为：**向量化 → 检索 → 导入上下文 → 输出结果**。适合快速验证，但各环节没有精细优化。

## 完整流程

```
1. 文档加载     Loader 读取 PDF / Word / Markdown / 网页
2. 文本切分     Chunking 按规则切成固定大小的片段
3. 向量化       Embedding 模型把文本转为向量
4. 入库         写入向量数据库（构建索引）
5. 查询向量化   用户问题同样转为向量
6. 相似度检索   Top-K 召回最相似的片段
7. 拼接上下文   检索片段 + 用户问题 → Prompt
8. 生成         LLM 基于上下文生成答案
```

## 关键组件

| 组件 | 作用 | 常见选型 |
|---|---|---|
| Embedding 模型 | 把文本编码为向量 | BGE、text-embedding、OpenAI embedding |
| 向量数据库 | 存储向量并做相似度检索 | FAISS、Milvus、Qdrant、pgvector |
| 相似度度量 | 衡量向量距离 | 余弦相似度、点积、L2 距离 |
| LLM | 基于上下文生成答案 | GPT、DeepSeek、Qwen 等 |

## 检索流程伪代码

```
query_vec = embed(user_query)
top_k_chunks = vector_db.search(query_vec, k=5)
context = concat(top_k_chunks)
prompt = build_prompt(context, user_query)
answer = llm.generate(prompt)
```

## 常见问题与局限

- **检索不精准**：切分粗糙、语义漂移，召回结果与问题相关性差
- **上下文混乱**：多片段拼接后逻辑割裂、信息冗余
- **幻觉仍存在**：检索结果质量低时，模型仍会编造
- **无记忆**：每次请求独立，不利用历史交互

## 改进方向

- 提升切分质量（语义切分、父子块）
- 混合检索（关键词 + 向量）
- 检索结果重排（Rerank）
- 走向 Advanced / Modular RAG（见后续文件）
