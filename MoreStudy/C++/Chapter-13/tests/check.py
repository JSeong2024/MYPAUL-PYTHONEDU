#!/usr/bin/env python3
"""Chapter 13 C++20 checks; student mode intentionally fails before TODO completion."""
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
EXPECT = {
    '01_standard_first.cpp': 'Max: 19\nMax double: 2.75\nExplicit type: 2.5\nHighest reading: 32\n',
    '02_template_deduction.cpp': 'Integer: true\nDouble: true\nExplicit: false\n',
    '03_concepts_and_requires.cpp': 'Even: true\nMidpoint: 2\n',
    '04_reading_contract.cpp': 'Alert: true\n',
    '05_class_templates.cpp': 'Integer samples: 2\nFirst double: 2.5\n',
    '06_nttp_ctad.cpp': 'Size: 3\nSum: 12\n',
    '07_variadic_fold.cpp': 'Total: 20\nEmpty: 0\n',
    '08_traits_specialization.cpp': 'Arithmetic: true\nLabel: integer\nOther: other\n',
    '09_if_constexpr.cpp': 'Integer: 12\nInvalid double: 0\n',
    '10_generic_lambda.cpp': 'Above 10: 2\n',
    '11_ranges_views.cpp': 'Selected: 24 38 40\n',
    '12_projection.cpp': 'A:8 B:4 C:2 \n',
    '13_forwarding.cpp': 'Pump-A, Pump-B\n',
    '14_optional_parser.cpp': 'Port: 8080\nInvalid: 0\n',
    '15_legacy_constraints.cpp': 'Legacy: true\nConcept: true\n',
    '16_api_contracts.cpp': 'Average: 6\n',
}
EXERCISES = ['01_reading_alert.cpp', '02_strong_quantity.cpp',
             '03_filter_devices.cpp', '04_strict_parser.cpp']
PROJECT_OUTPUT = ('Temperature: count=3, min=28.0, max=34.0, avg=31.3\n'
                  'Pressure: count=2, min=100.0, max=102.0, avg=101.0\n')

def execute(command, cwd=None):
    return subprocess.run([str(x) for x in command], cwd=cwd, text=True,
                          capture_output=True, timeout=45, check=False)

def check_result(name, command, expected, cwd):
    result = execute(command, cwd)
    if result.returncode == 0 and (expected is None or result.stdout == expected):
        print(f'[PASS] {name}')
        return True
    print(f'[FAIL] {name}: rc={result.returncode}')
    print('STDOUT:', repr(result.stdout))
    print('STDERR:', result.stderr[:2500])
    if expected is not None: print('EXPECTED:', repr(expected))
    return False

def main():
    arg = argparse.ArgumentParser(description='Chapter 13 checks')
    arg.add_argument('--compiler', default=shutil.which('g++-14') or shutil.which('g++') or shutil.which('clang++'))
    arg.add_argument('--mode', choices=['solutions','student'], default='solutions')
    arg.add_argument('--only', choices=['all','examples','exercises','project'], default='all')
    opt = arg.parse_args()
    if not opt.compiler: raise SystemExit('C++ compiler not found')
    flags = ['-std=c++20','-Wall','-Wextra','-Wpedantic']
    total=passed=0
    with tempfile.TemporaryDirectory(prefix='ch13_') as d:
        tmp=Path(d)
        binary=tmp/('test.exe' if os.name=='nt' else 'test')
        def compile_and_run(name, sources, expected, extra=()):
            nonlocal total,passed
            total += 1
            call=execute([opt.compiler,*flags,*extra,*sources,'-o',binary])
            if call.returncode or call.stderr.strip():
                print(f'[FAIL] {name} compile or warnings: {call.stderr[:2500]}')
                return
            if check_result(name,[binary],expected,tmp): passed+=1
        if opt.mode=='solutions' and opt.only in ('all','examples'):
            for fname,expected in EXPECT.items():
                compile_and_run('example-'+fname[:2],[ROOT/'examples'/fname],expected)
        if opt.only in ('all','exercises'):
            for idx,fname in enumerate(EXERCISES,1):
                path=(ROOT/('solutions' if opt.mode=='solutions' else 'exercises')/fname).resolve()
                define='-DCH13_SOURCE_PATH="'+path.as_posix()+'"'
                compile_and_run('exercise-'+str(idx).zfill(2),
                                [ROOT/'tests/cases'/f'exercise-{idx:02d}.cpp'],
                                None,extra=['-DCH13_LIBRARY_ONLY',define])
        if opt.only in ('all','project'):
            directory=ROOT/('solutions/telemetry_pipeline' if opt.mode=='solutions' else 'project')
            ci=ROOT/'examples/17_telemetry_pipeline'
            compile_and_run('project-behavior',[ROOT/'tests/cases/project_behavior.cpp'],
                            None,extra=['-I', directory/'include'])
            if opt.mode=='solutions':
                for label,base in [('ci-project',ci),('solution-project',directory)]:
                    total+=1
                    build=tmp/label
                    config=execute(['cmake','-S',base,'-B',build,'-DCMAKE_CXX_COMPILER='+str(opt.compiler),
                                    '-DCMAKE_CXX_STANDARD=20','-DCMAKE_CXX_STANDARD_REQUIRED=ON',
                                    '-DCMAKE_CXX_EXTENSIONS=OFF'])
                    if config.returncode:
                        print(f'[FAIL] {label}: configure\n{config.stderr[:1800]}');continue
                    built=execute(['cmake','--build',build,'--parallel','2'])
                    if built.returncode or 'warning:' in built.stderr:
                        print(f'[FAIL] {label}: build\n{built.stderr[:1800]}');continue
                    test=execute(['ctest','--test-dir',build,'--output-on-failure','--no-tests=error'])
                    run=execute([build/('telemetry_demo.exe' if os.name=='nt' else 'telemetry_demo')])
                    if test.returncode==0 and run.returncode==0 and run.stdout==PROJECT_OUTPUT:
                        passed+=1; print(f'[PASS] {label}: CMake + CTest + output')
                    else:
                        print(f'[FAIL] {label}: CTest rc={test.returncode}, output={run.stdout!r}\n{test.stdout[-1200:]}')
    print(f'Result: {passed}/{total} passed ({Path(opt.compiler).name}, C++20, {opt.mode})')
    return 0 if passed==total else 1

if __name__=='__main__':sys.exit(main())
