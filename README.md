# 🤖 AI Learning Agent

> 一个以 **工程化 + 结构化输出** 为核心的 AI / 大语言模型 / Agent 学习与实践仓库  
> 从「理解模型」到「设计 Agent」，从「Prompt」到「可评估学习系统」

---

## ✨ 项目目标

本仓库用于系统性记录我在学习 **大语言模型（LLM）与 Agent 架构** 过程中的：

- 核心概念理解
- Prompt 与 Agent 的对比与演进
- 结构化输出设计
- Learning Agent 的评估与纠偏机制
- 可复用、可评估、可扩展的学习路径设计

目标不是“记笔记”，而是 **构建一个可以持续演进的 AI Learning Agent**。

---

## 🧠 学习路径（按 Day 组织）

> 每一个 Day 对应一个明确的学习主题与产出

### 📘 基础认知
- [Day1｜LLM 基本理解](./days/Day1_llm_basic_understanding.md)
- [Day2｜AI 知识结构](./days/Day2_AI_knowledge_structure.md)

### ✍️ Prompt 设计与反思
- [Day3｜Prompt 反思](./days/Day3_prompt_reflection.md)
- [Day4｜Prompt vs Agent](./days/Day4_prompt_vs_agent.md)
- [Day5｜Role Prompt 设计](./days/Day5_role_prompt.md)

### 🧩 结构化输出与 Agent
- [Day6｜结构化输出设计](./days/Day6_structured_output_design.md)

---

## 🗂️ 仓库结构说明

```text
AI-learning-agent/
├── agents/        # Learning Agent 不同版本实现与演进
├── concepts/      # AI / LLM / Agent 核心概念拆解
├── days/          # 按天组织的学习路径与产出
├── prompts/       # Prompt 模板与结构化输出示例
├── README.md
├── CONTRIBUTING.md
└── CHANGELOG.md
```
---

## 🔧 Prompt 输出模板

- ./prompts/Prompt_output.md
- ./prompts/Prompt_output_v2.md

---

## 🧪 Learning Agent 设计理念

Learning Agent 的核心职责：

- 评估学习是否完成
- 未达标时强制纠偏
- 通过结构化输出驱动学习闭环

示例输出格式：

```json
{
  "evaluation": "pass | improve | fail",
  "reason": "string",
  "correction_required": "string",
  "next_action": "string"
}
```

---

## 🚀 使用建议

1. 按顺序阅读 `days/`
    
2. 对照 `prompts/` 进行实践
    
3. 理解 `agents/` 中 Learning Agent 的设计
    
4. 构建个人 Agent 学习系统

---
## 📌 项目定位

- 学习型 / 实验型仓库
    
- 强调结构、评估与演进
    
- 非教程、非速成
- 
---

