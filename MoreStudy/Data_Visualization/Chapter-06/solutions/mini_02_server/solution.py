from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]

def build_report(output_dir=None):
    out = Path(output_dir) if output_dir is not None else ROOT / 'output/mini_02_server'
    out.mkdir(parents=True, exist_ok=True)
    raw = pd.read_csv(ROOT / 'data/server_metrics.csv')
    raw['timestamp_utc'] = pd.to_datetime(raw['timestamp_utc'], utc=True, errors='raise')
    if raw['timestamp_utc'].duplicated().any():
        raise ValueError('Duplicate measurement timestamps')
    raw = raw.set_index('timestamp_utc').sort_index()
    start = pd.Timestamp('2026-10-26 00:00', tz='UTC')
    end = pd.Timestamp('2026-10-27 23:55', tz='UTC')
    times = pd.date_range(start, end, freq='5min')
    frame = raw.reindex(times)
    known = int(frame['latency_ms'].notna().sum())
    # Mask incomplete 1-hour windows, avoid manufacturing 0ms latency.
    avg_latency = frame['latency_ms'].rolling(12, min_periods=12).mean()
    fig, axes = plt.subplots(2, 1, figsize=(11, 6.5), sharex=True, layout='constrained')
    axes[0].plot(frame.index, frame['cpu_pct'], lw=.9)
    axes[0].axhline(80, color='#b33a3a', ls='--', lw=1, label='Example watch line (80%)')
    axes[0].set(ylabel='CPU (%)', title='Server measurements (UTC)')
    axes[0].legend()
    axes[1].plot(frame.index, frame['latency_ms'], alpha=.38, label='Observed latency')
    axes[1].plot(frame.index, avg_latency, color='#c15a18', lw=1.9, label='1-hour rolling mean')
    axes[1].set(ylabel='Latency (ms)', xlabel='Time (UTC)')
    axes[1].legend()
    for ax in axes: ax.grid(alpha=.25)
    fig.savefig(out / 'server_monitor.png', dpi=145)
    plt.close(fig)
    summary = {'expected_samples': len(frame), 'valid_samples': known, 'missing_samples': len(frame)-known, 'max_cpu': float(frame['cpu_pct'].max()), 'max_latency': float(frame['latency_ms'].max())}
    pd.Series(summary).to_json(out / 'summary.json', indent=2)
    return summary

if __name__ == '__main__':
    print(build_report())
