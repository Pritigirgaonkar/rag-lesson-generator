import argparse, json
from pathlib import Path
from workflow.graph import run_workflow

def main():
    parser = argparse.ArgumentParser(description="Self-evaluating beginner lesson generator")
    parser.add_argument("--topic", default="Introduction to RAG")
    parser.add_argument("--inject-error", action="store_true", help="Add a deliberate false claim to first draft")
    parser.add_argument("--max-retries", type=int, choices=[0,1,2], default=None)
    args = parser.parse_args()
    result = run_workflow(args.topic, args.inject_error, args.max_retries)
    Path("outputs").mkdir(exist_ok=True)
    if result.get("status") == "approved":
        Path("outputs/final_lesson.md").write_text(result["lesson"], encoding="utf-8")
    Path("outputs/rejection_log.json").write_text(json.dumps(result.get("rejection_log", []), indent=2), encoding="utf-8")
    Path("outputs/evaluation.json").write_text(json.dumps(result.get("evaluation", {}), indent=2), encoding="utf-8")
    print(f"Status: {result.get('status')}")
    print(f"Attempts: {result.get('retry_count', 0) + 1}")
    print(f"Rejection log: outputs/rejection_log.json")
    if result.get("status") == "approved":
        print("Approved lesson: outputs/final_lesson.md")
    else:
        print("No lesson approved. Review outputs/evaluation.json and rejection_log.json.")

if __name__ == "__main__":
    main()
