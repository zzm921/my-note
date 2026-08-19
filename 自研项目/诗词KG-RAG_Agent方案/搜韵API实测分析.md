---
created: 2026-07-01
tags: [搜韵, API实测, 诗词知识图谱]
---

# 搜韵 API 实测分析

> 基于实际调用 `open.cnkgraph.com` 的结果分析
> 测试日期：2026-07-01

---

## 一、实测结论

**搜韵的数据中，时间、地点、人物关系全部可用，且质量很高。**

---

## 二、关键数据字段解析

### 作品（Writing）数据结构

以《静夜思》为例（ID: 26460）：

```json
{
  "Id": 26460,
  "Dynasty": "盛唐",
  "Author": "李白",
  "AuthorId": 15188,
  "AuthorDate": "727年",           // ← 写作时间 ✅
  "AuthorPlace": "CN420982",       // ← 写作地点（行政区划ID）✅
  "Type": "绝句",
  "TypeDetail": "WuJue",
  "Rhyme": "阳",
  "Title": { "Content": "静夜思" },
  "Clauses": [
    { "Content": "床前明月光，", "Comments": [...] },
    { "Content": "疑是地上霜。", "Comments": [...] },
    ...
  ]
}
```

**关键发现：** `AuthorDate`（写作时间）和 `AuthorPlace`（写作地点）是搜韵**已经标好的字段**，不需要你从正文里去提取。

### 人物（People）数据结构

以李白为例（ID: 15188）：

```json
{
  "Id": 15188,
  "Name": "李白",
  "BirthYear": "701",
  "Birthday": "1/16",
  "DeathYear": "762",
  "Dynasty": "盛唐",
  "Aliases": [
    { "Name": "太白", "Type": "Zi" },
    { "Name": "青莲居士", "Type": "Hao" },
    { "Name": "诗仙", "Type": "BieCheng" },
    { "Name": "文", "Type": "ShiHao" }     // 谥号
  ],
  "Titles": ["翰林供奉", ...],              // 官职履历
  "Hometown": [{ "RegionId": "CN...", "Name": "..." }]  // 籍贯 ✅
}
```

### 地点（Map）数据结构

```json
// 查地点 CN420982（安陆市）
{
  "Region": {
    "Id": "CN420982",
    "Name": "安陆市",
    "Latitude": 31.26,
    "Longitude": 113.69,
    "ParentId": "CN4209",             // ← 父级区划
    "HasChild": true,
    "PeopleCount": 73,                // ← 关联人物数
    "Links": { "Count": 1626 },       // ← 关联作品/链接数
    "HistoryRecords": [...]           // ← 历史沿革
  }
}
```

**地点是有层级的（树结构），可以上下钻取：**
```
CN420982 安陆市
  → Parent: CN4209 孝感市
    → Parent: CN42 湖北省
```

---

## 三、各 API 实际可用性实测

| 接口 | 实测结果 | 数据量/示例 |
|------|---------|------------|
| `GET /api/people` | ✅ 可用 | 124,972 人，按朝代分组 |
| `GET /api/people/{id}` | ✅ 可用 | 返回完整个人档案 |
| `POST /api/people/find` | ✅ 可用 | 支持按 Name/ShiHao（谥号）搜索 |
| `GET /api/writing` | ✅ 可用 | **2,019,521 首作品**，按朝代分组 |
| `GET /api/writing/{id}` | ✅ 可用 | 含正文、时间、地点、韵部 |
| `GET /api/writing/{name}` | ✅ 可用 | 按名称搜作品 |
| `POST /api/writing/Find` | ✅ 可用 | 支持 All/Title/Content 搜索 |
| `GET /api/map/region/{id}` | ✅ 可用 | 经纬度、层级、历史沿革、关联计数 |
| `GET /api/tool/labelize` | 未实测 | 自动笺注 |
| `GET /api/tool/reference` | 未实测 | 化用分析 |

---

## 四、对你的项目价值判断

### ✅ 可以直接用（数据源级）

| 数据 | 来源 | 用途 |
|------|------|------|
| **写作时间** | `Writing.AuthorDate` | KG 中的时间维度，支持"按时间查诗" |
| **写作地点** | `Writing.AuthorPlace` → `Map/region` | KG 中的地点维度，支持"在某地写的诗" |
| **人物关系** | `People.Aliases` + `People.Titles` | KG 中的人物别名/官职/仕途轨迹 |
| **地点层级** | `Region.ParentId` + `HistoryRecords` | 地点上下钻取（江南→湖北→孝感→安陆） |
| **人物籍贯** | `People.Hometown` | 人物关系中的地域关联 |
| **诗句词典** | `Clauses[*].Comments[Type=WordDictInJson]` | 自动为诗句提供词语解释 |

### ⚠️ 需要注意的问题

1. **写作时间格式问题**：`AuthorDate` 是字符串 "727年"，有的是 "乾元二年" 这种年号格式，需要归一化处理
2. **地点ID前缀**：CN 开头的可能是现代行政区划，唐代的地名可能映射到不同 ID，需要兼容处理
3. **人物ID**：搜韵的 people ID 和你的项目 ID 体系不同，需要做映射表
4. **数据量**：200 万首作品，全量拉取需要大量时间。建议按朝代分批拉

### 对你的 KG 设计的影响

有了搜韵的这些数据，你的 Neo4j 可以直接从搜韵填充以下关系：

```cypher
(Poem)-[:WRITTEN_AT {time:"727年"}]->(Location {id:"CN420982"})
(Poem)-[:WRITTEN_BY]->(Author {id:15188, name:"李白"})
(Author)-[:HAS_ALIAS]->(Alias {name:"青莲居士", type:"Hao"})
(Author)-[:HELD_TITLE]->(Title {name:"翰林供奉"})
(Author)-[:FROM]->(Hometown {regionId:"CN...", name:"..."})
(Location)-[:BELONGS_TO]->(ParentLocation {id:"CN4209"})
```

---

## 五、建议的数据导入策略

```
Phase 1（你现在的需求）
  1. POST /api/people/find 搜作者 → 拿到人物ID
  2. POST /api/writing/Find 搜作品 → 拿到作品列表
  3. GET /api/writing/{id} 拿详情（含时间地点）
  4. GET /api/map/region/{id} 查地点详情
  5. 用 LLM 打情感/场景/意象标签
  6. 存入你自己的向量库 + PostgreSQL

Phase 2（扩展）
  - 调用 labelize 补充笺注
  - 调用 reference 建立化用关系（诗→诗）
  - 批量按朝代拉全量数据
```