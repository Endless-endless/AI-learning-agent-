import time

from memory_store import (
    load_memory,
    save_memory,
    record_success,
    record_failure,
    record_reflection
)

from llm_client import call_llm

MAX_RETRY = 2


def is_valid(result: dict, strict_mode: bool) -> bool:
    if not isinstance(result, dict):
        return False
    if "summary" not in result:
        return False

    threshold = 1.1
#    threshold = 0.8 if strict_mode else 0.7
    return result.get("confidence", 0) >= threshold


def init_state(goal: str) -> dict:
    """
    初始化 Agent 状态（短期记忆）
    """
    return {
        "goal": goal,
        "attempt": 0,
        "history": [],
        "final_result": None
    }


def should_be_stricter(memory, goal: str) -> bool:
    """
    根据历史失败次数决定是否启用严格模式
    """
    failures = memory.get("failures", [])
    failed_goals = [f["goal"] for f in failures]
    return failed_goals.count(goal) >= 2


def generate_reflection(goal: str, bad_output: dict) -> str:
    """
    失败反思生成（Day 13 核心）
    """
    prompt = f"""
刚才这个 AI 输出没有通过校验。

任务目标：
{goal}

模型输出：
{bad_output}

请用简洁的语言总结：
1. 这个输出为什么不合格
2. 下次回答时应该如何改进

请直接给出反思总结，不要重复原答案。
"""
    reflection = call_llm(prompt)

    if isinstance(reflection, dict):
        return reflection.get("summary", "")
    return str(reflection)


def run_agent(goal: str) -> dict:
    memory = load_memory()
    strict_mode = should_be_stricter(memory, goal)

    if strict_mode:
        print("[Agent] Strict mode enabled due to past failures")

    state = init_state(goal)

    # ===== Day 13：使用历史反思 =====
    past_reflections = [
        r["reflection"]
        for r in memory.get("reflections", [])
        if r["goal"] == goal
    ]

    if past_reflections:
        reflection_hint = "以下是你过去在该任务中的失败经验，请在回答时避免这些问题：\n"
        for r in past_reflections:
            reflection_hint += f"- {r}\n"
        current_input = reflection_hint + "\n\n" + goal
    else:
        current_input = goal

    # ===== 主控制循环 =====
    while state["attempt"] <= MAX_RETRY:
        time.sleep(1.5)
        print(f"\n[Agent] Attempt {state['attempt'] + 1}")

        try:
            result = call_llm(current_input)
        except RuntimeError as e:
            if str(e) == "RATE_LIMIT":
                print("[Agent] Rate limited, backing off...")
                time.sleep(3)
                continue
            else:
                raise

        state["history"].append({
            "attempt": state["attempt"] + 1,
            "input": current_input,
            "output": result
        })

        print("[Agent] LLM Output:", result)

        # ===== 成功分支 =====
        if is_valid(result, strict_mode):
            print("[Agent] Output accepted ✅")
            state["final_result"] = result
            record_success(memory, state)
            save_memory(memory)
            return state

        # ===== Day 13：失败反思（仅在最后一次失败时生成）=====
        if state["attempt"] == MAX_RETRY:
            try:
                reflection = generate_reflection(goal, result)
                record_reflection(memory, goal, reflection)
            except Exception:
                pass

        # ===== 失败记录 =====
        record_failure(memory, state)
        save_memory(memory)

        print("[Agent] Output rejected ❌, refining input...")
        current_input = goal + "\n请更清晰、更具体地总结，避免模糊表述。"
        state["attempt"] += 1

    print("[Agent] Max retry reached, returning last result")
    state["final_result"] = result
    return state


if __name__ == "__main__":
    state = run_agent("我想学习如何构建一个 AI Agent")

    print("\n[Agent] Final Result:")
    print(state["final_result"])

    print("\n[Agent] History:")
    for step in state["history"]:
        print(step)
