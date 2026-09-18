---
type: handout
domain: interview/agent
tags: [面试, Agent, LLM, 推理, 题库]
status: living
created: 2026-09-18
updated: 2026-09-18
module: M1
---

# M1 · LLM 基础与推理机制

> 大纲与进度：[[00-大纲与进度]] ｜ 逐日追加，**只加不改**。
> 出题规则：每日 3 题 = 1 概念 + 1 原理 + 1 实操/设计。

## 出题记录

| 日期 | 题号 | 题目 | 难度 |
|---|---|---|---|
| 2026-09-18 | Q1–Q3 | 请求链路 / 采样参数与结构化输出 / KV Cache | ★–★★ |
| 2026-09-18 | Q4–Q6 | prefill vs decode 优化取舍 / 量化对工具调用准确率的影响 / 推理引擎选型 | ★★–★★★ |

---

### Q1 · 概念 ★｜一次 LLM 请求的完整链路：tokenize → prefill → decode → 采样

**考点**：每个阶段的算力与延迟特征；TTFT 与总时延的区别；「输入长」和「输出长」为什么代价不同。

**答案要点**

1. **分词**：文本 → token id（BPE）。中文约 1 字 1–2 token，代码/JSON 更碎（缩进、符号都是 token）。这直接决定计费与上下文预算，也是 Agent 里最容易低估的一项成本。
2. **Prefill（预填充）**：把全部 prompt token **一次性并行**前向计算，产出 KV Cache。算力密集（FLOPs/byte 高），GPU 利用率高；**首字延迟（TTFT）主要由它决定**。
3. **Decode（解码）**：自回归，每步只生成 1 个 token，但每步都要读取全部 KV Cache。**显存带宽密集**（FLOPs/byte 低），单步延迟约等于「读一遍 KV 的时间」；吞吐靠 continuous batching 把多请求拼批。
4. **采样**：logits → 温度 / top-p / top-k → 选出 token；重复第 3 步直到 EOS 或 max_tokens。

**追问**：为什么「输入 10 万 token」只是首字慢，而「输出 1 万 token」是持续慢？→ prefill 是并行的一次性计算；decode 是串行 per-token，时长与输出长度成正比。

**易错点**：把 TTFT 与总时延混为一谈；以为「输入 token 单价低」就等于总成本低——长 prompt 会长期占用 KV Cache 显存、压低并发数。

---

### Q2 · 原理 ★★｜温度 / top-p / top-k 对 Agent 结构化输出稳定性的影响

**考点**：采样参数与「可靠性 vs 多样性」的权衡；Agent 各环节该用什么参数。

**答案要点**

1. **温度 T**：对 logits 做缩放后再 softmax。T→0 近似 argmax（贪心，最稳定）；T 越大分布越平，越容易采到低频 token。
2. **top-k / top-p**：截断策略。top-k 固定候选数；top-p（核采样）按累积概率自适应截断，通常比 top-k 更稳。
3. **Agent 场景分工**：工具调用 / JSON 输出 / 分类抽取 → **T = 0～0.2**；创意文案 → 0.7～1.0；需要探索方案多样性时可临时调高。
4. **为什么高温会毁结构化输出**：JSON 的引号、逗号、右括号属于**低频 token**，分布变平后最容易被替换或漏掉，于是「少一个括号」的解析失败就出现了。
5. **T=0 也不保证合法**：仍需约束解码（grammar/JSON schema）或后处理校验 + 失败重试。

**追问**：T=0 时同一 prompt 一定完全可复现吗？→ 不一定。批处理中的浮点累加顺序、MoE 路由差异、batch 组成变化、硬件/驱动/内核不同，都会让 logits 有微小差异，长输出可能分叉。所以**评测要跑多次看稳定性**，不能只信单次。

**易错点**：只调 temperature 不做 schema 校验；top-p 与 top-k 同时乱设互相干扰。

---

### Q3 · 原理 + 计算 ★★｜KV Cache 是什么、显存怎么算、为什么长上下文贵

