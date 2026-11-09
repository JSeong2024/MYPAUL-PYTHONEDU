#!/usr/bin/env python3
"""Chapter 18: C++20 standalone, behavior, CMake, and relocated SDK tests.

Usage:
  python3 tests/check.py --compiler g++-14
  python3 tests/check.py --compiler clang++
  python3 tests/check.py --mode student --only exercise-01
"""
from __future__ import annotations
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "01_network_layers": "Application: framing and validation\nTransport: TCP stream / UDP datagram\nAddress: 127.0.0.1 (IPv4 loopback)\n",
    "02_network_byte_order": "1 2 3 4\n",
    "03_tcp_stream_chunking": "Message: HELLO\nMessage: WORLD\nCount: 2\n",
    "04_length_prefix_codec": "Frame bytes: 6\nPayload: OK\n",
    "05_strict_command_parser": "valid: true / 8080\ninvalid: false\n",
    "06_socket_raii": "Owner moved: true\n",
    "07_tcp_loopback": "Reply: ECHO:hello\n",
    "08_udp_loopback": "Datagram: sensor=42\n",
    "09_receive_timeout": "Timeout configured (100 ms)\n",
    "10_error_result": "Known: 200\nUnknown: true\n",
    "11_request_response": "PONG\nREADY\nERR unknown command\n",
    "12_thread_safe_server_state": "Processed: 1000\n",
    "13_cooperative_shutdown": "Stopped: true\n",
    "14_posix_pipe": "POSIX pipe requires a POSIX system\n" if os.name == 'nt' else "IPC: from child\n",
 "15_unix_domain_socket": "socketpair demonstration requires POSIX\n" if os.name == 'nt' else "Local socket: LOCAL\n",
    "16_defensive_protocol": "Rejected: oversized payload\nAccepted: 8 bytes\n",
}
EXERCISES = [
    '01_frame_decoder.cpp', '02_reading_parser.cpp',
    '03_retry_policy.cpp', '04_bounded_queue.cpp'
]
PROJECTS = {
    'basic': 'examples/17_loopback_echo',
    'advanced': 'solutions/advanced_telemetry_server',
    'pro': 'solutions/pro_loopback_sdk',
}


def call(args: list[str], *, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, capture_output=True, text=True, timeout=timeout)


