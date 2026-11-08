"""Example: UTC boundary to KST calendar day."""
import pandas as pd
instant = pd.Timestamp('2026-09-30T22:00:00Z')
print('UTC:', instant)
print('KST:', instant.tz_convert('Asia/Seoul'))
