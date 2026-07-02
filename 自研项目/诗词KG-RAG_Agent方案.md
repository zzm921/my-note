# 诗词 KG-RAG Agent 方案文档

## 一、项目概述

基于现有诗词库的 25 张关系型表，构建一个独立的知识图谱 RAG Agent 项目，实现诗词智能问答、赏析、作者查询、语义检索等功能。

**核心思路：** 将现有关系型数据转化为知识图谱，结合向量检索和 LLM，构建多路检索的 RAG 管线。

---

## 二、现有数据结构分析

### 2.1 核心实体关系图

```
                    evaluations_tags_themes (主题)
                           │ themeId
                    evaluations_tags (标签)
                           │ tagId (config_tags关联)
    evaluations_author ─── evaluations (诗词) ─── evaluations_contents (章节)
    (作者)  authorId          │  bookId              │  contentId
         │                    │                      ├──→ evaluations_contents_detail (详情:释义/注释/赏析)
    evaluations_dynastys      │                      ├──→ evaluations_contents_understand (理解)
    (朝代)  dynasty字符串关联  │                      ├──→ evaluations_contents_questions (问答)
         │                    │                      └──→ evaluations_contents_replys (回复)
    evaluations_understands ──┘
    (理解)  bookId
         │
    evaluations_understands_questions (理解问答)
```

### 2.2 现有表清单

| 表名 | 用途 | 关键字段 |
|------|------|---------|
| evaluations | 诗词主表 | name, content, author, dynasty, shiyi, shangxi |
| evaluations_author | 作者 | name, dynasty, desc, star, authorId |
| evaluations_dynastys | 朝代 | dynasty, index |
| evaluations_tags | 标签 | name, introduction, themeId, index, status |
| evaluations_tags_themes | 标签主题 | name, index |
| evaluations_config_tags | 标签-诗词关联 | tagId, evaluationId, sort |
| evaluations_contents | 章节 | bookId, content, url, index |
| evaluations_contents_detail | 章节详情 | bookId, shiyi, zhushi, shangxi, famous |
| evaluations_contents_questions | 章节问答 | contentId, question, answer, score |
| evaluations_contents_replys | 章节回复 | bookId, reply, replyUrl |
| evaluations_contents_understand | 章节理解 | contentId, understand, url |
| evaluations_understands | 理解 | bookId, understand, url |
| evaluations_understands_questions | 理解问答 | bookId, question, answer, score |
| evaluations_comments | 评论 | comment, userId, evaluationId |
| evaluations_collects | 收藏 | userId, evaluationId |
| evaluations_shares | 分享 | content, userId, evaluationId, audio, image |
| evaluations_shares_comments | 分享评论 | comment, userId, shareId |
| evaluations_shares_stars | 分享点赞 | userId, shareId |
| evaluations_activitys | 活动 | name, description, type, period, status |
| evaluations_activitys_comments | 活动评论 | comment, activityId, userId, evaluationId |
| evaluations_records | 记录 | appkey, uid, deviceId, userId |
| evaluations_records_book | 阅读记录 | bookId, uid, appkey, deviceId |
| evaluations_records_content | 内容记录 | contentId, uid, deviceId |
| evaluations_records_details | 记录详情 | recordId, bookId, contentId, step, status |
| evaluations_guidances | 引导 | themeId, text, url, guidancePrompt |
| evaluations_content_detail_test | 详情测试 | name, author, details |

### 2.3 天然的知识图谱雏形

现有表关系已构成结构化图：

- **诗词 → 作者**：`evaluations.authorId` → `evaluations_author.authorId`
- **作者 → 朝代**：通过 `dynasty` 字符串关联（设计缺陷）
- **诗词 → 标签**：通过 `evaluations_config_tags` 中间表
- **标签 → 主题**：`evaluations_tags.themeId` → `evaluations_tags_themes.id`
- **诗词 → 章节**：`evaluations_contents.bookId` → `evaluations.id`
- **章节 → 详情**：`evaluations_contents_detail.bookId` 关联
- **章节 → 问答**：`evaluations_contents_questions.contentId` 关联

---

## 三、现有数据问题

### 3.1 字段类型错误（严重）

