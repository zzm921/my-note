# 项目约定（my-note / my-agent-lab）

## 两个仓库的关系

| 仓库 | 路径 | 远程 | 角色 |
|---|---|---|---|
| my-note | `D:\workspace\my-note` | `git@github.com:zzm921/my-note.git` | **笔记库，唯一写作源**（Obsidian） |
| my-agent-lab | `D:\workspace\my-agent-lab` | `git@github.com:zzm921/my-agent-lab.git` | **线上站点，产物**（Vue3 + FastAPI） |

**核心约定**：笔记库是源，站点是产物。不要在站点里手工大改卡片正文——改笔记、跑同步脚本。

## 站点内容机制（重要）

- 内容源目录：`my-agent-lab/backend/content/`，**一篇 md = 一张卡片**，共 45 张。
- 权威索引：`backend/content/tags.md`（声明 7 个分区 → groups → 卡片 id 顺序）。
- 读取方式：`backend/app/api/content.py` **每次请求实时读盘**，因此**改卡片正文后服务器只需 `git pull`，刷新页面即生效，无需 build、无需重启**。
- 卡片 md 格式：YAML frontmatter（`id/name/shortDesc/icon/difficulty/...`）+ 正文（从 `##` 开始，**不含 H1**）。
- `experience: false` = 纯知识卡（隐藏「立即体验」按钮）。

站点 7 个分区：`agent-engineering` / `agent` / `rag` / `protocol` / `eval` / `ops` / `ml`。

## 笔记库设计规范要点

- 顶层目录：`00-Inbox` `01-Maps` `10-AI` `20-Backend` `30-Data` `40-Network` `50-Ops` `60-Frontend` `70-Interview` `80-Projects` `90-Daily` `95-Life` `99-Attachments` `99-Archive` `_Templates`。
- `10-AI/*` 七个子目录与站点七分区一一对应。
- 全文规范见 `01-Maps/文档体系设计与规范.md`。
- 发布字段：`publish: true` + `site: <分区>` + `cardId: <kebab-case>`，默认不发布。
- 正文硬性要求：第一行 H1（全文唯一）+ 紧跟 `> 摘要行`；分节只用 `##`/`###`；站外不渲染 `[[双链]]`。
- 命名：文件名不含空格；序号只用 `NN-` 前缀；目录不用「学习」等冗余词。

## 站点卡片认领与发布字段

- **已全部认领**（站点 7 分区 → 笔记库）：

  | 站点分区 | 卡片数 | 笔记库位置 | 备注 |
  |---|---|---|---|
  | `agent-engineering` | 7（+Harness 7） | `10-AI/agent-engineering/` | 13 篇，已认领 |
  | `agent` | 8 | `10-AI/agent/` | 8 篇，已认领 |
  | `rag` | 13 | `10-AI/rag/` | 11 篇（另 2 篇评评估归 `eval/`） |
  | `protocol` | 4 | `10-AI/protocol/` | 4 篇，已认领 |
  | `eval` | 4 | `10-AI/eval/` | 4 篇，已认领 |
  | `ops` | 6 | — | ✅ 复用 `agent-engineering` Harness 层 |
  | `ml` | 4 | `10-AI/ml/` | 笔记为源，只补发布声明 |

- **frontmatter 分层**：根级放笔记规范字段；站点渲染字段收进 `site_meta:` 嵌套块
  （`id/name/icon/difficulty/accent/prompts/techFilters/…`）；另加
  `publish: true` / `site: <分区>` / `cardId: <id>`。
  ⚠️ 站点字段**不要平铺**，否则 `tags` 键重复、YAML 解析会丢字段。
- `10-AI/ops/` **不持有实体笔记**：站点的 `ops` 分区与 `agent-engineering` Harness 层
  是同一批 6 张卡（交叉视图），实体统一在 `agent-engineering/`。

## ⚠️ 认领前必须抽样判定「谁是源」

**不要默认笔记库更全**——实测两边都可能更成熟，方向反了会把好内容覆盖掉：

| 域 | 比对 | 结论 |
|---|---|---|
| `rag` | 站点卡片 7~27KB vs 笔记旧提纲 1.7~2.9KB | **站点为源** → 反向认领，旧提纲归档到 `99-Archive/rag-旧提纲/` |
| `ml` | 笔记 14~16KB vs 站点卡片 4~5KB | **笔记为源** → 只补 3 行发布声明 |

