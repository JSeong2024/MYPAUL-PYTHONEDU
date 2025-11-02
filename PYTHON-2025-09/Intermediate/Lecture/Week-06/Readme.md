```
!sudo apt-get install -y fonts-nanum
!sudo fc-cache -fv
!rm ~/.cache/matplotlib -rf
```

```
# 사용 가능한 폰트 목록 확인
import matplotlib.font_manager
fpaths = matplotlib.font_manager.findSystemFonts()
font_names = []
for i in fpaths:
    f = matplotlib.font_manager.get_font(i)
    font_names.append(f.family_name)

print(font_names[:5])

for fn in font_names:
    if 'malgun' in fn.lower():
        print(fn)
```

```
# 한글 폰트 깨짐 방지
from matplotlib import rcParams
rcParams["font.family"] = "NanumMyeongjo"
rcParams["axes.unicode_minus"] = False
```

```
import numpy as np
import pandas as pd

data = pd.DataFrame(data={
    'A': [1,4,3,6,5,8,7,9],
    'B': [6,5,7,8,9,9,8,9],
    'C': [8.8,7.7,6.6,5.5,4.4,3.3,2.2,1.1]
})
```

```
import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
y = [10, 20, 25, 30, 45]

plt.plot(x, y, marker='o', linestyle='-')
plt.title('Line Plot')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.grid(True)
plt.show()
```
