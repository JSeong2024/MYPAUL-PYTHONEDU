"""C++20 Chapter 06: compile and validate runnable examples, solutions, and project."""
import argparse
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
# Each case: (standard input, exit code, stdout, stderr)
EXAMPLES = {
    "01_fixed_array": [("", 0, "Samples: 4\nFirst: 21\nLast: 23\n", "")],
    "02_dynamic_vector": [("", 0, "After reserve and insert: 3\nAfter resize: 4\nFourth: 0\n", "")],
    "03_checked_access": [("", 0, "Index out of range: 3\nat() rejected the index\n", "")],
    "04_accumulate_readings": [("", 0, "Total: 60\nMin: 8\nMax: 16\nAverage: 12.00\n", "")],
    "05_sort_search": [("", 0, "Total: 164\nSlow: 2\nHas 31: true\nFirst sorted: 18\n", "")],
    "06_span_view": [("", 0, "Array total: 60\nVector total: 10\n", "")],
    "07_two_dimensional_array": [("", 0, "Rows: 3\nColumns: 4\nBlocked: 4\nCell (1, 3): 1\n", "")],
    "08_string_methods": [("", 0, "Prefix: true\nSuffix: true\nContains ROOM: true\nCategory: SENSOR\nUpdated: SENSOR-ROOM-07-A\n", "")],
    "09_line_input": [
        ("LiDAR Front Left\n", 0, "Device: Registered: LiDAR Front Left\n", ""),
        ("\n", 1, "Device: ", "Error: device name required.\n"),
        ("", 1, "Device: ", "Error: device name required.\n"),
    ],
    "10_string_view": [("", 0, "Category: MOTOR\n", "")],
    "11_from_chars": [("", 0, "Accepted: 42\nRejected: 42ms\nAccepted: -7\n", "")],
    "12_delimited_fields": [("", 0, "ROOM-01: OK\nRejected: ROOM-02|WARN|EXTRA\n", "")],
    "13_utf8_bytes": [("", 0, "Bits per byte: 8\nASCII bytes: 3\nKorean bytes (UTF-8): 3\n", "")],
}

EXERCISES = {
    "01_vector_statistics": [
        ("5\n18 22 22 25 13\n", 0, "Count: 5\nMin: 13\nMax: 25\nAverage: 20.00\n", ""),
        ("1\n-7\n", 0, "Count: 1\nMin: -7\nMax: -7\nAverage: -7.00\n", ""),
        ("3\n100 -100 0\n", 0, "Count: 3\nMin: -100\nMax: 100\nAverage: 0.00\n", ""),
        ("0\n", 1, "", "Error: invalid input.\n"),
        ("21\n", 1, "", "Error: invalid input.\n"),
        ("2\n99 abc\n", 1, "", "Error: invalid input.\n"),
        ("2\n1 101\n", 1, "", "Error: invalid input.\n"),
    ],
    "02_device_lookup": [
        ("3\nMotor A\nLiDAR Front\nIMU Main\nLiDAR Front\n", 0, "Found: LiDAR Front (index 2)\n", ""),
        ("2\nSensor\nSensor\nSensor\n", 0, "Found: Sensor (index 1)\n", ""),
        ("1\nA\na\n", 0, "Not found\n", ""),
        ("1\nDev\nOther\n", 0, "Not found\n", ""),
        ("0\n", 1, "", "Error: invalid input.\n"),
        ("1\n\nA\n", 1, "", "Error: invalid input.\n"),
    ],
    "03_comma_separated_values": [
        ("20,25,19,21\n", 0, "Count: 4\nSum: 85\n", ""),
        (" -100 , 0, 100 \n", 0, "Count: 3\nSum: 0\n", ""),
        ("7\n", 0, "Count: 1\nSum: 7\n", ""),
        ("\n", 1, "", "Error: invalid input.\n"),
        ("20,,30\n", 1, "", "Error: invalid input.\n"),
        ("20,30ms\n", 1, "", "Error: invalid input.\n"),
        ("20,101\n", 1, "", "Error: invalid input.\n"),
        ("20,\n", 1, "", "Error: invalid input.\n"),
        ("1,2,3,4,5,6,7,8,9,10,11\n", 1, "", "Error: invalid input.\n"),
    ],
    "04_grid_border": [
        ("4 3\n....\n.#..\n....\n", 0, "Blocked: 1\nBorders clear: yes\n", ""),
        ("4 3\n#...\n.#..\n....\n", 0, "Blocked: 2\nBorders clear: no\n", ""),
        ("1 1\n.\n", 0, "Blocked: 0\nBorders clear: yes\n", ""),
        ("1 1\n#\n", 0, "Blocked: 1\nBorders clear: no\n", ""),
        ("3 1\n.#.\n", 0, "Blocked: 1\nBorders clear: no\n", ""),
        ("3 2\n..\n...\n", 1, "", "Error: invalid grid.\n"),
        ("2 1\nA.\n", 1, "", "Error: invalid grid.\n"),
        ("0 2\n", 1, "", "Error: invalid grid.\n"),
    ],
}

