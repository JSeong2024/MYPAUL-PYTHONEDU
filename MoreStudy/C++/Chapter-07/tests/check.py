"""Compile and test Chapter 07 C++20 examples, answers, and Mini Project."""
import argparse
import os
from pathlib import Path
import shlex
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
# stdin, expected exit status, stdout, stderr
EXAMPLES = {
    "01_addresses_and_dereference": [("",0,"Original: 24 C\nUpdated: 26 C\nSame object: true\n","")],
    "02_nullable_pointer": [("",0,"Sensor: 23 C\nNo sensor reading\n","")],
    "03_reference_parameters": [("",0,"First: true\nSecond: false\nMotor: 2500 RPM\n","")],
    "04_const_correctness": [("",0,"Backup: 80\nSpeed: 130\nRead-only speed: 130\n","")],
    "05_pointer_lookup": [("",0,"Found: camera\nMissing: true\n","")],
    "06_span_parameter": [("",0,"Fixed: 20.0\nDynamic: 50.0\nEmpty: true\n","")],
    "07_vector_invalidation": [("",0,"Selected: 20\nSize: 3\n","")],
    "08_unique_ptr": [("",0,"Previous owner empty: true\nCurrent device: sensor-A\n","")],
    "09_shared_and_weak_ptr": [("",0,"Active: navigation-map\nExpired: true\n","")],
    "10_pointer_and_length_boundary": [("",0,"Checksum sum: 10\nInvalid: true\n","")],
    "11_reference_wrapper": [("",0,"Front: 1100\nRear: 1300\n","")],
    "12_optional_reference": [("",0,"Renamed: lidar-front\n","")],
    "13_sanitizer_safe_example": [("",0,"First: 10\nEmpty: -1\n","")],
}
EXERCISES = {
    "01_motor_limit": [("",0,"First: true, Second: false, RPM: 2500\n","")],
    "02_sensor_average": [("",0,"Average: 25.0\nEmpty: true\n","")],
    "03_device_lookup": [("",0,"Found: imu\nMissing: true\n","")],
    "04_shared_observer": [("",0,"Active: sensor-hub\nExpired: true\n","")],
}
PREFIX = "Readings (3 values, 0-100): Channel (0-3): Adjustment (-20 to 20): "
def report(selected, initial, adjusted, avg, status):
    lines = [PREFIX, "--- Channel Report ---", f"Selected: {selected}"]
    if selected != "NONE":
        lines.extend([f"Before: {initial}", f"After: {adjusted}"])
    lines.extend([f"Average: {avg:.2f}", f"Status: {status}"])
    return "\n".join(lines) + "\n"
PROJECT = [
    ("25 83 47\n2\n-5\n",0,report("2",83,78,50.0,"NORMAL"),""),
    ("25 83 47\n2\n0\n",0,report("2",83,83,155/3,"ALERT"),""),
    ("0 0 0\n1\n20\n",0,report("1",0,20,20/3,"NORMAL"),""),
    ("100 0 0\n1\n-20\n",0,report("1",100,80,80/3,"ALERT"),""),
    ("20 30 40\n0\n10\n",0,report("NONE",0,0,30.0,"NO CHANNEL"),""),
    ("2 4 6\n3\n10\n",0,report("3",6,16,22/3,"NORMAL"),""),
    ("80 85 90\n2\n20\n",1,PREFIX,"Error: adjusted reading out of range.\n"),
    ("5 10 15\n1\n-20\n",1,PREFIX,"Error: adjusted reading out of range.\n"),
    ("101 5 10\n1\n0\n",1,"Readings (3 values, 0-100): ","Error: reading out of range.\n"),
    ("-1 5 10\n1\n0\n",1,"Readings (3 values, 0-100): ","Error: reading out of range.\n"),
    ("10 20 30\n4\n0\n",1,"Readings (3 values, 0-100): Channel (0-3): ","Error: invalid channel.\n"),
    ("10 20 30\n-1\n0\n",1,"Readings (3 values, 0-100): Channel (0-3): ","Error: invalid channel.\n"),
    ("10 20 30\n1\n21\n",1,PREFIX,"Error: invalid adjustment.\n"),
    ("10 20 30\n1\n-21\n",1,PREFIX,"Error: invalid adjustment.\n"),
    ("x 20 30\n1\n0\n",1,"Readings (3 values, 0-100): ","Error: invalid input.\n"),
    ("10 20 30\nx\n0\n",1,"Readings (3 values, 0-100): Channel (0-3): ","Error: invalid channel.\n"),
    ("10 20 30\n1\nx\n",1,PREFIX,"Error: invalid adjustment.\n"),
]

