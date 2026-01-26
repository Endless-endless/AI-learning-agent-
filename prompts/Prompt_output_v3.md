
这是在Day7学习了反馈和控制流之后的一个实验案例，核心目的就是认识到纠偏的工作机制：

`你是一名学习 Agent。`

`目标：`
`评估用户是否理解“为什么需要纠偏机制”。`

`请遵守以下 JSON 结构：`
`{`
  `"evaluation": "pass | improve | fail",`
  `"reason": "string",`
  `"correction_required": "string",`
  `"next_action": "string"`
`}`

`现在评估以下用户回答：`
`“我想 Agent 能纠偏是因为它比 Prompt 更高级。”`

`请返回 JSON。`
