#!/usr/bin/env python3
# Chapter 09 examples, solutions, project, and class behavior checks.
from __future__ import annotations
import argparse
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_OUTPUTS = {
    '01_inheritance_basics': 'TEMP-01: 24.5 C\n',
    '02_access_control': 'Accepted: true, rejected: false, speed: 1200\n',
    '03_virtual_dispatch': 'Sensor: generic\nSensor: distance\n',
    '04_override_and_final': '79: false, 80: true\n',
    '05_abstract_interface': 'Critical: true\n',
    '06_virtual_destructor': 'Using camera\nCamera closed\nDevice closed\n',
    '07_polymorphic_collection': 'Sensors: 2, total: 37\n',
    '08_object_slicing': 'By value: device\nBy reference: camera\n',
    '09_dynamic_cast': 'Camera FPS: 60\nNot a camera\n',
    '10_composition_vs_inheritance': 'Moved: true, battery: 25%\n',
    '11_interface_segregation': 'Before: 1\nAfter: 0\n',
    '12_nonvirtual_interface': 'Invalid: false, high: true\n',
    '13_dependency_injection_test': 'Transport test: PASS\n',
    '14_variant_alternative': 'Distance: 35 cm\n',
    '15_constructor_dispatch': 'Base constructor: base\nDerived constructor: derived\nAfter construction: derived\n',
}
SOLUTION_OUTPUTS = {
    '01_alarm_channels': '79: false, 80: true\n',
    '02_robot_motor': 'First: true, second: false, RPM: 2000\n',
    '03_sensor_registry': 'High: 2\n',
    '04_fault_detector': 'Sent: true, rejected: false, messages: 1\n',
}
PROJECT_CASES = [
    ('three-mixed', '3\nTEMP 75\nDIST 22\nTEMP 85\n', 0,
     'Sensors (1-5): Sensor 1 (TEMP/DIST value): Sensor 2 (TEMP/DIST value): Sensor 3 (TEMP/DIST value): --- Robot Sensor Monitor ---\nTEMP 75: CLEAR\nDIST 22: ALERT\nTEMP 85: ALERT\nTotal: 3\nAlerts: 2\n', ''),
    ('lower-bounds', '2\nTEMP -40\nDIST 0\n', 0,
     'Sensors (1-5): Sensor 1 (TEMP/DIST value): Sensor 2 (TEMP/DIST value): --- Robot Sensor Monitor ---\nTEMP -40: CLEAR\nDIST 0: ALERT\nTotal: 2\nAlerts: 1\n', ''),
    ('upper-bounds', '2\nTEMP 125\nDIST 400\n', 0,
     'Sensors (1-5): Sensor 1 (TEMP/DIST value): Sensor 2 (TEMP/DIST value): --- Robot Sensor Monitor ---\nTEMP 125: ALERT\nDIST 400: CLEAR\nTotal: 2\nAlerts: 1\n', ''),
    ('thresholds', '2\nTEMP 80\nDIST 30\n', 0,
     'Sensors (1-5): Sensor 1 (TEMP/DIST value): Sensor 2 (TEMP/DIST value): --- Robot Sensor Monitor ---\nTEMP 80: ALERT\nDIST 30: ALERT\nTotal: 2\nAlerts: 2\n', ''),
    ('invalid-count', '0\n', 1, 'Sensors (1-5): ', 'Error: invalid count\n'),
    ('invalid-type', '1\nWIFI 5\n', 1, 'Sensors (1-5): Sensor 1 (TEMP/DIST value): ', 'Error: invalid sensor\n'),
    ('invalid-value', '1\nTEMP 130\n', 1, 'Sensors (1-5): Sensor 1 (TEMP/DIST value): ', 'Error: invalid sensor\n'),
    ('invalid-input', '1\nTEMP no\n', 1, 'Sensors (1-5): Sensor 1 (TEMP/DIST value): ', 'Error: invalid reading\n'),
]
DRIVERS = {
    '01_alarm_channels': r'''
int main() {
    HighAlarm a{80};
    HighAlarm b{10};
    const Alarm& base = a;
    return !base.triggered(79) && base.triggered(80) && base.triggered(100)
        && !base.triggered(-100) && !b.triggered(9) && b.triggered(10) ? 0 : 1;
}
''',
    '02_robot_motor': r'''
int main() {
    ElectricMotor m;
    Motor& base = m;
    if (base.speed() != 0 || base.set_speed(-1) || base.speed() != 0) return 1;
    if (!base.set_speed(3000) || base.speed() != 3000) return 2;
    if (base.set_speed(3001) || base.speed() != 3000) return 3;
    if (!base.set_speed(0) || base.speed() != 0) return 4;
    return 0;
}
''',
    '03_sensor_registry': r'''
int main() {
    std::vector<std::unique_ptr<Sensor>> sensors;
    if (count_high(sensors, 80) != 0) return 1;
    sensors.push_back(std::make_unique<FixedSensor>(79));
    sensors.push_back(nullptr);
    sensors.push_back(std::make_unique<FixedSensor>(80));
    sensors.push_back(std::make_unique<FixedSensor>(100));
    if (count_high(sensors, 80) != 2) return 2;
    if (count_high(sensors, 100) != 1) return 3;
    return 0;
}
''',
    '04_fault_detector': r'''
int main() {
    FakeTransport fake;
    if (report_fault(fake, 0) || report_fault(fake, -1)) return 1;
    if (!fake.messages().empty()) return 2;
    if (!report_fault(fake, 42) || !report_fault(fake, 7)) return 3;
    if (fake.messages().size() != 2) return 4;
    if (fake.messages()[0] != "FAULT:42" || fake.messages()[1] != "FAULT:7") return 5;
    class FailedTransport final : public Transport {
    public:
        bool send(std::string_view) override { return false; }
    };
    FailedTransport failed;
    if (report_fault(failed, 42)) return 6;
    return 0;
}
''',
}

