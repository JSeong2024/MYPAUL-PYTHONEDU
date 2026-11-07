import pandas as pd

raw = pd.Series([" seoul ", "BUSAN", "Gwangju", "unknown"], dtype="string")
lookup = {"seoul": "Seoul", "busan": "Busan", "gwangju": "Gwangju"}
normalized = raw.str.strip().str.casefold().map(lookup)
print("Normalized:", normalized.fillna("INVALID").tolist())
