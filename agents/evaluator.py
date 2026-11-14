from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from agents.prompts import EVALUATOR_SYSTEM
from models import Evaluation
from config import MOCK_MODE, OPENAI_MODEL
from pathlib import Path


def load_trusted_reference():
    """Load the trusted RAG reference document."""
    reference_path = (
        Path(__file__).resolve().parent.parent
        / "docs"
        / "rag_reference.md"
    )

    if not reference_path.exists():
        raise FileNotFoundError(
            f"Trusted reference not found: {reference_path}"
        )

    return reference_path.read_text(encoding="utf-8")


RUBRIC = [
    ("A1", "Accuracy and grounding", "Explains RAG accurately; does not claim RAG retrains the model or guarantees correctness."),
    ("B1", "Beginner-friendly language", "Uses simple sentences and explains technical ideas in accessible language."),
    ("C1", "Teaches by example", "Includes a concrete, understandable example that walks through a question and retrieved information."),
    ("D1", "No unexplained jargon", "Defines important terms such as embedding, retrieval, and language model before or when using them."),
    ("E1", "Key-point coverage", "Covers what RAG is, why it matters, and the main stages of how it works."),
    ("F1", "Coherent teaching flow", "Moves in a sensible order from definition to motivation, process, example, limitations, and recap."),
]


def _mock_evaluate(lesson: str) -> Evaluation:
    low = lesson.lower()
    checks = []

    def add(cid, dim, passed, evidence, fix=""):
        checks.append({
            "check_id": cid,
            "dimension": dim,
            "passed": bool(passed),
            "evidence": evidence,
            "fix": fix
        })

    # A1: Accuracy
    false_claims = [
        "rag means the model retrains itself on every question",
        "rag guarantees that every answer is correct",
        "rag automatically fine-tunes the model"
    ]

    inaccurate = any(claim in low for claim in false_claims)

    add(
        "A1",
        "Accuracy and grounding",
        not inaccurate,
        "No known false RAG claim detected."
        if not inaccurate else "A known false RAG claim was detected.",
        "Explain that RAG retrieves external information at answer time."
        if inaccurate else ""
    )

    # B1: Beginner-friendly language
    beginner = (
        len(lesson.split()) >= 180
        and ("think of" in low or "imagine" in low)
    )

    add(
        "B1",
        "Beginner-friendly language",
        beginner,
        "A familiar analogy and sufficient explanation are present."
        if beginner else "Beginner-friendly explanation is insufficient.",
        "Use simple sentences and a familiar analogy."
        if not beginner else ""
    )

    # C1: Practical example
    example = (
        "example" in low
        and ("student" in low or "library" in low)
        and ("question" in low)
    )

    add(
        "C1",
        "Teaches by example",
        example,
        "A practical example is present."
        if example else "A meaningful example is missing.",
        "Explain a real-world question and how RAG finds its answer."
        if not example else ""
    )

    # D1: Jargon explanations
    definitions = (
        "embedding is" in low or "embedding means" in low
    )

    jargon = all(
        term in low
        for term in ["embedding", "retrieval", "language model"]
    ) and definitions

    add(
        "D1",
        "No unexplained jargon",
        jargon,
        "Important technical terms have explanations."
        if jargon else "Some important technical terms need definitions.",
        "Define embedding, retrieval and language model simply."
        if not jargon else ""
    )

    # E1: Coverage
    coverage = all(
        term in low
        for term in ["what is", "why", "how", "retrieve", "generate"]
    )

    add(
        "E1",
        "Key-point coverage",
        coverage,
        "Definition, purpose and working process are covered."
        if coverage else "One or more key concepts are missing.",
        "Explain what RAG is, why it matters and how it works."
        if not coverage else ""
    )

    # F1: Teaching flow
    flow = all(
        term in low
        for term in ["recap", "example", "how does", "why is"]
    )

    add(
        "F1",
        "Coherent teaching flow",
        flow,
        "The lesson follows a logical structure."
        if flow else "The lesson structure needs improvement.",
        "Organize the lesson from definition to example and recap."
        if not flow else ""
    )

    failed = [c for c in checks if not c["passed"]]

    return Evaluation(
        passed=len(failed) == 0,
        checks=checks,
        summary=(
            "All rubric checks passed."
            if not failed
            else f"{len(failed)} of {len(checks)} checks failed."
        ),
        retry_guidance=[
            c["fix"] for c in failed if c["fix"]
        ]
    )



def evaluate_lesson(lesson: str) -> Evaluation:
    if MOCK_MODE:
        return _mock_evaluate(lesson)

    # Load trusted source material
    reference = load_trusted_reference()

    llm = ChatOpenAI(
        model=OPENAI_MODEL,
        temperature=0
    )

    structured = llm.with_structured_output(Evaluation)

    rubric_text = "\n".join(
        f"{cid} | {dim}: {desc}"
        for cid, dim, desc in RUBRIC
    )

    return structured.invoke([
        SystemMessage(content=EVALUATOR_SYSTEM),
        HumanMessage(content=f"""
TRUSTED REFERENCE DOCUMENT:
{reference}

EVALUATION RUBRIC:
{rubric_text}

LESSON TO EVALUATE:
{lesson}

Instructions:
1. Compare factual claims in the lesson against the reference.
2. Identify contradictions and unsupported claims.
3. Do not assume that an unsupported claim is automatically false.
4. If the reference does not contain enough information to verify
   a claim, explain that limitation.
5. Evaluate all six rubric checkpoints.
6. Mark each checkpoint strictly PASS or FAIL.
7. Approve only if every checkpoint passes.
""")
    ])
