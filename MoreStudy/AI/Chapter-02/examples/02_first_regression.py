"""거리만으로 배송 소요 시간을 예측하는 Linear Regression."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "delivery_times.csv"
OUTPUT = ROOT / "outputs" / "example_02_regression.png"


def main():
    frame = pd.read_csv(DATA)
    X = frame[["distance_km"]]
    y = frame["duration_min"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )
    baseline = DummyRegressor(strategy="mean").fit(X_train, y_train)
    model = LinearRegression().fit(X_train, y_train)
    baseline_mae = mean_absolute_error(y_test, baseline.predict(X_test))
    model_mae = mean_absolute_error(y_test, model.predict(X_test))
    print(f"Baseline MAE: {baseline_mae:.3f} min")
    print(f"Linear Regression MAE: {model_mae:.3f} min")
    print(f"Coefficient: {model.coef_[0]:.3f} min/km")
    print(f"Intercept: {model.intercept_:.3f} min")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    ordered = X_test.sort_values("distance_km")
    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    ax.scatter(X_test["distance_km"], y_test, alpha=.65, label="Test samples")
    ax.plot(ordered["distance_km"], model.predict(ordered), label="Regression prediction")
    ax.set(xlabel="Distance (km)", ylabel="Duration (min)", title="Delivery duration prediction")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUTPUT, dpi=145)
    plt.close(fig)
    return {"baseline_mae": baseline_mae, "mae": model_mae, "coefficient": float(model.coef_[0])}


if __name__ == "__main__":
    main()
