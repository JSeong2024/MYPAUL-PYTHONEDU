"""Example 03. 붓꽃 측정값으로 품종을 분류하고 간단한 결과를 저장합니다."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]


def classify_iris(output_path: Path | None = None) -> dict:
    iris = load_iris()
    indices = np.arange(len(iris.target))
    x_train, x_test, y_train, y_test, _, test_indices = train_test_split(
        iris.data, iris.target, indices, test_size=0.2, random_state=42,
        stratify=iris.target,
    )
    model = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5))
    model.fit(x_train, y_train)
    predicted = model.predict(x_test)
    accuracy = float(accuracy_score(y_test, predicted))
    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig, ax = plt.subplots(figsize=(7.2, 4.8))
        scatter = ax.scatter(x_test[:, 2], x_test[:, 3], c=predicted, cmap="viridis", s=55)
        wrong = predicted != y_test
        if wrong.any():
            ax.scatter(x_test[wrong, 2], x_test[wrong, 3], marker="x", s=150,
                       linewidths=2, color="black", label="Incorrect")
            ax.legend()
        ax.set(xlabel="Petal length (cm)", ylabel="Petal width (cm)",
               title=f"Iris test predictions (accuracy: {accuracy:.1%})")
        ax.grid(alpha=0.2)
        fig.colorbar(scatter, ax=ax, ticks=[0, 1, 2], label="Predicted class")
        fig.tight_layout()
        fig.savefig(output_path, dpi=160)
        plt.close(fig)
    return {
        "accuracy": accuracy, "test_size": len(y_test), "correct": int((predicted == y_test).sum()),
        "test_indices": test_indices, "predicted": predicted, "true_labels": y_test,
    }


def main() -> None:
    destination = ROOT / "outputs" / "example_03_iris_predictions.png"
    result = classify_iris(destination)
    print(f"정답: {result['correct']}/{result['test_size']} (정확도 {result['accuracy']:.1%})")
    print(f"결과 그림: {destination.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