**考点**：能写出 KV Cache 显存公式并手算量级；说清长上下文贵的三个原因；至少列 4 种优化手段。

**答案要点**

1. **是什么**：缓存每一层、每个已处理 token 的 Key / Value 向量，decode 时直接复用，避免重算历史。
2. **显存公式**：
   `KV bytes = 2 × layers × kv_heads × head_dim × seq_len × batch × dtype_bytes`
3. **手算量级**（32 层、32 头、head_dim 128、fp16=2B、1 万 token、batch 8）：
   `2×32×32×128×10000×8×2B ≈ 4.2 GB`；若用 GQA（kv_heads=8）则降到约 1 GB。
4. **长上下文为什么贵**：
   - 显存随 seq_len 线性增长 → 并发数被挤掉，甚至要 offload 到 CPU/SSD；
   - decode 每步都要读完整 KV → 带宽成为瓶颈，token/s 下降；
   - prefill 的注意力计算随长度平方增长 → TTFT 上升。
5. **优化手段**：MQA / GQA、KV 量化（FP8 / INT4）、PagedAttention、**前缀缓存（prefix cache）**、跨层 KV 共享、滑窗 / 稀疏注意力。

**追问**：为什么说 prefill 是算力密集、decode 是带宽密集？→ prefill 对全部 token 做一次大矩阵乘（高 FLOPs/byte，GPU 吃满）；decode 每步只算 1 个 token 却要读整份 KV（低 FLOPs/byte，等数据）。

**易错点**：把 KV Cache 说成「把 prompt 存在磁盘上」；算显存时漏掉 batch 维度。

---

### Q4 · 原理 ★★★｜Agent 场景更该优化 prefill 还是 decode？为什么

**考点**：能按 Agent 的真实流量特征（输入远大于输出）判断瓶颈，并给出两侧各自的优化手段与量化依据。

**答案要点**

1. **先量流量特征再谈优化**：聊天场景输入输出比约 1:10，而 Agent 单步请求通常是「长 prompt + 短输出」——system prompt + 工具 schema + 历史 + 检索片段合起来 5k–30k token，模型只回 200–1500 token（含一段 JSON），**输入:输出 ≈ 10:1～50:1**。所以**成本与算力大头在 prefill**，这是与聊天应用最大的区别。
2. **算一笔账**：8B 模型 fp16 跑 10k token prompt，prefill 算力 ≈ `2 × 参数量 × seq_len = 2×8e9×1e4 ≈ 1.6e14 FLOPs ≈ 160 TFLOPs`，在 H800（fp16 峰值约 1000 TFLOPs、实际 MFU 30–50%）上是 0.3–0.5s；而 decode 每步要读一遍权重+KV，8B fp16 权重 16GB，HBM 带宽约 3.35 TB/s → 单序列上限约 **180–200 token/s**，与上下文长度关系不大。
3. **结论：先优化 prefill**，两个理由：① 它是成本和算力的主项；② 多步 Agent 的端到端时延 ≈ `步数 × (TTFT + 工具耗时)`，**TTFT 被 prefill 主导**，N 步循环里 TTFT 的收益被放大 N 倍。
4. **prefill 侧手段**：前缀缓存（prompt caching：写 1.25×、读 0.1× 单价或自动 50% 输入折扣）、上下文裁剪/摘要、把稳定内容（system prompt、工具 schema）放最前面以保证前缀可命中、chunked prefill 让长 prefill 切块与 decode 交错（避免阻塞队列）、P/D 分离部署（prefill 与 decode 拆到不同实例按比例扩缩）。
5. **什么时候该掉头优化 decode**：单轮输出 >2k token（长报告、代码、批处理）、流式体验敏感、高并发下 decode 已经把 KV 带宽吃满（此时吞吐瓶颈是 KV 而非算力）、以及需要压 **TPOT/ITL**（inter-token latency）的语音/交互场景。手段不同：投机解码（speculative decoding，1.5–2.5×）、权重 INT8/FP8（带宽减半）、MTP/EAGLE、小模型草稿。
6. **别搞混两侧手段**：投机解码对 prefill 无收益；前缀缓存对「每次都是全新长文本」的负载收益接近 0；chunked prefill 只改善调度公平性，不减少总算力。