几乎所有表的 `createtime` / `updatetime` 使用了 `Sequelize.TIME`，但 `TIME` 类型只存储 `HH:MM:SS`，不包含日期。应改为 `Sequelize.DATE`。

### 3.2 朝代关联用字符串而非 ID（设计缺陷）

```javascript
// evaluations.js - 用 dynasty 字符串
dynasty: { type: Sequelize.STRING }

// evaluations_author.js - 也用 dynasty 字符串
dynasty: { type: Sequelize.STRING }

// evaluations_dynastys.js - 定义了朝代
dynasty: { type: Sequelize.STRING }
```

`evaluations_dynastys` 和 `evaluations_author` / `evaluations` 之间通过 `dynasty` **字符串**关联，而非外键 ID，存在数据不一致风险（如"唐" vs "唐代"）。

### 3.3 作者关联冗余

```javascript
// evaluations.js 同时有 author 字符串和 authorId
authorId: { type: Sequelize.INTEGER },
author: { type: Sequelize.STRING },
```

`author` 字符串和 `authorId` 并存，容易不一致。

### 3.4 bookId 命名歧义

`evaluations_contents.bookId` 实际关联的是 `evaluations.id`，但命名叫 `bookId`，容易混淆。

### 3.5 缺少向量检索支持

现有表均为关系型结构，没有任何向量字段或 embedding 存储，无法直接做语义检索（RAG 的核心）。

---

## 四、技术栈选型

| 层 | 推荐方案 | 理由 |
|----|---------|------|
| 知识图谱 | **Neo4j** | 诗词关系天然适合图结构，多跳查询能力强 |
| 向量检索 | **Neo4j Vector Index**（5.11+内置） | 图谱+向量一体化，免维护独立向量库 |
| LLM | GPT-4o / DeepSeek | 中文古文理解能力强 |
| Embedding | bge-large-zh-v1.5 | 中文语义检索效果最好 |
| Agent 框架 | LangChain / LlamaIndex | 成熟的工具调用+RAG管线 |
| 后端 | Python FastAPI | AI 生态最完善 |
| 数据导入 | 从现有 MySQL 导出 | 复用已有的25张表数据 |

---

## 五、知识图谱设计

### 5.1 节点(Node)定义

```
节点类型：
  - Poem        诗词    {id, name, content, shiyi, shangxi, grade, volume}
  - Author      作者    {id, name, dynasty, desc, star}
  - Dynasty     朝代    {id, name, index}
  - Tag         标签    {id, name, introduction}
  - Theme       主题    {id, name, index}
  - Content     章节    {id, content, url, index}
  - Detail      详情    {id, shiyi, zhushi, shangxi, famous}
  - Question    问答    {id, question, answer, score}
  - Understand  理解    {id, text, url}
```

### 5.2 关系(Relationship)定义

```
(Poem)-[:WRITTEN_BY]->(Author)
(Author)-[:BELONGS_TO]->(Dynasty)
(Poem)-[:HAS_TAG]->(Tag)
(Tag)-[:IN_THEME]->(Theme)
(Poem)-[:CONTAINS]->(Content)
(Content)-[:HAS_DETAIL]->(Detail)
(Content)-[:HAS_QUESTION]->(Question)
(Poem)-[:HAS_UNDERSTAND]->(Understand)
```

### 5.3 图谱结构可视化

```
                    ┌──────────┐
                    │  Dynasty  │
                    └────▲─────┘
                         │ BELONGS_TO
                    ┌────┴─────┐
                    │  Author  │
                    └────▲─────┘
                         │ WRITTEN_BY
┌─────────┐     ┌───────┴───────┐     ┌──────────┐
│  Theme  │◄────│     Poem      │────►│   Tag    │
└─────────┘ IN  └───────┬───────┘ HAS └──────────┘
               THEME     │ TAG
                    ┌────┴─────┐
                    │ Content  │
                    └────┬─────┘
              ┌──────────┼──────────┐
              ▼          ▼          ▼
        ┌──────────┐ ┌────────┐ ┌───────────┐
        │  Detail  │ │Question│ │Understand │
        └──────────┘ └────────┘ └───────────┘
```

---

