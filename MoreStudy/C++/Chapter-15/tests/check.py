#!/usr/bin/env python3
"""Chapter 15 C++20 correctness tests. No third-party Python dependencies.

    python3 tests/check.py
    python3 tests/check.py --compiler clang++
    python3 tests/check.py --mode student --only exercise-02
    python3 tests/check.py --only project
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FLAGS = ["-std=c++20", "-O2", "-Wall", "-Wextra", "-Wpedantic", "-Werror"]
EXAMPLES = {
    "01_measure_before_optimizing.cpp": "Count: 4\nTotal: 84, Peak: 30\n",
    "02_lifetime_and_storage.cpp": "Fixed: 2, Dynamic: 6, Owned: 12\n",
    "03_vector_reserve.cpp": "Size: 8, Capacity enough: true\nBuffer unchanged: true\n",
    "04_contiguous_traversal.cpp": "Vector: 15, List: 15\n",
    "05_span_view.cpp": "Array: 15, Vector: 30\n",
    "06_aos_soa.cpp": "Rows: 3, Sum: 60\n",
    "07_false_sharing_layout.cpp": "Alignment >= 64: true\nValues: 30\n",
    "08_row_major_access.cpp": "Row-first: 21, Column-first: 21\n",
    "09_pmr_monotonic.cpp": "Items: 5, Last: 5\n",
    "10_pmr_pool.cpp": "Pool values: 7, 9\n",
    "11_lookup_structure.cpp": "Vector found: true, Hash found: true\n",
    "12_copy_and_view.cpp": "Copy size: 11, View size: 11\n",
    "13_algorithm_pipeline.cpp": "Nonnegative sum: 15\n",
    "14_steady_clock_benchmark.cpp": "Trials: 5, Checksum: 10000\n",
    "15_checked_integer.cpp": "Safe: 50, Overflow rejected: true\n",
    "16_sorted_index.cpp": "Has 5: true, Count 3: 2\n",
}
EXERCISES = [
    "01_reserve_squares.cpp", "02_span_statistics.cpp",
    "03_pmr_filtered.cpp", "04_sorted_unique.cpp",
]
PROJECT_EXPECTED = (
    "Devices: 3\nAccepted: 5, Rejected: 2\n"
    "Total: 125\nMatches: true\n"
)


def run(command: list[str], cwd: Path | None = None, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, capture_output=True, text=True, cwd=cwd,
                          encoding="utf-8", errors="replace", timeout=timeout, check=False)


def main() -> int:
    parser = argparse.ArgumentParser(description="Chapter 15 memory and performance tests")
    parser.add_argument("--compiler", default=os.environ.get("CXX", "g++-14"))
    parser.add_argument("--mode", choices=("solutions", "student"), default="solutions")
    parser.add_argument("--only", choices=("all", "examples", "project",
                                            "exercise-01", "exercise-02",
                                            "exercise-03", "exercise-04"), default="all")
    args = parser.parse_args()
    passed = failed = 0
    with tempfile.TemporaryDirectory(prefix="cpp_ch15_") as temp:
        build_dir = Path(temp)
        executable = build_dir / ("run.exe" if os.name == "nt" else "run")

        def verify(label: str, sources: list[Path], expected: str,
                   extra: list[str] | None = None, timeout: int = 15) -> None:
            nonlocal passed, failed
            compile_line = [args.compiler, *FLAGS, *(extra or []),
                            *(str(path) for path in sources), "-o", str(executable)]
            try:
                compile_result = run(compile_line, timeout=75)
                if compile_result.returncode != 0 or compile_result.stderr.strip():
                    raise RuntimeError(f"compile/warnings:\n{compile_result.stderr[-2000:]}")
                result = run([str(executable)], cwd=build_dir, timeout=timeout)
                if result.returncode != 0 or result.stdout != expected or result.stderr:
                    raise RuntimeError(f"exit={result.returncode}; stdout={result.stdout!r}; "
                                       f"stderr={result.stderr!r}; expected={expected!r}")
            except (RuntimeError, subprocess.TimeoutExpired, OSError) as error:
                failed += 1
                print(f"[FAIL] {label}: {error}")
            else:
                passed += 1
                print(f"[PASS] {label}")

        if args.only in ("all", "examples"):
            for filename, expected in EXAMPLES.items():
                verify(filename, [ROOT / "examples" / filename], expected)

        for index, filename in enumerate(EXERCISES, 1):
            key = f"exercise-{index:02}"
            if args.only in ("all", key):
                source = ROOT / ("solutions" if args.mode == "solutions" else "exercises") / filename
                define = '-DCH15_SOURCE_PATH="' + source.as_posix() + '"'
                verify(key, [ROOT / "tests/cases" / (key + ".cpp")], "PASS\n",
                       ["-DCH15_LIBRARY_ONLY", define])

        if args.only in ("all", "project"):
            project = ROOT / ("solutions/sensor_batch_analyzer" if args.mode == "solutions"
                              else "project")
            options = ["-I", str(project / "include")]
            verify("project-demo", [project / "src/main.cpp", project / "src/analyzer.cpp"],
                   PROJECT_EXPECTED, options)
            verify("project-behavior", [project / "tests/test_analyzer.cpp",
                                         project / "src/analyzer.cpp"], "", options)

    print(f"Result: {passed}/{passed + failed} passed "
          f"({args.compiler}, C++20, {args.mode})")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
