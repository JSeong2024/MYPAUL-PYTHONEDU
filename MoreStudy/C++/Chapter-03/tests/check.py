"""Compile and check Chapter 03 C++20 examples, solutions and exercises.

Run examples and solutions: python3 tests/check.py
Run one student exercise: python3 tests/check.py --mode student --only exercise-04
Run student project: python3 tests/check.py --mode student --only project
Use Clang: python3 tests/check.py --compiler clang++
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
    label: str
    stdin: str
    stdout: str
    stderr: str = ""
    exit_code: int = 0


def c(label: str, stdin: str, stdout: str, stderr: str = "", exit_code: int = 0) -> Case:
    return Case(label, stdin, stdout, stderr, exit_code)


EXAMPLES: dict[str, tuple[str, list[Case]]] = {
    "example-01": ("examples/01_arithmetic_and_assignment.cpp", [
        c("arithmetic", "", "Full boxes: 3\nRemaining items: 2\nPacked items: 15\n")]),
    "example-02": ("examples/02_comparison_expressions.cpp", [
        c("comparison", "", "At warning limit: true\nLow battery: true\nAbove limit: false\n")]),
    "example-03": ("examples/03_logical_short_circuit.cpp", [
        c("short circuit", "", "High average: false\nAlarm: true\n")]),
    "example-04": ("examples/04_if_else_branches.cpp", [
        c("if branches", "", "SLOW DOWN\n")]),
    "example-05": ("examples/05_guard_clauses.cpp", [
        c("valid", "35\n", "Battery (0-100): Accepted: 35%\n"),
        c("lower bound", "0\n", "Battery (0-100): Accepted: 0%\n"),
        c("upper bound", "100\n", "Battery (0-100): Accepted: 100%\n"),
        c("below bound", "-1\n", "Battery (0-100): ", "Error: battery percentage must be 0-100.\n", 1),
        c("non numeric", "invalid\n", "Battery (0-100): ", "Error: enter a battery percentage.\n", 1),
    ]),
    "example-06": ("examples/06_switch_and_enum.cpp", [
        c("switch", "", "Waiting for input\n")]),
    "example-07": ("examples/07_if_initializer_and_ternary.cpp", [
        c("conditional", "", "Response: NORMAL\nRetries available: 2\n")]),
    "example-08": ("examples/08_bitwise_status_flags.cpp", [
        c("flags", "", "Ready: true\nFlags: 3\nFault set: false\n")]),
    "example-09": ("examples/09_boundaries_and_parentheses.cpp", [
        c("boundaries", "", "Valid battery: true\nWarning: true\n")]),
}

TASKS: dict[str, tuple[str, str, list[Case]]] = {
    "exercise-01": (
        "exercises/01_box_counter.cpp", "solutions/01_box_counter.cpp", [
            c("normal", "17\n5\n", "Items: Capacity: Full boxes: 3\nRemaining items: 2\n"),
            c("zero items", "0\n5\n", "Items: Capacity: Full boxes: 0\nRemaining items: 0\n"),
            c("capacity one", "7\n1\n", "Items: Capacity: Full boxes: 7\nRemaining items: 0\n"),
            c("zero capacity", "7\n0\n", "Items: Capacity: ", "Error: invalid box input.\n", 1),
            c("negative items", "-1\n5\n", "Items: Capacity: ", "Error: invalid box input.\n", 1),
            c("non numeric", "abc\n5\n", "Items: ", "Error: invalid box input.\n", 1),
        ]
    ),
    "exercise-02": (
        "exercises/02_distance_alert.cpp", "solutions/02_distance_alert.cpp", [
            c("zero", "0\n", "Distance (0-400 cm): STOP\n"),
            c("stop upper", "29\n", "Distance (0-400 cm): STOP\n"),
            c("slow lower", "30\n", "Distance (0-400 cm): SLOW DOWN\n"),
            c("slow upper", "100\n", "Distance (0-400 cm): SLOW DOWN\n"),
            c("clear lower", "101\n", "Distance (0-400 cm): CLEAR\n"),
            c("clear upper", "400\n", "Distance (0-400 cm): CLEAR\n"),
            c("below", "-1\n", "Distance (0-400 cm): ", "Error: distance must be 0-400.\n", 1),
            c("above", "401\n", "Distance (0-400 cm): ", "Error: distance must be 0-400.\n", 1),
            c("text", "oops\n", "Distance (0-400 cm): ", "Error: distance must be 0-400.\n", 1),
        ]
    ),
    "exercise-03": (
        "exercises/03_mode_selector.cpp", "solutions/03_mode_selector.cpp", [
            c("off", "0\n", "Mode (0-2): OFF\n"),
            c("standby", "1\n", "Mode (0-2): STANDBY\n"),
            c("active", "2\n", "Mode (0-2): ACTIVE\n"),
            c("negative", "-1\n", "Mode (0-2): ", "Error: mode must be 0-2.\n", 1),
            c("out of range", "3\n", "Mode (0-2): ", "Error: mode must be 0-2.\n", 1),
            c("text", "invalid\n", "Mode (0-2): ", "Error: mode must be 0-2.\n", 1),
        ]
    ),
    "exercise-04": (
        "exercises/04_status_flags.cpp", "solutions/04_status_flags.cpp", [
            c("none", "0\n", "Flags (0-7): NOT READY\n"),
            c("power only", "1\n", "Flags (0-7): NOT READY\n"),
            c("sensor only", "2\n", "Flags (0-7): NOT READY\n"),
            c("ready", "3\n", "Flags (0-7): READY\n"),
            c("fault only", "4\n", "Flags (0-7): FAULT\n"),
            c("all on", "7\n", "Flags (0-7): FAULT\n"),
            c("negative", "-1\n", "Flags (0-7): ", "Error: flags must be 0-7.\n", 1),
            c("above", "8\n", "Flags (0-7): ", "Error: flags must be 0-7.\n", 1),
            c("text", "off\n", "Flags (0-7): ", "Error: flags must be 0-7.\n", 1),
        ]
    ),
    "project": (
        "project/device_health_report.cpp", "solutions/device_health_report.cpp", [
            c("overheat higher priority", "18\n78\n3\n",
              "Battery (0-100): Temperature (-40 to 125 C): Flags (0-7): \n"
              "--- Device Health ---\nBattery: 18%\nTemperature: 78 C\n"
              "Power: ON\nSensor: READY\nFault: NO\nStatus: OVERHEAT\n"),
            c("ready", "80\n25.5\n3\n",
              "Battery (0-100): Temperature (-40 to 125 C): Flags (0-7): \n"
              "--- Device Health ---\nBattery: 80%\nTemperature: 25.5 C\n"
              "Power: ON\nSensor: READY\nFault: NO\nStatus: READY\n"),
            c("battery threshold", "20\n74.9\n3\n",
              "Battery (0-100): Temperature (-40 to 125 C): Flags (0-7): \n"
              "--- Device Health ---\nBattery: 20%\nTemperature: 74.9 C\n"
              "Power: ON\nSensor: READY\nFault: NO\nStatus: LOW BATTERY\n"),
            c("temperature threshold", "21\n75\n3\n",
              "Battery (0-100): Temperature (-40 to 125 C): Flags (0-7): \n"
              "--- Device Health ---\nBattery: 21%\nTemperature: 75 C\n"
              "Power: ON\nSensor: READY\nFault: NO\nStatus: OVERHEAT\n"),
            c("fault highest", "18\n78\n7\n",
              "Battery (0-100): Temperature (-40 to 125 C): Flags (0-7): \n"
              "--- Device Health ---\nBattery: 18%\nTemperature: 78 C\n"
              "Power: ON\nSensor: READY\nFault: YES\nStatus: FAULT\n"),
            c("power off", "50\n20\n2\n",
              "Battery (0-100): Temperature (-40 to 125 C): Flags (0-7): \n"
              "--- Device Health ---\nBattery: 50%\nTemperature: 20 C\n"
              "Power: OFF\nSensor: READY\nFault: NO\nStatus: POWER OFF\n"),
            c("sensor off", "50\n20\n1\n",
              "Battery (0-100): Temperature (-40 to 125 C): Flags (0-7): \n"
              "--- Device Health ---\nBattery: 50%\nTemperature: 20 C\n"
              "Power: ON\nSensor: NOT READY\nFault: NO\nStatus: SENSOR NOT READY\n"),
            c("lower temperature", "0\n-40\n3\n",
              "Battery (0-100): Temperature (-40 to 125 C): Flags (0-7): \n"
              "--- Device Health ---\nBattery: 0%\nTemperature: -40 C\n"
              "Power: ON\nSensor: READY\nFault: NO\nStatus: LOW BATTERY\n"),
            c("upper temperature", "100\n125\n3\n",
              "Battery (0-100): Temperature (-40 to 125 C): Flags (0-7): \n"
              "--- Device Health ---\nBattery: 100%\nTemperature: 125 C\n"
              "Power: ON\nSensor: READY\nFault: NO\nStatus: OVERHEAT\n"),
            c("battery below", "-1\n22\n3\n",
              "Battery (0-100): ", "Error: battery must be 0-100.\n", 1),
            c("battery invalid", "bad\n22\n3\n",
              "Battery (0-100): ", "Error: battery must be 0-100.\n", 1),
            c("temperature above", "50\n125.1\n3\n",
              "Battery (0-100): Temperature (-40 to 125 C): ", "Error: temperature must be -40 to 125.\n", 1),
            c("temperature below", "50\n-40.1\n3\n",
              "Battery (0-100): Temperature (-40 to 125 C): ", "Error: temperature must be -40 to 125.\n", 1),
            c("flags above", "50\n25\n8\n",
              "Battery (0-100): Temperature (-40 to 125 C): Flags (0-7): ", "Error: flags must be 0-7.\n", 1),
            c("flags invalid", "50\n25\noff\n",
              "Battery (0-100): Temperature (-40 to 125 C): Flags (0-7): ", "Error: flags must be 0-7.\n", 1),
        ]
    ),
}


def compile_source(compiler: str, source: Path, executable: Path) -> tuple[bool, str]:
    command = [compiler, "-std=c++20", "-Wall", "-Wextra", "-Wpedantic", str(source), "-o", str(executable)]
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=40, encoding="utf-8", errors="replace")
    except (OSError, subprocess.TimeoutExpired) as error:
        return False, str(error)
    if result.returncode:
        return False, result.stderr.strip() or result.stdout.strip()
    return True, ""


def verify(executable: Path, case: Case) -> tuple[bool, str]:
    try:
        result = subprocess.run([str(executable)], input=case.stdin, capture_output=True,
                                text=True, timeout=5, encoding="utf-8", errors="replace")
    except (OSError, subprocess.TimeoutExpired) as error:
        return False, str(error)
    failures = []
    if result.returncode != case.exit_code:
        failures.append(f"exit code {result.returncode} != expected {case.exit_code}")
    if result.stdout != case.stdout:
        failures.append(f"stdout {result.stdout!r} != expected {case.stdout!r}")
    if result.stderr != case.stderr:
        failures.append(f"stderr {result.stderr!r} != expected {case.stderr!r}")
    return not failures, "; ".join(failures)


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify Chapter 03 programs")
    parser.add_argument("--mode", choices=("solutions", "student"), default="solutions")
    parser.add_argument("--only", choices=sorted([*EXAMPLES, *TASKS]), help="Check one example or task")
    parser.add_argument("--compiler", default="g++", help="Compiler executable")
    args = parser.parse_args()

    selected: list[tuple[str, str, list[Case]]] = []
    for name, (path, cases) in EXAMPLES.items():
        if args.only is None or args.only == name:
            selected.append((name, path, cases))
    for name, (exercise, solution, cases) in TASKS.items():
        if args.only is None or args.only == name:
            selected.append((name, exercise if args.mode == "student" else solution, cases))

    passed = failed = 0
    with tempfile.TemporaryDirectory(prefix="cpp_ch03_") as temp:
        for index, (name, path, cases) in enumerate(selected, 1):
            executable = Path(temp) / (f"run_{index}.exe" if sys.platform == "win32" else f"run_{index}")
            ok, detail = compile_source(args.compiler, ROOT / path, executable)
            if not ok:
                print(f"[FAIL] {name}: compile: {detail}")
                failed += 1
                continue
            for case in cases:
                ok, detail = verify(executable, case)
                if ok:
                    print(f"[PASS] {name}: {case.label}")
                    passed += 1
                else:
                    print(f"[FAIL] {name}: {case.label}: {detail}")
                    failed += 1
    print(f"Result: {passed} PASS, {failed} FAIL")
    return int(failed != 0)


if __name__ == "__main__":
    raise SystemExit(main())
