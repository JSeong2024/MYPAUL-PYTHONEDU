"""Mini 02 — NumPy로 Gradient Descent를 구현하고 LinearRegression과 비교합니다."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "outputs" / "mini_02_gradient_descent.png"


def sample_data(seed: int = 42) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    x = np.linspace(-2, 2, 41)
    y = 1.5 * x + 2.8 + rng.normal(0, 0.25, x.size)
    return x, y


def gradient_descent(x: np.ndarray, y: np.ndarray, learning_rate: float = 0.05,
                     steps: int = 250) -> tuple[float, float, np.ndarray]:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if x.ndim != 1 or y.ndim != 1 or x.shape != y.shape or x.size == 0:
        raise ValueError("x, y의 모양이 올바르지 않습니다.")
    if not np.isfinite(x).all() or not np.isfinite(y).all():
        raise ValueError("유한한 수치만 사용할 수 있습니다.")
    if learning_rate <= 0 or not np.isfinite(learning_rate) or steps <= 0:
        raise ValueError("학습률과 반복 횟수를 확인하세요.")
    weight, bias = 0.0, 0.0
    losses = []
    for _ in range(steps):
        errors = weight * x + bias - y
        grad_weight = 2.0 * float(np.mean(errors * x))
        grad_bias = 2.0 * float(np.mean(errors))
        weight -= learning_rate * grad_weight
        bias -= learning_rate * grad_bias
        losses.append(float(np.mean((weight * x + bias - y) ** 2)))
    return weight, bias, np.asarray(losses, dtype=float)


def compare() -> dict:
    x, y = sample_data()
    weight, bias, losses = gradient_descent(x, y)
    reference = LinearRegression().fit(x.reshape(-1, 1), y)
    return {
        "x": x, "y": y, "weight": weight, "bias": bias, "losses": losses,
        "reference_weight": float(reference.coef_[0]),
        "reference_bias": float(reference.intercept_),
    }


def draw(result: dict, output_path: Path = OUTPUT_PATH) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7.0, 4.4))
    ax.plot(np.arange(1, result["losses"].size + 1), result["losses"])
    ax.set(xlabel="Iteration", ylabel="MSE", title="Mini 02 — Gradient Descent loss")
    fig.tight_layout()
    fig.savefig(output_path, dpi=145)
    plt.close(fig)


def main() -> None:
    result = compare()
    print(f"Gradient Descent: w={result['weight']:.4f}, b={result['bias']:.4f}")
    print(f"LinearRegression: w={result['reference_weight']:.4f}, b={result['reference_bias']:.4f}")
    print(f"MSE: {result['losses'][0]:.4f} -> {result['losses'][-1]:.4f}")
    draw(result)


if __name__ == "__main__":
    main()
