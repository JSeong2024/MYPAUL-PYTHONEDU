"""얕은 복사와 중첩 객체의 공유를 확인."""

from copy import deepcopy

original = [{"id": "S-01", "scores": [80, 90]}]
shallow = original.copy()
deep = deepcopy(original)

shallow[0]["scores"][0] = 60
print("원본 점수:", original[0]["scores"])
print("얕은 복사 점수:", shallow[0]["scores"])
print("깊은 복사 점수:", deep[0]["scores"])
print("바깥 리스트는 같은 객체?:", original is shallow)
