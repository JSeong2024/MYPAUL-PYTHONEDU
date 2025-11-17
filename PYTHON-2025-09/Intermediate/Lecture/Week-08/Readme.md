# Guide
- [Week 8-1.](#week-8-1-coding-practice)
- [Week 8-2.](#week-8-2-data-visualization)

# Week 8-1. Coding Practice

## Problem 8.1. 쇼핑 리스트 관리 및 합계 계산
```
shopping_list = {'사과': 1200, '바나나': 2500, '귤': 800, '수박': 15000}
```

## Problem 8.2. 카페 메뉴 가격 계산기
```
menu = {'커피': 3000, '라떼': 4000, '케이크': 5000}
customer_order = ['커피', '케이크', '라떼', '커피’]
```

## Problem 8.3. 재고 관리 및 주문 시스템 시뮬레이션
```
# 초기 재고 상태
current_inventory = {
    '사과': 100,
    '바나나': 50,
    '귤': 200
}

# 주문 목록
order_list = [
    {'제품': '사과', '수량': 30},
    {'제품': '바나나', '수량': 60},
    {'제품': '귤', '수량': 150},
    {'제품': '수박', '수량': 10}
]
```

## Problem 8.4. 도서관 재고 및 대출 관리 시스템
```
# {제목: 저자}
books = {
    '파이썬 중급': '이수영',
    '데이터 과학': '주사랑.',
    '맛있는 피자': '박수진'
}

# {제목: 현재_대출자_ID (None이면 대출 가능)}
borrow_status = {
    '파이썬 중급': None,
    '데이터 과학': 'user101',
    '맛있는 피자': None
}

def display_status():
    print("\n--- 현재 도서관 대출 상태 ---")
    print(f"{'제목':<23} | {'저자':<11} | {'대출자 ID (None:가능)':<25}")
    print("-" * 60)
    for title, author in books.items():
        borrower = borrow_status.get(title, "상태불명")
        print(f"{title:<20} | {author:<10} | {borrower}")
    print("-" * 60)
```

```
print("\n--- 대출 테스트 ---")
print(borrow_book('파이썬 중급', 'user202')) 
print(borrow_book('데이터 과학', 'user303'))     
print(borrow_book('파이썬 고급', 'user202'))

display_status()
```

```
print("\n--- 반납 테스트 ---")
print(return_book('파이썬 중급', 'user202'))
print(return_book('데이터 과학', 'user303'))
print(return_book('맛있는 피자', 'user101'))

display_status()
```

# Week 8-2. Data Visualization
## 8.1.2. 선 그래프
```
year = [2014,2015,2016,2017,2018,2019,2020,2021,2022]
gdp = [3079.9,3250.1,3398.8,3574,3678.2,3721.8,3744,4003.6,4165.5]

plt.plot(year, gdp)  # 그래프 입력
plt.show()           # 그래프 출력(보여주기)
```

```
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 6, 7)
y = x**2

plt.plot(x, y, marker='o', color='blue')
plt.show()
```

```
import numpy as np
import matplotlib.pyplot as plt

# 1. x 값의 범위를 설정
# 0부터 6까지 촘촘한 간격으로 7개의 점을 생성(기본값=50개)
x = np.linspace(0, 6, 7)

# 2. y 값을 계산 (y = 2 * x^2)
y = x**2

# 3. 그래프 그리기
plt.figure(figsize=(8, 6)) # 그래프 크기 설정 (선택 사항)
plt.plot(x, y, label='$y = x^2$', marker='o', color='blue') # 선 그래프 그리기

# 4. 그래프에 레이블과 제목, 그리드를 추가
#plt.title('Graph of y = x^2')
plt.legend() # 범례 표시
#plt.grid(True) # 그리드 표시

# 5. 그래프를 화면에 출력
plt.show()
```

## 8.1.3. 막대 그래프
```
season = ['spring', 'summer', 'autumn', 'winter']
precipitation = [330.5, 612.8, 256.4, 13.3]
```

```
preci_dict = {'spring': 330.5, 'summer': 612.8, 'autumn': 256.4, 'winter': 13.3}
```

## 8.1.4. 산점도
```
year = [2000, 2005, 2010, 2015, 2020]
single_person = [15.5, 20.0, 23.9, 27.2, 31.7]
baby_born = [640089, 438707, 470171, 438420, 272337]
```

```
import matplotlib.pyplot as plt

year = [2000, 2005, 2010, 2015, 2020]
single_person = [15.5, 20.0, 23.9, 27.2, 31.7]
baby_born = [640089, 438707, 470171, 438420, 272337]

# 산점도 생성
plt.scatter(single_person, baby_born, color='red', marker='o')

# 각 점에 연도(year) 주석(annotation) 추가
for i, txt in enumerate(year):
  # 각 데이터 포인트 (x[i], y[i]) 옆에 텍스트 txt를 표시
  # xytext와 textcoords를 사용하여 주석 위치를 미세 조정
  plt.annotate(txt, 
              (single_person[i], baby_born[i]), 
              xytext=(5, 5), 
              textcoords='offset points', 
              fontsize=10, 
              color='blue')

# 그래프 제목과 축 라벨 설정
plt.title('Scatter Plot')
plt.xlabel('Single-Person Household Ratio (%)')
plt.ylabel('Number of Babies Born')

# 그래프 출력
plt.show()
```
