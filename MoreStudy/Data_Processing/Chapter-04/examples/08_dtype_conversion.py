import pandas as pd

raw = pd.DataFrame({"price_text": ["2,500", "N/A", "1,200"],
                    "date_text": ["2026-10-01", "invalid", "2026-10-03"]})
clean = raw.copy()
clean["price"] = pd.to_numeric(
    clean["price_text"].str.replace(",", "", regex=False), errors="coerce"
).astype("Int64")
clean["order_date"] = pd.to_datetime(clean["date_text"], format="%Y-%m-%d", errors="coerce")
print("Parsed prices:", clean["price"].astype("string").fillna("NA").tolist())
print("Price dtype:", clean["price"].dtype)
print("Invalid price/date:", int(clean["price"].isna().sum()), int(clean["order_date"].isna().sum()))
print("Original columns:", raw.columns.tolist())
