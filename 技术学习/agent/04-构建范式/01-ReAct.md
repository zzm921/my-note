# ReAct 范式

## 大纲

### 1. 概念
- ReAct = **Reasoning + Acting**，推理与行动交替进行，形成"思考→行动→观察"循环

### 2. 核心循环
```
Thought  (分析现状、决定下一步)
  ↓
Action   (调用工具 / 执行动作)
  ↓
Observation (观察结果)
  ↓
Thought  (基于结果继续推理)
  ... 直到无需行动 → Final Answer
```

### 3. 示例轨迹
```
Thought: 用户想知道北京的天气，需要天气工具
Action: get_weather(city="北京")
Observation: 晴，26℃
Thought: 天气晴好，直接回答
Final: 今天北京晴，26℃
```

### 4. 伪代码
```
messages = [system, user]
while True:
    resp = llm.chat(messages)
    if resp.action:
        obs = execute(resp.action)
        messages.append(obs)     # Observation 回填
    else:
        return resp.final_answer
```

### 5. 优点
- 可解释：决策路径完整可追溯
- 灵活：边做边改，适应动态任务
- 简单：无需预先完整规划

### 6. 缺点
- 每步都调 LLM，成本与延迟高
- 可能出现无效循环（Action → 失败 → 再 Action）
- 长任务容易丢失原始目标

### 7. 适用场景
- 需要与工具/环境频繁交互的任务
- 步骤不固定、结果影响后续的任务

### 8. 改进方向
- 加入最大步数 / 时间限制
- 失败时带反思重试（ReAct + Reflexion）
- 高成本场景改用 Plan-and-Execute
