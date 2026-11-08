"""Compile and verify C++20 Chapter 08 examples, solutions and project."""
import argparse
import os
from pathlib import Path
import shlex
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = {
    '01_struct_record': 'TEMP-A: 23.5 C (online: true)\n',
    '02_designated_initializers': 'Packet 42: 128 bytes, encrypted: true\n',
    '03_encapsulation': 'Accepted: true, rejected: false, RPM: 1500\n',
    '04_explicit_constructor': 'Device ID: 1024\n',
    '05_member_initialization': 'Retries: 3, delay: 250 ms\nLIDAR on channel 2\n',
    '06_const_member_functions': 'Samples: 2\n',
    '07_optional_factory': '23 C allowed: true\nInvalid range rejected: true\n',
    '08_delegating_constructor': 'Temperature: threshold 100\nVibration: threshold 80\n',
    '09_composition': 'Moved: true, battery: 25%\n',
    '10_static_members': 'Before: 0\nInside: 2\nAfter: 0\n',
    '11_defaulted_comparison': 'a == b: true\na == c: false\n',
    '12_this_and_fluent_api': 'Alarm at 70: true\n',
    '14_rule_of_zero': 'Copied: 1, moved: 1\n',
}
MULTI = 'First: true, duplicate: false, second: true\nRegistered: 2\n'
SOLUTIONS = {
    '01_device_profile': 'Valid: true, invalid: false\n',
    '02_bank_account': 'Deposit: true, withdraw: true, balance: 8500 cents\n',
    '03_temperature_window': '23 C allowed: true\n',
    '04_robot_battery': 'Short: true, long: false, battery: 95%\n',
}

def report(items):
    head='Devices (1-5): '+''.join(f'Device {i} (ID power_W online_0_or_1): ' for i in range(1,len(items)+1))
    top=max(items,key=lambda x:x[1])
    return (head+'\n--- Device Inventory ---\n'+f'Registered: {len(items)}\n'
            +f'Online: {sum(x[2] for x in items)}\n'
            +f'Total power: {sum(x[1] for x in items)} W\n'
            +f'Active power: {sum(x[1] for x in items if x[2])} W\n'
            +f'Highest power: {top[0]} ({top[1]} W)\n')

P0='Devices (1-5): '
P1=P0+'Device 1 (ID power_W online_0_or_1): '
P2=P1+'Device 2 (ID power_W online_0_or_1): '
PROJECT = [
    ('3\nCAM-01 12 1\nLIDAR-02 25 0\nIMU-03 8 1\n',0,report([('CAM-01',12,1),('LIDAR-02',25,0),('IMU-03',8,1)]),''),
    ('1\nTEMP 0 0\n',0,report([('TEMP',0,0)]),''),
    ('2\nA 2000 1\nB 2000 1\n',0,report([('A',2000,1),('B',2000,1)]),''),
    ('3\nA 7 1\nB 3 1\nC 7 0\n',0,report([('A',7,1),('B',3,1),('C',7,0)]),''),
    ('5\nA 1 1\nB 2 0\nC 3 1\nD 4 0\nE 5 1\n',0,report([('A',1,1),('B',2,0),('C',3,1),('D',4,0),('E',5,1)]),''),
    ('2\nSENSOR 10 0\nSENSOR 5 1\n',1,P2,'Error: invalid or duplicate device.\n'),
    ('1\nA -1 1\n',1,P1,'Error: invalid or duplicate device.\n'),
    ('1\nA 2001 1\n',1,P1,'Error: invalid or duplicate device.\n'),
    ('1\nA 15 2\n',1,P1,'Error: invalid device input.\n'),
    ('1\nA 15 -1\n',1,P1,'Error: invalid device input.\n'),
    ('0\n',1,P0,'Error: invalid device count.\n'),
    ('6\n',1,P0,'Error: invalid device count.\n'),
    ('foo\n',1,P0,'Error: invalid device count.\n'),
    ('2\nA 1 1\n',1,P2,'Error: invalid device input.\n'),
    ('1\nA 1 x\n',1,P1,'Error: invalid device input.\n'),
]

