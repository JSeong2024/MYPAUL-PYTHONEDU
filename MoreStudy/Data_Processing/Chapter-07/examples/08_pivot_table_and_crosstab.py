import pandas as pd

data = pd.DataFrame({
    "region": ["서울", "서울", "서울", "부산"],
    "category": ["문구", "문구", "디지털", "문구"],
    "sales_won": [5000, 7000, 30000, 8000],
})
table = data.pivot_table(index="region", columns="category", values="sales_won", aggfunc="sum", fill_value=0)
counts = pd.crosstab(data["region"], data["category"])
print("Sales:")
print(table.to_string())
print("Row counts:")
print(counts.to_string())
