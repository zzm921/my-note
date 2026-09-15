---
created: 2026-07-01
tags: [搜韵, 诗词知识图谱, API分析, 技术调研]
---

# 搜韵诗词知识图谱 API 整理 & 可用性分析

> 来源：open.cnkgraph.com  OpenAPI 文档
> 整理时间：2026-07-01

---

## 一、API 完整清单

### 1.1 人物 / 作者

| 接口 | 方法 | 用途 | 参数 |
|------|------|------|------|
| `/api/people` | GET | 人物总览 | 无 |
| `/api/people/dynasty` | GET | 按朝代浏览人物 | 无 |
| `/api/people/{id}` | GET | 获取特定人物介绍 | 人物ID |
| `/api/people/find` | POST | 按谥号搜索人物列表 | scope(谥号类型), key(关键词) |

### 1.2 作品

| 接口 | 方法 | 用途 |
|------|------|------|
| `/api/writing` | GET | 作品总览 |
| `/api/writing/dynasty` | GET | 按朝代浏览 |
| `/api/writing/dynasty/{authorName}/{authorId}/{writingType}` | GET | 按作家浏览（分页） |
| `/api/writing/{writingId}` | GET | 获取特定作品 |
| `/api/writing/couplet/{coupletWords}` | GET | 获取含特定对仗词汇组的律句 |
| `/api/writing/find` | POST | 查询符合某平仄句式的律句 |
| `/api/writing/SimilarClauses/{key}` | GET | 获取有相似句子的作品 |
| `/api/writing/SameRhymes/{key}` | GET | 获取押相同韵脚的作品 |
| `/api/writing/{writingId}/tones` | GET | 为作品标注平仄 |
| `/api/writing/{writingId}/bookLinks` | GET | 作品在古籍库中的出处 |
| `/api/writing/{writingId}/labelize` | GET | 自动笺注 |

### 1.3 古籍库

| 接口 | 方法 | 用途 |
|------|------|------|
| `/api/book` | GET | 古籍库总览 |
| `/api/book/{category}/{subCategory}` | GET | 某分类下详细书目 |
| `/api/book/{bookId}` | GET | 某部书的详细信息 |
| `/api/book/volume/{volumeId}` | GET | 某一卷详细内容 |
| `/Api/Book/Find` | POST | 检索同时含多个关键词的古籍 |

### 1.4 行政区划 & 景观

| 接口 | 方法 | 用途 |
|------|------|------|
| `/api/map/region` | GET | 行政区划总览 |
| `/api/map/region/{regionId}` | GET | 按ID查某一区划及下级 |
| `/api/map/region/{regionName}` | GET | 按名称查某一区划及下级 |
| `/api/map/region/{regionId}/links` | GET | 区划相关的关联链接 |
| `/api/map/scenery/{regionId}` | GET | 某区划下的景观列表 |
| `/api/map/scenery/{regionId}/{name}` | GET | 某一景观的详细信息 |
| `/api/map/scenery/{regionId}/{name}/links` | GET | 景观的相关链接 |

### 1.5 日历 / 时间

| 接口                                | 方法  | 用途                    |
| --------------------------------- | --- | --------------------- |
| `/api/calendar`                   | GET | 总览                    |
| `/api/calendar/dynasty`           | GET | 按朝代浏览                 |
| `/api/calendar/eraYear/{name}`    | GET | 查看某年号详情（如"宋绍兴"）       |
| `/api/calendar/date/{date}`       | GET | 查某一年（如"901年"）         |
| `/api/calendar/date/{date}`       | GET | 查某一具体日期（如"宋绍兴五年七月丁酉"） |
| `/api/calendar/GanZhi/{ganzhi}`   | GET | 查历代某一干支年（如"庚子"）       |
| `/api/calendar/date/{date}/links` | GET | 查询与某一时间相关的链接          |

### 1.6 工具类

| 接口 | 方法 | 用途 | 参数 |
|------|------|------|------|
| `/api/tool/charsetConvert` | POST | 繁体转简体 | content, mode |
| `/api/tool/labelize` | POST | 自动笺注（给古文做标注） | content, dynasty |
| `/api/tool/reference` | POST | 出处与化用分析 | content |
| `/api/tool/texting` | POST | 短信息查询 | content |

### 1.7 词谱 / 曲谱

| 接口 | 方法 | 用途 |
|------|------|------|
| `/api/ciTune` | GET | 词谱总览 |
| `/api/ciTune/{id}` | GET | 查询特定词谱 |
| `/api/ciTune/{id}/writings` | GET | 查询使用该词谱的作品 |
| `/api/ciTune/find` | POST | 搜索含关键词的词谱 |
| `/api/ciTune/pattern` | POST | 查询含某平仄结构的词牌 |
| `/api/quTune` | GET | 曲谱总览 |
| `/api/quTune/{id}` | GET | 查询特定曲谱 |
| `/api/quTune/{id}/writings` | GET | 查询使用该曲谱的作品 |
| `/api/quTune/find` | POST | 搜索含关键词的曲谱 |

### 1.8 词典 / 典故