## 六、RAG 检索流程

### 6.1 整体架构

```
用户提问
   │
   ▼
┌──────────────┐     ┌─────────────────────┐
│  意图识别     │────▶│  查询路由            │
│  (LLM)       │     │  KG查询 / 向量检索    │
└──────────────┘     └─────┬───────────────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
      ┌──────────┐  ┌──────────┐  ┌──────────┐
      │ 知识图谱  │  │ 向量库   │  │ 全文检索  │
      │ (Neo4j)  │  │(Neo4j内置)│  │(关键词匹配)│
      └────┬─────┘  └────┬─────┘  └────┬─────┘
           │             │             │
           └─────────────┼─────────────┘
                         ▼
              ┌─────────────────────┐
              │  上下文组装 + LLM生成 │
              └─────────────────────┘
                         │
                         ▼
                    诗词Agent回答
```

### 6.2 检索流程详解

```
用户提问: "李白写的关于月亮的诗，赏析一下"
         │
         ▼
┌─────────────────┐
│ 1. 意图识别(LLM) │  → {intent: "poem_search", 
│                 │     entities: {author:"李白", topic:"月亮"},
│                 │     action: "explain"}
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────┐
│ 2. 多路检索(并行)                │
│                                 │
│  ① KG查询(Cypher):              │
│     MATCH (p:Poem)-[:WRITTEN_BY]->(a:Author {name:'李白'})│
│     WHERE p.content CONTAINS '月'│
│     RETURN p                     │
│                                 │
│  ② 向量检索:                    │
│     question embedding → top-k  │
│     相似诗词(语义匹配"月亮"主题) │
│                                 │
│  ③ 图谱扩展:                    │
│     命中诗词 → 关联作者/朝代/    │
│     标签/详情/问答              │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────┐
│ 3. 上下文组装    │  按相关性排序，截断到token上限
│                 │  组装: 诗词原文 + 释义 + 赏析 + 作者信息
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 4. LLM生成回答   │  Prompt: 上下文 + 问题 → 生成赏析
└─────────────────┘
```

---

## 七、Agent 工具设计

```python
# Agent 可调用的工具(Tools)
tools = [
    {
        "name": "search_by_author",
        "description": "按作者搜索诗词",
        "cypher": "MATCH (p:Poem)-[:WRITTEN_BY]->(a:Author {name:$author}) RETURN p"
    },
    {
        "name": "search_by_dynasty",
        "description": "按朝代搜索诗词",
        "cypher": "MATCH (p:Poem)-[:WRITTEN_BY]->(a:Author)-[:BELONGS_TO]->(d:Dynasty {name:$dynasty}) RETURN p,a"
    },
    {
        "name": "search_by_tag",
        "description": "按标签/主题搜索诗词",
        "cypher": "MATCH (p:Poem)-[:HAS_TAG]->(t:Tag)-[:IN_THEME]->(th:Theme {name:$theme}) RETURN p"
    },
    {
        "name": "get_poem_detail",
        "description": "获取诗词详情(释义/注释/赏析)",
        "cypher": "MATCH (p:Poem {id:$id})-[:CONTAINS]->(c:Content)-[:HAS_DETAIL]->(d:Detail) RETURN p,c,d"
    },
    {
        "name": "semantic_search",
        "description": "语义搜索诗词(向量检索)",
        "vector": True
    },
    {
        "name": "get_author_info",
        "description": "获取作者信息和代表作",
        "cypher": "MATCH (a:Author {name:$name})-[:WRITTEN_BY]-(p:Poem) RETURN a,p ORDER BY p.star DESC LIMIT 5"
    },
    {
        "name": "find_similar_poems",
        "description": "找相似诗词(同标签/同主题/同朝代)",
        "cypher": "MATCH (p:Poem {id:$id})-[:HAS_TAG]->(t:Tag)<-[:HAS_TAG]-(similar:Poem) RETURN similar"
    }
]
```

---

## 八、项目结构

