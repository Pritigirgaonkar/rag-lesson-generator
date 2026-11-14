from typing import TypedDict, Any
from langgraph.graph import StateGraph, END
from agents.generator import generate_lesson
from agents.evaluator import evaluate_lesson
from memory.memory_manager import (
    save_run,
    get_memory_summary,
    get_historical_guidance
)
from config import MAX_RETRIES

class AgentState(TypedDict, total=False):
    topic: str
    lesson: str
    evaluation: dict
    retry_count: int
    max_retries: int
    rejection_log: list
    feedback: list
    inject_error: bool
    status: str


def generate_node(state: AgentState):

    # Get feedback from previous runs
    historical_feedback = get_historical_guidance()

    # Get feedback from the current evaluation
    current_feedback = state.get("feedback", [])

    # Combine both types of feedback
    all_feedback = historical_feedback + current_feedback

    lesson = generate_lesson(
        state["topic"],
        feedback=all_feedback,
        inject_error=(
            state.get("inject_error", False)
            and state.get("retry_count", 0) == 0
        )
    )

    return {"lesson": lesson}


def evaluate_node(state: AgentState):
    result = evaluate_lesson(state["lesson"])
    return {"evaluation": result.model_dump()}

def decide_node(state: AgentState):
    evaluation = state["evaluation"]
    failed = [c for c in evaluation["checks"] if not c["passed"]]
    if not failed:
        return {"status": "approved", "feedback": []}
    entry = {
        "attempt": state.get("retry_count", 0) + 1,
        "summary": evaluation["summary"],
        "failed_checks": failed,
        "changes_requested": evaluation.get("retry_guidance", [])
    }
    log = state.get("rejection_log", []) + [entry]
    next_retry = state.get("retry_count", 0) + 1
    if next_retry <= state.get("max_retries", MAX_RETRIES):
        return {"status": "retry", "retry_count": next_retry, "rejection_log": log,
                "feedback": evaluation.get("retry_guidance", [])}
    return {"status": "rejected", "retry_count": next_retry, "rejection_log": log}

def route_after_decision(state: AgentState):
    if state["status"] == "retry":
        return "generate"
    return "finish"

def finish_node(state: AgentState):
    save_run(state["topic"], state.get("retry_count", 0) + 1,
             state["status"] == "approved", state.get("rejection_log", []), state.get("lesson", ""))
    return {}

def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("generate", generate_node)
    graph.add_node("evaluate", evaluate_node)
    graph.add_node("decide", decide_node)
    graph.add_node("finish", finish_node)
    graph.set_entry_point("generate")
    graph.add_edge("generate", "evaluate")
    graph.add_edge("evaluate", "decide")
    graph.add_conditional_edges("decide", route_after_decision, {"generate": "generate", "finish": "finish"})
    graph.add_edge("finish", END)
    return graph.compile()

def run_workflow(topic: str, inject_error: bool = False, max_retries: int | None = None):
    app = build_graph()
    initial: AgentState = {
        "topic": topic,
        "retry_count": 0,
        "max_retries": MAX_RETRIES if max_retries is None else max(0, min(max_retries, 2)),
        "rejection_log": [],
        "feedback": [],
        "inject_error": inject_error,
        "status": "running"
    }
    return app.invoke(initial)
