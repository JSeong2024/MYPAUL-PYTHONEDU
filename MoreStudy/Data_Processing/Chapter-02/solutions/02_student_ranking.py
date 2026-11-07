"""Exercise 02 정답 — 중첩 딕셔너리와 복수 기준 정렬."""

students = [
    {"name": "서아", "scores": {"Python": 95, "Math": 95}},
    {"name": "도윤", "scores": {"Python": 80, "Math": 90}},
    {"name": "민지", "scores": {"Python": 88, "Math": 92}},
    {"name": "하준", "scores": {"Python": 90, "Math": 90}},
]

results = [
    {"name": student["name"], "average": sum(student["scores"].values()) / len(student["scores"])}
    for student in students
]
ranked = sorted(results, key=lambda item: (-item["average"], item["name"]))

for rank, student in enumerate(ranked, start=1):
    print(f"{rank}위 {student['name']}: {student['average']:.1f}점")
