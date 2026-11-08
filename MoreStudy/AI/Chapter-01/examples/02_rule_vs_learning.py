"""Example 02. 같은 날씨 자료를 규칙과 학습 모델로 각각 판단합니다."""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]


def rule_predict(rain: np.ndarray) -> np.ndarray:
    """강수 확률이 60% 이상이면 우산을 선택하는 단순 규칙."""
    return (np.asarray(rain) >= 60).astype(int)


def evaluate() -> dict:
    df = pd.read_csv(ROOT / "data" / "weather_choices.csv")
    features = ["rain_probability_pct", "wind_speed_kmh"]
    x_train, x_test, y_train, y_test = train_test_split(
        df[features], df["umbrella_chosen"], test_size=0.25,
        random_state=42, stratify=df["umbrella_chosen"],
    )
    model = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5))
    model.fit(x_train, y_train)
    rule_results = rule_predict(x_test["rain_probability_pct"].to_numpy())
    learned_results = model.predict(x_test)
    return {
        "rule_accuracy": float(accuracy_score(y_test, rule_results)),
        "model_accuracy": float(accuracy_score(y_test, learned_results)),
        "test_size": len(y_test),
        "model": model,
    }


def main() -> None:
    result = evaluate()
    print(f"평가용 데이터: {result['test_size']}건")
    print(f"규칙 기반 정확도: {result['rule_accuracy']:.1%}")
    print(f"학습 모델 정확도: {result['model_accuracy']:.1%}")
    print("어느 방식이 항상 우수하다는 뜻은 아닙니다. 다른 자료에서도 검토해야 합니다.")


if __name__ == "__main__":
    main()
