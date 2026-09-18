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

> 下一组（Q4–Q6）：Agent 场景该优化 prefill 还是 decode / 量化对工具调用的影响 / 推理引擎选型