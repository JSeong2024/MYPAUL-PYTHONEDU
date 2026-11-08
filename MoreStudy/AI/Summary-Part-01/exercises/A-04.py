"""A-04 — Misleading Validation Score (Starter Code).

입력: make_classification dataset
출력: best_params.json, test_metrics.json, audit_report.md
문제 원문: ../problem.md의 A-04 절
"""
from sklearn.datasets import make_classification
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

def main() -> None:
    # STEP 1: X/y를 먼저 Train/Test 분할
    # STEP 2: Scaler+KNN Pipeline과 GridSearchCV(cv=5)
    # STEP 3: Test에서 단 한 번 Accuracy/Balanced Accuracy 계산
    raise NotImplementedError("TODO: main() 구현")


if __name__ == "__main__":
    main()
