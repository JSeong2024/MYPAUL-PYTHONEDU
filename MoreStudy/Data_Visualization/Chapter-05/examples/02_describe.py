from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
sns.set_theme(style='whitegrid')

df = pd.read_csv(ROOT / 'data/support_tickets.csv')
minutes = df['first_response_min'].dropna()
summary = minutes.describe(percentiles=[.5,.9])
print(summary[['count','mean','50%','90%']].round(2).to_string())
fig, ax = plt.subplots(figsize=(6.5, 3.5))
values = [summary['mean'], summary['50%'], summary['90%']]
ax.bar(['Mean','Median','P90'], values, color=['#5089B3','#6CA59A','#D09C72'])
ax.set(title='Three views of response time', ylabel='Minutes')
fig.tight_layout(); fig.savefig(ROOT / 'figures/02_describe.png',dpi=145);plt.close(fig)
