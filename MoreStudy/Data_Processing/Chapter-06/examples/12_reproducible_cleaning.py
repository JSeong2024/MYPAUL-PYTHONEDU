import pandas as pd

source = pd.Series([" Seoul ", "BUSAN"], dtype="string")
def normalize_regions(values):
    return values.str.strip().str.casefold().map({"seoul": "Seoul", "busan": "Busan"})

once = normalize_regions(source)
twice = normalize_regions(once)
print("Original unchanged:", source.iloc[0] == " Seoul ")
print("Same after rerun:", once.equals(twice))
