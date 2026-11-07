import pandas as pd

data = pd.DataFrame({"product": ["커피", "노트", "펜"], "stock": [8, 2, 0]})
subset = data.loc[data["stock"] <= 2, ["product", "stock"]].copy()
subset.loc[subset["product"] == "노트", "stock"] = 5
print("Original notebook stock:", int(data.loc[data["product"] == "노트", "stock"].iloc[0]))
print("Subset notebook stock:", int(subset.loc[subset["product"] == "노트", "stock"].iloc[0]))
data.loc[data["product"] == "펜", "stock"] = 4
print("Updated original pen stock:", int(data.loc[data["product"] == "펜", "stock"].iloc[0]))
