"""Advanced 02: 반복 기록에서 Random/Group Split의 차이를 검증한다."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score,balanced_accuracy_score
from sklearn.model_selection import train_test_split,GroupShuffleSplit,GroupKFold
from sklearn.neighbors import KNeighborsClassifier

ROOT=Path(__file__).resolve().parents[2]


def load_data(path=ROOT / "data/device_cycles.csv"):
    """TODO: 장비별 Label이 일관적인지 검증."""
    df=pd.read_csv(path)
    raise NotImplementedError


def audit_overlap(groups,train_idx,test_idx):
    """TODO: Train과 Test에 동시에 등장한 장비 ID 개수 반환."""
    raise NotImplementedError


def evaluate(df):
    """TODO: Random/Group Holdout, GroupKFold의 Balanced Accuracy 비교."""
    # GroupShuffleSplit(...).split(X, y, groups=groups)
    raise NotImplementedError


def plot_result(result):
    """TODO: 두 분할의 평가 점수와 Group 중복 건수를 그래프로 저장."""
    raise NotImplementedError


def main():
    result=evaluate(load_data())
    print(result)
    print(plot_result(result))


if __name__ == "__main__":
    main()
