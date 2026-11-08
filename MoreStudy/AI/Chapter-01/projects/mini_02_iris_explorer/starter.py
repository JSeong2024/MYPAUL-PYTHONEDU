"""Mini 02 Starter — 붓꽃 분류 결과를 확인하고 오분류를 분석합니다."""
from pathlib import Path
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]


def run() -> None:
    iris = load_iris()
    # TODO 1: iris.data / iris.target을 확인합니다.
    # TODO 2: 학습(80%)과 평가(20%) 데이터로 나눕니다.
    # TODO 3: StandardScaler + KNN(n_neighbors=5)를 학습합니다.
    # TODO 4: Accuracy·오분류 건수·혼동행렬을 계산합니다.
    # TODO 5: 결과를 그림으로 저장합니다.
    print(f"샘플: {len(iris.target)}개, 특성: {iris.data.shape[1]}개")
    raise NotImplementedError("TODO 1~5")


if __name__ == "__main__":
    run()
