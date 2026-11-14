# Architecture and Design Notes

## Problem statement
Build a system that creates a beginner lesson and decides whether it meets a minimum quality bar before release. A single generation prompt is insufficient because it does not independently inspect quality or create an auditable rejection trail.

## Components
- **Input layer:** topic, retry limit, and optional deliberate-error flag.
- **Generator:** writes a standalone lesson in Markdown.
- **Evaluator:** applies a six-check binary rubric and returns evidence plus corrections.
- **Decision node:** approves only when every check passes; otherwise retries with feedback.
- **Memory layer:** stores run summaries, rejection logs, and approved lessons in SQLite.
- **Output layer:** final Markdown lesson, JSON evaluation, and rejection log.

## Why separate generation and evaluation?
A separate evaluator creates a distinct quality-control stage. It can challenge the draft instead of treating fluent writing as proof of correctness. The two components may still share model limitations, so factual grounding should be strengthened with source documents and human review for important content.

## Retry policy
The maximum retry count is configurable from zero to two. A failure log is appended before retrying. The next generator call receives the failed checks' specific correction instructions. When the retry budget is exhausted, the workflow ends with `rejected`.

## Self-evolution and memory
The implementation stores failures across runs. It does not silently rewrite its own rubric. A safe next step is to aggregate repeated failures by rubric ID, suggest prompt/rubric updates, test them against a fixed evaluation set, and require human approval before promoting a new rubric version. This gives controlled improvement rather than uncontrolled drift.

## Risks and mitigations
- **Evaluator false pass:** use a fixed test set, reference sources, and human review.
- **Evaluator false fail:** inspect evidence and allow a human override outside the automated gate.
- **Prompt injection in source documents:** treat retrieved text as untrusted data and never as system instructions.
- **API cost or outage:** bounded retries and offline mock mode.
- **Memory privacy:** store only lesson and run data needed for evaluation; do not store secrets or personal learner data.

## Success criteria
1. Produces a standalone lesson.
2. Evaluates every rubric checkpoint as pass/fail.
3. Retries on failure with explicit feedback.
4. Terminates within the configured retry budget.
5. Saves rejection history and run outcome across runs.
6. Demonstrates rejection of a known false statement.
