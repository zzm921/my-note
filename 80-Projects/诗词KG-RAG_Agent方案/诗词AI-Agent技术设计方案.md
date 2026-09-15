---
created: 2026-06-29
tags: [诗词AI-Agent, 产品设计, 知识图谱, RAG]
status: 设计稿
---

# 诗词 AI Agent 技术设计方案 v1.0

> 基于"一句话/一张图"从诗词库中找到最匹配的诗词

---

## 一、总体架构

```
┌─────────────────────────────────────────────────────────────┐
│                        用户交互层                            │
│       飞书/微信/Web: 一句话文本 / 一张图片                    │
└────────────────────────────────┬────────────────────────────┘
                                 │
┌────────────────────────────────▼────────────────────────────┐
│                        输入理解层                            │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────┐  ┌──────────────────────────────┐  │
│  │ 文本输入处理          │  │ 图片输入处理                  │  │
│  │ LLM 提取:            │  │ Chinese-CLIP:                │  │
│  │  - 情感              │  │  - 场景标签提取               │  │
│  │  - 场景              │  │  - 意象识别                   │  │
│  │  - 意象              │  │  - 氛围判断                   │  │
│  │  - 用户意图           │  │  → 结构化 Query              │  │
│  └─────────┬───────────┘  └────────────┬─────────────────┘  │
│            └──────────┬────────────────┘                    │
│                 结构化 Query（JSON）                         │
│    { emotion: "思念", scene: "月夜", mood: "孤独" }         │
└────────────────────────────────┬────────────────────────────┘
                                 │
┌────────────────────────────────▼────────────────────────────┐
│                        混合检索引擎                          │
├─────────────────────────────────────────────────────────────┤
│  ┌────────────────────┐    ┌─────────────────────────────┐  │
│  │ 知识图谱检索 (Path A)│    │ 向量语义检索 (Path B)        │  │
│  │ Neo4j               │    │ FAISS + M3E                │  │
│  │                     │    │                            │  │
│  │ 结构化 Query →       │    │ Query Embedding →          │  │
│  │ Cypher 查询          │    │ 余弦相似度 Top-30          │  │
│  │                     │    │ → 元数据过滤(朝代/作者)      │  │
│  │ Top-10              │    │ → Top-10                   │  │
│  └─────────┬───────────┘    └─────────────┬───────────────┘  │
│            └──────────┬──────────────────┘                  │
│                   RRF 融合排序                              │
│         Reciprocal Rank Fusion → Top-10                    │
└────────────────────────────────┬────────────────────────────┘
                                 │
┌────────────────────────────────▼────────────────────────────┐
│                      LLM 精排 & 输出                         │
├─────────────────────────────────────────────────────────────┤
│  - 对 Top-10 进行语义重排序                                  │
│  - 生成匹配理由（为什么这首最贴切）                           │
│  - 补充诗词完整信息（作者、朝代、译文、背景、写作地址）       │
│  - 输出 Top-3 结果                                           │
└─────────────────────────────────────────────────────────────┘
```

---

## 二、知识图谱设计（核心）

### 2.1 实体类型