**追问**：前缀缓存为什么要求前缀严格逐字节不变？→ 缓存按 token 前缀的 block 粒度做 hash 匹配（如 16 token/block），prompt 里任何一个早期动态字段（时间戳、随机 session id、按字典序重排的工具列表）都会让该 block 及之后全部 miss，命中率直接掉到 0。所以工程约定是：固定内容在前、动态内容一律后置。

**易错点**：① 拿「输入 token 便宜」推导出长 prompt 无所谓——它还会长期占用 KV 显存、压低并发；② 把 TTFT 与总时延混为一谈，用 decode 手段去治 TTFT。

---

### Q5 · 概念 + 数据 ★★｜量化（int8 / fp8 / int4）对工具调用准确率的影响

**考点**：知道量化的误差从哪来、各精度档的典型退化量级，以及为什么 Agent 对量化的敏感度高于聊天。

**答案要点**

1. **误差机制**：权重/激活从 fp16 降到低位宽会引入舍入误差，真正的杀伤来自**激活离群值（outlier）**——少数通道的激活幅值可达其余通道的数十倍，均匀量化时量化尺度被离群点撑大，其余通道的有效比特被吃掉。所以 INT8 需要 SmoothQuant 之类把激活难度迁移到权重，FP8 需要 per-tensor/per-channel scale 选择。
2. **精度档与典型退化**（同一模型、同评测集的经验量级）：W8A8（INT8）、FP8（E4M3，H100 起原生支持）对困惑度影响通常在 1% 以内，多数任务上与 fp16 差距 ≤1–2 个点；W4A16（GPTQ / AWQ，group_size=128）困惑度退化 1–5%，下游任务掉几个点；INT4 激活量化（W4A4）需更激进技巧，退化显著、工程上要谨慎。
3. **为什么 Agent 比聊天敏感得多**：工具调用是「长链路 + 精确 token」任务——工具名、枚举参数、JSON 括号、数值参数（金额、坐标、ID）。工具名多为低频 token，分布被扰动后模型容易选到语义相近的另一个工具，或让参数少一层嵌套。聊天里这种错误还能被语言通顺掩盖，Agent 里直接表现为**调错工具 / 参数校验失败**，甚至多步任务连锁失败。
4. **正确的评测口径**：不要只看 PPL/MMLU。要跑函数调用类基准（BFCL、τ-bench）**加**自建 200–500 条业务 goldenset，报三级指标：工具选择准确率、参数 exact match 率、多步任务端到端完成率。经验上 FP8/INT8 与 fp16 基本持平，AWQ-INT4 常见 4–10 个点下滑，且错误集中在该模型本就不熟的复杂嵌套 schema 上。
5. **KV Cache 量化是另一个坑**：KV 量化（FP8 KV 已较成熟）直接影响注意力分数，长上下文多步任务上的退化往往比权重量化更明显，表现为「忘了前面的步骤」「丢掉上一步工具结果」。稳妥做法是只对 KV 用 FP8 + per-channel scale，不要对 attention 输出做 INT4。
6. **取舍与补救**：收益很实在——70B 权重从 140GB 降到约 35GB（单机可部署），decode 带宽减半使吞吐接近翻倍。补救手段：按路径分级路由（工具调用/参数抽取走 FP8/BF16，闲聊与摘要走 INT4）、约束解码 + schema 校验兜底、上线前用自家 goldenset 做 A/B，不信公开榜单结论。
7. **口径要一致**：不同量化工具与格式的结果不可直接比较（GGUF Q4_K_M、AWQ、GPTQ、FP8 的量化粒度与校准集都不同），对比实验必须固定格式、校准数据与推理引擎。