做法：先挑 3 对同名/同 id 文件比字节数与结构，再定整批方向。

## 附件约定

- **图片统一放 `99-Attachments/`**（Obsidian `attachmentFolderPath` 已设为该目录）。
- 引用写法用 Obsidian wiki-embed **`![[文件名.png]]`** —— 按文件名解析、与目录无关，移动文件不断链。**优先用这种写法**。
- 避免相对路径 `../` 引用（目前仅 1 处，已改）。
- ⚠️ **判「孤儿附件」必须扫四种语法**：wiki-embed / Markdown 图片 / 裸路径(含 gitbook) /
  **被转义的 wiki-embed**（`!\[\[`）。只扫一种会大量误判——曾把 23 张活图判成孤儿。
  另外文件名**可能含空格**，正则别写 `[^>\s)]+`。

## 用户偏好

- 会先要「规划与设计」，确认后再实施；方案要给实施阶段划分与风险。
- 重视「现状诊断要有证据」（数量、路径、实测结论），不接受空泛建议。
- 说「执行」即表示已确认，可以动手；但**破坏性操作前须自行打还原点**。
- 会质疑既有结论（如「孤儿图片该删吗」），**要用事实回答，不能顺着说**——
  结论与事实相反时要明确说不，并给出证据。

## 图谱与链接规范（Obsidian）

- ⚠️ **图谱节点按「文件名」标识，不显示文件夹**。所以入口文档**不能都叫 `README.md`**——
  19 个同名节点在图上完全无法区分。
- 现约定入口文档命名为 **`<域>-地图.md`**，域内唯一、图谱可直接辨识。
  例：`10-AI/rag/RAG-地图.md`、`20-Backend/后端-地图.md`、根目录 `库总览.md`。
  全部 18 个子域 + 根目录共 19 个（`99-Archive/归档区-地图.md` 等）。
- 代价：失去 GitHub 上 README 自动渲染。**这是用户明确认可的取舍**。
- 图谱配色在 `.obsidian/graph.json` 的 `colorGroups`，按顶层目录着色；
  归档/日报/模板用灰色淡化，核心域鲜艳色。
- 全库 `[[链接]]` 的**两种形态都要处理**：
  - 表格内转义管道符 `[[路径\|别名]]` ← 最容易漏，正则要写 `\\?\|`
  - Markdown 链接 `[文本](路径.md)` ← `SUMMARY.md` 全用这种
- 孤岛诊断口径：**出链 × 入链**。必须分层——归档/日报/模板孤立属正常（豁免），
  只看剩余部分才有意义。目前 245 篇中 50 篇值得处理。
- ⚠️ **跨目录断链最隐蔽**：目录重组后，文档里 `[x.md](x.md)` 这类**同目录相对链接**
  最容易断（文件被分到兄弟目录了）。校验器若只按**文件名兜底匹配**会静默放过。
  → 解析顺序必须是「同目录 → 库根 → 裸文件名兜底」。
  已修案例：`agent/multi-agent.md → ../agent-engineering/task-system.md`。
- 校验器报告要**区分真断链 vs 四类合法误报**：语法示例/占位符、跨仓库外链
  （`file:///`、`../app/...`）、图片名占位（`xxx.png`）、归档模板示例。
- **系列长文**（如 ML 十篇）加「上一篇/下一篇」导航块，用 `<!-- ml-nav -->`
  这类注释标记包裹，便于幂等重跑。

## 内容质量分档口径

- 用 `effective = words + code_lines * 8` 判档，**不能只看字数**：
  代码密集型笔记（手写实现、面试题）文字少但价值高。
  踩过：`Promise详解.md` 报「202 字/薄」，实际 12,371 字节 / 453 行。
- 档位阈值：`<80` 空壳 / `<300` 薄 / `<1200` 一般 / `<3000` 充实 / 其余厚重。
- 当前分布（246 篇）：厚重 98 / 充实 47 / 一般 75 / 薄 16 / 空壳 9。
  脚本：`.workbuddy-ai/scripts/audit_quality.py`

## 笔记 frontmatter 规范（已全库落地）