def run(args: argparse.Namespace) -> int:
    checks: list[tuple[str, bool, str]] = []
    compiler = args.compiler or os.environ.get('CXX', 'g++')
    flags = ['-std=c++20', '-Wall', '-Wextra', '-Wpedantic', '-Werror', '-pthread']
    if os.name == 'nt':
        # GNU MinGW is supported here; MSVC uses the CMake project path instead.
        flags += ['-lws2_32']
    def record(name: str, passed: bool, detail: str = '') -> None:
        checks.append((name, passed, detail))
        print(f"[{'PASS' if passed else 'FAIL'}] {name}", flush=True)
        if not passed and detail:
            print('    ' + detail[-1700:].replace('\n', '\n    '), flush=True)
    with tempfile.TemporaryDirectory(prefix='ch18_cpp20_') as work:
        temp = Path(work)
        if args.only in ('all','examples'):
            for name, output in EXPECTED.items():
                source = ROOT/'examples'/f'{name}.cpp'
                exe = temp / ('test_' + name + ('.exe' if os.name == 'nt' else ''))
                command = [compiler,*flags[:6],str(source),'-o',str(exe)]
                if os.name == 'nt':command.append('-lws2_32')
                cp = call(command)
                if cp.returncode:
                    record(name,False,cp.stderr);continue
                cp = call([str(exe)],timeout=7)
                record(name,cp.returncode == 0 and cp.stdout == output and not cp.stderr,
                       f'exit={cp.returncode}, output={cp.stdout!r}, err={cp.stderr!r}')
        for i, source_name in enumerate(EXERCISES,1):
            key=f'exercise-{i:02d}'
            if args.only not in ('all',key):continue
            source=ROOT/('solutions' if args.mode=='solutions' else 'exercises')/source_name
            driver=temp/f'{key}_driver.cpp'
            driver.write_text('#define CH18_LIBRARY_ONLY\n#include "' + source.as_posix() + '"\n' +
                              (ROOT/'tests/cases'/f'{key}.cpp').read_text(encoding='utf-8'),encoding='utf-8')
            exe=temp/key
            cp=call([compiler,*flags[:6],str(driver),'-o',str(exe)])
            if cp.returncode:record(key,False,cp.stderr);continue
            try:
                cp=call([str(exe)],timeout=7)
                record(key, cp.returncode == 0 and not cp.stderr,
                       f'exit={cp.returncode}, err={cp.stderr!r}')
            except subprocess.TimeoutExpired:
                record(key,False,'timed out')
        if args.only in ('all','projects','basic','advanced','pro'):
            for key,path in PROJECTS.items():
                if args.only not in ('all','projects',key):continue
                if args.mode=='student' and key in ('advanced','pro'):
                    path=path.replace('solutions/','projects/')
                build=temp/('build_'+key)
                options=['cmake','-S',str(ROOT/path),'-B',str(build),
                         '-DCMAKE_CXX_COMPILER='+compiler,'-DCMAKE_CXX_STANDARD=20',
                         '-DCMAKE_CXX_STANDARD_REQUIRED=ON','-DCMAKE_CXX_EXTENSIONS=OFF',
                         '-DCMAKE_BUILD_TYPE=Release']
                try:
                    results=[call(options,timeout=50)]
                    if results[-1].returncode == 0:results.append(call(['cmake','--build',str(build),'--parallel','2'],timeout=70))
                    if results[-1].returncode == 0:results.append(call(['ctest','--test-dir',str(build),
                                                                    '--output-on-failure','--no-tests=error'],timeout=50))
                    passed= len(results)==3 and all(r.returncode==0 for r in results)
                    record('project-'+key,passed,'\n'.join(r.stdout[-600:]+r.stderr[-1100:] for r in results))
                except subprocess.TimeoutExpired:record('project-'+key,False,'CMake timeout')
                if key=='pro' and passed and args.mode=='solutions':
                    # Separate install prefix, move it, and configure an independent consumer project.
                    stage=temp/'stage'
                    moved=temp/'relocated'
                    r=call(['cmake','--install',str(build),'--prefix',str(stage)])
                    if r.returncode:
                        record('pro-relocated-consumer',False,r.stderr);continue
                    shutil.move(str(stage),str(moved))
                    consumer=temp/'consumer-build'
                    cmds=[['cmake','-S',str(ROOT/path/'consumer'),'-B',str(consumer),
                           '-DCMAKE_CXX_COMPILER='+compiler,'-DCMAKE_CXX_STANDARD=20',
                           '-DCMAKE_PREFIX_PATH='+str(moved)],
                          ['cmake','--build',str(consumer),'--parallel','2'],
                          ['ctest','--test-dir',str(consumer),'--output-on-failure','--no-tests=error']]
                    results=[]
                    for command in cmds:
                        result=call(command,timeout=55)
                        results.append(result)
                        if result.returncode:break
                    record('pro-relocated-consumer',len(results)==3 and all(x.returncode==0 for x in results),
                           '\n'.join(x.stdout[-600:]+x.stderr[-1000:] for x in results))
    passed=sum(ok for _,ok,_ in checks)
    print(f'\nResult: {passed}/{len(checks)} PASS ({compiler}, C++20, {args.mode})')
    return 0 if checks and passed==len(checks) else 1

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--compiler',default=None)
    parser.add_argument('--mode',choices=['solutions','student'],default='solutions')
    parser.add_argument('--only',choices=['all','examples','projects','basic','advanced','pro',
                                          'exercise-01','exercise-02','exercise-03','exercise-04'],default='all')
    sys.exit(run(parser.parse_args()))