UNIT_CHECKS = {
    "01_motor_limit": r"""
    int rpm{42};
    if (!try_set_rpm(rpm, 0) || rpm != 0) return 1;
    if (!try_set_rpm(rpm, 3'000) || rpm != 3'000) return 2;
    if (try_set_rpm(rpm, -1) || rpm != 3'000) return 3;
    if (try_set_rpm(rpm, 3'001) || rpm != 3'000) return 4;
    if (!try_set_rpm(rpm, 85) || rpm != 85) return 5;
    """,
    "02_sensor_average": r"""
    if (average(std::span<const int>{}).has_value()) return 1;
    const std::array readings{2, 4, 9};
    const auto avg = average(readings);
    if (!avg || *avg != 5.0) return 2;
    const std::array negatives{-3, 4};
    const auto half = average(negatives);
    if (!half || *half != 0.5) return 3;
    const std::array single{100};
    if (average(single).value_or(-1) != 100.0) return 4;
    """,
    "03_device_lookup": r"""
    const std::vector<std::string> devices{"x", "y", "x"};
    if (find_device(devices, "x") != &devices[0]) return 1;
    if (find_device(devices, "y") != &devices[1]) return 2;
    if (find_device(devices, "missing") != nullptr) return 3;
    const std::vector<std::string> empty{};
    if (find_device(empty, "x") != nullptr) return 4;
    """,
}

def main():
    parser = argparse.ArgumentParser(description="Validate C++20 Chapter 07")
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--exercise",choices=["01","02","03","04"],help="Test your edited exercise file")
    selection.add_argument("--project",action="store_true",help="Test your edited project starter")
    args = parser.parse_args()
    compiler = shlex.split(os.environ.get("CXX", "g++"))
    if args.exercise:
        name = next(n for n in EXERCISES if n.startswith(args.exercise+"_"))
        targets = [(f"exercises/{name}.cpp",EXERCISES[name])]
    elif args.project:
        targets = [("project/channel_report.cpp",PROJECT)]
    else:
        targets = [(f"examples/{name}.cpp",cases) for name,cases in EXAMPLES.items()]
        targets += [(f"solutions/{name}.cpp",cases) for name,cases in EXERCISES.items()]
        targets += [("solutions/channel_report.cpp",PROJECT)]

    passed = failed = 0
    with tempfile.TemporaryDirectory(prefix="cpp_ch07_") as scratch:
        for index, (source, cases) in enumerate(targets):
            executable = Path(scratch)/f"test_{index}"
            cmd = compiler + ["-std=c++20","-Wall","-Wextra","-Wpedantic","-Werror",str(ROOT/source),"-o",str(executable)]
            build = subprocess.run(cmd,capture_output=True,text=True,check=False)
            if build.returncode:
                failed += len(cases)
                print(f"[FAIL] {source}: compilation\n{build.stderr}")
                continue
            for ci,(user_input,exit_status,stdout,stderr) in enumerate(cases,1):
                try:
                    proc=subprocess.run([str(executable)],input=user_input,text=True,capture_output=True,timeout=4,check=False)
                    ok=(proc.returncode==exit_status and proc.stdout==stdout and proc.stderr==stderr)
                except subprocess.TimeoutExpired:
                    ok=False;proc=None
                if ok:
                    passed += 1
                    print(f"[PASS] {source} #{ci}")
                else:
                    failed += 1
                    print(f"[FAIL] {source} #{ci}")
                    print(f"  expected exit={exit_status}, stdout={stdout!r}, stderr={stderr!r}")
                    if proc is not None:
                        print(f"  actual exit={proc.returncode}, stdout={proc.stdout!r}, stderr={proc.stderr!r}")
        # Function-level cases prevent hard-coded demonstration output from passing.
        if args.exercise and name in UNIT_CHECKS:
            unit_sources = [(f"exercises/{name}.cpp", name)]
        elif not args.exercise and not args.project:
            unit_sources = [(f"solutions/{name}.cpp", name) for name in UNIT_CHECKS]
        else:
            unit_sources = []
        for unit_number, (source, key) in enumerate(unit_sources):
            original = (ROOT/source).as_posix()
            code = (f'#define main chapter_demo_main\n#include "{original}"\n'
                    '#undef main\nint main() {\n'
                    + UNIT_CHECKS[key] + '\n    return 0;\n}\n')
            harness = Path(scratch)/f"unit_{unit_number}.cpp"
            harness.write_text(code,encoding="utf-8")
            executable = Path(scratch)/f"unit_{unit_number}"
            build = subprocess.run(compiler + ["-std=c++20","-Wall","-Wextra","-Wpedantic","-Werror","-Wno-return-type",str(harness),"-o",str(executable)], capture_output=True,text=True,check=False)
            if build.returncode:
                failed += 1
                print(f"[FAIL] unit {source}: compilation\n{build.stderr}")
                continue
            run = subprocess.run([str(executable)],capture_output=True,text=True,timeout=4,check=False)
            if run.returncode == 0:
                passed += 1
                print(f"[PASS] unit {source}: edge cases")
            else:
                failed += 1
                print(f"[FAIL] unit {source}: exit={run.returncode}, stdout={run.stdout!r}, stderr={run.stderr!r}")
    print(f"Result: {passed} PASS, {failed} FAIL (total {passed+failed})")
    return 1 if failed else 0

if __name__ == "__main__":
    raise SystemExit(main())
