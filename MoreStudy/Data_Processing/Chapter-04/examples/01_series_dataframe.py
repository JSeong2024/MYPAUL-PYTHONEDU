import pandas as pd

scores = pd.Series([82, 95, 78], index=["민수", "지은", "하나"], name="score")
students = pd.DataFrame({"name": ["민수", "지은", "하나"], "score": [82, 95, 78]})

print("Series:", scores.to_dict())
print("Series dtype:", scores.dtype)
print("DataFrame shape:", students.shape)
print(students.to_string(index=False))
