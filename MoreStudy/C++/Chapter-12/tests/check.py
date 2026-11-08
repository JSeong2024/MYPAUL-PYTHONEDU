#!/usr/bin/env python3
"""Chapter 12 C++20 검증 스크립트. 기본값은 모범답안과 예제 검사."""
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_EXPECTED = {
    '01_scope_lifetime.cpp': 'Open: outer\nOpen: inner\nWorking\nClose: inner\nEnd of main\nClose: outer\n',
    '02_raii_lock_guard.cpp': 'Count: 2\n',
    '03_unique_ownership.cpp': 'Device: Motor-A\nOld owner empty: true\nDevice: Motor-A\n',
    '04_custom_deleter.cpp': 'Temporary file written\n',
    '05_move_semantics.cpp': 'Target: sensor-packet\nSource: reused\n',
    '06_move_only.cpp': 'Jobs: 10 / 20\n',
    '06_shared_weak.cpp': 'Owners: 2\nValue: 42\nExpired: true\n',
    '07_value_categories.cpp': 'Lvalue\nRvalue\nLvalue\n',
    '07_copy_move_tracing.cpp': 'Copy\nMove\n',
    '08_rule_of_zero.cpp': 'Copy samples: 3\nMove samples: 3\n',
    '09_rule_of_five.cpp': 'Copy: 50, Moved: 7, Old size: 0\n',
    '10_exchange_state.cpp': 'New: 42, Old: -1\nReleased: 1\n',
    '11_copy_elision.cpp': 'Token: 27\n',
    '12_move_if_noexcept.cpp': 'Copy\n',
    '13_exception_safety.cpp': 'Rejected\nFirst: 10\n',
    '14_borrowed_view.cpp': 'sensor-A: 12\n',
    '15_optional_factory.cpp': 'Created: sensor-A\nRejected empty id\n',
    '16_resource_contracts.cpp': 'Inspect: Pump-A\nInspect: Pump-A\nRegistered\nOwner empty: true\n',
}
PROJECT_EXPECTED = ('Connected: sensor-A\nSamples: 21, 24, 22\n'
                    'Closed sessions: 1\nRejected: empty id\n')


def execute(command, cwd=None):
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False,
                          timeout=25)


def run(args):
    compiler = args.compiler or (shutil.which('g++-14') or shutil.which('g++') or shutil.which('clang++'))
    if not compiler:
        print('C++20 compiler not found', file=sys.stderr)
        return 2
    flags = ['-std=c++20', '-Wall', '-Wextra', '-Wpedantic']
    category = args.only
    cases = []
    if args.mode == 'solutions':
        if category in ('all', 'examples'):
            cases += [(f'example-{p[:2]}', [ROOT/'examples'/p], expected, None)
                      for p, expected in EXAMPLE_EXPECTED.items()]
        if category in ('all', 'project'):
            cases.append(('project-demo',
                          [ROOT/'examples/17_device_session/main.cpp', ROOT/'examples/17_device_session/session.cpp'],
                          PROJECT_EXPECTED, None))
    for i in range(1, 5):
        key = f'exercise-{i:02d}'
        if category in ('all', key):
            path = ROOT / ('solutions' if args.mode == 'solutions' else 'exercises') / [
                '01_transactional_update.cpp', '02_unique_owner.cpp',
                '03_move_only_packet.cpp', '04_device_factory.cpp'][i-1]
            cases.append((key, [ROOT/'tests/cases'/f'{key}.cpp'], None, path))
    if category in ('all', 'project'):
        path = ROOT / ('solutions/device_session' if args.mode == 'solutions' else 'project')
        cases.append(('project-behavior', [ROOT/'tests/cases/project.cpp', path/'session.cpp'],
                      None, path))
    if not cases:
        print('No checks selected', file=sys.stderr)
        return 2
    ok = 0
    with tempfile.TemporaryDirectory(prefix='chapter12_test_') as tmp:
        target = Path(tmp)/('case.exe' if os.name == 'nt' else 'case')
        for key, source_files, expected, extra in cases:
            command = [compiler, *flags]
            if isinstance(extra, Path) and extra.is_file():
                command += ['-DCH12_LIBRARY_ONLY', '-DCH12_SOURCE_PATH='+f'"{extra.as_posix()}"']
            if isinstance(extra, Path) and extra.is_dir():
                command += ['-I', str(extra)]
            command += [str(f) for f in source_files] + ['-o', str(target)]
            compiled = execute(command)
            if compiled.returncode != 0 or compiled.stderr.strip():
                print(f'[FAIL] {key}: compilation/warnings\n{compiled.stderr}')
                continue
            result = execute([str(target)], cwd=tmp)
            if result.returncode == 0 and (expected is None or result.stdout == expected):
                ok += 1
                print(f'[PASS] {key}')
            else:
                print(f'[FAIL] {key}: exit={result.returncode}\n'
                      f'expected={expected!r}\nactual={result.stdout!r}\n{result.stderr}')
    print(f'Result: {ok}/{len(cases)} passed ({Path(compiler).name}, C++20, {args.mode})')
    return 0 if ok == len(cases) else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Chapter 12 example & solution checks')
    parser.add_argument('--compiler', help='e.g. g++-14 or clang++')
    parser.add_argument('--mode', choices=['solutions', 'student'], default='solutions')
    parser.add_argument('--only', choices=['all', 'examples', 'project',
                                             'exercise-01', 'exercise-02',
                                             'exercise-03', 'exercise-04'], default='all')
    sys.exit(run(parser.parse_args()))
