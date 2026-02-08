import json
import os
import time
from datetime import datetime

MEMORY_FILE = "agent_memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {"failures": [], "successes": []}
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

def record_success(memory, state):
    assert state["final_result"] is not None, "final_result must exist before recording success"

    memory["successes"].append({
        "goal": state["goal"],
        "summary": state["final_result"]["summary"],
        "confidence": state["final_result"]["confidence"],
        "timestamp": datetime.now().isoformat()
    })

def record_failure(memory, state):
    memory["failures"].append({
        "goal": state["goal"],
        "history": state["history"],
        "timestamp": datetime.now().isoformat()
    })

# ✅ Day 13 新增：记录反思
def record_reflection(memory, goal, reflection_text):
    memory["reflections"].append({
        "goal": goal,
        "reflection": reflection_text,
        "timestamp": time.time()
    })