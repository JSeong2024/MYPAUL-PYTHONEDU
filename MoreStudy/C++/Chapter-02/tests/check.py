"""Compile and verify Chapter 02 C++20 examples, solutions, or student work.

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
    label: str
    stdin: str
    stdout: str
    stderr: str = ""
    exit_code: int = 0


EXAMPLES: dict[str, tuple[str, list[Case]]] = {
    "example-01": ("examples/01_variables_and_initialization.cpp", [
        Case("variables", "", "Sensor: Sensor-A\nSamples: 12\nConnected: true\nUpdated samples: 15\n"),
    ]),
    "example-02": ("examples/02_fundamental_types.cpp", [
        Case("types", "", "Channel: B\nCount: 24\nTotal: 1000000\nRatio: 0.5\nTemperature: 23.75 C\nLabel: Thermal sensor\n"),
    ]),
    "example-03": ("examples/03_integer_ranges.cpp", [
        Case("ranges", "", "Position: -250\nPort: 8080\nuint16_t maximum: 65535\nint32_t minimum: -2147483648\n"),
    ]),
    "example-04": ("examples/04_literals_and_units.cpp", [
        Case("literals", "", "Sampling rate: 1000 Hz\nStatus mask: 5\nColor value: 255\nDistance: 2.5 m\n"),
    ]),
    "example-05": ("examples/05_const_constexpr_auto.cpp", [
        Case("constants", "", "Device: Counter-01\nCapacity: 100\nRecorded: 12\nUpdated: 15\n"),
    ]),
    "example-06": ("examples/06_explicit_conversions.cpp", [
        Case("conversion", "", "Measurement: 8.9\nWhole part: 8\nFits in uint8_t: false\n"),
    ]),
    "example-07": ("examples/07_floating_point.cpp", [
        Case("precision", "", "Sum: 0.30000000000000004\nExpected: 0.29999999999999999\nDisplayed: 0.30\n"),
    ]),
    "example-08": ("examples/08_scoped_enum.cpp", [
        Case("enum", "", "State code: 1\n"),
    ]),
}

TASKS: dict[str, tuple[str, str, list[Case]]] = {
    "exercise-01": (
        "exercises/01_device_profile.cpp",
        "solutions/01_device_profile.cpp",
        [Case("device", "", "Device: Sensor-A1\nID: 1024\nReady: true\n")],
    ),
    "exercise-02": (
        "exercises/02_constants_and_literals.cpp",
        "solutions/02_constants_and_literals.cpp",
        [Case("constants", "", "Timeout: 1500 ms\nRetry limit: 3\nStatus mask: 5\n")],
    ),
    "exercise-03": (
        "exercises/03_explicit_conversion.cpp",
        "solutions/03_explicit_conversion.cpp",
        [
            Case("positive fraction", "8.9\n", "Reading: Original: 8.9\nWhole part: 8\n"),
            Case("negative fraction", "-3.9\n", "Reading: Original: -3.9\nWhole part: -3\n"),
            Case("integer input", "12\n", "Reading: Original: 12\nWhole part: 12\n"),
        ],
    ),
    "exercise-04": (
        "exercises/04_temperature_adjustment.cpp",
        "solutions/04_temperature_adjustment.cpp",
        [
            Case("offset negative", "23.75\n-0.25\n", "Temperature (C): Offset (C): Original: 23.75 C\nAdjusted: 23.50 C\n"),
            Case("offset positive", "18.5\n0.75\n", "Temperature (C): Offset (C): Original: 18.50 C\nAdjusted: 19.25 C\n"),
            Case("zero", "0\n0\n", "Temperature (C): Offset (C): Original: 0.00 C\nAdjusted: 0.00 C\n"),
        ],
    ),
    "project": (
        "project/measurement_card.cpp",
        "solutions/measurement_card.cpp",
        [
            Case(
                "name with spaces",
                "Robotics Lab Sensor\n23.75\n-0.25\n12\n",
                "Device: Temperature (C): Offset (C): Samples: \n"
                "--- Measurement Card ---\n"
                "Device: Robotics Lab Sensor\n"
                "Temperature: 23.75 C\nOffset: -0.25 C\nAdjusted: 23.50 C\n"
                "Samples: 12\nWhole degrees: 23\n",
            ),
            Case(
                "changed input",
                "Sensor B\n18.5\n0.75\n7\n",
                "Device: Temperature (C): Offset (C): Samples: \n"
                "--- Measurement Card ---\n"
                "Device: Sensor B\n"
                "Temperature: 18.50 C\nOffset: 0.75 C\nAdjusted: 19.25 C\n"
                "Samples: 7\nWhole degrees: 18\n",
            ),
            Case(
                "negative temperature",
                "Cold Room\n-3.75\n0.25\n4\n",
                "Device: Temperature (C): Offset (C): Samples: \n"
                "--- Measurement Card ---\n"
                "Device: Cold Room\n"
                "Temperature: -3.75 C\nOffset: 0.25 C\nAdjusted: -3.50 C\n"
                "Samples: 4\nWhole degrees: -3\n",
            ),
        ],
    ),
}


def compile_cpp(compiler: str, source: Path, target: Path) -> tuple[bool, str]:
    command = [compiler, "-std=c++20", "-Wall", "-Wextra", "-Wpedantic", str(source), "-o", str(target)]
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=40, encoding="utf-8", errors="replace")
    except (OSError, subprocess.TimeoutExpired) as error:
        return False, str(error)
    if result.returncode != 0:
        return False, result.stderr.strip() or result.stdout.strip()
    return True, ""


def run_case(executable: Path, case: Case) -> tuple[bool, str]:
    try:
        result = subprocess.run(
            [str(executable)], input=case.stdin, capture_output=True, text=True,
            timeout=5, encoding="utf-8", errors="replace",
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        return False, str(error)
    errors = []
    if result.returncode != case.exit_code:
        errors.append(f"exit code {result.returncode}, expected {case.exit_code}")
    if result.stdout != case.stdout:
        errors.append(f"stdout {result.stdout!r}, expected {case.stdout!r}")
    if result.stderr != case.stderr:
        errors.append(f"stderr {result.stderr!r}, expected {case.stderr!r}")
    return not errors, "; ".join(errors)


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify Chapter 02 C++20 programs")
    parser.add_argument("--mode", choices=("solutions", "student"), default="solutions")
    parser.add_argument("--only", choices=sorted([*EXAMPLES, *TASKS]), help="Check one example or task")
    parser.add_argument("--compiler", default="g++", help="Compiler executable (default: g++)")
    args = parser.parse_args()

    targets = []
    for name, (source, cases) in EXAMPLES.items():
        if args.only is None or args.only == name:
            targets.append((name, source, cases))
    for name, (student, solution, cases) in TASKS.items():
        if args.only is None or args.only == name:
            targets.append((name, solution if args.mode == "solutions" else student, cases))

    passed = 0
    failed = 0
    with tempfile.TemporaryDirectory(prefix="cpp_ch02_") as temp:
        for index, (name, path, cases) in enumerate(targets, 1):
            executable = Path(temp) / (f"check_{index}.exe" if sys.platform == "win32" else f"check_{index}")
            success, message = compile_cpp(args.compiler, ROOT / path, executable)
            if not success:
                print(f"[FAIL] {name}: compile: {message}")
                failed += 1
                continue
            for case in cases:
                success, message = run_case(executable, case)
                if success:
                    print(f"[PASS] {name}: {case.label}")
                    passed += 1
                else:
                    print(f"[FAIL] {name}: {case.label}: {message}")
                    failed += 1
    print(f"Result: {passed} PASS, {failed} FAIL")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
