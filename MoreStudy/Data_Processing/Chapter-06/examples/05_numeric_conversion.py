import pandas as pd

raw = pd.Series(["12", " 3 ", "unknown", "1.5", ""], dtype="string")
parsed = pd.to_numeric(raw, errors="coerce")
integer_ok = parsed.notna() & parsed.gt(0) & parsed.mod(1).eq(0)
print("Valid positive integers:", int(integer_ok.fillna(False).sum()))
print("Invalid values:", int((~integer_ok.fillna(False)).sum()))
