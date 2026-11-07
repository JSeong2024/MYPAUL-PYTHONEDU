"""원소별 연산과 범용 함수(ufunc)."""
import numpy as np

quantity = np.array([2, 3, 1])
unit_price = np.array([1500, 2000, 5000])
sales = quantity * unit_price
print("판매액:", sales)
print("총판매액:", sales.sum())

celsius = np.array([0.0, 20.0, 35.0])
fahrenheit = celsius * 9 / 5 + 32
print("화씨:", fahrenheit)
print("제곱근:", np.sqrt(np.array([1, 4, 9])))
