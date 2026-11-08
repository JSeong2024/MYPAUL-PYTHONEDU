"""Chapter 05 실습용 합성 데이터 생성. 외부 다운로드 없음."""
from pathlib import Path
import csv
import math
import random

DATA = Path(__file__).resolve().parents[1] / 'data'


def write_csv(name, header, rows):
    DATA.mkdir(parents=True, exist_ok=True)
    with (DATA / name).open('w', newline='', encoding='utf-8') as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        writer.writerows(rows)


def main():
    random_generator = random.Random(2026)
    sensor_rows = []
    for day in range(1, 21):
        values = [round(48 + 4 * j + 0.6 * day + 2.2 * math.sin(day * 0.7 + j), 2) for j in range(4)]
        if day in (4, 13):
            values[1] = -1.0
        if day in (7, 18):
            values[3] = -1.0
        sensor_rows.append([f'D{day:02}', *values])
    write_csv('sensor_readings.csv', ['day', 'sensor_01', 'sensor_02', 'sensor_03', 'sensor_04'], sensor_rows)

    pairs = [[round(i * 0.5, 3), round(0.65 + 1.6 * i * 0.5 + random_generator.uniform(-0.08, 0.08), 4)] for i in range(12)]
    write_csv('calibration_pairs.csv', ['input_signal', 'reference_value'], pairs)

    event_rows = []
    for i in range(1, 49):
        zone = ['north', 'central', 'south'][i % 3]
        temp = round(23 + (i % 7) * 0.8 + random_generator.uniform(-0.4, 0.4), 2)
        vib = round(1.2 + (i % 9) * 0.48 + random_generator.uniform(-0.1, 0.1), 3)
        hour = (i * 5) % 24
        label = int(temp >= 27 and vib >= 3.3)
        event_rows.append([f'EV{i:03}', zone, hour, temp, vib, label])
    write_csv('facility_events.csv', ['event_id', 'zone', 'hour', 'temperature_c', 'vibration_mm_s', 'alert_label'], event_rows)

    audit_rows = []
    for i in range(13):
        x = -1.5 + 0.25 * i
        target = math.tanh(0.7 * x - 0.2) + random_generator.uniform(-0.02, 0.02)
        audit_rows.append([round(x, 4), round(target, 6)])
    write_csv('gradient_audit.csv', ['input_signal', 'target_value'], audit_rows)

    invalid_rows = list(event_rows[:3])
    invalid_rows[1][3] = ''
    write_csv('facility_events_invalid.csv', ['event_id', 'zone', 'hour', 'temperature_c', 'vibration_mm_s', 'alert_label'], invalid_rows)


if __name__ == '__main__':
    main()
