"""Compile and check Chapter 05 C++20 examples, solutions, and project."""
import argparse
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
# (stdin, returncode, stdout, stderr)
EXAMPLES = {
    '01_function_basics': [('', 0, 'Area: 10 m2\n', '')],
    '02_declaration_definition': [('', 0, 'Remaining: 12\n', '')],
    '03_pass_by_value': [('', 0, 'Original: SENSOR\nUpdated: SENSOR-A\n', '')],
    '04_return_and_void': [('', 0, 'Squared: 36\n', '')],
    '05_read_only_parameters': [('', 0, 'Device: DEV-42\nValid prefix: true\n', '')],
    '06_defaults_and_overloads': [('', 0, 'Shipping: 3000 won\nCustom shipping: 4500 won\nCount: 12\nTemperature: 23.5 C\n', '')],
    '07_scope_and_lifetime': [('', 0, 'Attempt: 4\n', '')],
    '08_optional_result': [('', 0, 'Utilization: 75%\nInvalid capacity\n', '')],
    '09_constexpr_and_attributes': [('', 0, 'Score: 100\n', '')],
    '11_function_tests': [('', 0, 'All tests passed (3 cases)\n', '')],
    '12_lambda_capture': [('', 0, 'Above threshold: 3\n', '')],
}
EXERCISES = {
    '01_temperature_converter': [
        ('25\n', 0, 'Fahrenheit: 77.0\n', ''),
        ('0\n', 0, 'Fahrenheit: 32.0\n', ''),
        ('-40\n', 0, 'Fahrenheit: -40.0\n', ''),
        ('invalid\n', 1, '', 'Error: invalid temperature.\n'),
    ],
    '02_shipping_fee': [
        ('42000 0\n', 0, 'Shipping: 3000 won\n', ''),
        ('49999 1\n', 0, 'Shipping: 5000 won\n', ''),
        ('50000 0\n', 0, 'Shipping: 0 won\n', ''),
        ('50000 1\n', 0, 'Shipping: 2000 won\n', ''),
        ('-1 0\n', 1, '', 'Error: invalid order.\n'),
        ('30000 2\n', 1, '', 'Error: invalid order.\n'),
        ('bad\n', 1, '', 'Error: invalid order.\n'),
    ],
    '03_function_overload': [
        ('', 0, 'Count: 12\nTemperature: 23.5 C\n', ''),
    ],
    '04_lambda_threshold': [
        ('60\n42 68 73 49 81\n', 0, 'High readings: 3\n', ''),
        ('100\n0 1 2 3 4\n', 0, 'High readings: 0\n', ''),
        ('0\n0 1 2 3 4\n', 0, 'High readings: 4\n', ''),
        ('invalid\n', 1, '', 'Error: invalid threshold.\n'),
        ('3\n1 2 3 X 5\n', 1, '', 'Error: invalid reading.\n'),
    ],
}

def project_expected(name, offset, readings):
    avg = sum(readings)/3
    adjusted = avg+offset
    prefix = (f'Device: Offset (C): Reading 1 (C): Reading 2 (C): Reading 3 (C): '
              f'\n--- Calibration Report ---\nDevice: {name}\nOffset: {offset:.2f} C\n'
              f'Average (raw): {avg:.2f} C\nAverage (adjusted): {adjusted:.2f} C\n'
              f'Status: {"HIGH" if adjusted>35.0 else "NORMAL"}\n')
    return prefix

PROJECT = [
    ('Lab Sensor A\n-0.5\n20\n22\n24\n', 0, project_expected('Lab Sensor A', -0.5, [20,22,24]), ''),
    ('Temp Device\n0\n35\n35\n35\n', 0, project_expected('Temp Device',0,[35,35,35]), ''),
    ('Temp Device\n1\n35\n35\n35\n', 0, project_expected('Temp Device',1,[35,35,35]), ''),
    ('Sensor\n-20\n-50\n-50\n-50\n', 0, project_expected('Sensor',-20,[-50,-50,-50]), ''),
    ('\n0\n1\n2\n3\n',1,'Device: ','Error: invalid device name.\n'),
    ('Sensor\n21\n1\n2\n3\n',1,'Device: Offset (C): Reading 1 (C): Reading 2 (C): Reading 3 (C): ','Error: invalid measurement.\n'),
    ('Sensor\n0\n151\n2\n3\n',1,'Device: Offset (C): Reading 1 (C): Reading 2 (C): Reading 3 (C): ','Error: invalid measurement.\n'),
    ('Sensor\n0\n1\ninvalid\n3\n',1,'Device: Offset (C): Reading 1 (C): Reading 2 (C): ','Error: invalid measurement.\n'),
]


def main():
    parser=argparse.ArgumentParser(description='Compile and validate Chapter 05 programs')
    mode=parser.add_mutually_exclusive_group()
    mode.add_argument('--exercise', choices=('01','02','03','04'), help='Check your exercise')
    mode.add_argument('--project', action='store_true', help='Check your project starter')
    args=parser.parse_args()
    compiler=shlex.split(os.environ.get('CXX','g++'))
    targets=[]
    if args.exercise:
        stem=next(x for x in EXERCISES if x.startswith(args.exercise+'_'))
        targets=[([f'exercises/{stem}.cpp'], EXERCISES[stem])]
    elif args.project:
        targets=[(['project/calibration_report.cpp'],PROJECT)]
    else:
        targets=[([f'examples/{name}.cpp'], cases) for name,cases in EXAMPLES.items()]
        targets.append((['examples/10_multi_file/main.cpp','examples/10_multi_file/inventory.cpp'],[('',0,'Available: 12\n','')]))
        targets += [([f'solutions/{name}.cpp'], cases) for name,cases in EXERCISES.items()]
        targets.append((['solutions/calibration_report.cpp'],PROJECT))

    total=0
    failed=0
    with tempfile.TemporaryDirectory(prefix='cpp_ch05_') as tmp:
        for index,(sources,cases) in enumerate(targets):
            executable=Path(tmp)/f'program_{index}'
            cmd=compiler+['-std=c++20','-Wall','-Wextra','-Wpedantic','-Werror']+[str(ROOT/s) for s in sources]+['-o',str(executable)]
            compiled=subprocess.run(cmd,capture_output=True,text=True,check=False)
            if compiled.returncode:
                total+=1;failed+=1
                print(f'FAIL compile {sources}: {compiled.stderr}')
                continue
            for case_no,(input_text,code,out,err) in enumerate(cases,1):
                total+=1
                try:
                    run=subprocess.run([str(executable)],input=input_text,capture_output=True,text=True,timeout=5,check=False)
                    actual=(run.returncode,run.stdout,run.stderr)
                    if actual == (code,out,err):
                        print(f'PASS {sources[0]} case {case_no}')
                    else:
                        failed+=1
                        print(f'FAIL {sources[0]} case {case_no}: expected {(code,out,err)!r}; actual {actual!r}')
                except subprocess.TimeoutExpired:
                    failed+=1
                    print(f'FAIL {sources[0]} case {case_no}: timeout')
    print(f'\nResult: {total-failed}/{total} PASS')
    return 1 if failed else 0

if __name__ == '__main__':
    sys.exit(main())
