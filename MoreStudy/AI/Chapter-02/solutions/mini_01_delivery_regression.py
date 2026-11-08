"""Mini 01 — 평균 예측과 Linear Regression을 같은 데이터에서 비교합니다."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "delivery_times.csv"
OUTPUT_PATH = ROOT / "outputs" / "mini_01_delivery_regression.png"
REQUIRED = ["order_id", "distance_km", "stops", "duration_min"]


def validate(frame: pd.DataFrame) -> pd.DataFrame:
    missing = set(REQUIRED) - set(frame.columns)
    if missing:
        raise ValueError(f"필수 열 누락: {sorted(missing)}")
    if frame.empty or frame["order_id"].isna().any() or frame["order_id"].duplicated().any():
        raise ValueError("비어 있거나 중복된 order_id가 있습니다.")
    numeric = frame[["distance_km", "stops", "duration_min"]].apply(pd.to_numeric, errors="coerce")
    if numeric.isna().any().any() or not np.isfinite(numeric.to_numpy()).all():
        raise ValueError("누락되거나 유한하지 않은 수치가 있습니다.")
    if (numeric["distance_km"] <= 0).any() or (numeric["stops"] < 0).any() or (numeric["duration_min"] <= 0).any():
        raise ValueError("거리·경유지·시간 범위가 올바르지 않습니다.")
    if not np.all(numeric["stops"] == np.floor(numeric["stops"])):
        raise ValueError("경유지 수는 정수여야 합니다.")
    return frame.copy()


def evaluate(frame: pd.DataFrame) -> dict:
    validated = validate(frame)
    X = validated[["distance_km"]]
    y = validated["duration_min"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )
    baseline = DummyRegressor(strategy="mean").fit(X_train, y_train)
    model = LinearRegression().fit(X_train, y_train)
    predicted = model.predict(X_test)
    return {
        "baseline_mae": float(mean_absolute_error(y_test, baseline.predict(X_test))),
        "mae": float(mean_absolute_error(y_test, predicted)),
        "mse": float(mean_squared_error(y_test, predicted)),
        "slope": float(model.coef_[0]),
        "intercept": float(model.intercept_),
        "X_test": X_test,
        "y_test": y_test,
        "model": model,
    }


def draw(result: dict, output_path: Path = OUTPUT_PATH) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    X_test = result["X_test"]
    ordered = X_test.sort_values("distance_km")
    fig, ax = plt.subplots(figsize=(7.2, 4.7))
    ax.scatter(X_test["distance_km"], result["y_test"], alpha=0.7, label="Test samples")
    ax.plot(ordered["distance_km"], result["model"].predict(ordered), label="Linear model")
    ax.set(xlabel="Distance (km)", ylabel="Duration (min)", title="Mini 01 — Delivery duration")
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path, dpi=145)
    plt.close(fig)


def main() -> None:
    result = evaluate(pd.read_csv(DATA_PATH))
    print(f"Baseline MAE: {result['baseline_mae']:.3f} min")
    print(f"Linear MAE: {result['mae']:.3f} min")
    print(f"Linear MSE: {result['mse']:.3f} min^2")
    print(f"slope: {result['slope']:.3f} min/km, intercept: {result['intercept']:.3f} min")
    draw(result)


if __name__ == "__main__":
    main()
