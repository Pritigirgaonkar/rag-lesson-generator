import sqlite3
import json
from pathlib import Path
from datetime import datetime, timezone

DB_PATH = Path("memory/agent_memory.sqlite3")

def _connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''CREATE TABLE IF NOT EXISTS runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT NOT NULL,
        topic TEXT NOT NULL,
        attempts INTEGER NOT NULL,
        passed INTEGER NOT NULL,
        rejection_log TEXT NOT NULL
    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS lessons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT NOT NULL,
        topic TEXT NOT NULL,
        lesson TEXT NOT NULL
    )''')
    return conn

def save_run(topic: str, attempts: int, passed: bool, rejection_log: list, lesson: str):
    now = datetime.now(timezone.utc).isoformat()
    with _connect() as conn:
        conn.execute("INSERT INTO runs(created_at,topic,attempts,passed,rejection_log) VALUES(?,?,?,?,?)",
                     (now, topic, attempts, int(passed), json.dumps(rejection_log)))
        if passed:
            conn.execute("INSERT INTO lessons(created_at,topic,lesson) VALUES(?,?,?)", (now, topic, lesson))

def get_memory_summary(limit: int = 10):
    with _connect() as conn:
        rows = conn.execute("SELECT created_at,topic,attempts,passed,rejection_log FROM runs ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    return [{"created_at": r[0], "topic": r[1], "attempts": r[2], "passed": bool(r[3]), "rejection_log": json.loads(r[4])} for r in rows]

def get_past_lessons(topic: str, limit: int = 3):
    with _connect() as conn:
        rows = conn.execute("SELECT lesson FROM lessons WHERE topic=? ORDER BY id DESC LIMIT ?", (topic, limit)).fetchall()
    return [r[0] for r in rows]

def get_historical_guidance(limit: int = 20):
    """
    Learn from previous rejected drafts.
    Collect frequently failed checkpoints and their suggested fixes.
    """
    history = get_memory_summary(limit)
    failure_counts = {}
    guidance = {}

    for run in history:
        for rejection in run.get("rejection_log", []):
            for check in rejection.get("failed_checks", []):
                check_id = check.get("check_id")
                fix = check.get("fix")

                if check_id and fix:
                    failure_counts[check_id] = (
                        failure_counts.get(check_id, 0) + 1
                    )
                    guidance[check_id] = fix

    result = []

    for check_id, count in failure_counts.items():
        result.append(
            f"Historical issue: {check_id} failed "
            f"{count} time(s). Improvement: {guidance[check_id]}"
        )

    return result
