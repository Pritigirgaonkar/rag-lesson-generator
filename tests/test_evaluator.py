from agents.evaluator import evaluate_lesson
from agents.generator import _mock_lesson

from agents.evaluator import load_trusted_reference

def test_trusted_reference_is_available():
    reference = load_trusted_reference()

    assert len(reference) > 100
    assert "Retrieval-Augmented Generation" in reference
    assert "does not automatically retrain" in reference

def test_mock_lesson_passes_rubric():
    lesson = _mock_lesson("Introduction to RAG")
    result = evaluate_lesson(lesson)
    assert result.passed

def test_evaluator_catches_deliberate_false_claim():
    lesson = _mock_lesson("Introduction to RAG", inject_error=True)
    result = evaluate_lesson(lesson)
    assert not result.passed
    assert any(c.check_id == "A1" and not c.passed for c in result.checks)


def test_evaluator_rejects_false_rag_guarantee():
    lesson = _mock_lesson("Introduction to RAG")

    lesson += """
    RAG guarantees that every answer is correct.
    """

    result = evaluate_lesson(lesson)

    assert result.passed is False
    assert any(
        check.check_id == "A1" and not check.passed
        for check in result.checks
    )

