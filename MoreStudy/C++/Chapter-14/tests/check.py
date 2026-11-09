#!/usr/bin/env python3
"""Chapter 14 C++20 examples, solutions and project behavior checks.

    python tests/check.py
    python tests/check.py --compiler clang++
    python tests/check.py --mode student --only exercise-03
    python tests/check.py --only project
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FLAGS = ["-std=c++20", "-pthread", "-Wall", "-Wextra", "-Wpedantic", "-Werror"]
EXAMPLES = {
    "01_thread_basics.cpp": "Result: 42\n",
    "02_thread_lifecycle.cpp": "Old joinable: false\nJoined: true\n",
    "03_jthread_cancel.cpp": "Stop observed: true\nJoined: true\n",
    "04_race_free_counter.cpp": "Count: 4000\n",
    "05_lock_guard.cpp": "Samples: 4, Sum: 20\n",
    "06_scoped_lock.cpp": "Balances: 50, 100\n",
    "07_condition_queue.cpp": "Received: 42\n",
    "08_stoppable_wait.cpp": "Stopped waiting: true\n",
    "09_atomic_counter.cpp": "Processed: 2000\n",
    "10_memory_order.cpp": "Payload: 42\n",
    "11_atomic_wait.cpp": "Payload: 73\n",
    "12_async_future.cpp": "Result: 42\n",
    "13_promise_exception.cpp": "Error: sensor offline\n",
    "14_shared_mutex.cpp": "Reads: 124\n",
    "15_latch_barrier.cpp": "Values: 30, 20\n",
    "16_thread_local.cpp": "Local counters: 2, 1\n",
}
EXERCISES = [
    "01_parallel_sum.cpp", "02_safe_inventory.cpp",
    "03_closing_queue.cpp", "04_async_results.cpp",
]
PROJECT_OUTPUT = (
    "Accepted: 4\nProcessed: 4\nRejected: 1\n"
    "Alerts: 2\nChecksum: 10252\n"
)


def command(args: list[str], cwd: Path | None = None, timeout: int = 30) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True,
                          timeout=timeout, encoding="utf-8", errors="replace", check=False)


def main() -> int:
    parser = argparse.ArgumentParser(description="Chapter 14 concurrency tests")
    parser.add_argument("--compiler", default=os.environ.get("CXX", "g++-14"))
    parser.add_argument("--mode", choices=("solutions", "student"), default="solutions")
    parser.add_argument("--only", choices=("all", "examples", "project", *(
        f"exercise-{i:02d}" for i in range(1, 5))), default="all")
    args = parser.parse_args()
    passed = failed = 0
    with tempfile.TemporaryDirectory(prefix="chapter14_", dir=None) as temporary:
        temp = Path(temporary)
        exe = temp / ("run.exe" if os.name == "nt" else "run")

        def verify(name: str, sources: list[Path], expected: str, extra: list[str] | None = None) -> None:
            nonlocal passed, failed
            compile_command = [args.compiler, *FLAGS, *(extra or []),
                               *(str(source) for source in sources), "-o", str(exe)]
            try:
                build = command(compile_command, timeout=50)
                if build.returncode != 0 or build.stderr.strip():
                    raise RuntimeError(f"compile/warning:\n{build.stderr[-2000:]}")
                result = command([str(exe)], cwd=temp, timeout=10)
                if result.returncode != 0 or result.stdout != expected or result.stderr:
                    raise RuntimeError(f"exit={result.returncode}, stdout={result.stdout!r}, "
                                       f"stderr={result.stderr!r}, expected={expected!r}")
            except (RuntimeError, subprocess.TimeoutExpired, OSError) as exc:
                failed += 1
                print(f"[FAIL] {name}: {exc}")
            else:
                passed += 1
                print(f"[PASS] {name}")

        if args.only in ("all", "examples"):
            for name, expected in EXAMPLES.items():
                verify(name, [ROOT / "examples" / name], expected)
        for number, filename in enumerate(EXERCISES, 1):
            key = f"exercise-{number:02d}"
            if args.only in ("all", key):
                source = ROOT / ("solutions" if args.mode == "solutions" else "exercises") / filename
                # Include the source under test in the harness, without its own main().
                define = '-DCH14_SOURCE_PATH="' + source.as_posix() + '"'
                verify(key, [ROOT / "tests" / "cases" / (key + ".cpp")], "PASS\n",
                       ["-DCH14_LIBRARY_ONLY", define])
        if args.only in ("all", "project"):
            project = ROOT / ("solutions/sensor_dispatcher" if args.mode == "solutions" else "project")
            include = ["-I", str(project / "include")]
            verify("project-output", [project / "src/main.cpp", project / "src/dispatcher.cpp"],
                   PROJECT_OUTPUT, include)
            verify("project-behavior", [project / "tests/test_dispatcher.cpp",
                                        project / "src/dispatcher.cpp"], "", include)
    print(f"Result: {passed}/{passed + failed} passed "
          f"({args.compiler}, C++20, {args.mode})")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
