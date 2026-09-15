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

- **已认领**：`10-AI/agent-engineering/`(13) `10-AI/protocol/`(4) `10-AI/eval/`(4) 共 21 篇，
  由 `my-agent-lab/backend/content/*.md` 反向生成，**笔记库现为写作源**。
- `10-AI/ops/` **不持有实体笔记**：站点的 `ops` 分区与 `agent-engineering` Harness 层
  是同一批 6 张卡（交叉视图），实体统一在 `agent-engineering/`。
- **frontmatter 分层**：根级放笔记规范字段；站点渲染字段收进 `site_meta:` 嵌套块
  （`id/name/icon/difficulty/accent/prompts/techFilters/…`）；另加
  `publish: true` / `site: <分区>` / `cardId: <id>`。
  ⚠️ 站点字段**不要平铺**，否则 `tags` 键重复、YAML 解析会丢字段。
- 尚未认领：站点 `agent` 分区 8 张卡。

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

## 环境坑（Windows）

- **`git mv` 在中文路径下会静默失败** → 批量移动文件一律用 Python `shutil.move`。
- **`git rm -r "中文路径"` 会截断成上层目录** —— 曾误删整个 `99-Archive/`（65 文件）。
  → **中文路径不要传给 `git rm` / `git mv`**；改用 Python `unlink`/`rmtree` + `git add -A`。
- **`git reset --hard` 会清掉未提交内容**（含未跟踪新文件）→ **阶段性成果尽早 commit**。
- 判断磁盘真实状态用 Python `rglob`，**不要用 Git Bash 的 `find`**（中文路径返回空）。
- `git status`/`git ls-files` 显示的路径不代表磁盘有文件——索引可能领先于工作区。
- 校验内容完整性时须把 `\r\n` 规范化为 `\n`，否则 git show 与工作区会全部误判为不同。
- 沉淀技能：`~/.workbuddy-ai/skills/windows-bulk-file-move/SKILL.md`
