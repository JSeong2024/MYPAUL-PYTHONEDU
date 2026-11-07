# 데이터의 의미(수량, 분류, 날짜)와 Python 자료형을 구분합니다.
records = [
    {"student_id": "S-001", "subject": "Python", "score": 92},
    {"student_id": "S-002", "subject": "Python", "score": 85},
]

print("기록 수:", len(records))
print("첫 번째 기록:", records[0])
print("점수 자료형:", type(records[0]["score"]).__name__)
print("학생 번호 자료형:", type(records[0]["student_id"]).__name__)
