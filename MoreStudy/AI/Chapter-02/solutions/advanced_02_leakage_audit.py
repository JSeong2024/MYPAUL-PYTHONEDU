"""Advanced 02 — 예측 시점에 없는 Feature를 사용했을 때의 오류를 비교합니다."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "energy_usage.csv"
OUTPUT_PATH = ROOT / "outputs" / "advanced_02_leakage_audit.png"
AVAILABLE = ["temperature_c", "floor_area_m2", "occupancy"]
LATE = "meter_finalized_kwh"
TARGET = "energy_kwh"


def validate(frame: pd.DataFrame) -> pd.DataFrame:
    required = {"record_id", TARGET, LATE, *AVAILABLE}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"필수 열 누락: {sorted(missing)}")
    if frame.empty or frame["record_id"].isna().any() or frame["record_id"].duplicated().any():
        raise ValueError("record_id를 확인하세요.")
    numeric = frame[AVAILABLE + [LATE, TARGET]].apply(pd.to_numeric, errors="coerce")
    if numeric.isna().any().any() or not np.isfinite(numeric.to_numpy()).all():
        raise ValueError("누락되거나 유한하지 않은 수치가 있습니다.")
    if (numeric[["floor_area_m2", "occupancy", TARGET, LATE]] <= 0).any().any():
        raise ValueError("면적·인원·에너지 값은 양수여야 합니다.")
    if not np.all(numeric["occupancy"] == np.floor(numeric["occupancy"])):
        raise ValueError("occupancy는 정수여야 합니다.")
    return frame.copy()


def unavailable_features(selected: list[str]) -> list[str]:
    """측정 종료 후 생성되는 Feature를 사용했는지 검사합니다."""
    return [col for col in selected if col == LATE]


def evaluate(frame: pd.DataFrame) -> dict:
    frame = validate(frame)
    train_index, test_index = train_test_split(
        np.arange(len(frame)), test_size=0.25, random_state=42
    )
    y_train = frame.iloc[train_index][TARGET]
    y_test = frame.iloc[test_index][TARGET]
    legitimate = LinearRegression().fit(frame.iloc[train_index][AVAILABLE], y_train)
    leaked_features = AVAILABLE + [LATE]
    leaked = LinearRegression().fit(frame.iloc[train_index][leaked_features], y_train)
    legitimate_mae = float(mean_absolute_error(
        y_test, legitimate.predict(frame.iloc[test_index][AVAILABLE])
    ))
    leaked_mae = float(mean_absolute_error(
        y_test, leaked.predict(frame.iloc[test_index][leaked_features])
    ))
    return {
        "legitimate_mae": legitimate_mae,
        "leaked_mae": leaked_mae,
        "unavailable": unavailable_features(leaked_features),
        "n_test": len(test_index),
    }


def draw(result: dict, output_path: Path = OUTPUT_PATH) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    bars = ax.bar(["Available features", "Post-measurement feature"],
                  [result["legitimate_mae"], result["leaked_mae"]])
    for bar in bars:
        ax.annotate(f"{bar.get_height():.2f}",
                    (bar.get_x() + bar.get_width()/2, bar.get_height()),
                    ha="center", va="bottom")
    ax.set(ylabel="MAE (kWh)", title="Advanced 02 — Data Leakage")
    fig.tight_layout()
    fig.savefig(output_path, dpi=145)
    plt.close(fig)


def main() -> None:
    result = evaluate(pd.read_csv(DATA_PATH))
    print(f"Valid features MAE: {result['legitimate_mae']:.3f} kWh")
    print(f"Leaked feature MAE: {result['leaked_mae']:.3f} kWh")
    print(f"Unavailable at prediction time: {', '.join(result['unavailable'])}")
    draw(result)


if __name__ == "__main__":
    main()
