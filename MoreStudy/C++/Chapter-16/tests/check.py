#!/usr/bin/env python3
"""Chapter 16 offline verification; checks real behavior, CMake targets and installed SDK consumer."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_OUTPUTS = {
    '01_build_pipeline': 'Build pipeline: source -> object -> executable\n',
    '02_translation_units': 'Tokens: 3\n',
    '03_target_design': 'Total: 42\n',
    '04_header_contracts': 'Count: 3\n',
    '05_cpp20_standard': 'Has B: true\n',
    '06_static_library_client': 'sensor-A: 3\n',
    '07_shared_library_boundary': 'Alert: true\n',
    '08_interface_requirements': 'Peak: 9\n',
    '09_target_warnings': 'Can add: true\n',
    '10_compile_definitions': 'Trace: disabled\n',
    '11_presets_and_options': 'Mode: Debug-like\n',
    '12_ctest_behavior': 'Test: PASS\n',
    '13_install_public_api': 'Public API total: 20\n',
    '14_package_consumer': 'First: 2\n',
    '15_dependency_strategy': 'Parsed: true, value=120\n',
    '16_reproducible_builds': 'Valid: true\n',
}
EXERCISES = (
    '01_versioned_target', '02_include_contract',
    '03_configuration_flag', '04_release_safe_tests',
)
PROJECTS = (
    ('basic', ROOT / 'examples/17_device_report'),
    ('advanced', ROOT / 'solutions/advanced_pipeline'),
    ('pro', ROOT / 'solutions/pro_sensor_sdk'),
)


def execute(argv: list[str], *, cwd: Path | None = None, timeout: int = 90) -> subprocess.CompletedProcess[str]:
    return subprocess.run(argv, cwd=cwd, capture_output=True, text=True, timeout=timeout, check=False)


def must_run(argv: list[str], *, cwd: Path | None = None, timeout: int = 90) -> subprocess.CompletedProcess[str]:
    process = execute(argv, cwd=cwd, timeout=timeout)
    if process.returncode:
        raise RuntimeError(f'Command: {argv}\nstdout:\n{process.stdout}\nstderr:\n{process.stderr}')
    return process


def main() -> int:
    parser = argparse.ArgumentParser(description='C++20 Chapter 16 tests')
    parser.add_argument('--compiler', default=os.environ.get('CXX', 'g++'))
    parser.add_argument('--mode', choices=['solutions', 'student'], default='solutions')
    parser.add_argument('--only', choices=['all', 'examples', 'exercises', 'basic', 'advanced', 'pro'], default='all')
    args = parser.parse_args()
    failures = []
    checked = 0

    def check(label: str, callback) -> None:
        nonlocal checked
        checked += 1
        try:
            callback()
            print(f'[PASS] {label}', flush=True)
        except (RuntimeError, OSError, subprocess.TimeoutExpired, AssertionError) as e:
            failures.append(label)
            print(f'[FAIL] {label}: {e}', flush=True)

    with tempfile.TemporaryDirectory(prefix='cpp_ch16_') as temporary:
        root = Path(temporary)
        flags = ['-std=c++20', '-Wall', '-Wextra', '-Wpedantic', '-Werror']
        if args.only in ('all', 'examples'):
            for index, (name, expected) in enumerate(EXAMPLE_OUTPUTS.items(), start=1):
                def test_example(name=name, expected=expected, index=index):
                    output = root / f'example_{index}'
                    must_run([args.compiler, *flags, str(ROOT/'examples'/f'{name}.cpp'), '-o', str(output)])
                    actual = must_run([str(output)]).stdout
                    if actual != expected:
                        raise AssertionError(f'expected={expected!r} actual={actual!r}')
                check(f'example / {name}', test_example)

        if args.only in ('all', 'exercises'):
            source_folder = 'solutions' if args.mode == 'solutions' else 'exercises'
            for index, stem in enumerate(EXERCISES, start=1):
                for diagnostics in ([False, True] if index == 3 else [False]):
                    def test_exercise(stem=stem,index=index,diagnostics=diagnostics):
                        source = (ROOT/source_folder/(stem+'.cpp')).as_posix()
                        driver = (ROOT/'tests/cases'/f'exercise-{index:02d}.cpp').as_posix()
                        harness = root/f'harness_{index}_{int(diagnostics)}.cpp'
                        harness.write_text('#define CH16_LIBRARY_ONLY\n#include '+repr(source).replace("'",'"')+
                            '\n#include '+repr(driver).replace("'",'"')+'\n',encoding='utf-8')
                        output = root/f'exercise_{index}_{int(diagnostics)}'
                        extra = ['-DCH16_DIAGNOSTICS'] if diagnostics else []
                        must_run([args.compiler,*flags,*extra,str(harness),'-o',str(output)])
                        must_run([str(output)])
                    check(f'exercise / {stem}'+(' (diagnostics)' if diagnostics else ''), test_exercise)

        if args.only in ('all', 'basic', 'advanced', 'pro'):
            for level, location in PROJECTS:
                if args.only not in ('all', level):
                    continue
                project = location if (args.mode == 'solutions' or level == 'basic') else ROOT/'projects'/location.name
                def test_project(level=level,project=project):
                    build = root/f'build_{level}'
                    must_run(['cmake','-S',str(project),'-B',str(build),
                              '-DCMAKE_CXX_COMPILER='+args.compiler,
                              '-DCMAKE_CXX_STANDARD=20','-DCMAKE_CXX_STANDARD_REQUIRED=ON',
                              '-DCMAKE_CXX_EXTENSIONS=OFF','-DCMAKE_BUILD_TYPE=Release'], timeout=90)
                    must_run(['cmake','--build',str(build),'--parallel','2'],timeout=90)
                    must_run(['ctest','--test-dir',str(build),'--output-on-failure','--no-tests=error'],timeout=50)
                check(f'CMake / {level}',test_project)

            if args.only in ('all','pro'):
                def test_install_consumer():
                    source = ROOT/('solutions/pro_sensor_sdk' if args.mode=='solutions' else 'projects/pro_sensor_sdk')
                    build = root/'pro_install_build'
                    prefix = root/'temporary_prefix'
                    moved = root/'moved_prefix'
                    must_run(['cmake','-S',str(source),'-B',str(build),
                              '-DCMAKE_CXX_COMPILER='+args.compiler,'-DCMAKE_BUILD_TYPE=Release',
                              '-DSENSORSDK_BUILD_TESTS=OFF', '-DCMAKE_INSTALL_PREFIX='+str(prefix)])
                    must_run(['cmake','--build',str(build),'--parallel','2'])
                    must_run(['cmake','--install',str(build)])
                    shutil.move(str(prefix),str(moved)) # relocatability: do not rely on old prefix
                    consumer = root/'consumer_build'
                    must_run(['cmake','-S',str(source/'consumer'),'-B',str(consumer),
                              '-DCMAKE_CXX_COMPILER='+args.compiler,'-DCMAKE_PREFIX_PATH='+str(moved),
                              '-DCMAKE_CXX_STANDARD=20','-DCMAKE_CXX_STANDARD_REQUIRED=ON'])
                    must_run(['cmake','--build',str(consumer),'--parallel','2'])
                    exe = consumer / ('sensor_consumer.exe' if os.name=='nt' else 'sensor_consumer')
                    result = must_run([str(exe)])
                    if result.stdout!='Consumer avg: 8\n':
                        raise AssertionError(result.stdout)
                check('Pro / installed consumer and relocated prefix',test_install_consumer)

    print(f'Result: {checked - len(failures)}/{checked} passed ({args.compiler}, {args.mode})')
    return 1 if failures else 0


if __name__=='__main__':
    sys.exit(main())
