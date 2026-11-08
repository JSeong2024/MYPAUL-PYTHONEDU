"""Advanced Project 02. 숫자 분류의 낮은 지지율을 사람 검토 대상으로 분리합니다."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_digits
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]


def review_decision(max_votes: np.ndarray, threshold: float) -> np.ndarray:
    if not isinstance(threshold, (int, float)) or not np.isfinite(threshold) or not 0 <= threshold <= 1:
        raise ValueError("threshold는 0~1 사이의 유한한 숫자여야 합니다.")
    votes = np.asarray(max_votes, dtype=float)
    if not np.isfinite(votes).all() or np.any((votes < 0) | (votes > 1)):
        raise ValueError("max_votes는 0~1 사이의 숫자여야 합니다.")
    return votes < threshold


def analyze_digits(output_path: Path | None = None, threshold: float = 0.8) -> dict:
    if not isinstance(threshold, (int, float)) or not np.isfinite(threshold) or not 0 <= threshold <= 1:
        raise ValueError("threshold는 0~1 사이의 유한한 숫자여야 합니다.")
    digits = load_digits()
    x_train, x_test, y_train, y_test = train_test_split(
        digits.data, digits.target, test_size=0.2, stratify=digits.target,
        random_state=42,
    )
    model = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5))
    model.fit(x_train, y_train)
    predicted = model.predict(x_test)
    # KNN의 predict_proba는 가까운 이웃의 투표 비율이며 확률 보정을 보장하지 않습니다.
    votes = model.predict_proba(x_test).max(axis=1)
    review_mask = review_decision(votes, threshold)
    auto_mask = ~review_mask
    result = {
        "n_test": len(y_test),
        "total_accuracy": float(accuracy_score(y_test, predicted)),
        "review_count": int(review_mask.sum()),
        "auto_count": int(auto_mask.sum()),
        "auto_accuracy": float(accuracy_score(y_test[auto_mask], predicted[auto_mask])) if auto_mask.any() else None,
        "review_mask": review_mask,
        "votes": votes,
        "true_labels": y_test,
        "predicted": predicted,
        "model": model,
    }
    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        first_review = np.flatnonzero(review_mask)[:4]
        first_auto = np.flatnonzero(auto_mask)[:4]
        selection = np.concatenate((first_review, first_auto))
        fig, axes = plt.subplots(2, 4, figsize=(9, 5))
        for ax, index in zip(axes.flat, selection):
            ax.imshow(x_test[index].reshape(8, 8), cmap="gray_r", interpolation="nearest")
            tag = "REVIEW" if review_mask[index] else "AUTO"
            ax.set_title(f"{tag} | {predicted[index]}/{y_test[index]} | {votes[index]:.1f}", fontsize=9)
            ax.axis("off")
        for ax in axes.flat[len(selection):]:
            ax.axis("off")
        fig.suptitle("Digits: decision / true label / neighbor vote")
        fig.tight_layout()
        fig.savefig(output_path, dpi=160)
        plt.close(fig)
    return result


def main() -> None:
    destination = ROOT / "outputs" / "advanced_02_digit_review.png"
    r = analyze_digits(destination)
    print(f"평가 데이터: {r['n_test']}건 / 전체 정확도: {r['total_accuracy']:.1%}")
    print(f"자동 분류 {r['auto_count']}건 / 사람 검토 {r['review_count']}건")
    print("자동 분류 정확도:", "자료 없음" if r['auto_accuracy'] is None else f"{r['auto_accuracy']:.1%}")
    print("주의: 이웃 투표 비율은 보정된 참 확률이 아닙니다.")
    print(f"결과 그림: {destination.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
