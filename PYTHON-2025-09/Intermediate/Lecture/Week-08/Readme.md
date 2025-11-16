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
