
`你是一名 Learning Agent。`

`你的任务是评估用户是否完成指定学习任务。`

`请严格按照以下 JSON 格式输出，不要输出任何多余文本：`

`{`
  `"evaluation": "pass | improve | fail",`
  `"reason": "string",`
  `"next_action": "string"`
 `}`

`现在评估以下用户反馈：`

`用户反馈：`
`“我已完成任务，结果如下：我理解了 Prompt 和 Agent 的核心区别，Prompt 是一次性指令，而 Agent 是有流程和状态的系统。”`


我在GPT上用这段话进行试验，得到以下结果：


`{`  
`"evaluation": "pass",`  
`"reason": "用户准确理解了 Prompt 与 Agent 的核心区别，能够清晰指出 Prompt 是一次性指令，而 Agent 具备流程与状态，符合学习目标。",`  
`"next_action": "可以继续学习 Agent 的关键组成部分，例如工具调用、记忆机制和决策循环。"`  
`}`

显然，这里我设计了一个输出接口，而AI也符合了我们的接口规范。
目前已经实现了**用户反馈 → Agent评估 → JSON输出**

这也就是接下来我们继续打造agent的基础。
