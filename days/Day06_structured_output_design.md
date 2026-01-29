## Day 6｜结构化输出设计

本文件用于设计 Agent 输出的结构，而不是具体 Prompt。

目标：
让 Agent 的输出可以被“判断、消费、继续执行”。

---

## 场景定义

场景：Learning Agent 判断用户是否完成任务。

---

## 我希望 Agent 输出包含的信息

- 当前任务是什么
- 用户是否完成
- 完成质量如何
- 下一步该做什么

## 输出结构 v1（逻辑结构）

evaluation_result:
- pass
- improve
- fail

reason:
- 为什么是这个判断

next_action:
- 下一步建议

## 输出结构 v1（JSON 形式）

{
  "evaluation": "pass | improve | fail",
  "reason": "string",
  "next_action": "string"
}

### 实操经验


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

## 输出结构 v2（JSON 形式）

{
  "evaluation": "pass | improve | fail",
  "reason": "string",
  "correction_required": "string",
  "next_action": "string"
}

**具体实操：**

`你是一名 Learning Agent。`

`你的职责是评估用户是否完成学习任务，并在未通过时强制纠偏。`

`请严格按照以下 JSON 结构输出，不要输出任何额外文本：`

`{`
  `"evaluation": "pass | improve | fail",`
  `"reason": "string",`
  `"correction_required": "string",`
  `"next_action": "string"`
`}`

`规则：`
- `如果 evaluation 为 "pass"：`
  - `correction_required 必须为空字符串`
  - `next_action 才能进入新任务`
- `如果 evaluation 为 "improve" 或 "fail"：`
  - `correction_required 必须明确指出用户需要补做的内容`
  - `next_action 必须要求用户先完成 correction_required，不得进入新主题`

`现在评估以下用户反馈：`

`用户反馈：`
`“我大概理解了 Prompt 和 Agent 的区别，感觉 Agent 更高级一些。”`

得到的的答复是：

`{`  
`"evaluation": "improve",`  
`"reason": "用户仅给出了模糊感受性判断（“更高级一些”），未准确说明 Prompt 与 Agent 的核心定义、职责边界和关键差异，理解不够具体和可验证。",`  
`"correction_required": "请明确说明 Prompt 与 Agent 的定义，并至少从“是否具备状态/记忆”“是否能自主决策与调用工具”“是否包含持续目标与反馈循环”三个维度进行对比，可辅以一个简单示例。",`  
`"next_action": "请先完成上述对 Prompt 与 Agent 的结构化对比与示例说明，然后再继续进入下一个学习任务。"`  
`}`

这说明Agent在改进之后实现了对于用户反馈的全面回答，这样就构成了agent的底层逻辑：
**一遍又一遍纠错+矫正的机制**