- 字段：`type` / `domain` / `tags` / `status` / `created` / `updated`（可选 `source`）。
- `type`：`concept` / `tutorial` / `howto` / `issue` / `moc` / `daily`。
- `status`：`draft`（草稿，正文<300字或含 todo）/ `done` / `living`（地图类）。
- `domain`：**语义化路径**，如 `ai/ml`、`backend/node/db`、`ops/gitlab`、`frontend/typescript`；元文件用 `元`。**不要用目录名**（如 `10-AI`）。
- **`90-Daily` 日报是例外**：不套用完整规范，只按 `YYYY-MM-DD.md` 命名，靠文件名做时序检索。
- 维护脚本：`.workbuddy-ai/scripts/add_frontmatter.py`（dry-run 默认，带 `OVERRIDE` 人工覆写表）。

## 归档约定

- `99-Archive/` 只进不出，**归档 ≠ 删除**，且必登记（写入 `99-Archive/README.md` 或专项清单）。
- 合并/重命名后原文归档，不在主区留同名副本，引用改指向新合并稿。
- 现有归档子目录：`agent-旧提纲/` `rag-旧提纲/` `typescript-碎片/` `碎片/`
  `合并-2026-09-16/` `空壳清理-2026-09-16/`。
  （`孤儿图片/` 已撤销——那 23 张全是活图，已还原至 `99-Attachments/`）
- ⚠️ 归档后要跑**全库断链检查**；注意 `01-Maps/迁移清单-待确认.md` 是纯路径表（无 `[[`），
  不算断链，别误改。
- 归档用 Python `shutil.move` / `Path.replace`，**不要用 git 的中文路径子命令**。

## 有用脚本（`.workbuddy-ai/scripts/`）

| 脚本 | 用途 |
|---|---|
| `claim_site_cards.py` | 从站点卡片反向认领生成笔记源（`SECTIONS` 声明分区/目录/卡片；默认 dry-run） |
| `fix_site_meta.py` | 把平铺的站点字段收敛进 `site_meta:` 块，消除重复键（改 `DIRS` 列表） |
| `fix_gitbook_imgs.py` | GitBook 相对路径 → `![[wiki-embed]]` |
| `archive_rag_stubs.py` | 把被取代的薄提纲搬入 `99-Archive/`（可改 `STUBS` 复用） |
| `rename_readmes.py` | README → `*-地图.md` 批量改名 + 引用改写（幂等，默认 dry-run） |
| `fix_readme_refs.py` | 补齐转义管道符 `\|` 与 Markdown 链接形态的引用改写 |
| `configure_graph.py` | 配置 `.obsidian/graph.json` 的颜色分组与布局参数 |
| `diagnose_islands.py` | 孤岛笔记诊断（出链×入链，含豁免区分层） |
| `audit_quality.py` | 内容质量盘点（`words + code_lines*8` 分档） |
| `verify_all_links.py` | **全库链接完整性校验**（wiki + md，区分真断链与合法误报） |
| `find_orphan_images.py` | 孤儿附件扫描（四语法覆盖 + 排除远程 URL 与清单自登记） |
| `add_frontmatter.py` | 全库补 frontmatter（带人工 `OVERRIDE` 表） |
| `merge_ts.py` | 合并碎片笔记 |

> 习惯：一次性脚本前加 `_`（如 `_check_xxx.py`），常驻可复用脚本不加。

## 环境坑（Windows）

- **`git mv` 在中文路径下会静默失败** → 批量移动文件一律用 Python `shutil.move`。
- **`git rm -r "中文路径"` 会截断成上层目录** —— 曾误删整个 `99-Archive/`（65 文件）。
  → **中文路径不要传给 `git rm` / `git mv`**；改用 Python `unlink`/`rmtree` + `git add -A`。
- **`git reset --hard` 会清掉未提交内容**（含未跟踪新文件）→ **阶段性成果尽早 commit**。
- 判断磁盘真实状态用 Python `rglob`，**不要用 Git Bash 的 `find`**（中文路径返回空）。
- `git status`/`git ls-files` 显示的路径不代表磁盘有文件——索引可能领先于工作区。
- 校验内容完整性时须把 `\r\n` 规范化为 `\n`，否则 git show 与工作区会全部误判为不同。
- 沉淀技能：`~/.workbuddy-ai/skills/windows-bulk-file-move/SKILL.md`
