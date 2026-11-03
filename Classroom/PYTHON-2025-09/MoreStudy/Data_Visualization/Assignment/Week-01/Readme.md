# 1.0. matplotlib 한글 폰트 설정
```
# 실행 후, 런타임 →  세션 다시 시작(Ctrl+M+.)
!sudo apt-get install -y fonts-nanum
!sudo fc-cache -fv
!rm ~/.cache/matplotlib -rf
```
```
# 한글 폰트 깨짐 방지
from matplotlib import rcParams
rcParams["font.family"] = "NanumGothicCoding"
rcParams["axes.unicode_minus"] = False
```
위의 두 코드를 실행하면 됨.

```
# 사용 가능한 폰트 목록 확인(선택사항)
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

# 1.1. Study: Graph Basic 
- numpy, pandas, matplotlib 활용
- file: `study_1.1.csv`

# 1.2. Problem
- file: `problem_1.csv`
