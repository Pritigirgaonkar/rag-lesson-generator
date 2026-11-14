from typing import Literal
from pydantic import BaseModel, Field

class CheckResult(BaseModel):
    check_id: str
    dimension: str
    passed: bool
    evidence: str = Field(description="Brief evidence supporting pass or fail")
    fix: str = Field(default="", description="Specific correction if failed")

class Evaluation(BaseModel):
    passed: bool
    checks: list[CheckResult]
    summary: str
    retry_guidance: list[str] = []

class WorkflowState(dict):
    """LangGraph state is represented as a TypedDict in graph.py."""
