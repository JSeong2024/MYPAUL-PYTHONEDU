```
import pandas as pd

data = {
    'name': ['Jessica', 'Liam', 'Sophia', 'Ryan', 'Alex'],
    'exam': [45, 30, 40, 37, 48],
    'assign1': [20, 17, 22, 18, 24],
    'assign2': [19, 14, 18, 15, 25],
    'sum': [84, 61, 80, 70, 97],
    'grade': ['B', 'C', 'B', 'C', 'A']
}

df = pd.DataFrame(data)
```

```
import matplotlib.pyplot as plt

plt.figure(figsize=(5,3))
plt.bar(df['name'], df['sum'])
plt.ylabel('score')
plt.show()
```

```
import matplotlib.pyplot as plt

plt.figure(figsize=(5,3))
plt.bar(df['name'], df['exam'], label='exam')
plt.bar(df ['name'], df['assign1'], bottom=df['exam'], label='assign1')
plt.bar(df ['name'], df['assign2'], bottom=df['exam']+df ['assign1'], label='assign2')
plt.legend()
plt.ylabel('score')
plt.show()
```
