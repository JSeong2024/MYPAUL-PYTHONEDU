from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

ROOT = Path(__file__).resolve().parents[2]

def build_report(output_dir=None):
    output = Path(output_dir) if output_dir is not None else ROOT / 'output/mini_01_sales'
    output.mkdir(parents=True, exist_ok=True)
    raw = pd.read_csv(ROOT / 'data/sales_daily.csv', parse_dates=['date'])
    if raw.duplicated(['date', 'store_id']).any():
        raise ValueError('Duplicate store-date keys')
    stores = sorted(raw['store_id'].unique())
    expected = pd.date_range('2026-08-01', '2026-10-31', freq='D')
    wide = raw.pivot(index='date', columns='store_id', values='revenue_krw').reindex(expected)
    wide.index.name = 'date'
    missing = wide.isna().sum().astype(int)
    # Observed zero revenue must remain zero. Missing observations must remain NaN.
    totals = wide.sum(skipna=True).astype(int)
    fig, axes = plt.subplots(2, 1, figsize=(11, 7), sharex=True, layout='constrained')
    for name in stores:
        axes[0].plot(wide.index, wide[name], label=name, lw=1.2, marker='.', ms=2)
        axes[1].plot(wide.index, wide[name].rolling(7, min_periods=7).mean(), label=name)
    axes[0].set(title='Daily revenue by store (gaps preserved)', ylabel='KRW')
    axes[1].set(title='7-day rolling mean (7 valid days required)', ylabel='KRW', xlabel='Date')
    for ax in axes:
        ax.grid(alpha=.25)
        ax.legend(loc='upper left', ncol=3)
    axes[1].xaxis.set_major_locator(mdates.MonthLocator())
    axes[1].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    fig.savefig(output / 'sales_trends.png', dpi=145)
    plt.close(fig)
    pd.DataFrame({'store_id': stores, 'observed_total_krw': [int(totals[s]) for s in stores], 'missing_days': [int(missing[s]) for s in stores]}).to_csv(output / 'store_summary.csv', index=False)
    return {'rows': len(raw), 'stores': len(stores), 'missing_cells': int(wide.isna().sum().sum()), 'total_krw': int(raw['revenue_krw'].sum()), 'figure': str(output / 'sales_trends.png')}

if __name__ == '__main__':
    print(build_report())
