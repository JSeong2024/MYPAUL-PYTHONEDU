"""Mini Project 01. 규칙 기반 판단과 학습 모델의 출력을 비교합니다."""
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
REQUIRED = {"case_id", "rain_probability_pct", "wind_speed_kmh", "umbrella_chosen"}


def validate_weather(df: pd.DataFrame) -> None:
    if not REQUIRED.issubset(df.columns):
        raise ValueError(f"누락 열: {sorted(REQUIRED - set(df.columns))}")
    if df.empty or df["case_id"].isna().any() or df["case_id"].duplicated().any():
        raise ValueError("case_id는 누락·중복 없이 존재해야 합니다.")
    numeric = df[["rain_probability_pct", "wind_speed_kmh", "umbrella_chosen"]].apply(
        pd.to_numeric, errors="coerce"
    )
    if not np.isfinite(numeric.to_numpy(dtype=float)).all():
        raise ValueError("숫자 데이터에는 결측값·문자열·무한대를 허용하지 않습니다.")
    if not numeric["rain_probability_pct"].between(0, 100).all() or (numeric["wind_speed_kmh"] < 0).any():
        raise ValueError("강수 확률 또는 풍속이 허용 범위를 벗어났습니다.")
    if not numeric["umbrella_chosen"].isin([0, 1]).all():
        raise ValueError("umbrella_chosen은 0 또는 1이어야 합니다.")


def rule_predict(rain_probability: np.ndarray) -> np.ndarray:
    return (np.asarray(rain_probability) >= 60).astype(int)


def evaluate_weather(df: pd.DataFrame, output_path: Path | None = None) -> dict:
    validate_weather(df)
    x = df[["rain_probability_pct", "wind_speed_kmh"]]
    y = df["umbrella_chosen"].astype(int)
    if len(df) < 16 or y.nunique() != 2 or y.value_counts().min() < 4:
        raise ValueError("학습을 위해 각 정답이 충분히 포함된 데이터가 필요합니다.")
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=42, stratify=y,
    )
    model = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5))
    model.fit(x_train, y_train)
    predicted = model.predict(x_test)
    rule = rule_predict(x_test["rain_probability_pct"].to_numpy())
    result = {
        "n_test": len(y_test),
        "rule_accuracy": float(accuracy_score(y_test, rule)),
        "model_accuracy": float(accuracy_score(y_test, predicted)),
        "rule_correct": int((rule == y_test.to_numpy()).sum()),
        "model_correct": int((predicted == y_test.to_numpy()).sum()),
        "model": model,
    }
    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig, ax = plt.subplots(1, 2, figsize=(10, 4.3), sharex=True, sharey=True)
        for a, values, title in zip(ax, [rule, predicted], ["Rule based", "Learned model"]):
            colors = values.astype(int)
            a.scatter(x_test.iloc[:, 0], x_test.iloc[:, 1], c=colors, cmap="viridis",
                      vmin=0, vmax=1, s=55)
            mistakes = values != y_test.to_numpy()
            if mistakes.any():
                a.scatter(x_test.iloc[mistakes, 0], x_test.iloc[mistakes, 1],
                          marker="x", c="black", s=90, linewidths=1.5)
            a.set(title=f"{title} ({accuracy_score(y_test, values):.1%})",
                  xlabel="Rain probability (%)", ylabel="Wind (km/h)")
            a.grid(alpha=0.2)
        fig.suptitle("Weather decision / x = incorrect prediction")
        fig.tight_layout()
        fig.savefig(output_path, dpi=150)
        plt.close(fig)
    return result


def main() -> None:
    df = pd.read_csv(ROOT / "data" / "weather_choices.csv")
    destination = ROOT / "outputs" / "mini_01_weather_decision.png"
    r = evaluate_weather(df, destination)
    print(f"규칙 기반: {r['rule_correct']}/{r['n_test']} ({r['rule_accuracy']:.1%})")
    print(f"학습 모델: {r['model_correct']}/{r['n_test']} ({r['model_accuracy']:.1%})")
    print(f"결과 그림: {destination.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
