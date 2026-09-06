agent评估：
L1：行为层（确定性·轨迹性）
- tool selectton accuracy：工具选择准确率
- Argument fidelity：参数保真度
- Trajectory conformance 执行路径是否与预期路径一样
- protocol compliance ：协议合规性
- guardrail compliance 护栏合规性
- task success：端到端是否完成任务

L2 语义层
- Faithfulness /groundedness 忠实度：答案是否基于事实，没有编造
- Answer Relevance 答案相关性：答案是否切题
- correctness 正确性：答案对照金标答案对不对
- context preceision 上下文精确度：提供给模型的上下文有多少是真正有用的
- abstention、refusal 拒答：u确定是否正确时拒答而非编造