```yaml
Poem（诗词）:
  属性:
    - id: string (主键)
    - title: string (标题)
    - content: text (正文)
    - translation: text (白话译文)
    - background: text (创作背景)
    - writing_location: string (写作地点)
    - dynasty: string (朝代)
    - rhythm_pattern: string (格律/词牌名)
    - style: string[] (风格标签: 豪放/婉约/山水/边塞/田园/咏物/怀古)
    - difficulty: enum (易/中/难)
    - popularity: int (热度评分 1-10)
    - keywords: string[] (关键词自动抽取)
  关系:
    - WRITTEN_BY → Author
    - HAS_SCENE → Scene
    - EXPRESSES → Emotion
    - CONTAINS → Imagery
    - HAS_TAG → Tag
    - WRITTEN_AT → Location
    - SIMILAR_TO → Poem (自关联，人工标注相似诗)

Author（作者）:
  属性:
    - name: string
    - dynasty: string
    - birth_year: int
    - death_year: int
    - biography: text (生平简介)
    - style: string[] (创作风格)
    - representative_works: string[] (代表作)
    - alias: string (字号/别称)
  关系:
    - BELONGS_TO → Dynasty
    - WROTE → Poem

Scene（场景）:  # 60-80个日常生活场景
  属性:
    - name: string (场景名)
    - category: string (大类: 职场/情感/旅行/季节/节日/日常/独处)
    - description: text (场景描述，用于 LLM 匹配)
    - associated_emotions: string[] (关联情感)
    - associated_imageries: string[] (关联意象)
    - example_queries: string[] (用户可能输入的话)

Emotion（情感）:  # 8大类，30+子类
  属性:
    - name: string
    - category: string (大类)
    - intensity: int (强度 1-5)
    - antonyms: string[] (相反情感)
    - synonyms: string[] (相近情感)

Imagery（意象）:  # 200+诗词常见意象
  属性:
    - name: string
    - category: string (自然/人物/器物/时间/动物/植物)
    - description: text
    - cultural_meaning: text (文化含义，如"月→思乡")
    - related_imageries: string[] (相关意象)

Location（地点）:
  属性:
    - name: string
    - modern_name: string (现代地名)
    - latitude: float
    - longitude: float
    - historical_significance: text

Tag（标签）:
  属性:
    - name: string
    - category: string (流派/体裁/主题/手法)
```

### 2.2 场景维度体系（完整版）

```
┌───────────── 场景维度（60-80个） ─────────────┐
│                                                │
│  🏫 毕业/离别 → 送别、前程、各奔东西              │
│  💼 职场奋斗 → 加班、晋升、坚持、理想              │
│  💔 失恋/分手 → 相思、回忆、遗憾                  │
│  ❤️ 恋爱/表白 → 初见、陪伴、承诺                  │
│  🏠 思乡/归家 → 游子、故土、归心                  │
│  🌅 夕阳/黄昏 → 时光流逝、暮年、感怀              │
│  🌙 夜晚/赏月 → 静谧、思念、独处                  │
│  🍂 秋日感怀 → 萧瑟、丰收、离愁                   │
│  🌸 春日踏青 → 生机、喜悦、惜春                   │
│  ❄️ 冬日雪景 → 寂寥、纯洁、温暖                   │
│  🏔️ 山水游记 → 壮丽、隐逸、自在                   │
│  🍜 美食/聚餐 → 欢聚、烟火、闲适                  │
│  🎉 节日/过年 → 团圆、喜庆、思亲                  │
│  🧘 独处/冥想 → 宁静、自省、淡泊                  │
│  📚 读书/求学 → 勤奋、求索、苦读                  │
│  🎓 金榜题名 → 得意、功名、荣耀                  │
│  ⚔️ 边塞/征战 → 豪迈、苍凉、报国                  │
│  🚢 泛舟/江上 → 漂泊、逍遥、豁达                  │
│  🍷 饮酒/醉意 → 豪放、愁绪、洒脱                  │
│  🌧️ 雨夜/听雨 → 凄凉、思念、闲适                  │
│  ...（共60-80个场景）                            │
└────────────────────────────────────────────────┘
```

### 2.3 情感维度体系

```yaml
八大情感大类:
  1. 喜悦 (Joy):
     - 子类: 闲适、满足、得意、欢聚、惊喜
  2. 忧愁 (Sorrow):
     - 子类: 离愁、春愁、秋思、感怀、怅惘
  3. 思念 (Longing):
     - 子类: 思乡、怀人、怀古、忆旧、相思
  4. 豪迈 (Heroism):
     - 子类: 壮志、报国、慷慨、激昂、豁达
  5. 孤独 (Loneliness):
     - 子类: 寂寥、漂泊、隐居、清高、冷清
  6. 淡然 (Detachment):
     - 子类: 禅意、隐逸、旷达、逍遥、淡泊
  7. 愤懑 (Indignation):
     - 子类: 不平、讽刺、愤世、无奈、悲愤
  8. 爱情 (Love):
     - 子类: 相思、甜蜜、哀怨、誓言、离别
```

---

## 三、技术栈选型

