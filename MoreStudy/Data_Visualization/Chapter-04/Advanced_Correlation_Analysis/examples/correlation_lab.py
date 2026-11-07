"""Correlation study lab: Pearson, L2 norm, ACF, and lagged CCF.

Run from the extracted ZIP:
    python examples/correlation_lab.py

Figure outputs are written to ../figures/ relative to this script.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # Save figures without requiring a desktop display.

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "figures"
FIGURES.mkdir(parents=True, exist_ok=True)


def pearson_l2(x: np.ndarray, y: np.ndarray) -> float:
    """Pearson correlation, expressed using a dot product and L2 norms."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if x.ndim != 1 or y.ndim != 1 or len(x) != len(y) or len(x) < 2:
        raise ValueError("x and y must be 1D arrays of equal length >= 2.")
    if not (np.isfinite(x).all() and np.isfinite(y).all()):
        raise ValueError("Inputs must contain only finite values.")

    xc = x - x.mean()
    yc = y - y.mean()
    denominator = np.linalg.norm(xc, ord=2) * np.linalg.norm(yc, ord=2)
    if denominator == 0:
        raise ValueError("Correlation is undefined for a constant series.")
    return float(np.dot(xc, yc) / denominator)


def lagged_pearson(x: np.ndarray, y: np.ndarray, lag: int) -> float:
    """Overlapping-window Pearson correlation between X_t and Y_(t-lag).

    Positive lag means the Y observation precedes the X observation.
    Negative lag means the Y observation follows the X observation.

    This is NOT identical to every conventional sample ACF/CCF estimator.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if x.ndim != 1 or y.ndim != 1 or len(x) != len(y):
        raise ValueError("x and y must be 1D arrays of equal length.")
    if not isinstance(lag, (int, np.integer)) or abs(lag) >= len(x):
        raise ValueError("lag must be an integer with absolute value < n.")

    if lag > 0:
        a, b = x[lag:], y[:-lag]
    elif lag < 0:
        a, b = x[:lag], y[-lag:]
    else:
        a, b = x, y

    if len(a) < 3:
        return float("nan")
    try:
        return pearson_l2(a, b)
    except ValueError:
        return float("nan")


def conventional_sample_acf(x: np.ndarray, max_lag: int) -> np.ndarray:
    """One common sample ACF: common global mean and fixed denominator."""
    x = np.asarray(x, dtype=float)
    if x.ndim != 1 or len(x) < 3 or not 0 <= max_lag < len(x):
        raise ValueError("Require a 1D series of length >= 3 and 0 <= max_lag < n.")
    if not np.isfinite(x).all():
        raise ValueError("Inputs must be finite.")

    centered = x - x.mean()
    denominator = float(np.dot(centered, centered))
    if denominator == 0:
        raise ValueError("ACF is undefined for a constant series.")

    return np.array(
        [float(np.dot(centered[k:], centered[: len(x) - k]) / denominator)
         for k in range(max_lag + 1)]
    )


def plot_pearson_examples() -> None:
    rng = np.random.default_rng(19)
    x = np.linspace(-2, 2, 140)
    e = rng.normal(0, 0.5, x.size)
    cases = [
        (x + e, "Positive linear"),
        (-x + e, "Negative linear"),
        (x**2 + 0.12 * (rng.normal(size=x.size)), "Nonlinear"),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.6), layout="constrained")
    for ax, (y, label) in zip(axes, cases):
        r = pearson_l2(x, y)
        ax.scatter(x, y, alpha=0.72, s=15)
        ax.set_title(f"{label}\nPearson r = {r:+.2f}")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.grid(alpha=0.18)
    fig.suptitle("Pearson correlation measures linear association", fontsize=13)
    fig.savefig(FIGURES / "pearson_relationships.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def generate_timeseries() -> tuple[np.ndarray, np.ndarray, np.ndarray, int]:
    rng = np.random.default_rng(2026)
    n = 180
    shift = 3

    noise = rng.normal(0, 1, n + 220)
    persistent = np.empty(n + 220)
    persistent[0] = noise[0]
    for t in range(1, persistent.size):
        persistent[t] = 0.72 * persistent[t - 1] + noise[t]
    auto_series = persistent[220:]

    driver_y = rng.normal(0, 1, n)
    response_x = rng.normal(0, 0.28, n)
    response_x[shift:] += driver_y[:-shift]
    return auto_series, driver_y, response_x, shift


def plot_lag_alignment(y: np.ndarray, x: np.ndarray, shift: int) -> None:
    t = np.arange(28)
    fig, ax = plt.subplots(figsize=(11, 4.4), layout="constrained")
    ax.plot(t, y[:28], marker="o", markersize=4, label="Y: earlier signal")
    ax.plot(t, x[:28], marker="s", markersize=4, label=f"X: response (lag +{shift})")
    ax.set_title(f"Positive lag convention: compare X[t] with Y[t - {shift}]")
    ax.set_xlabel("Time index t")
    ax.set_ylabel("Observed value")
    ax.set_xticks(np.arange(0, 28, 3))
    ax.grid(alpha=0.2)
    ax.legend()
    fig.savefig(FIGURES / "lag_alignment.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def plot_acf_ccf(auto_series: np.ndarray, y: np.ndarray, x: np.ndarray, shift: int) -> None:
    max_lag = 14
    acf = conventional_sample_acf(auto_series, max_lag)
    lags = np.arange(-max_lag, max_lag + 1)
    ccf = np.array([lagged_pearson(x, y, int(k)) for k in lags])

    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.1), layout="constrained")
    axes[0].bar(np.arange(max_lag + 1), acf)
    axes[0].axhline(0, linewidth=1)
    axes[0].set(title="Sample ACF: one series vs. its past", xlabel="Lag k", ylabel="Correlation")
    axes[0].set_ylim(-1, 1)

    axes[1].bar(lags, ccf)
    axes[1].axvline(shift, linestyle="--", linewidth=1.5, label=f"Injected lag: +{shift}")
    axes[1].axhline(0, linewidth=1)
    axes[1].set(title="Lagged Pearson CCF: X[t] vs. Y[t-k]", xlabel="Lag k")
    axes[1].set_ylim(-1, 1)
    axes[1].legend()
    for ax in axes:
        ax.grid(axis="y", alpha=0.18)
    fig.savefig(FIGURES / "acf_ccf.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    valid = np.isfinite(ccf)
    best = int(lags[valid][np.argmax(ccf[valid])])
    print(f"Peak lagged CCF = {best:+d} (constructed delay: +{shift})")
    print(f"Overlap-window ACF at lag 1 = {lagged_pearson(auto_series, auto_series, 1):+.4f}")
    print(f"Fixed-denominator ACF at lag 1 = {acf[1]:+.4f}")


def main() -> None:
    x = np.array([1.0, 2.0, 3.0])
    y = np.array([2.0, 4.0, 6.0])
    assert np.isclose(pearson_l2(x, y), np.corrcoef(x, y)[0, 1])
    print(f"Pearson via L2 norms: {pearson_l2(x, y):+.4f}")

    u = np.array([-2.0, -1.0, 0.0, 1.0, 2.0])
    print(f"Nonlinear example r (x vs. x^2): {pearson_l2(u, u**2):+.4f}")

    a = np.array([0, 0, 1, 3, 2, 5], dtype=float)
    b = np.array([1, 3, 2, 5, 4, 6], dtype=float)
    print(f"Example cross-correlation at lag +2: {lagged_pearson(a, b, 2):+.4f}")

    auto_series, driver, response, shift = generate_timeseries()
    plot_pearson_examples()
    plot_lag_alignment(driver, response, shift)
    plot_acf_ccf(auto_series, driver, response, shift)
    print(f"Created figures in: {FIGURES}")


if __name__ == "__main__":
    main()