| 接口 | 方法 | 用途 |
|------|------|------|
| `/api/glossary/词典/{id}` | GET | 按词汇ID查询 |
| `/api/glossary/典故/{id}` | GET | 按典故ID查询 |
| `/api/glossary/佛典/{id}` | GET | 按佛典ID查询 |
| `/api/glossary/词典/{ids}` | POST | 按词典ID批量查询 |
| `/api/glossary/典故/find` | POST | 按关键词查询典故 |

### 1.9 类书

| 接口 | 方法 | 用途 |
|------|------|------|
| `/api/category` | GET | 类书列表 |
| `/api/category/{bookName}` | GET | 某一类书的目录结构 |
| `/api/category/{bookName}/{entry}/{volume}` | GET | 某条目某卷详细内容 |
| `/api/category/{bookName}/{entry}` | GET | 某条目详细内容 |
| `/api/category/find` | POST | 查询含某关键词的条目 |

### 1.10 韵书

| 接口 | 方法 | 用途 |
|------|------|------|
| `/api/rhyme` | GET | 韵书总览 |
| `/api/rhyme/{book}` | GET | 某韵书韵目信息 |
| `/api/rhyme/{book}/{rhyme}` | GET | 某韵目字表 |
| `/api/rhyme/{book}/{rhyme}/{char}` | GET | 某韵字详细信息 |
| `/api/rhyme/find` | POST | 查某字在韵书中的信息 |

### 1.11 汉字

| 接口 | 方法 | 用途 |
|------|------|------|
| `/api/char/{char}` | GET | 查字 |

---

## 二、对你项目的可用性分析

### ✅ 可以直接用的接口

| 接口                                      | 用途     | 价值判断                                  |
| --------------------------------------- | ------ | ------------------------------------- |
| **`/api/writing/{id}/labelize`**        | 自动笺注   | **高**。你返回诗词时如果有笺注信息，体验会好很多。不需要自己建笺注能力 |
| **`/api/tool/reference`**               | 化用分析   | **高**。"这句诗出自哪里"——这是诗词 Agent 很常见的追问场景  |
| **`/api/tool/charsetConvert`**          | 繁简转换   | **中**。如果用户输入繁体或数据有繁体，需要转换             |
| **`/api/writing/SimilarClauses/{key}`** | 相似句子   | **高**。和你的"找意境相似的诗词"直接相关，可作为向量检索的补充/备选 |
| **`/api/writing/SameRhymes/{key}`**     | 同韵作品   | **中**。如果用户想找押韵的诗词，这个接口直接给答案           |
| **`/api/writing/{id}/tones`**           | 平仄标注   | **中**。如果你要做诗词格律分析                     |
| **`/api/rhyme`** 系列                     | 韵书查询   | **低**。只有专业用户才会用到                      |
| **`/api/ciTune/pattern`**               | 平仄匹配词牌 | **低**。创作辅助场景                          |

### ⚠️ 部分可用，但需要改造

| 接口 | 问题 | 建议 |
|------|------|------|
| `writing/find` | 按平仄查律句，但你的核心需求是语义匹配 | 可作为垂直场景的补充检索 |
| `people/find` | 按谥号搜索（"文正"这种），普通用户不会这么查 | 可以作为作者信息的补充来源 |
| `calendar` 系列 | 干支/年号查询很专业，但你的用户不会用干支查诗 | 只有当你做"时间轴"功能时才有用 |

### ❌ 跟你的项目核心无关

| 接口 | 原因 |
|------|------|
| **古籍库**（book 系列） | 你专注的是"诗词"，不是整个古籍。如果要扩展知识范围才用得上 |
| **类书**（category 系列） | 古今图书集成、渊鉴类函—这些是类书，不是诗词，跟你的项目方向不同 |
| **词典/典故/佛典** | 典故可以作为诗词背景补充，但需要场景驱动。单独查典故不是你的核心场景 |
| **词谱/曲谱总览** | 创作辅助工具，如果你的 Agent 定位是"找诗"而非"写诗"，相关性低 |
| **景观/地图**（map 系列） | 搜韵的景观系统很强大（西湖、黄鹤楼等），但你的用户不需要在地图上查诗。不过如果有写作地点数据，你可以参考它的**行政区划层级结构**来设计自己的地点数据 |

---

## 三、我的建议

| 优先级 | 接口 | 集成方式 | 理由 |
|--------|------|---------|------|
| **P0** | `/api/writing/{id}/labelize` | 返回诗词结果时，调这个接口补充笺注 | 提升内容深度，用户感知你"懂诗" |
| **P0** | `/api/tool/reference` | 用户追问"这句化用自哪"时调 | 多轮对话体验关键能力 |
| **P1** | `/api/writing/SimilarClauses` | 作为语义检索的补充 | 向量搜不到的，关键词匹配可能搜到 |
| **P1** | `/api/writing/{id}/tones` | 展示诗词时标注平仄 | 细节加分 |
| **P2** | `calendar` 系列 | 如果你做"时间轴"或"按时间查诗"功能 | 目前不需要 |

**核心判断：搜韵 API 可以为你提供"检索结果增强"的能力，但不能替代你自己的语义匹配引擎。**

搜韵做的是检索，你做的是匹配。两条腿走路：
1. 你自己的向量 + KG 做核心匹配
2. 搜韵的接口做结果后处理（笺注、化用分析、平仄标注）

这两个不冲突，反而互补。