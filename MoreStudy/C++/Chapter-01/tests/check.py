"""Optional chapter checks. Uses only the Python standard library.

Examples:
    python tests/check.py
    python tests/check.py --mode student --only exercise-04
    python tests/check.py --mode student --only project
    python tests/check.py --compiler clang++
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Case:
    name: str
    stdin: str
    stdout: str
    stderr: str = ""
    exit_code: int = 0


EXAMPLES: dict[str, tuple[str, list[Case]]] = {
    "example-01": (
        "examples/01_hello_world.cpp",
        [Case("hello", "", "Hello, C++20!\n")],
    ),
    "example-02": (
        "examples/02_program_structure.cpp",
        [Case("structure", "", "Source code\nExecutable program\n")],
    ),
    "example-03": (
        "examples/03_output_streams.cpp",
        [Case("separate streams", "", "Result: success\n", "Notice: demonstration message\n")],
    ),
    "example-04": (
        "examples/04_token_input.cpp",
        [Case("token", "robotics basics\n", "Keyword: First token: robotics\n")],
    ),
    "example-05": (
        "examples/05_line_input.cpp",
        [Case("full line", "Kim Min Su\n", "Full name: Hello, Kim Min Su!\n")],
    ),
    "example-06": (
        "examples/06_two_lines.cpp",
        [Case("two lines", "Kim Min Su\nRobotics Club\n", "Name: Interest: Profile: Kim Min Su | Robotics Club\n")],
    ),
}

TASKS: dict[str, tuple[str, str, list[Case]]] = {
    "exercise-01": (
        "exercises/01_console_banner.cpp",
        "solutions/01_console_banner.cpp",
        [Case("fixed output", "", "Hello, C++20!\nReady to learn.\n")],
    ),
    "exercise-02": (
        "exercises/02_output_channels.cpp",
        "solutions/02_output_channels.cpp",
        [Case("stdout and stderr", "", "Status: running\n", "Notice: check log\n")],
    ),
    "exercise-03": (
        "exercises/03_keyword_echo.cpp",
        "solutions/03_keyword_echo.cpp",
        [
            Case("one word", "network\n", "Keyword: You typed: network\n"),
            Case("whitespace separation", "data science\n", "Keyword: You typed: data\n"),
            Case("changed input", "compiler\n", "Keyword: You typed: compiler\n"),
        ],
    ),
    "exercise-04": (
        "exercises/04_full_name.cpp",
        "solutions/04_full_name.cpp",
        [
            Case("name with spaces", "Park Ji Min\n", "Full name: Welcome, Park Ji Min!\n"),
            Case("changed input", "Ada Lovelace\n", "Full name: Welcome, Ada Lovelace!\n"),
        ],
    ),
    "project": (
        "project/registration_card.cpp",
        "solutions/registration_card.cpp",
        [
            Case(
                "registration",
                "Kim Min Su\nC++ Basics\nRead source code\n",
                "Name: Course: Goal: \n--- Registration Card ---\n"
                "Name: Kim Min Su\nCourse: C++ Basics\nGoal: Read source code\n",
            ),
            Case(
                "different learner",
                "Lee Hana\nProgramming 101\nCompile and run\n",
                "Name: Course: Goal: \n--- Registration Card ---\n"
                "Name: Lee Hana\nCourse: Programming 101\nGoal: Compile and run\n",
            ),
        ],
    ),
}


def compile_cpp(compiler: str, source: Path, target: Path) -> tuple[bool, str]:
    command = [compiler, "-std=c++20", "-Wall", "-Wextra", "-Wpedantic", str(source), "-o", str(target)]
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=35, encoding="utf-8", errors="replace")
    except (OSError, subprocess.TimeoutExpired) as error:
        return False, str(error)
    if result.returncode != 0:
        return False, result.stderr.strip() or result.stdout.strip()
    return True, ""


def run_case(executable: Path, case: Case) -> tuple[bool, str]:
    try:
        result = subprocess.run(
            [str(executable)], input=case.stdin, capture_output=True,
            text=True, timeout=5, encoding="utf-8", errors="replace",
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        return False, str(error)
    differences = []
    if result.returncode != case.exit_code:
        differences.append(f"exit code {result.returncode} (expected {case.exit_code})")
    if result.stdout != case.stdout:
        differences.append(f"stdout {result.stdout!r} (expected {case.stdout!r})")
    if result.stderr != case.stderr:
        differences.append(f"stderr {result.stderr!r} (expected {case.stderr!r})")
    return not differences, "; ".join(differences)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Chapter 01 C++20 examples and tasks")
    parser.add_argument("--mode", choices=("solutions", "student"), default="solutions")
    parser.add_argument("--only", choices=sorted([*EXAMPLES, *TASKS]), help="Check a single item")
    parser.add_argument("--compiler", default="g++", help="C++ compiler command (default: g++)")
    args = parser.parse_args()

    targets: list[tuple[str, str, list[Case]]] = []
    for name, (source, cases) in EXAMPLES.items():
        if args.only is None or args.only == name:
            targets.append((name, source, cases))
    for name, (student, solution, cases) in TASKS.items():
        if args.only is None or args.only == name:
            targets.append((name, solution if args.mode == "solutions" else student, cases))

    passed = 0
    failed = 0
    with tempfile.TemporaryDirectory(prefix="cpp_ch01_") as temp:
        for number, (name, source, cases) in enumerate(targets, start=1):
            executable = Path(temp) / (f"check_{number}.exe" if sys.platform == "win32" else f"check_{number}")
            ok, reason = compile_cpp(args.compiler, ROOT / source, executable)
            if not ok:
                print(f"[FAIL] {name}: compilation failed: {reason}")
                failed += 1
                continue
            for case in cases:
                success, detail = run_case(executable, case)
                if success:
                    print(f"[PASS] {name}: {case.name}")
                    passed += 1
                else:
                    print(f"[FAIL] {name}: {case.name}: {detail}")
                    failed += 1

    print(f"Result: {passed} PASS, {failed} FAIL")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
