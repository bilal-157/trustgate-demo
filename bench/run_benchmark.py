"""
TrustGate Benchmark Runner
Loops through all seeded issue branches + clean branches,
triggers the orchestrator, and compares findings against ground truth.
"""
import json
import subprocess
import time
import os
from pathlib import Path

CASES = json.loads(Path("bench/cases.json").read_text())
DEMO = Path("demo_target/base")


def checkout(branch):
    subprocess.run(["git", "-C", str(DEMO), "checkout", branch], check=True)


def run_orchestrator(branch):
    result = subprocess.run(
        ["python", "backend/orchestrator.py", "--pr", branch],
        capture_output=True, text=True
    )
    return result.stdout


def load_latest_run():
    runs = sorted(Path("runs").glob("*.json"), key=os.path.getmtime)
    if not runs:
        return None
    return json.loads(runs[-1].read_text())


def benchmark():
    detected, missed, false_pos = 0, 0, 0
    total_manual = 0
    results = []

    for case in CASES:
        checkout(case["branch"])
        t0 = time.time()
        run_orchestrator(case["branch"])
        elapsed = time.time() - t0
        run = load_latest_run()

        found = False
        if run and run.get("findings"):
            for f in run["findings"]:
                if f.get("file") == case["truth_file"]:
                    found = True
                    break

        if found:
            detected += 1
        else:
            missed += 1

        total_manual += case["manual_min"]
        results.append({
            "id": case["id"],
            "detected": found,
            "agent_time_sec": round(elapsed, 1),
            "manual_min": case["manual_min"]
        })

    for b in ["clean-01", "clean-02", "clean-03"]:
        checkout(b)
        run_orchestrator(b)
        run = load_latest_run()
        if run and run.get("findings"):
            false_pos += len(run["findings"])

    print(f"Detected: {detected}/{len(CASES)}")
    print(f"Missed: {missed}")
    print(f"False positives on clean branches: {false_pos}")
    print(f"Manual total: {total_manual} min")
    print(f"Agent total: {sum(r['agent_time_sec'] for r in results)} sec")

    Path("bench/results.json").write_text(json.dumps(results, indent=2))


if __name__ == "__main__":
    benchmark()