# Self-Evaluating Lesson Content Generator

A small agentic content system for the GenAI Engineer take-home assessment. It creates a beginner lesson, evaluates it using hard pass/fail checkpoints, and retries with evaluator feedback (maximum two retries). It saves run history and rejection logs in SQLite/JSON.

## Features

- **Generator:** creates a standalone beginner lesson for a supplied topic.
- **Evaluator:** checks six dimensions: accuracy, beginner-friendly language, examples, jargon, key-point coverage, and teaching flow.
- **Conditional retry loop:** retries only when at least one checkpoint fails; stops after the configured maximum (0–2 retries).
- **Rejection log:** records failed checks, evidence, and requested changes for each rejected draft.
- **Persistent memory:** stores run metadata and approved lessons in SQLite across executions.
- **Demo mode:** runs without an API key and includes a deliberate-error test.
- **Streamlit UI:** allows topic entry, retry selection, and error injection.

## Architecture

```text
Topic
  |
  v
Generator node -----> Draft lesson
                         |
                         v
                   Evaluator node
                         |
                         v
                    Decision node
                    /          \
                 PASS          FAIL
                  |              |
                  v              v
                Finish      Feedback + retry
                  |              |
                  v              +----> Generator
             SQLite + files
```

The workflow is implemented with LangGraph. The evaluator uses structured output in live mode so each rubric checkpoint is represented as a boolean with evidence and a specific fix. The workflow is deliberately bounded to avoid endless loops.

## Setup

Requires Python 3.10 or newer.

```bash
# 1. Create and activate a virtual environment
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
copy .env.example .env   # Windows
# cp .env.example .env    # macOS/Linux
```

### Run offline (no API key)

In `.env`, set:

```env
MOCK_MODE=true
MAX_RETRIES=2
```

Then run:

```bash
python main.py --topic "Introduction to RAG" --inject-error
```

The first draft contains an intentionally false statement. The evaluator should reject it, give feedback, and the next draft should pass.

### Run with a live model

In `.env`, set:

```env
MOCK_MODE=false
OPENAI_API_KEY=your_real_key
OPENAI_MODEL=gpt-4o-mini
MAX_RETRIES=2
```

Keep your API key private. Never commit `.env` to GitHub. The project uses the `ChatOpenAI` integration; use a model available to your API account.

### Start the web app

```bash
streamlit run app.py
```

Tick **Inject a deliberate error** to demonstrate evaluator rejection and regeneration.

## Run tests

```bash
pytest -q
```

## Output files

- `outputs/final_lesson.md` — latest approved lesson (only written when approved)
- `outputs/rejection_log.json` — failed checks and changes requested
- `outputs/evaluation.json` — final evaluation result
- `memory/agent_memory.sqlite3` — persistent run history and approved lesson records

Generated runtime files are intentionally excluded from version control.

## Rubric design

Every checkpoint is binary. The lesson is approved only if **all six** pass.

| ID | Dimension | Pass condition |
|---|---|---|
| A1 | Accuracy and grounding | No false claim that RAG retrains the model or guarantees correctness |
| B1 | Beginner-friendly language | Accessible explanation and familiar analogy |
| C1 | Teaches by example | Concrete question-to-retrieved-context-to-answer example |
| D1 | No unexplained jargon | Key terms are defined in simple language |
| E1 | Key-point coverage | What, why, and how are all covered |
| F1 | Coherent teaching flow | Logical order with example, limitations, and recap |

**Important limitation:** an LLM evaluator is not a perfect truth oracle. In live mode, use it as a quality gate, not proof of correctness. For high-stakes or factual lessons, add trusted reference documents, claim-level citations, and human review.

## Memory and self-evolution

The SQLite store preserves run outcomes and rejection logs across runs. This is persistent operational memory, not model-weight training. The current implementation also feeds the current run's evaluator feedback into the retry prompt. A next iteration could summarize repeated failures by rubric ID and use that summary to propose rubric/prompt revisions, with human approval and versioning.

## Design choices and trade-offs

1. **LangGraph:** explicit nodes and conditional edges make the loop inspectable.
2. **Separate generator and evaluator:** reduces the chance that the generator simply declares its own work successful.
3. **Binary rubric:** makes the release gate clear and auditable.
4. **Two-retry cap:** controls cost and guarantees termination.
5. **SQLite:** simple local persistence without requiring a hosted database.
6. **Mock mode:** lets reviewers run the demonstration without credentials; live mode uses an API model.
7. **Streamlit:** fast way to show an end-to-end workflow without spending time on frontend complexity.

## Suggested 15–20 minute demo

1. Introduce the problem and architecture (2–3 min).
2. Run a normal topic and show the lesson plus all six checks (3 min).
3. Enable deliberate error injection and show A1 fail (3 min).
4. Show feedback, retry, and final pass (3 min).
5. Open rejection log and SQLite memory (2 min).
6. Explain trade-offs, limitations, and next improvements (3–4 min).

## Repository checklist

- [ ] Add your own name and contact details if desired.
- [ ] Run tests locally.
- [ ] Run the demo in mock mode and record screenshots.
- [ ] Add your own Loom video link to this README after recording.
- [ ] Push the project to a public/private GitHub repository as required by the recruiter.