PREFIX = "Device: Readings (-100 to 100, comma-separated): "
def report(name, readings):
    sorted_readings = sorted(readings)
    return (PREFIX + "\n--- Sensor Batch Report ---\n"
            f"Device: {name}\nCount: {len(readings)}\n"
            f"Minimum: {min(readings)}\nMaximum: {max(readings)}\n"
            f"Average: {sum(readings)/len(readings):.2f}\n"
            "Sorted: " + ", ".join(str(v) for v in sorted_readings) + "\n")

PROJECT = [
    ("LiDAR Front\n18, 22, 19, 24\n", 0, report("LiDAR Front", [18,22,19,24]), ""),
    ("Sensor A\n-100, 0, 100\n", 0, report("Sensor A", [-100,0,100]), ""),
    ("X\n7\n", 0, report("X", [7]), ""),
    ("X\n3, 3, 3\n", 0, report("X", [3,3,3]), ""),
    ("X\n 1 , -2, 4 \n", 0, report("X", [1,-2,4]), ""),
    ("\n1,2\n", 1, "Device: ", "Error: invalid device.\n"),
    ("X\n\n", 1, PREFIX, "Error: invalid readings.\n"),
    ("X\n2,,3\n", 1, PREFIX, "Error: invalid readings.\n"),
    ("X\n2,3x\n", 1, PREFIX, "Error: invalid readings.\n"),
    ("X\n101\n", 1, PREFIX, "Error: invalid readings.\n"),
    ("X\n" + ",".join(str(i) for i in range(21)) + "\n", 1, PREFIX, "Error: invalid readings.\n"),
]

def main():
    ap = argparse.ArgumentParser(description="Compile and check C++ Chapter 06 files")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--exercise", choices=["01", "02", "03", "04"], help="Check your edited exercise")
    mode.add_argument("--project", action="store_true", help="Check your edited project starter")
    args = ap.parse_args()
    compiler = shlex.split(os.environ.get("CXX", "g++"))
    if args.exercise:
        stem = next(x for x in EXERCISES if x.startswith(args.exercise + "_"))
        targets = [("exercises/" + stem + ".cpp", EXERCISES[stem])]
    elif args.project:
        targets = [("project/sensor_batch_report.cpp", PROJECT)]
    else:
        targets = [("examples/" + stem + ".cpp", cases) for stem,cases in EXAMPLES.items()]
        targets += [("solutions/" + stem + ".cpp", cases) for stem,cases in EXERCISES.items()]
        targets.append(("solutions/sensor_batch_report.cpp", PROJECT))
    total = failed = 0
    with tempfile.TemporaryDirectory(prefix="cpp_ch06_") as temp:
        for index, (source, cases) in enumerate(targets):
            executable = Path(temp) / f"program_{index}"
            cmd = compiler + ["-std=c++20", "-Wall", "-Wextra", "-Wpedantic", "-Werror", str(ROOT / source), "-o", str(executable)]
            compiled = subprocess.run(cmd, capture_output=True, text=True, check=False)
            if compiled.returncode:
                failed += 1; total += 1
                print(f"FAIL compile {source}\n{compiled.stderr}")
                continue
            for case_index, (stdin, expected_code, stdout, stderr) in enumerate(cases, 1):
                total += 1
                try:
                    executed = subprocess.run([str(executable)], input=stdin, capture_output=True, text=True, timeout=5, check=False)
                    actual = (executed.returncode, executed.stdout, executed.stderr)
                    if actual == (expected_code, stdout, stderr):
                        print(f"PASS {source} #{case_index}")
                    else:
                        failed += 1
                        print(f"FAIL {source} #{case_index}: expected {(expected_code, stdout, stderr)!r}; got {actual!r}")
                except subprocess.TimeoutExpired:
                    failed += 1
                    print(f"FAIL {source} #{case_index}: timeout")
    print(f"\nResult: {total - failed}/{total} PASS")
    return 1 if failed else 0

if __name__ == "__main__":
    sys.exit(main())
