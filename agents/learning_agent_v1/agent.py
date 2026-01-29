from llm_client import call_llm

MAX_RETRY = 2

def is_valid(result: dict) -> bool:
    if not isinstance(result, dict):
        return False
    if "summary" not in result:
        return False
    if result.get("confidence", 0) < 0.7:
        return False
    return True


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


def run_agent(goal: str) -> dict:
    state = init_state(goal)
    current_input = goal

    while state["attempt"] <= MAX_RETRY:
        print(f"\n[Agent] Attempt {state['attempt'] + 1}")

        result = call_llm(current_input)

        # 记录一次尝试（短期记忆）
        state["history"].append({
            "attempt": state["attempt"] + 1,
            "input": current_input,
            "output": result
        })

        print("[Agent] LLM Output:", result)

        if is_valid(result):
            print("[Agent] Output accepted ✅")
            state["final_result"] = result
            return state

        print("[Agent] Output rejected ❌, refining input...")
        current_input = (
            goal
            + "\n请更清晰、更具体地总结，避免模糊表述。"
        )
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
