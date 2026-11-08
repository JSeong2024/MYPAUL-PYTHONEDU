"""Advanced Project 01. 드문 사건에서 단순 정확도가 왜 부족한지 확인합니다."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
COLUMNS = {"record_id", "sensor_a", "sensor_b", "is_rare_event"}


def validate_records(df: pd.DataFrame) -> None:
    if not COLUMNS.issubset(df.columns):
        raise ValueError(f"누락 열: {sorted(COLUMNS - set(df.columns))}")
    if df.empty or df.isna().any().any() or df["record_id"].duplicated().any():
        raise ValueError("데이터가 비었거나 누락·중복된 값이 있습니다.")
    if not np.isfinite(df[["sensor_a", "sensor_b"]].to_numpy(dtype=float)).all():
        raise ValueError("센서값은 유한한 숫자여야 합니다.")
    if not df["is_rare_event"].isin([0, 1]).all():
        raise ValueError("is_rare_event는 0 또는 1이어야 합니다.")


def evaluate_rare_event(df: pd.DataFrame, output_path: Path | None = None) -> dict:
    validate_records(df)
    y = df["is_rare_event"].astype(int)
    if len(df) < 40 or y.nunique() != 2 or y.value_counts().min() < 8:
        raise ValueError("두 클래스별 충분한 관측이 필요합니다.")
    x_train, x_test, y_train, y_test = train_test_split(
        df[["sensor_a", "sensor_b"]], y,
        test_size=0.25, random_state=42, stratify=y,
    )
    model = make_pipeline(
        StandardScaler(), LogisticRegression(class_weight="balanced", max_iter=1000),
    )
    model.fit(x_train, y_train)
    baseline = np.zeros(len(y_test), dtype=int)
    predicted = model.predict(x_test)
    result = {
        "n_test": len(y_test),
        "n_rare_test": int(y_test.sum()),
        "baseline_accuracy": float(accuracy_score(y_test, baseline)),
        "baseline_rare_recall": float(recall_score(y_test, baseline, pos_label=1, zero_division=0)),
        "baseline_balanced_accuracy": float(balanced_accuracy_score(y_test, baseline)),
        "model_accuracy": float(accuracy_score(y_test, predicted)),
        "model_rare_recall": float(recall_score(y_test, predicted, pos_label=1, zero_division=0)),
        "model_balanced_accuracy": float(balanced_accuracy_score(y_test, predicted)),
        "model": model,
    }
    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        keys = ["accuracy", "rare_recall", "balanced_accuracy"]
        titles = ["Accuracy", "Rare event recall", "Balanced accuracy"]
        x = np.arange(len(keys))
        fig, ax = plt.subplots(figsize=(8, 4.5))
        ax.bar(x - 0.19, [result[f"baseline_{k}"] for k in keys], 0.38, label="Always normal")
        ax.bar(x + 0.19, [result[f"model_{k}"] for k in keys], 0.38, label="Learned model")
        ax.set(xticks=x, xticklabels=titles, ylabel="Score", ylim=(0, 1.08),
               title="Rare event: high accuracy can hide missed cases")
        ax.legend()
        ax.grid(axis="y", alpha=0.2)
        fig.tight_layout()
        fig.savefig(output_path, dpi=160)
        plt.close(fig)
    return result


def main() -> None:
    df = pd.read_csv(ROOT / "data" / "rare_events.csv")
    destination = ROOT / "outputs" / "advanced_01_rare_event.png"
    r = evaluate_rare_event(df, destination)
    print(f"평가 데이터: {r['n_test']}건 (드문 사건 {r['n_rare_test']}건)")
    for prefix in ["baseline", "model"]:
        print(f"{prefix}: 정확도 {r[prefix + '_accuracy']:.1%}, "
              f"드문 사건 재현율 {r[prefix + '_rare_recall']:.1%}, "
              f"균형 정확도 {r[prefix + '_balanced_accuracy']:.1%}")
    print(f"결과 그림: {destination.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