| 层 | 组件 | 选型 | 选型原因 |
|---|------|------|---------|
| **数据存储** | 图数据库 | **Neo4j** | 案例①验证可行，Cypher 查询灵活，社区活跃 |
| | 向量数据库 | **FAISS + Milvus** | 原型用FAISS，上线转Milvus支持高并发 |
| | 关系型 | **PostgreSQL** | 存储用户反馈、使用日志 |
| **模型** | 中文嵌入 | **BAAI/bge-base-zh-v1.5** | MTEB中文榜前列，768维效果好 |
| | 多模态 | **Chinese-CLIP** | 案例⑤验证，适配中文场景 |
| | LLM | **DeepSeek** (已部署) | 复用现有资源，成本低 |
| **框架** | RAG | **LangChain + LlamaIndex** | 社区方案成熟，案例②验证 |
| | 后端 | **FastAPI + Python** | 轻量高性能 |
| | 部署 | **Docker + Docker Compose** | 与现有RAGFlow基础设施一致 |
| **前端** | 渠道 | **飞书 Bot（现有）→ 微信** | 复用Hermes渠道 |

---

## 四、核心流程详解

### 4.1 文本输入流程

```
用户: "今天加班到深夜，好累啊"

Step 1 - LLM Query 解析
  └→ { emotion: "疲惫/坚持", scene: "职场奋斗", mood: "孤独" }

Step 2a - 知识图谱检索
  └→ MATCH (s:Scene {name:"职场奋斗"})<-[:HAS_SCENE]-(p:Poem)
     WHERE p.dynasty IN ["唐","宋"]
     RETURN p.title, p.content, p.author
     LIMIT 10

Step 2b - 向量语义检索
  └→ query_embedding = bge.encode("加班到深夜好累")
     results = faiss_search(query_embedding, top_k=30)
     filter(results, dynasty=["唐","宋"])
     → Top-10

Step 3 - RRF 融合
  └→ RRF(KG结果, 向量结果) → Top-10

Step 4 - LLM 精排
  └→ 输入: Top-10 诗词 + 用户原文
     输出: 最贴合的前3首 + 理由

Step 5 - 返回结果
  └→ Top-1: "锄禾日当午，汗滴禾下土" — 李绅
     理由：同是辛勤劳作场景
     Top-2: "路漫漫其修远兮，吾将上下而求索" — 屈原
     理由：深夜加班的坚持精神
     Top-3: "晨兴理荒秽，带月荷锄归" — 陶渊明
     理由：晚归劳作，意境相似
```

### 4.2 图片输入流程

```
用户: 上传一张夕阳湖面的照片

Step 1 - 多模态解析
  └→ Chinese-CLIP 提取场景标签
     → ["日落(0.92)", "湖面(0.88)", "孤舟(0.75)", "晚霞(0.71)"]
     → 提取意象: "落日", "江", "舟"

Step 2 - 结构化 Query
  └→ { scene: "夕阳/黄昏", imagery: ["落日","江","舟"] }

Step 3 - 知识图谱检索
  └→ MATCH (p:Poem)-[:CONTAINS]->(i:Imagery)
     WHERE i.name IN ["落日","江","舟"]
     MATCH (p)-[:EXPRESSES]->(e:Emotion)
     WHERE e.name IN ["感怀","淡然"]
     RETURN p
     LIMIT 10

Step 4 - 向量检索
  └→ prompt = "夕阳湖面孤舟晚霞"
     query_embedding = bge.encode(prompt)
     faiss_search(query_embedding, top_k=30)

Step 5 - RRF + LLM 精排
  └→ Top-1: "落霞与孤鹜齐飞，秋水共长天一色" — 王勃
     Top-2: "一道残阳铺水中，半江瑟瑟半江红" — 白居易
     Top-3: "孤帆远影碧空尽，唯见长江天际流" — 李白
```

---

## 五、数据标注策略

### 5.1 知识图谱构建

```yaml
数据来源:
  - chinese-poetry/chinese-poetry (5.7万首) 
  - 开源诗词扩展包 (可到10万+)
  - 古诗文网爬取 (补充译文/背景)

标注方式:
  第一阶段 - 自动标注（覆盖80%）:
    - NLP 规则提取意象（基于诗词意象词典）
    - LLM 批量标注情感/场景（GPT-4o / DeepSeek）
    - 基于作者朝代/风格自动关联
  
  第二阶段 - 人工校验（精标20%）:
    - 重点诗词人工校对（Top 5000首高频诗词）
    - 场景-诗词映射人工确认
    - 相似诗词关系标注

  第三阶段 - 持续优化:
    - 用户反馈收集（点赞/踩）
    - A/B测试不同标注方案
```

