"""Mini Project 02. 붓꽃 분류 결과와 오분류 사례를 시각화합니다."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_iris
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]


def analyze_iris(output_path: Path | None = None, k: int = 5) -> dict:
    if not isinstance(k, int) or not 1 <= k <= 20:
        raise ValueError("k는 1~20의 정수여야 합니다.")
    iris = load_iris()
    x_train, x_test, y_train, y_test = train_test_split(
        iris.data, iris.target, test_size=0.2, random_state=42,
        stratify=iris.target,
    )
    model = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=k))
    model.fit(x_train, y_train)
    predicted = model.predict(x_test)
    matrix = confusion_matrix(y_test, predicted, labels=[0, 1, 2])
    result = {
        "accuracy": float(accuracy_score(y_test, predicted)),
        "test_size": len(y_test),
        "wrong_count": int((predicted != y_test).sum()),
        "confusion_matrix": matrix,
        "true_labels": y_test,
        "predicted": predicted,
        "model": model,
    }
    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig, ax = plt.subplots(figsize=(6.4, 5))
        ConfusionMatrixDisplay(matrix, display_labels=iris.target_names).plot(
            ax=ax, colorbar=False, values_format="d", cmap="Blues",
        )
        ax.set_title(f"Iris test results (accuracy: {result['accuracy']:.1%})")
        fig.tight_layout()
        fig.savefig(output_path, dpi=155)
        plt.close(fig)
    return result


def main() -> None:
    destination = ROOT / "outputs" / "mini_02_iris_confusion.png"
    r = analyze_iris(destination)
    print(f"평가 데이터: {r['test_size']}건")
    print(f"정확도: {r['accuracy']:.1%} / 오분류: {r['wrong_count']}건")
    print(f"결과 그림: {destination.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
