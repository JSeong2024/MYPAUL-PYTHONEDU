#!/usr/bin/env python3
"""Chapter 17 tests: standard-library-only Python runner.

Examples:
  python tests/check.py --compiler g++-14
  python tests/check.py --compiler clang++ --only projects
  python tests/check.py --mode student --only exercise-02  # expected failure
"""
from __future__ import annotations
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_RESULTS = {
 "01_explicit_checks.cpp":"PASS: 2 checks\n",
 "02_boundary_tests.cpp":"PASS: 6 boundaries\n",
 "03_test_double.cpp":"Alert: true\n",
 "04_deterministic_dependency.cpp":"Clock tests: PASS\n",
 "05_parameterized_tests.cpp":"Shipping cases: 4\n",
 "06_invariant_tests.cpp":"Invariant: preserved\n",
 "07_regression_test.cpp":"Regression: PASS\n",
 "08_exception_tests.cpp":"Error contract: PASS\n",
 "09_ctest_exit_status.cpp":"Use --self-test\n",
 "10_debugger_repro.cpp":"Positive sum: 12\n",
 "11_address_sanitizer_fix.cpp":"Bounds: handled\n",
 "12_undefined_behavior_fix.cpp":"Overflow: rejected\n",
 "13_thread_sanitizer_fix.cpp":"Counter: 2000\n",
 "14_steady_clock.cpp":"Timer: monotonic\n",
 "15_benchmark_checks.cpp":"Result: 3000\n",
 "16_profiling_baseline.cpp":"Matches: 2\n",
}
EXERCISE_FILES=["01_strict_parser.cpp","02_batch_total.cpp","03_rolling_max.cpp","04_sensor_fake.cpp"]
PROJECTS = {
  "basic":"examples/17_device_validator",
  "advanced":"solutions/advanced_event_audit",
  "pro":"solutions/pro_quality_gate",
}

def run(command,cwd=None,timeout=120):
    return subprocess.run([str(x) for x in command],cwd=cwd,capture_output=True,text=True,
                          encoding='utf-8',errors='replace',timeout=timeout,check=False)

def main() -> int:
    parser=argparse.ArgumentParser(description="Chapter 17 independent tests")
    parser.add_argument('--compiler',default=os.environ.get('CXX','g++'),help='C++ compiler executable')
    parser.add_argument('--mode',choices=('solutions','student'),default='solutions')
    parser.add_argument('--only',choices=('all','examples','projects','exercise-01','exercise-02','exercise-03','exercise-04'),default='all')
    args=parser.parse_args()
    if not shutil.which(args.compiler):
        print('Compiler not available: '+args.compiler,file=sys.stderr);return 2
    passed=0;total=0
    def check(label,fn):
        nonlocal passed,total
        total+=1
        try:
            fn()
            passed+=1
            print('[PASS]',label,flush=True)
        except (AssertionError,RuntimeError,subprocess.TimeoutExpired) as exc:
            print('[FAIL]',label,':',str(exc),flush=True)
    def verify(command,label,cwd=None,expected=None,timeout=120):
        result=run(command,cwd,timeout)
        if result.returncode != 0 or (expected is not None and result.stdout!=expected):
            raise RuntimeError(f'{label}: exit={result.returncode} stdout={result.stdout[:400]!r} stderr={result.stderr[:800]!r}')
        return result
    with tempfile.TemporaryDirectory(prefix='ch17_test_') as tmp:
        path=Path(tmp)
        if args.only in ('all','examples'):
            for number,(filename,expected) in enumerate(EXAMPLE_RESULTS.items(),1):
                source=ROOT/'examples'/filename
                exe=path/('example_'+str(number))
                def task(source=source,exe=exe,expected=expected):
                    verify([args.compiler,'-std=c++20','-Wall','-Wextra','-Wpedantic','-Werror',
                            '-pthread',str(source),'-o',str(exe)],'compile')
                    verify([str(exe)],'run',expected=expected,timeout=6)
                check('example / '+filename,task)
        for i,filename in enumerate(EXERCISE_FILES,1):
            if args.only not in ('all',f'exercise-{i:02d}'):
                continue
            source=ROOT/('solutions' if args.mode=='solutions' else 'exercises')/filename
            driver=ROOT/'tests/cases'/f'exercise-{i:02d}.cpp'
            exe=path/('exercise_'+str(i))
            def task(source=source,driver=driver,exe=exe):
                verify([args.compiler,'-std=c++20','-Wall','-Wextra','-Wpedantic','-Werror',
                        '-DCH17_SOURCE_PATH="'+source.as_posix()+'"',str(driver),'-o',str(exe)],'compile')
                verify([exe],'run',expected='',timeout=6)
            check('exercise / '+filename,task)
        if args.only in ('all','projects'):
            for key,solution in PROJECTS.items():
                project=ROOT/(solution if args.mode=='solutions' or key=='basic'
                              else solution.replace('solutions/','projects/',1))
                build=path/('build_'+key)
                def task(key=key,project=project,build=build):
                    verify(['cmake','-S',project,'-B',build,'-DCMAKE_CXX_COMPILER='+args.compiler,
                            '-DCMAKE_CXX_STANDARD=20','-DCMAKE_CXX_STANDARD_REQUIRED=ON',
                            '-DCMAKE_BUILD_TYPE=Release'],'configure')
                    verify(['cmake','--build',build,'--parallel','2'],'build')
                    verify(['ctest','--test-dir',build,'--output-on-failure','--no-tests=error'],'ctest')
                check('project / '+key,task)
            if args.mode=='solutions':
                def consumer():
                    build=path/'build_pro'
                    install=path/'pkg_original'
                    moved=path/'relocated_sdk'
                    verify(['cmake','--install',build,'--prefix',install],'install')
                    shutil.move(str(install),str(moved))
                    b=path/'consumer'
                    src=ROOT/'solutions/pro_quality_gate/consumer'
                    verify(['cmake','-S',src,'-B',b,'-DCMAKE_CXX_COMPILER='+args.compiler,
                            '-DCMAKE_PREFIX_PATH='+str(moved)],'consumer configure')
                    verify(['cmake','--build',b,'--parallel','2'],'consumer build')
                    verify([b/'quality_consumer'],'consumer run',expected='Consumer: PASS\n')
                check('project / Pro package relocation & external consumer',consumer)
    print(f'Result: {passed}/{total} PASS ({args.compiler}, C++20, {args.mode})')
    return 0 if passed==total else 1

if __name__=='__main__':
    raise SystemExit(main())
