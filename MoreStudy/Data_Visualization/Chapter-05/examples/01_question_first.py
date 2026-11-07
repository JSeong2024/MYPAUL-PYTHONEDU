from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
sns.set_theme(style='whitegrid')

raw = pd.read_csv(ROOT / 'data/shipments.csv')
print('Rows:', len(raw))
print('Unique IDs:', raw['shipment_id'].nunique())
print('Status:', raw['status'].value_counts().to_dict())
print('Known duration:', raw['actual_days'].notna().sum())
fig, ax = plt.subplots(figsize=(6, 3.6))
raw['status'].value_counts().plot.bar(ax=ax, color=['#4E85AF','#CB9362'])
ax.set(title='Shipment record status', ylabel='Records', xlabel='Status')
fig.tight_layout()
fig.savefig(ROOT / 'figures/01_question_first.png', dpi=145)
plt.close(fig)
