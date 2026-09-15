# Reflexion 范式

## 大纲

### 1. 概念
- Reflexion = 执行失败后**反思原因**，带着"教训"重试，形成 尝试 → 反思 → 再尝试 的循环

### 2. 核心循环
```
执行任务
  ├─ 成功 → 返回结果
  └─ 失败 → 反思（为什么失败）→ 生成教训/新策略 → 重试
                                            ↑
                          max_retries 内循环，或达到上限兜底
```

### 3. 反思输出
- 失败原因分析
- 具体教训（下次别这样做）
- 新策略（下次怎么做）

### 4. 伪代码
```
for attempt in range(max_tries):
    result = execute(task)
    if is_success(result):
        return result
    feedback = evaluate(result, task)          # 外部/自评信号
    reflection = llm.reflect(task, result, feedback)  # 反思
    task = revise(task, reflection)            # 修订策略
return fallback_answer
```

### 5. 反思信号的来源
- 工具报错信息
- 自评打分（忠实度、相关性）
- 外部校验结果
- 人工反馈

### 6. 优点
- 显著提升复杂/可重试任务的最终成功率
- 经验可沉淀（教训写入记忆）

### 7. 缺点
- 多次重试成本高
- 反思质量依赖模型能力
- 无脑重试可能浪费资源

### 8. 适用场景
- 高难度任务（代码生成、推理题）
- 对成功率要求高的场景
- 可与 ReAct 结合（失败后反思再试）

### 9. 设计要点
- 设置最大重试次数与兜底答案
- 反思必须"可执行"（能转化为具体改动）
- 记录反思轨迹用于复盘
