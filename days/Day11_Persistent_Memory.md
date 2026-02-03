# 📘 Day 11｜Agent 长期记忆（Persistent Memory）

> 今日主题：  
> **让 Agent 在程序重启后仍然“记得发生过什么”**

---

## 一、今日目标（What）

> 今天要解决的核心问题是什么？

`构建 Agent 的长期记忆机制，使 Agent 能够在多次运行之间保留成功与失败的经验，而不是每次都从零开始。`

---

## 二、Agent 能力升级（What Changed）

> 对比 Day 10，Agent 今天多了什么“不可逆能力”？

-  引入长期 memory（跨运行存在）
    
-  明确区分 state（运行态）与 memory（经验态）
    
-  成功 / 失败结果被结构化记录
    
-  Agent 开始具备“经验积累”的基础
    

---

## 三、核心结构设计（How）

### 1️⃣ State（短期运行态）

`state = {`
    `"goal": goal,`
    `"attempt": int,`
    `"history": list,`
    `"final_result": dict | None`
`}`

**定位：**

- 仅在一次 Agent 执行中存在
    
- 描述“这一次任务是如何被解决的”
    
- 是 memory 的事实来源（source of truth）
    

---

### 2️⃣ Memory（长期经验）

`memory = {`
    `"successes": [],`
    `"failures": []`
`}`

**定位：**

- 跨多次运行存在
    
- 存储的是“经验总结”，而非过程流水
    
- 与具体 Prompt 解耦
    

---

## 四、关键工程认知（Key Insights）

> 今天真正想通的几件事

### 1️⃣ state ≠ memory

`state 描述的是“我这一次在干什么” memory 描述的是“我以前学到了什么”`

两者的边界不是数量或 retry 次数，而是：

> **是否在程序重启后仍然存在**

---

### 2️⃣ memory 只能记录“已成为事实的结果”

一个关键错误与修正：

- ❌ 在 `state["final_result"]` 尚未确定前写 memory
    
- ✅ 先确认结果 → 再记录 memory
    

`state 是事实源，memory 是基于事实的历史`

memory 记录的是一次 Agent 执行结束后，
由 state 确认的最终 outcome（**无论成功或失败**），
而不是中途的候选输出或未完成的状态。

---

### 3️⃣ LLM 的输出 ≠ Agent 的事实

- LLM 输出只是候选
    
- 只有被 Agent 接受的结果，才进入 memory
    
- 决策权始终在 Agent 程序中
    

---

## 五、今日遇到的问题 & 修正（Debug Notes）

### 问题：

`TypeError: 'NoneType' object is not subscriptable`

### 根因：

- 在写 memory 时，`state["final_result"]` 尚未赋值
    

### 修正原则：

`先更新 state，再写 memory`

这是一个典型的 **Agent 状态时序问题**。

---

## 六、与 Day 10 的本质差异

|Day 10|Day 11|
|---|---|
|Agent 有控制流|Agent 有经验|
|state 存在|state + memory|
|一次性运行|跨运行持续|
|不会“记住”|开始“积累”|

---

## 七、当前 Agent 的能力边界（Reality Check）

> 现在的 Agent 还**不能**做什么？

- ❌ 主动利用 memory 影响决策
    
- ❌ 避免重复失败
    
- ❌ 形成策略偏好
    

👉 这些是 **Day 12 的目标**。

---

## 八、今日一句话总结（One-liner）

`Day 11 让我意识到：Agent 的学习不来自模型，而来自对“事实与经验”的工程化管理。`