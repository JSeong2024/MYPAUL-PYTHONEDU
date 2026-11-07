# 기본 유효성 규칙: 점수는 0~100, 학생 번호는 고유값입니다.
records = [
    {"student_id": "S-01", "score": 90},
    {"student_id": "S-02", "score": 110},
    {"student_id": "S-01", "score": 80},
    {"student_id": "S-03", "score": None},
]
seen = set()
valid = []
reasons = []

for record in records:
    student_id = record["student_id"]
    score = record["score"]
    if student_id in seen:
        reasons.append("중복 학생 번호")
    elif not isinstance(score, (int, float)) or isinstance(score, bool):
        reasons.append("점수 누락 또는 자료형 오류")
    elif not 0 <= score <= 100:
        reasons.append("점수 범위 초과")
    else:
        seen.add(student_id)
        valid.append(record)

print("유효 기록:", len(valid))
print("제외 기록:", len(reasons))
print("사유:", ", ".join(reasons))
