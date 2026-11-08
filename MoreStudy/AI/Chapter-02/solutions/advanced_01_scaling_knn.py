"""Advanced 01 — Feature Scaling 전후의 KNN 분류를 비교합니다."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "sensor_signals.csv"
OUTPUT_PATH = ROOT / "outputs" / "advanced_01_scaling_knn.png"
FEATURES = ["vibration_mm_s", "ambient_lux"]


def validate(frame: pd.DataFrame) -> pd.DataFrame:
    required = {"sample_id", *FEATURES, "fault_label"}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"필수 열 누락: {sorted(missing)}")
    if frame.empty or frame["sample_id"].isna().any() or frame["sample_id"].duplicated().any():
        raise ValueError("sample_id를 확인하세요.")
    numeric = frame[FEATURES + ["fault_label"]].apply(pd.to_numeric, errors="coerce")
    if numeric.isna().any().any() or not np.isfinite(numeric.to_numpy()).all():
        raise ValueError("입력 데이터에 수치 오류가 있습니다.")
    if (numeric[FEATURES] < 0).any().any():
        raise ValueError("진동과 조도는 음수가 될 수 없습니다.")
    if not numeric["fault_label"].isin([0, 1]).all():
        raise ValueError("fault_label은 0 또는 1이어야 합니다.")
    if numeric["fault_label"].nunique() < 2:
        raise ValueError("두 클래스가 모두 있어야 합니다.")
    return frame.copy()


def evaluate(frame: pd.DataFrame) -> dict:
    frame = validate(frame)
    X_train, X_test, y_train, y_test = train_test_split(
        frame[FEATURES], frame["fault_label"],
        test_size=0.25, random_state=42, stratify=frame["fault_label"],
    )
    raw_model = KNeighborsClassifier(n_neighbors=7).fit(X_train, y_train)
    scaled_model = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=7))
    scaled_model.fit(X_train, y_train)
    raw_pred = raw_model.predict(X_test)
    scaled_pred = scaled_model.predict(X_test)
    return {
        "raw_accuracy": float(accuracy_score(y_test, raw_pred)),
        "scaled_accuracy": float(accuracy_score(y_test, scaled_pred)),
        "changed": int(np.count_nonzero(raw_pred != scaled_pred)),
        "n_test": len(y_test),
        "model": scaled_model,
    }


def draw(result: dict, output_path: Path = OUTPUT_PATH) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    bars = ax.bar(["Raw", "StandardScaler"],
                  [result["raw_accuracy"], result["scaled_accuracy"]])
    for bar in bars:
        ax.annotate(f"{bar.get_height():.1%}", (bar.get_x() + bar.get_width() / 2,
                    bar.get_height()), ha="center", va="bottom")
    ax.set(ylim=(0, 1.08), ylabel="Accuracy", title="Advanced 01 — KNN and Feature Scaling")
    fig.tight_layout()
    fig.savefig(output_path, dpi=145)
    plt.close(fig)


def main() -> None:
    result = evaluate(pd.read_csv(DATA_PATH))
    print(f"Raw Accuracy: {result['raw_accuracy']:.1%}")
    print(f"Scaled Accuracy: {result['scaled_accuracy']:.1%}")
    print(f"Changed predictions: {result['changed']} / {result['n_test']}")
    draw(result)


if __name__ == "__main__":
    main()
