"""Python 표준 라이브러리만 사용하는 Chapter 02 기본 검증.

Chapter-02에서 실행: python tests/test_library_loan_report.py
"""

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "examples" / "10_library_loan_report.py"
spec = importlib.util.spec_from_file_location("library_loan_report", MODULE_PATH)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

records = json.loads((ROOT / "data" / "library_loans.json").read_text(encoding="utf-8"))
original = json.dumps(records, ensure_ascii=False, sort_keys=True)
report = module.summarize(records)
assert report["input_count"] == 15
assert report["valid_count"] == 12
assert sum(report["errors"].values()) == 3
assert report["unique_books"] == 10
assert report["categories"] == {"과학": 5, "문학": 4, "역사": 3}
assert report["by_branch"] == {"중앙": 5, "동부": 4, "서부": 3}
assert report["overdue_by_branch"] == {"중앙": 1, "서부": 2, "동부": 2}
assert json.dumps(records, ensure_ascii=False, sort_keys=True) == original

# 빈 입력과 단일 정상 입력
empty_report = module.summarize([])
assert empty_report["valid_count"] == 0
valid_record = {"loan_id": "L-100", "branch": "중앙", "book_id": "B-01",
                "category": "과학", "status": "borrowed", "days_overdue": 0}
assert module.summarize([valid_record])["valid_count"] == 1
assert module.summarize([dict(valid_record, days_overdue=True)])["valid_count"] == 0

print("Chapter 02 tests: OK (기본·빈 입력·자료형·원본 보존)")
