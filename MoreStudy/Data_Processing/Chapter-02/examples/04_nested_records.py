"""중첩된 레코드에서 과목별 점수를 조회."""

students = [
    {"id": "S-01", "name": "민지", "scores": {"Python": 90, "Math": 82}},
    {"id": "S-02", "name": "도윤", "scores": {"Python": 76, "Math": 91}},
    {"id": "S-03", "name": "서아", "scores": {"Python": 88}},
]

for student in students:
    python_score = student["scores"].get("Python")
    math_score = student["scores"].get("Math")
    math_text = str(math_score) if math_score is not None else "미응시"
    print(f"{student['id']} {student['name']}: Python {python_score}, Math {math_text}")

print("학생 수:", len(students))