```
poetry-agent/
├── data/                    # 数据导入脚本
│   ├── export_from_mysql.py # 从现有MySQL导出
│   ├── import_to_neo4j.py   # 导入Neo4j图谱
│   └── generate_embeddings.py # 生成向量
├── graph/                   # 知识图谱层
│   ├── schema.py            # 图谱schema定义
│   ├── queries.py           # Cypher查询模板
│   └── connection.py        # Neo4j连接
├── rag/                     # RAG管线
│   ├── intent.py            # 意图识别
│   ├── retriever.py         # 多路检索器
│   ├── context_builder.py   # 上下文组装
│   └── generator.py         # LLM回答生成
├── agent/                   # Agent层
│   ├── tools.py             # 工具定义
│   ├── memory.py            # 多轮对话记忆
│   └── chain.py             # Agent编排
├── api/                     # FastAPI接口
│   └── main.py
├── config.py                # 配置
└── requirements.txt
```

---

## 九、关键实现代码

### 9.1 RAG 检索器

```python
# rag/retriever.py - 核心检索器
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer
import numpy as np

class PoetryRetriever:
    def __init__(self, neo4j_uri, embedding_model='BAAI/bge-large-zh-v1.5'):
        self.driver = GraphDatabase.driver(neo4j_uri, auth=("neo4j", "password"))
        self.embedder = SentenceTransformer(embedding_model)

    def retrieve(self, question, top_k=5):
        """多路检索：KG + 向量 + 全文"""

        # 1. 向量检索 - 语义匹配
        query_embedding = self.embedder.encode(question)
        vector_results = self._vector_search(query_embedding, top_k)

        # 2. KG检索 - 结构化查询
        kg_results = self._kg_search(question)

        # 3. 图谱扩展 - 获取关联信息
        enriched = self._enrich_with_graph(vector_results + kg_results)

        # 4. 去重排序
        ranked = self._rank_and_dedup(enriched, query_embedding)

        return ranked[:top_k]

    def _vector_search(self, embedding, top_k):
        """Neo4j内置向量检索"""
        with self.driver.session() as session:
            result = session.run("""
                CALL db.index.vector.queryNodes('poem_embeddings', $k, $embedding)
                YIELD node, score
                RETURN node.id as poem_id, node.name as name,
                       node.content as content, score
                ORDER BY score DESC LIMIT $k
            """, embedding=embedding.tolist(), k=top_k)
            return [dict(r) for r in result]

    def _kg_search(self, question):
        """基于关键词的图谱查询"""
        with self.driver.session() as session:
            # 搜索作者名匹配
            result = session.run("""
                MATCH (p:Poem)-[:WRITTEN_BY]->(a:Author)
                WHERE question CONTAINS a.name
                RETURN p.id as poem_id, p.name as name,
                       p.content as content, a.name as author
                LIMIT 10
            """, question=question)
            return [dict(r) for r in result]

    def _enrich_with_graph(self, results):
        """图谱扩展：获取诗词的完整关联信息"""
        enriched = []
        for r in results:
            poem_id = r.get('poem_id')
            if not poem_id:
                continue
            with self.driver.session() as session:
                detail = session.run("""
                    MATCH (p:Poem {id:$id})
                    OPTIONAL MATCH (p)-[:WRITTEN_BY]->(a:Author)
                    OPTIONAL MATCH (p)-[:CONTAINS]->(c:Content)-[:HAS_DETAIL]->(d:Detail)
                    OPTIONAL MATCH (p)-[:HAS_TAG]->(t:Tag)
                    RETURN p, a, collect(DISTINCT c) as contents,
                           collect(DISTINCT d) as details,
                           collect(DISTINCT t.name) as tags
                """, id=poem_id).single()

                if detail:
                    enriched.append({
                        'poem': dict(detail['p']),
                        'author': dict(detail['a']) if detail['a'] else None,
                        'contents': [dict(c) for c in detail['contents']],
                        'details': [dict(d) for d in detail['details']],
                        'tags': detail['tags']
                    })
        return enriched
```

### 9.2 Agent 编排