def main():
    parser = argparse.ArgumentParser(description='Chapter 09 C++20 checks')
    parser.add_argument('--compiler', default=os.environ.get('CXX', 'g++'))
    parser.add_argument('--mode', choices=['reference', 'student'], default='reference')
    parser.add_argument('--only', choices=['all', 'exercise-01', 'exercise-02', 'exercise-03', 'exercise-04', 'project'], default='all')
    args = parser.parse_args()
    source_dir = 'solutions' if args.mode == 'reference' else 'exercises'
    passes = failures = 0
    with tempfile.TemporaryDirectory(prefix='cpp09_') as tmp:
        base = Path(tmp)
        def build(name, files):
            dest = base / name
            command = [args.compiler, '-std=c++20', '-Wall', '-Wextra', '-Wpedantic', *map(str,files), '-o', str(dest)]
            r = subprocess.run(command, text=True, capture_output=True)
            if r.returncode: raise RuntimeError(r.stderr or 'compile failed')
            return dest
        def check(label, fn):
            nonlocal passes, failures
            try:
                fn()
                print('[PASS]', label)
                passes += 1
            except Exception as exc:
                print('[FAIL]', label, ':', exc)
                failures += 1
        def run(exe, data=''):
            return subprocess.run([str(exe)], input=data, text=True, capture_output=True, timeout=5)
        def match(exe, expected, code=0):
            r=run(exe)
            assert r.returncode == code, f'exit {r.returncode} != {code}: {r.stderr}'
            assert r.stdout == expected, f'output: {r.stdout!r} != {expected!r}'
        if args.only == 'all':
            for name, expected in EXAMPLE_OUTPUTS.items():
                def test(name=name,expected=expected):
                    exe=build('example_'+name, [ROOT/'examples'/(name+'.cpp')]); match(exe,expected)
                check('example / '+name, test)
            def multifile():
                p=ROOT/'examples/16_robot_monitor'
                exe=build('multi', [p/'main.cpp',p/'monitor.cpp'])
                r=run(exe)
                assert r.returncode == 0 and r.stdout == (
                    '--- Robot Sensor Monitor ---\nTEMP 75: CLEAR\nDIST 22: ALERT\n'
                    'TEMP 85: ALERT\nTotal: 3\nAlerts: 2\n'),r.stdout
                r2=subprocess.run([str(exe),'--self-test'], capture_output=True,timeout=5)
                assert r2.returncode == 0
            check('example / 16_robot_monitor (multi-file)',multifile)
        target_names = [name for name in SOLUTION_OUTPUTS if args.only in ('all','exercise-'+name[:2])]
        for name in target_names:
            path=ROOT/source_dir/(name+'.cpp')
            if args.only == 'all' or args.only == 'exercise-'+name[:2]:
                def test_sample(name=name,path=path):
                    exe=build('practice_'+name,[path]);match(exe,SOLUTION_OUTPUTS[name])
                check(source_dir+' / '+name,test_sample)
                def test_driver(name=name,path=path):
                    text=path.read_text(encoding='utf-8')
                    driver=base/('driver_'+name+'.cpp')
                    driver.write_text('#define main old_chapter_main\n'+text+'\n#undef main\n'+DRIVERS[name],encoding='utf-8')
                    exe=build('driver_'+name,[driver]);r=run(exe)
                    assert r.returncode == 0, f'function check failed (exit {r.returncode}): {r.stderr}'
                check('function behavior / '+name,test_driver)
        if args.only in ('all','project'):
            source = ROOT/('solutions/robot_monitor.cpp' if args.mode=='reference' else 'project/robot_monitor.cpp')
            try:
                project_exe=build('project',[source])
                for case,data,code,out,err in PROJECT_CASES:
                    def test_project(case=case,data=data,code=code,out=out,err=err):
                        r=run(project_exe,data)
                        assert r.returncode == code, f'exit {r.returncode} != {code}'
                        assert r.stdout == out, f'stdout {r.stdout!r} != {out!r}'
                        assert r.stderr == err, f'stderr {r.stderr!r} != {err!r}'
                    check('project / '+case,test_project)
            except Exception as error:
                check('project / compile', lambda message=str(error): (_ for _ in ()).throw(RuntimeError(message)))
    print(f'\nResult: {passes} PASS, {failures} FAIL')
    return 1 if failures else 0
if __name__ == '__main__':
    sys.exit(main())