UNITS = {
'01_device_profile': '''
    const DeviceProfile a{"a", 0.0, false};
    const DeviceProfile b{"b", 2000.0, true};
    const DeviceProfile c{"c", -1.0, true};
    const DeviceProfile d{"", 3.0, true};
    const DeviceProfile e{"x", std::numeric_limits<double>::infinity(), true};
    const DeviceProfile f{"x", std::numeric_limits<double>::quiet_NaN(), true};
    if (!a.valid() || !b.valid() || c.valid() || d.valid() || e.valid() || f.valid()) return 1;
''',
'02_bank_account': '''
    BankAccount a{0};
    if (a.deposit(0) || a.withdraw(-1) || a.balance_cents() != 0) return 1;
    if (!a.deposit(20) || !a.withdraw(20) || a.withdraw(1)) return 2;
    BankAccount b{std::numeric_limits<std::int64_t>::max()};
    if (b.deposit(1) || b.balance_cents() != std::numeric_limits<std::int64_t>::max()) return 3;
    BankAccount c{40};
    if (c.withdraw(41) || c.balance_cents() != 40) return 4;
''',
'03_temperature_window': '''
    const auto valid = TemperatureWindow::create(-20.0, -20.0);
    if (!valid || !valid->contains(-20.0) || valid->contains(-19.0)) return 1;
    if (TemperatureWindow::create(30.0, 10.0)) return 2;
    if (TemperatureWindow::create(std::numeric_limits<double>::infinity(), 20.0)) return 3;
    if (TemperatureWindow::create(0.0, std::numeric_limits<double>::quiet_NaN())) return 4;
    if (valid->contains(std::numeric_limits<double>::quiet_NaN())) return 5;
''',
'04_robot_battery': '''
    Robot robot{2};
    if (!robot.move(1) || robot.battery_percent() != 1) return 1;
    if (!robot.move(5) || robot.battery_percent() != 0) return 2;
    if (robot.move(1) || robot.battery_percent() != 0) return 3;
    Robot another{100};
    if (another.move(0) || another.move(1001) || another.battery_percent() != 100) return 4;
    if (!another.move(6) || another.battery_percent() != 98) return 5;
'''
}

def main():
    ap=argparse.ArgumentParser(description='Validate C++20 Chapter 08')
    group=ap.add_mutually_exclusive_group()
    group.add_argument('--exercise', choices=['01','02','03','04'], help='Check edited exercise')
    group.add_argument('--project', action='store_true', help='Check project starter')
    args=ap.parse_args()
    cxx=shlex.split(os.environ.get('CXX','g++'))
    flags=['-std=c++20','-Wall','-Wextra','-Wpedantic','-Werror']
    if args.exercise:
        name=next(x for x in SOLUTIONS if x.startswith(args.exercise+'_'))
        targets=[([f'exercises/{name}.cpp'],[('',0,SOLUTIONS[name],'')])]
        units=[(f'exercises/{name}.cpp',name)]
    elif args.project:
        targets=[(['project/device_inventory.cpp'],PROJECT)]
        units=[]
    else:
        targets=[([f'examples/{name}.cpp'],[('',0,output,'')]) for name,output in EXAMPLES.items()]
        targets.append((['examples/13_device_registry_main.cpp','examples/13_device_registry.cpp'],[('',0,MULTI,'')]))
        targets.extend(([f'solutions/{name}.cpp'],[('',0,output,'')]) for name,output in SOLUTIONS.items())
        targets.append((['solutions/device_inventory.cpp'],PROJECT))
        units=[(f'solutions/{name}.cpp',name) for name in UNITS]
    passed=failed=0
    with tempfile.TemporaryDirectory(prefix='cpp_ch08_') as temp:
        tmp=Path(temp)
        for i,(sources,cases) in enumerate(targets):
            exe=tmp/f'test_{i}'
            label=', '.join(sources)
            build=subprocess.run(cxx+flags+[str(ROOT/x) for x in sources]+['-o',str(exe)],capture_output=True,text=True)
            if build.returncode:
                failed+=len(cases)
                print(f'[FAIL] {label} compilation\n{build.stderr}')
                continue
            for j,(input_text,rc,stdout,stderr) in enumerate(cases,1):
                try:
                    run=subprocess.run([str(exe)],input=input_text,capture_output=True,text=True,timeout=4)
                    ok=(run.returncode,run.stdout,run.stderr)==(rc,stdout,stderr)
                except subprocess.TimeoutExpired:
                    run=None; ok=False
                if ok:
                    passed+=1
                    print(f'[PASS] {label} #{j}')
                else:
                    failed+=1
                    print(f'[FAIL] {label} #{j}: expected {(rc,stdout,stderr)!r}; actual {None if run is None else (run.returncode,run.stdout,run.stderr)!r}')
        for i,(source,name) in enumerate(units):
            harness=tmp/f'unit_{i}.cpp'
            harness.write_text(f'#define main chapter_demo_main\n#include "{(ROOT/source).as_posix()}"\n#undef main\n#include <limits>\nint main() {{\n'+UNITS[name]+'\nreturn 0;\n}\n',encoding='utf-8')
            exe=tmp/f'unit_{i}'
            build=subprocess.run(cxx+flags+['-Wno-return-type']+[str(harness),'-o',str(exe)],capture_output=True,text=True)
            if build.returncode:
                failed+=1
                print(f'[FAIL] unit {source}: compilation\n{build.stderr}')
                continue
            run=subprocess.run([str(exe)],capture_output=True,text=True,timeout=4)
            if run.returncode==0:
                passed+=1
                print(f'[PASS] unit {source}: boundary cases')
            else:
                failed+=1
                print(f'[FAIL] unit {source}: exit={run.returncode}')
    print(f'Result: {passed} PASS, {failed} FAIL (total {passed+failed})')
    return int(failed>0)

if __name__=='__main__':
    raise SystemExit(main())