```python
# agent/chain.py - Agent编排
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI

class PoetryAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
        self.retriever = PoetryRetriever("bolt://localhost:7687")

        self.tools = [
            self._make_search_tool(),
            self._make_detail_tool(),
            self._make_author_tool(),
            self._make_similar_tool()
        ]

    async def chat(self, question, history=None):
        # 1. 预检索 - 先做RAG拿到相关上下文
        context = self.retriever.retrieve(question)

        # 2. 构建Prompt
        system_prompt = f"""你是一个诗词专家助手。根据以下知识图谱检索结果回答问题。

检索到的诗词信息：
{self._format_context(context)}

回答要求：
- 引用诗词原文时标注出处
- 赏析要结合历史背景和文学价值
- 如果检索结果不足，可使用工具补充查询
"""

        # 3. Agent执行(可用工具进一步查询)
        messages = [SystemMessage(content=system_prompt)]
        if history:
            messages.extend(history)
        messages.append(HumanMessage(content=question))

        response = await self.agent.ainvoke({"messages": messages})
        return response['output']
```

### 9.3 数据迁移脚本

```python
# data/import_to_neo4j.py - 从MySQL导入Neo4j
import pymysql
from neo4j import GraphDatabase

class DataImporter:
    def __init__(self, mysql_config, neo4j_uri):
        self.mysql = pymysql.connect(**mysql_config)
        self.neo4j = GraphDatabase.driver(neo4j_uri, auth=("neo4j", "password"))

    def import_all(self):
        self._create_constraints()  # 创建唯一约束
        self._import_dynastys()     # 朝代
        self._import_authors()      # 作者 → 朝代
        self._import_poems()        # 诗词 → 作者
        self._import_tags()         # 标签 → 主题 → 诗词
        self._import_contents()     # 章节 → 详情 → 问答
        self._generate_embeddings() # 生成向量索引

    def _import_poems(self):
        """导入诗词并创建与作者的关系"""
        cursor = self.mysql.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM evaluations")

        with self.neo4j.session() as session:
            for row in cursor.fetchall():
                session.run("""
                    MERGE (p:Poem {id: $id})
                    SET p.name = $name, p.content = $content,
                        p.shiyi = $shiyi, p.shangxi = $shangxi,
                        p.dynasty = $dynasty, p.grade = $grade
                    WITH p
                    MATCH (a:Author {authorId: $authorId})
                    MERGE (p)-[:WRITTEN_BY]->(a)
                """, **row)
```

---

## 十、方案对比

| 维度 | 方案一 (MySQL + pgvector) | 方案二 (Neo4j + 向量库) ✅推荐 |
|------|--------------------------|-------------------------------|
| 改造成本 | 低，复用现有表 | 中，需迁移到图数据库 |
| 多跳查询 | 通过 JOIN 实现，3跳以内可接受 | 原生支持，任意深度 |
| 运维复杂度 | 低 | 中（额外 Neo4j） |
| 向量检索 | pgvector 统一管理 | Neo4j Vector Index 一体化 |
| 适合场景 | 诗词关系相对简单（≤3跳） | 复杂推理、路径查询多 |
| Agent能力 | 基础问答 | 多跳推理、关系探索 |

**推荐方案二**，理由：
- 诗词关系天然是图结构（作者→朝代、诗词→标签→主题、诗词→章节→详情→问答）
- Neo4j 5.11+ 内置向量索引，图谱+向量一体化，无需维护独立向量库
- Cypher 查询语言适合表达多跳关系查询
- 独立项目无历史包袱，可直接用最佳方案

---

## 十一、实施步骤

| 步骤 | 内容 | 依赖 |
|------|------|------|
| 1 | 搭建 Neo4j 环境，创建 schema | 无 |
| 2 | 从现有 MySQL 导出数据导入 Neo4j | 步骤1 |
| 3 | 用 bge-large-zh 生成诗词向量并建索引 | 步骤2 |
| 4 | 实现 RAG 检索管线（向量+KG+全文） | 步骤3 |
| 5 | 实现 Agent 工具链和对话能力 | 步骤4 |
| 6 | FastAPI 接口 + 前端对话界面 | 步骤5 |

---

## 十二、待确认问题

1. **部署环境**：Neo4j + Python 是否可接受？还是必须用 Node.js？
2. **LLM 选型**：用 OpenAI API 还是本地部署的开源模型？
3. **数据量**：现有诗词大概多少万首？影响向量索引方案
4. **是否需要前端界面**：还是只提供 API？
