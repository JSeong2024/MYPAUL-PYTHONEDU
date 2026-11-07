import pandas as pd

sales = pd.DataFrame({
    "region": ["서울", "서울", "부산", "부산"],
    "sales_won": [10000, 30000, 20000, 10000],
})
sales["region_total"] = sales.groupby("region")["sales_won"].transform("sum")
sales["share_pct"] = (100 * sales["sales_won"] / sales["region_total"]).round(1)
print(sales.to_string(index=False))
