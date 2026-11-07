"""집합을 이용한 중복 제거와 두 집단의 비교."""

monday = ["S-01", "S-02", "S-02", "S-03"]
tuesday = ["S-02", "S-04", "S-03"]
mon_ids = set(monday)
tue_ids = set(tuesday)

print("월요일 방문자:", sorted(mon_ids))
print("공통 방문자:", sorted(mon_ids & tue_ids))
print("월요일에만:", sorted(mon_ids - tue_ids))
print("전체 고유 방문자:", len(mon_ids | tue_ids))

# set의 순회 순서는 보장되지 않으므로 출력에서는 sorted()를 사용합니다.