### 5.2 LLM 标注 Prompt 示例

```
系统: 你是一位诗词专家，请为以下诗词打标签。

诗词: 《静夜思》李白
床前明月光，疑是地上霜。
举头望明月，低头思故乡。

请按以下格式输出JSON：
{
  "emotions": ["思念", "孤独"],
  "scenes": ["夜晚/赏月", "思乡/归家"],
  "imageries": ["月", "霜", "床"],
  "mood": "清冷",
  "intensity": 4
}
```

---

## 六、API 设计

```yaml
POST /api/poem/search
  描述: 诗词匹配搜索

  请求体:
    {
      "text": "加班到深夜好累",          # 文本输入（二选一）
      "image_url": "https://..."       # 图片URL（二选一）
      "top_k": 3,                      # 返回数量 (默认3)
      "filters": {"dynasty": "唐"}      # 可选过滤条件
    }

  返回:
    {
      "success": true,
      "query_analysis": {
        "emotion": "疲惫/坚持",
        "scene": "职场奋斗",
        "imageries": ["夜", "灯", "书"],
        "mood": "孤独"
      },
      "results": [
        {
          "rank": 1,
          "poem": {
            "title": "悯农",
            "author": "李绅",
            "dynasty": "唐",
            "content": "锄禾日当午，汗滴禾下土。谁知盘中餐，粒粒皆辛苦。",
            "translation": "...",
            "background": "...",
            "writing_location": ""
          },
          "match_reason": "同是辛勤劳作场景，表达坚持与不易",
          "match_score": 0.92
        },
        ...
      ]
    }

POST /api/poem/feedback
  描述: 用户反馈（用于优化排序）

  请求体:
    {
      "session_id": "xxx",
      "poem_id": "xxx",
      "action": "like" | "dislike",
      "user_input": "加班到深夜好累"
    }
```

---

## 七、项目实施计划

### Phase 1：核心引擎（2周）
```
Week 1:
  - 搭建 Neo4j 知识图谱（导入5万首诗词）
  - LLM 批量标注情感/场景/意象
  - 部署 FAISS 向量检索

Week 2:
  - 实现 KG + 向量 RRF 融合
  - LLM 精排 pipeline
  - 文本输入完整链路测试
```

### Phase 2：多模态 + 产品化（1周）
```
Week 3:
  - 接入 Chinese-CLIP 多模态
  - FastAPI 后端封装
  - 接入飞书 Bot（复用Hermes渠道）
  - 用户反馈收集链路
```

### Phase 3：优化迭代（持续）
```
  - 人工校验 Top 5000 诗词标签
  - 基于反馈数据调优排序权重
  - 扩展诗词库到10万+
  - 接入微信渠道
```

---

## 八、关键指标

| 指标 | 目标 | 衡量方式 |
|------|------|---------|
| Top-3 准确率 | ≥ 85% | 人工评估：结果是否贴切 |
| 响应时间 | ≤ 3s | API 监控 |
| 知识图谱覆盖率 | ≥ 90% | 5万首标注覆盖 |
| 用户满意度 | ≥ 4.0/5 | 反馈评分 |
| 多模态准确率 | ≥ 75% | 图片→诗词匹配人工评估 |

---

## 九、参考资源

| 资源 | 链接 | 用途 |
|------|------|------|
| chinese-poetry 数据集 | https://github.com/chinese-poetry/chinese-poetry | 诗词数据源（37K⭐） |
| PoemKnowledgeGraph | https://github.com/liuhuanyong/PoemKnowledgeGraph | 知识图谱参考实现 |
| Chinese-CLIP | https://github.com/OFA-Sys/Chinese-CLIP | 多模态基础模型 |
| BGE Embedding | https://huggingface.co/BAAI/bge-base-zh-v1.5 | 中文向量模型 |
| Neo4j | https://neo4j.com | 图数据库 |
| LangChain | https://github.com/langchain-ai/langchain | RAG 框架 |
| 清华九歌 | http://jiuge.thunlp.org | 产品体验参考 |
| 古诗文网 | https://www.gushiwen.cn | 产品对标 |