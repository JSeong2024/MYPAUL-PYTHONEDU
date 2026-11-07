"""Exercise 05 — 관측 커버리지 모범답안."""
import pandas as pd


def calculate_coverage(observations: pd.DataFrame, expected_slots: int) -> float:
    if isinstance(expected_slots, bool) or not isinstance(expected_slots, int) or expected_slots <= 0:
        raise ValueError("expected_slots must be a positive integer")
    if len(observations) > expected_slots:
        raise ValueError("accepted records exceed expected slots")
    return round(len(observations) / expected_slots * 100, 2)


if __name__ == "__main__":
    sample = pd.DataFrame({"observation_id": ["A", "B", "C"]})
    print(calculate_coverage(sample, 4))
