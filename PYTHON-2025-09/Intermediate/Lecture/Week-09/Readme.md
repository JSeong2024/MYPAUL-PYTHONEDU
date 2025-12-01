# Week 9-2. Numpy
## 9.2. 배열 활용
```
import matplotlib.pyplot as plt

year = [2006, 2009, 2012, 2015, 2018]
kor = [547, 546, 554, 524, 526]

plt.figure(figsize=(5, 3))
plt.plot(year, kor)
plt.ylim(500, 580)
plt.xlabel('year')
plt.ylabel('score')
plt.show()
```

```
import numpy as np

ind = np.arange(len(year))
plt.plot(ind, kor)
plt.xticks(ind, year)
```
