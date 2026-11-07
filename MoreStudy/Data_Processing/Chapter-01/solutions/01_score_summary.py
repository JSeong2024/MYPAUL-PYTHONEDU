"""Exercise 01 — 점수 목록 요약 정답."""

scores = [78, 92, 85, 100, 67]

print("인원:", len(scores), "명")
print("최저:", min(scores), "점")
print("최고:", max(scores), "점")
print(f"평균: {sum(scores) / len(scores):.1f}점")
print("80점 이상:", sum(score >= 80 for score in scores), "명")