**追问**：为什么 KV 量化对长对话 Agent 伤害更大？→ 误差落在 QKᵀ 上会改变注意力分布，长序列中逐层累积放大了分布偏移；权重误差只是让表示略糙，而注意力偏移是直接「看错地方」。

**易错点**：① 拿困惑度（PPL）当结论，认为「PPL 只涨 2% 所以没影响」；② 混用不同量化格式的实测数字互相比较；③ 只测单轮工具调用，漏掉多步场景下的误差累积。

---

### Q6 · 实操 + 选型 ★★｜vLLM / SGLang / TensorRT-LLM 的差异与选型依据

**考点**：说得清三者在 KV 管理、调度、编译方式上的技术差异，并能针对负载给出可辩护的选型决策。

**答案要点**

1. **定位一句话**：vLLM = 通用高吞吐服务框架，PagedAttention 起家，模型/多模态支持最快、生态最广；SGLang = 面向「多轮 + 大量共享前缀 + 结构化输出」的运行时，核心是 RadixAttention；TensorRT-LLM = NVIDIA 官方编译式方案，极致延迟/吞吐，代价是模型支持滞后与编译流程。
2. **KV 管理差异（最关键的辨析点）**：vLLM 用固定大小的 block（默认 16 token）做分页管理，前缀缓存按 block hash 命中；SGLang 的 RadixAttention 用基数树按 token 粒度共享任意公共前缀，天然适合「同一 system prompt + 工具 schema、历史逐轮增长」的 Agent 会话。
3. **调度与内核**：vLLM 有 continuous batching、chunked prefill、优先级与抢占，后端可挂 xgrammar/outlines 做结构化输出；SGLang 提供 overlap scheduler 与原生正则/JSON 约束；TensorRT-LLM 的 in-flight batching、FP8/INT4 kernel 与投机解码优化最全，但每个模型+精度要预先编译 engine（耗时且换卡/换版本要重编）。
4. **性能量级（给区间，不给神话）**：短输出高并发下 vLLM 与 SGLang 常在同一量级，差异多在 10–30% 且随负载翻转；SGLang 在多轮/共享长前缀场景可快 2–5 倍（省掉重复 prefill）；TensorRT-LLM 在小 batch、延迟敏感场景常有 1.2–2× 优势。国内信创或昇腾卡则看 LMDeploy(TurboMind) / MindIE。
5. **决策树（面试直接背这个）**：① 模型长尾多、要第一时间支持新模型、要开源社区可改 → vLLM；② 负载是 Agent 多轮、前缀高度共享、还要约束解码 → SGLang；③ 有 NVIDIA 官方支持、愿接受编译流程、追极致延迟 → TensorRT-LLM；④ 已有 K8s 化部署与多机推理需求 → 先看框架的分布式与 P/D 分离成熟度，再看性能。
6. **Agent 侧真正该看的指标**：不是单轮吞吐峰值，而是 **P99 TTFT、缓存命中率、TPOT/ITL、单卡并发数、以及约束解码的开销**（grammar 约束在大词表上会带来额外处理成本，选型时要实测）。

**追问**：为什么 SGLang 在 Agent 场景常更省算力？→ RadixAttention 把 system prompt、工具 schema、历史对话的公共前缀按 token 粒度做树共享，多轮会话命中率天然高，等价于免费获得前缀缓存；而 block+hash 方案在提示词只有局部差异时也可能因为块边界错过部分缓存块。

**易错点**：① 拿一张 benchmark 图直接下结论（负载、batch、模型不同结论完全相反）；② 只看单轮吞吐，忽略多轮与前缀复用维度；③ 上 TensorRT-LLM 后发现新模型支持慢、出问题改不动内核。

---

> 下一组：M1 Q7–Q8（结构化输出的两种实现 / 前缀缓存为什么对 Agent 特别值钱）+ M2 Q1（system prompt 的分层），M1 收官后进入 M2。