"""Chapter 03 실습용 합성 데이터 생성. 같은 시드에서 동일한 CSV를 생성한다."""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.datasets import make_moons

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def make_tickets():
    rng = np.random.default_rng(303)
    count = 480
    waiting_hours = np.round(rng.uniform(0.25, 20.0, count), 2)
    failed_attempts = rng.poisson(1.7, count).clip(0, 9)
    impacted_users = rng.integers(1, 150, count)
    score = -3.1 + 0.15 * waiting_hours + 0.73 * failed_attempts + 0.010 * impacted_users
    probability = 1 / (1 + np.exp(-score))
    urgent = rng.binomial(1, probability)
    data = pd.DataFrame({
        "ticket_id": [f"T{i:04d}" for i in range(1, count + 1)],
        "waiting_hours": waiting_hours,
        "failed_attempts": failed_attempts,
        "impacted_users": impacted_users,
        "urgent": urgent,
    })
    data.to_csv(DATA / "service_tickets.csv", index=False)


def make_stations():
    rng = np.random.default_rng(304)
    # 세 가지 사용 패턴을 혼합하되, 원래 패턴 ID는 파일에 포함하지 않는다.
    centers = np.array([[78, 72, 25], [25, 30, 86], [50, 54, 52]], dtype=float)
    groups = np.repeat(np.arange(3), 90)
    rng.shuffle(groups)
    signal = centers[groups] + rng.normal(0, [10, 11, 10], (len(groups), 3))
    signal = np.round(np.maximum(signal, 0), 1)
    df = pd.DataFrame(signal, columns=["morning_trips", "evening_trips", "weekend_trips"])
    df.insert(0, "station_id", [f"S{i:03d}" for i in range(1, len(df) + 1)])
    df.to_csv(DATA / "station_patterns.csv", index=False)


def make_work_modes():
    rng = np.random.default_rng(305)
    n = 540
    # 입력 변수는 연속 분포이며, 지정한 조합으로 만든 범주를 예측 대상으로 사용한다.
    morning = rng.normal(40, 14, n).clip(5, 85)
    remote = rng.normal(34, 15, n).clip(1, 85)
    evening = rng.normal(27, 12, n).clip(1, 70)
    score = 0.085 * morning - 0.075 * remote + 0.055 * evening + rng.normal(0, 0.7, n)
    boundaries = np.quantile(score, [1/3, 2/3])
    label = np.digitize(score, boundaries)
    df = pd.DataFrame({
        "record_id": [f"W{i:04d}" for i in range(1, n + 1)],
        "morning_activity": np.round(morning, 2),
        "remote_activity": np.round(remote, 2),
        "evening_activity": np.round(evening, 2),
        "work_mode": label,
    })
    df.to_csv(DATA / "work_modes.csv", index=False)


def make_paths():
    rng = np.random.default_rng(306)
    points, labels = make_moons(n_samples=440, noise=0.075, random_state=306)
    outliers = rng.uniform(low=[-1.5, -1.1], high=[2.6, 1.7], size=(24, 2))
    X = np.concatenate([points, outliers])
    reference = np.concatenate([labels, -np.ones(len(outliers), dtype=int)])
    order = rng.permutation(len(X))
    X, reference = X[order], reference[order]
    df = pd.DataFrame({
        "point_id": [f"P{i:04d}" for i in range(1, len(X) + 1)],
        "x_position": np.round(X[:, 0], 5),
        "y_position": np.round(X[:, 1], 5),
        "reference_group": reference.astype(int),
    })
    df.to_csv(DATA / "curved_paths.csv", index=False)


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    make_tickets()
    make_stations()
    make_work_modes()
    make_paths()
    print("4 synthetic datasets generated")

if __name__ == "__main__":
    main()
