"""자료구조 선택의 의미: 순서, 키 조회, 중복 제거."""

raw_ids = ["A-02", "A-01", "A-02", "A-03"]
unique_ids = list(dict.fromkeys(raw_ids))

scores = {"A-01": 84, "A-02": 92, "A-03": 77}
missing = "A-04"
print("원본 순서 유지 + 중복 제거:", unique_ids)
print("A-02 점수:", scores["A-02"])
print("미등록 학생 존재?:", missing in scores)

# 순서만 중요하면 list, Key 조회가 중요하면 dict,
# 순서 없는 고유값 집합이 필요하면 set을 고려합니다.
