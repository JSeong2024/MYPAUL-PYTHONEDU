from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]

def build_report(output_dir=None):
    out = Path(output_dir) if output_dir is not None else ROOT / 'output/mini_03_weather'
    out.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(ROOT / 'data/weather_hourly.csv', parse_dates=['timestamp_local'])
    if df.duplicated(['station_id','timestamp_local']).any():
        raise ValueError('Duplicate station-hour')
    stations = sorted(df['station_id'].unique())
    expected = pd.date_range('2026-10-01 00:00', '2026-10-14 23:00', freq='h')
    fig, axes = plt.subplots(len(stations), 1, figsize=(11, 8), sharex=True, layout='constrained')
    gaps = {}
    for ax, station in zip(axes, stations):
        s = df[df['station_id']==station].set_index('timestamp_local').sort_index().reindex(expected)
        gaps[station] = int(s['temperature_c'].isna().sum())
        # 24h rolling window: full 24 observed hours required.
        smooth = s['temperature_c'].rolling(24, min_periods=24).mean()
        ax.plot(s.index, s['temperature_c'], alpha=.3, label='Observed temperature')
        ax.plot(s.index, smooth, lw=1.7, label='24-hour mean')
        ax.set(ylabel='Temp (°C)', title=f'{station}: {gaps[station]} missing hourly records')
        ax.grid(alpha=.2)
    axes[0].legend(ncol=2)
    axes[-1].set_xlabel('Local timestamp (KST)')
    fig.savefig(out / 'weather_report.png', dpi=145)
    plt.close(fig)
    daily = df.assign(date=df['timestamp_local'].dt.floor('D')).groupby(['station_id','date'],as_index=False).agg(temperature_mean_c=('temperature_c','mean'),precipitation_total_mm=('precipitation_mm','sum'),readings=('temperature_c','size'))
    daily.to_csv(out/'daily_weather.csv',index=False)
    return {'stations': len(stations), 'rows': len(df), 'missing_hours': sum(gaps.values()), 'daily_rows': len(daily)}

if __name__ == '__main__':
    print(build_report())
