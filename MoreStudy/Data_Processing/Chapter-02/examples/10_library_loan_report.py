"""Chapter 02 Mini Project: 도서관 대출 데이터 구조화 및 집계."""

import json
from collections import Counter, defaultdict
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "library_loans.json"
REQUIRED_TEXT = ("loan_id", "branch", "book_id", "category", "status")


def validate_loan(row: object, seen: set[str]) -> tuple[dict | None, str | None]:
    """유효 레코드만 반환합니다. 원본 딕셔너리는 변경하지 않습니다."""
    if not isinstance(row, dict):
        return None, "레코드 형식 오류"
    if any(not isinstance(row.get(key), str) or not row[key].strip() for key in REQUIRED_TEXT):
        return None, "필수 문자열 오류"
    if row["status"] not in {"borrowed", "returned"}:
        return None, "대출 상태 오류"
    days = row.get("days_overdue")
    if type(days) is not int or days < 0:
        return None, "연체 일수 오류"

    cleaned = row.copy()
    for key in REQUIRED_TEXT:
        cleaned[key] = row[key].strip()
    if cleaned["loan_id"] in seen:
        return None, "대출 번호 중복"
    seen.add(cleaned["loan_id"])
    return cleaned, None


def summarize(records: list[object]) -> dict:
    """데이터 구조를 학습하기 위한 메모리 내 요약 기능."""
    seen: set[str] = set()
    valid: list[dict] = []
    errors: Counter[str] = Counter()

    for record in records:
        cleaned, reason = validate_loan(record, seen)
        if reason is not None:
            errors[reason] += 1
        else:
            valid.append(cleaned)

    categories = Counter(row["category"] for row in valid)
    by_branch: dict[str, int] = defaultdict(int)
    overdue_by_branch: Counter[str] = Counter()
    book_ids = set()

    for row in valid:
        branch = row["branch"]
        by_branch[branch] += 1
        book_ids.add(row["book_id"])
        if row["status"] == "borrowed" and row["days_overdue"] > 0:
            overdue_by_branch[branch] += 1

    return {
        "input_count": len(records),
        "valid_count": len(valid),
        "errors": errors,
        "unique_books": len(book_ids),
        "categories": categories,
        "by_branch": dict(by_branch),
        "overdue_by_branch": overdue_by_branch,
    }


def main() -> None:
    records = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    if not isinstance(records, list):
        raise ValueError("최상위 JSON 데이터는 배열이어야 합니다.")
    report = summarize(records)

    print("도서관 대출 현황")
    print(f"원본: {report['input_count']}건 | 유효: {report['valid_count']}건 | 제외: {sum(report['errors'].values())}건")
    print(f"고유 도서: {report['unique_books']}종")
    print("분류별 대출:")
    for category, count in sorted(report["categories"].items(), key=lambda item: (-item[1], item[0])):
        print(f"  {category}: {count}건")
    print("분관별 대출 / 현재 연체:")
    for branch in sorted(report["by_branch"]):
        print(f"  {branch}: {report['by_branch'][branch]}건 / {report['overdue_by_branch'][branch]}건")
    print("제외 사유:")
    for reason in sorted(report["errors"]):
        print(f"  {reason}: {report['errors'][reason]}건")


if __name__ == "__main__":
    main()
